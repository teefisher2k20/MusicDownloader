#!/usr/bin/env node
/**
 * render.js — Remotion render entry point (stub for local development).
 *
 * In production, replace this stub with the actual Remotion CLI invocation
 * or a custom render harness. The production script must:
 *   1. Load the composition identified by --composition <id>
 *   2. Ingest props from the JSON file at --props <path>
 *   3. Write the output MP4 to --output <path>
 *   4. Exit 0 on success, non-zero on failure
 *
 * Remotion quick-start:
 *   npx create-video@latest
 *   npx remotion render <composition> --props <file> --output <file>
 */

const path = require("path");
const fs = require("fs");

// Parse CLI args: --key value pairs
const args = {};
for (let i = 2; i < process.argv.length - 1; i += 2) {
  const key = process.argv[i].replace(/^--/, "");
  args[key] = process.argv[i + 1];
}

const { composition, props: propsFile, output } = args;

if (!composition || !propsFile || !output) {
  console.error(
    "Usage: node render.js --composition <id> --props <file> --output <file>",
  );
  process.exit(1);
}

// Load and validate props file
let props;
try {
  props = JSON.parse(fs.readFileSync(propsFile, "utf8"));
} catch (err) {
  console.error("Failed to read props file:", err.message);
  process.exit(1);
}

console.log(`[render.js] composition=${composition}`);
console.log(`[render.js] props keys=${Object.keys(props).join(",")}`);
console.log(`[render.js] output=${output}`);

// ── Stub behaviour ────────────────────────────────────────────────────────────
// Writes a minimal valid MP4 placeholder so the worker pipeline can complete.
// Replace this section with real Remotion rendering logic.

const outputDir = path.dirname(output);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Minimal ftyp+mdat box: not a real video, but satisfies "file exists and is
// non-empty" checks. A real render will produce a proper MP4 here.
const STUB_MP4_BYTES = Buffer.from(
  "0000001C667479706D703432000000006D703432697" +
    "36F6D0000000008667265650000000000",
  "hex",
);
fs.writeFileSync(output, STUB_MP4_BYTES);

console.log(
  "[render.js] stub render complete — replace with real Remotion logic",
);
process.exit(0);
