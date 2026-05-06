#!/usr/bin/env node
/**
 * BudouX で日本語テキストを phrase 単位に分割する薄い helper.
 *
 * usage:
 *   node scripts/budoux_split.mjs --in input.json --out phrases.json
 *
 * input.json:  { "segments": [ { "id": 0, "text": "..." }, ... ] }
 * phrases.json: { "segments": [ { "id": 0, "text": "...", "phrases": ["...", "..."] } ] }
 *
 * BudouX は Google 製の文節分割ライブラリ。Markov 風 model で日本語を意味境界で
 * 切るので、SuperMovie の「24 字制限で機械的に切る」ロジックの代替に使う。
 *
 * 公式: https://github.com/google/budoux/tree/main/javascript/
 *       https://www.npmjs.com/package/budoux
 *
 * 設計起点: Codex Phase 2b design (2026-05-04, CODEX_PHASE2B_BUDOUX)
 */
import { loadDefaultJapaneseParser } from "budoux";
import { readFileSync, writeFileSync } from "node:fs";
import { argv, exit } from "node:process";

function parseArgs(args) {
  const out = { in: null, out: null };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--in") out.in = args[++i];
    else if (a === "--out") out.out = args[++i];
    else if (a === "--text") out.text = args[++i]; // single-text mode
  }
  return out;
}

const opts = parseArgs(argv.slice(2));
const parser = loadDefaultJapaneseParser();

if (opts.text != null) {
  // single-text smoke test: stdout に phrases JSON を書く
  const phrases = parser.parse(opts.text);
  process.stdout.write(JSON.stringify({ text: opts.text, phrases }, null, 2));
  exit(0);
}

if (!opts.in || !opts.out) {
  console.error("usage: node budoux_split.mjs --in input.json --out phrases.json");
  console.error("       node budoux_split.mjs --text 'テキスト'");
  exit(2);
}

const input = JSON.parse(readFileSync(opts.in, "utf8"));
const segments = (input.segments || []).map((seg) => ({
  ...seg,
  phrases: parser.parse(seg.text || ""),
}));

writeFileSync(opts.out, JSON.stringify({ segments }, null, 2), "utf8");
console.error(`wrote: ${opts.out} (${segments.length} segments)`);
