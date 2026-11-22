/**
 * make.fun entry gta6-meme-x-01 — output stage.
 *
 * Copies POST.json from $MAKEFUN_BOT_DIR (default /bot) into
 * $MAKEFUN_OUTPUT_DIR (default /output), creating the destination
 * directory if it does not exist.
 *
 * Before copying, POST.json is read and parsed: it must be a JSON object
 * with a non-empty string `url`. Anything else is refused, so a corrupt or
 * truncated entry never reaches the output directory.
 *
 * Node 22, standard library only. No third-party packages, no network.
 *
 * Run: MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
 */

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR || "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const POST_FILE = "POST.json";

/** Print a diagnostic to stderr and terminate with a non-zero code. */
function fail(message: string, code = 1): never {
  console.error(`make.fun: ${message}`);
  process.exit(code);
}

/**
 * Read POST.json and assert it is the shape the house expects:
 * a JSON object whose `url` is a non-empty string.
 *
 * Exit codes: 2 when the file itself is absent, 1 when it exists but the
 * body is malformed.
 */
function readAndValidate(src: string): void {
  let raw: string;
  try {
    raw = readFileSync(src, "utf8");
  } catch (err) {
    const code = (err as NodeJS.ErrnoException).code;
    if (code === "ENOENT") {
      fail(`POST.json not found at ${src}`, 2);
    }
    fail(`cannot read ${src}: ${(err as Error).message}`, 1);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    fail(`${src} is not valid JSON: ${(err as Error).message}`);
  }

  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    fail(`${src} must contain a JSON object, got ${Array.isArray(parsed) ? "array" : typeof parsed}`);
  }

  const url = (parsed as Record<string, unknown>).url;
  if (typeof url !== "string" || url.trim() === "") {
    fail(`${src} must have a non-empty string "url" field`);
  }
}

function main(): void {
  const src = resolve(BOT_DIR, POST_FILE);
  const outDir = resolve(OUTPUT_DIR);
  const dest = join(outDir, POST_FILE);

  console.error(`make.fun: source ${src}`);
  console.error(`make.fun: destination ${dest}`);

  readAndValidate(src);

  try {
    mkdirSync(outDir, { recursive: true });
  } catch (err) {
    fail(`cannot create output dir ${outDir}: ${(err as Error).message}`);
  }

  try {
    copyFileSync(src, dest);
  } catch (err) {
    fail(`cannot copy ${src} -> ${dest}: ${(err as Error).message}`);
  }

  console.log(`copied ${src} -> ${dest}`);
}

main();
