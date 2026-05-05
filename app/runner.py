"""
Render runner: materialises props and invokes the Node.js Remotion render
subprocess. Captures progress, maps known error codes, and returns the
output artifact path.
"""

import json
import os
import re
import subprocess
from shutil import which
from pathlib import Path
from typing import Callable, Optional

from app.config import settings
from app.logging_config import logger


class RenderError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


# Maps substrings in stderr to structured error codes.
_STDERR_ERROR_MAP: dict[str, str] = {
    "Cannot find composition": "COMPOSITION_NOT_FOUND",
    "Could not find a composition": "COMPOSITION_NOT_FOUND",
    "Composition has validation errors": "COMPOSITION_PROPS_INVALID",
    "Could not find npm executable": "REMOTION_RUNTIME_MISSING",
    "Could not find entry point": "ENTRYPOINT_NOT_FOUND",
    "Command failed with ENOENT": "ENTRYPOINT_NOT_FOUND",
    "ENOMEM": "OUT_OF_MEMORY",
    "TIMEOUT": "RENDER_TIMEOUT",
    "JavaScript heap out of memory": "HEAP_EXHAUSTED",
    "ENOENT": "ASSET_NOT_FOUND",
}


def _classify_error(stderr: str) -> str:
    for fragment, code in _STDERR_ERROR_MAP.items():
        if fragment in stderr:
            return code
    return "RENDER_FAILURE"


_PROGRESS_PATTERN = re.compile(r"^REMOTION_PROGRESS:(\d{1,3})$")


class RenderRunner:
    def __init__(
        self,
        work_dir: str = settings.render_work_dir,
        script_path: str = settings.render_script_path,
    ) -> None:
        self._work_dir = Path(work_dir)
        self._script_path = script_path
        self._work_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        job_id: str,
        template_id: str,
        props: dict,
        on_progress: Optional[Callable[[int], None]] = None,
    ) -> str:
        """
        Materialise props to a temp JSON file, execute the Remotion render
        script, and return the path of the produced MP4.

        Raises RenderError on non-zero exit or known failure patterns.
        """
        props_file = self._work_dir / f"{job_id}.props.json"
        output_file = self._work_dir / f"{job_id}.mp4"

        with props_file.open("w", encoding="utf-8") as f:
            json.dump(props, f)

        cmd = self._build_render_command(
            template_id=template_id,
            props_file=props_file,
            output_file=output_file,
        )

        logger.info(
            "runner.start",
            job_id=job_id,
            template_id=template_id,
            cmd=" ".join(cmd),
        )

        if on_progress:
            on_progress(10)

        result = self._run_with_streamed_progress(cmd, on_progress=on_progress)

        if on_progress:
            on_progress(70)

        if result.returncode != 0:
            error_code = _classify_error(result.stderr)
            logger.error(
                "runner.failed",
                job_id=job_id,
                error_code=error_code,
                stderr=result.stderr[:1000],
            )
            raise RenderError(error_code, result.stderr.strip()[:512])

        if not output_file.exists():
            raise RenderError("OUTPUT_MISSING", "Render completed but output file not found.")

        logger.info(
            "runner.success",
            job_id=job_id,
            output_file=str(output_file),
            size_bytes=output_file.stat().st_size,
        )

        # Clean up props file
        props_file.unlink(missing_ok=True)

        return str(output_file)

    def _run_with_streamed_progress(
        self,
        cmd: list[str],
        on_progress: Optional[Callable[[int], None]],
    ) -> subprocess.CompletedProcess[str]:
        """
        Execute a render command and stream stdout/stderr, mapping progress
        marker lines to callback updates.

        Progress protocol from renderer script:
          REMOTION_PROGRESS:<0-100>
        """
        output_lines: list[str] = []
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        try:
            assert process.stdout is not None
            for raw_line in process.stdout:
                line = raw_line.rstrip("\n")
                output_lines.append(line)

                m = _PROGRESS_PATTERN.match(line.strip())
                if m and on_progress:
                    pct = max(0, min(100, int(m.group(1))))
                    on_progress(pct)

            return_code = process.wait(timeout=settings.worker_job_timeout_seconds)
        except subprocess.TimeoutExpired:
            process.kill()
            raise RenderError("RENDER_TIMEOUT", "Render command exceeded timeout.")

        combined = "\n".join(output_lines)
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=return_code,
            stdout=combined,
            stderr=combined,
        )

    def _build_render_command(
        self,
        template_id: str,
        props_file: Path,
        output_file: Path,
    ) -> list[str]:
        """
        Build a rendering command for the requested template.

        Plan A implementation:
          - release_trailer uses real Remotion CLI rendering (no fallback).
          - other templates continue through the existing node script contract.
        """
        if template_id == "release_trailer":
            return self._build_release_trailer_command(props_file, output_file)

        # Backward-compatible path used by all other templates for now.
        return [
            "node",
            self._script_path,
            "--composition", template_id,
            "--props", str(props_file),
            "--output", str(output_file),
        ]

    def _build_release_trailer_command(
        self,
        props_file: Path,
        output_file: Path,
    ) -> list[str]:
        """
        Real Remotion render path for the release_trailer hero template.

        Environment contract:
          - REMOTION_ENTRY: path to Remotion entry file (default: remotion/index.ts)
          - RELEASE_TRAILER_COMPOSITION: composition ID (default: ReleaseTrailerV1)

        If requirements are not met, raises RenderError.
        """
        if which("npx") is None:
            raise RenderError(
                "REMOTION_RUNTIME_MISSING",
                "npx was not found in PATH. Install Node.js/npm runtime for Remotion rendering.",
            )

        remotion_entry = os.getenv("REMOTION_ENTRY", "remotion/index.ts")
        composition_id = os.getenv("RELEASE_TRAILER_COMPOSITION", "ReleaseTrailerV1")
        renderer_script = os.getenv(
            "REMOTION_RENDERER_SCRIPT",
            "remotion/render-release-trailer.js",
        )
        entry_path = Path(remotion_entry)
        if not entry_path.exists():
            raise RenderError(
                "ENTRYPOINT_NOT_FOUND",
                f"Remotion entry file not found: {entry_path}",
            )

        renderer_path = Path(renderer_script)
        if not renderer_path.exists():
            raise RenderError(
                "ENTRYPOINT_NOT_FOUND",
                f"Remotion renderer script not found: {renderer_path}",
            )

        return [
            "node",
            str(renderer_path),
            "--entry",
            str(entry_path),
            "--composition",
            composition_id,
            "--props",
            str(props_file),
            "--output",
            str(output_file),
        ]


runner = RenderRunner()
