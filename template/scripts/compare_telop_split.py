#!/usr/bin/env python3
"""baseline と new の telop 分割を 5 KPI で比較する.

Codex Phase 2b design (2026-05-04, CODEX_PHASE2B_BUDOUX) Q3 の KPI ゲート:
  hard_word_split_count = 0
  linebreak_inside_preserve_count = 0
  single_char_telops_new <= baseline
  two_char_tail_telops_new <= baseline
  frame_overlap_count = 0

Usage:
    # 1. baseline (旧ロジック) で生成
    python3 scripts/build_telop_data.py --baseline
    cp src/テロップテンプレート/telopData.ts /tmp/telop_baseline.ts

    # 2. new (BudouX) で生成
    python3 scripts/build_telop_data.py
    cp src/テロップテンプレート/telopData.ts /tmp/telop_new.ts

    # 3. 比較
    python3 scripts/compare_telop_split.py /tmp/telop_baseline.ts /tmp/telop_new.ts
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent


def parse_telop_data_ts(ts_path: Path) -> list[dict]:
    """telopData.ts から telop 配列を抽出 (簡易 parser)."""
    text = ts_path.read_text(encoding="utf-8")
    # `text: "..."` 部分は \n や 引用符のエスケープがあるので JSON で読む
    items = []
    for m in re.finditer(
        r"\{\s*id:\s*(\d+),\s*startFrame:\s*(\d+),\s*endFrame:\s*(\d+),\s*text:\s*(.+?),\s*style:\s*'(\w+)'",
        text,
        re.S,
    ):
        idn, sf, ef, txt_raw, style = m.groups()
        # txt_raw は JSON 文字列 (例: "abc\\nd") として書かれている
        try:
            txt = json.loads(txt_raw)
        except json.JSONDecodeError:
            txt = txt_raw.strip().strip(",").strip("\"")
        items.append({
            "id": int(idn),
            "startFrame": int(sf),
            "endFrame": int(ef),
            "text": txt,
            "style": style,
        })
    return items


def kpi_metrics(telops: list[dict], words: list[dict], preserve: list[str]) -> dict:
    """telopData から KPI を計算する."""
    out = {
        "telop_count": len(telops),
        "single_char_telops": 0,
        "two_char_tail_telops": 0,  # 改行後の最終行が 2 字以下
        "linebreak_inside_preserve_count": 0,
        "hard_word_split_count": 0,
        "frame_overlap_count": 0,
    }
    # single char telop
    for t in telops:
        plain = t["text"].replace("\n", "")
        if len(plain) <= 1:
            out["single_char_telops"] += 1
        # 改行後の最終行が 2 字以下
        if "\n" in t["text"]:
            last_line = t["text"].split("\n")[-1]
            if len(last_line) <= 2:
                out["two_char_tail_telops"] += 1
            # 改行位置が preserve 内に入っていないか
            line1, line2 = t["text"].split("\n", 1)
            joined = t["text"].replace("\n", "")
            i = len(line1)  # 改行位置
            for p in preserve:
                if not p:
                    continue
                idx = joined.find(p)
                while idx >= 0:
                    end = idx + len(p)
                    if idx < i < end:
                        out["linebreak_inside_preserve_count"] += 1
                        break
                    idx = joined.find(p, idx + 1)
    # frame overlap
    sorted_t = sorted(telops, key=lambda t: t["startFrame"])
    for i in range(len(sorted_t) - 1):
        if sorted_t[i]["endFrame"] > sorted_t[i + 1]["startFrame"]:
            out["frame_overlap_count"] += 1

    # hard_word_split: telop 境界が transcript の word 途中に入った件数
    # word.text を順に連結して各 word の文字 index を取得、
    # telop の text を joined 全文に対して find で一致位置を取得、
    # その境界 (前の telop の終わり + 次の始まり) が word の途中に来ていないか
    out["hard_word_split_count"] = 0
    if not words:
        return out
    full_text = "".join(w.get("text", "") for w in words)
    word_starts = []  # 各 word の full_text 上の開始位置
    cursor = 0
    for w in words:
        word_starts.append(cursor)
        cursor += len(w.get("text", ""))
    # 各 telop の境界の文字位置 (full_text 上)
    cursor = 0
    last_end = 0
    for t in telops:
        plain = t["text"].replace("\n", "")
        idx = full_text.find(plain, last_end)
        if idx < 0:
            continue
        end_pos = idx + len(plain)
        # 次 telop は end_pos 以降から探す, ここで「end_pos が word 途中」をチェック
        for ws_idx, ws in enumerate(word_starts):
            we = ws + len(words[ws_idx].get("text", ""))
            if ws < end_pos < we:
                out["hard_word_split_count"] += 1
                break
        last_end = end_pos
    return out


def main():
    if len(sys.argv) < 3:
        print("usage: compare_telop_split.py <baseline.ts> <new.ts>", file=sys.stderr)
        sys.exit(2)
    baseline_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])

    transcript = json.loads((PROJ / "transcript_fixed.json").read_text(encoding="utf-8"))
    typo = (PROJ / "typo_dict.json")
    typo_dict = json.loads(typo.read_text(encoding="utf-8")) if typo.exists() else {}
    preserve = typo_dict.get("preserve", [])
    words = transcript.get("words", [])

    base_telops = parse_telop_data_ts(baseline_path)
    new_telops = parse_telop_data_ts(new_path)
    base_kpi = kpi_metrics(base_telops, words, preserve)
    new_kpi = kpi_metrics(new_telops, words, preserve)

    print("=== KPI comparison (baseline -> new) ===")
    keys = ["telop_count", "single_char_telops", "two_char_tail_telops",
            "linebreak_inside_preserve_count", "hard_word_split_count", "frame_overlap_count"]
    print(f"{'metric':35} {'baseline':>10} {'new':>6} {'delta':>8}")
    print("-" * 64)
    for k in keys:
        b = base_kpi[k]
        n = new_kpi[k]
        delta = n - b
        sign = "+" if delta > 0 else ""
        print(f"{k:35} {b:>10} {n:>6} {sign}{delta:>7}")

    print()
    print("=== gate evaluation (Codex Phase 2b Q3) ===")
    gates = []
    gates.append(("hard_word_split_count == 0", new_kpi["hard_word_split_count"] == 0))
    gates.append(("linebreak_inside_preserve_count == 0", new_kpi["linebreak_inside_preserve_count"] == 0))
    gates.append(("single_char_telops_new <= baseline", new_kpi["single_char_telops"] <= base_kpi["single_char_telops"]))
    gates.append(("two_char_tail_telops_new <= baseline", new_kpi["two_char_tail_telops"] <= base_kpi["two_char_tail_telops"]))
    gates.append(("frame_overlap_count == 0", new_kpi["frame_overlap_count"] == 0))
    for desc, ok in gates:
        print(f"  {'PASS' if ok else 'FAIL'}: {desc}")

    if all(ok for _, ok in gates):
        print("\nALL PASS")
        sys.exit(0)
    else:
        print("\nSOME FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
