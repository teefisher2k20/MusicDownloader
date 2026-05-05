"""
Render runner: materialises props and invokes the Node.js Remotion render
subprocess. Captures progress, maps known error codes, and returns the
output artifact path.
"""

import json
import os
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

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=settings.worker_job_timeout_seconds,
        )

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

    def _build_render_command(
        self,
        template_id: str,
        props_file: Path,
        output_file: Path,
    ) -> list[str]:
        """
        Build a rendering command for the requested template.

        Plan A implementation:
          - release_trailer prefers real Remotion CLI rendering when configured.
          - other templates continue through the existing node script contract.
        """
        if template_id == "release_trailer":
            cmd = self._build_release_trailer_command(props_file, output_file)
            if cmd:
                return cmd

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
    ) -> Optional[list[str]]:
        """
        Real Remotion render path for the release_trailer hero template.

        Environment contract:
          - REMOTION_ENTRY: path to Remotion entry file (default: remotion/index.ts)
          - RELEASE_TRAILER_COMPOSITION: composition ID (default: ReleaseTrailerV1)

        If requirements are not met, returns None and caller falls back.
        """
        if which("npx") is None:
            return None

        remotion_entry = os.getenv("REMOTION_ENTRY", "remotion/index.ts")
        composition_id = os.getenv("RELEASE_TRAILER_COMPOSITION", "ReleaseTrailerV1")
        entry_path = Path(remotion_entry)
        if not entry_path.exists():
            return None

        return [
            "npx",
            "remotion",
            "render",
            str(entry_path),
            composition_id,
            str(output_file),
            f"--props={str(props_file)}",
            "--codec=h264",
            "--concurrency=1",
        ]


runner = RenderRunner()
