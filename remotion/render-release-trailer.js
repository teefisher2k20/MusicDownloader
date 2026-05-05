#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { bundle } = require("@remotion/bundler");
const { getCompositions, renderMedia } = require("@remotion/renderer");

const args = {};
for (let i = 2; i < process.argv.length - 1; i += 2) {
  const key = process.argv[i].replace(/^--/, "");
  args[key] = process.argv[i + 1];
}

const entry = args.entry;
const compositionId = args.composition;
const propsFile = args.props;
const output = args.output;

if (!entry || !compositionId || !propsFile || !output) {
  console.error(
    "Usage: node remotion/render-release-trailer.js --entry <entry.ts> --composition <id> --props <file.json> --output <file.mp4>",
  );
  process.exit(1);
}

async function main() {
  const entryPath = path.resolve(entry);
  const propsPath = path.resolve(propsFile);
  const outputPath = path.resolve(output);

  if (!fs.existsSync(entryPath)) {
    console.error(`Could not find entry point: ${entryPath}`);
    process.exit(1);
  }

  if (!fs.existsSync(propsPath)) {
    console.error(`Props file not found: ${propsPath}`);
    process.exit(1);
  }

  const outputDir = path.dirname(outputPath);
  fs.mkdirSync(outputDir, { recursive: true });

  let inputProps;
  try {
    inputProps = JSON.parse(fs.readFileSync(propsPath, "utf8"));
  } catch (err) {
    console.error(`Failed to parse props JSON: ${err.message}`);
    process.exit(1);
  }

  const serveUrl = await bundle({ entryPoint: entryPath });
  const compositions = await getCompositions(serveUrl, {
    inputProps,
  });

  const composition = compositions.find((c) => c.id === compositionId);
  if (!composition) {
    console.error(`Could not find a composition with id '${compositionId}'`);
    process.exit(1);
  }

  let lastPct = -1;
  await renderMedia({
    serveUrl,
    composition,
    codec: "h264",
    outputLocation: outputPath,
    inputProps,
    onProgress: (progress) => {
      let pct = 0;

      if (typeof progress === "number") {
        pct = Math.round(progress * 100);
      } else if (progress && typeof progress.progress === "number") {
        pct = Math.round(progress.progress * 100);
      } else if (
        progress &&
        typeof progress.renderedFrames === "number" &&
        typeof composition.durationInFrames === "number" &&
        composition.durationInFrames > 0
      ) {
        pct = Math.round(
          (progress.renderedFrames / composition.durationInFrames) * 100,
        );
      }

      pct = Math.max(0, Math.min(100, pct));
      if (pct !== lastPct) {
        lastPct = pct;
        console.log(`REMOTION_PROGRESS:${pct}`);
      }
    },
  });
}

main().catch((err) => {
  const message = err && err.message ? err.message : String(err);
  console.error(message);
  process.exit(1);
});
