/**
 * make.fun meme entry - output stage.
 *
 * Copies POST.json from $MAKEFUN_BOT_DIR (default /bot) into
 * $MAKEFUN_OUTPUT_DIR (default /output), creating the destination
 * directory when missing. Exits 1 on any failure.
 *
 * Run: MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
 */

import { copyFileSync, mkdirSync } from "node:fs";
import { join, resolve } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR || "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const POST_FILE = "POST.json";

function fail(message: string, code = 1): never {
  console.error(`make.fun: ${message}`);
  process.exit(code);
}

function main(): void {
  const src = resolve(BOT_DIR, POST_FILE);
  const outDir = resolve(OUTPUT_DIR);
  const dest = join(outDir, POST_FILE);

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
