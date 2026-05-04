#!/usr/bin/env python3
"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.

3 format (youtube/short/square) × N frame で `npx remotion still` を生成し、
各 PNG の dimension が format 期待値と一致するか ffprobe で検証する。

| format | width × height | aspect |
|--------|---------------|--------|
| youtube | 1920 × 1080 | 16:9 |
| short   | 1080 × 1920 | 9:16 |
| square  | 1080 × 1080 | 1:1 |

不一致 = exit non-zero (regression として CI/Roku 視認の双方で検知)。
ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。

Codex Phase 3G design (2026-05-04, CODEX_PHASE3G_NEXT) 推奨:
- videoConfig.ts FORMAT を try/finally で in-place 切替 + restore
- per-format remotion still、frame 30/90 デフォルト
- 各 still を ffprobe で width/height 検証
- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)

前提:
- 対象 SuperMovie project (main.mp4 / node_modules / remotion installed)
- ffprobe / ffmpeg コマンドが PATH に存在 (Phase 3-A 以降 preflight で検証済み)

Usage:
    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
    python3 scripts/visual_smoke.py --formats youtube,short
    python3 scripts/visual_smoke.py --frames 30,90,180
    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)

Exit code:
    0 = 全 still 出力 + dimension 一致
    2 = 1 件以上 dimension mismatch (regression)
    3 = remotion still / ffprobe / ffmpeg 実行失敗 (環境問題)
    4 = videoConfig.ts 解析失敗 (FORMAT 行 regex 不一致)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
SMOKE_OUT = PROJ / "out" / "visual_smoke"
COMPOSITION_ID = "MainVideo"

FORMAT_DIMS = {
    "youtube": (1920, 1080),
    "short": (1080, 1920),
    "square": (1080, 1080),
}
FORMAT_LINE_RE = re.compile(
    r"^(export const FORMAT: VideoFormat = ')(youtube|short|square)(';)$",
    re.MULTILINE,
)


def patch_format(content: str, fmt: str) -> str:
    """videoConfig.ts の FORMAT 行を fmt に書き換える。

    一致 0 件で ValueError、複数一致でも先頭1件のみ書換 (Anchored multi-line)。
    """
    if not FORMAT_LINE_RE.search(content):
        raise ValueError(
            f"FORMAT 行が videoConfig.ts に見つからない: pattern={FORMAT_LINE_RE.pattern}"
        )
    return FORMAT_LINE_RE.sub(rf"\g<1>{fmt}\g<3>", content, count=1)


def probe_dim(png: Path) -> tuple[int, int]:
    """ffprobe で PNG の width × height を取得。"""
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "json",
            str(png),
        ],
        text=True,
    )
    info = json.loads(out)
    s = info["streams"][0]
    return int(s["width"]), int(s["height"])


def render_still(project: Path, frame: int, png_out: Path) -> None:
    """`npx remotion still` で 1 frame の PNG 出力。"""
    png_out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            "npx",
            "--no-install",
            "remotion",
            "still",
            COMPOSITION_ID,
            str(png_out),
            "--frame",
            str(frame),
        ],
        cwd=str(project),
    )


def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: list[int]) -> None:
    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。

    ffmpeg filter_complex で hstack (frame 軸) → vstack (format 軸) する。
    各 cell に format/frame ラベルを drawtext で焼き込み (debug 即見可).
    """
    if not stills:
        return
    grid_out.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    for s in stills:
        inputs.extend(["-i", str(s)])

    n_fmt = len(formats)
    n_frm = len(frames)
    filter_parts: list[str] = []
    # 各 cell をラベル付き thumb にスケーリング (短辺 360px に固定)
    for i, s in enumerate(stills):
        fmt = formats[i // n_frm]
        frm = frames[i % n_frm]
        label = f"{fmt} f{frm}"
        # label 付きで scale
        filter_parts.append(
            f"[{i}:v]scale=-2:360,"
            f"drawtext=text='{label}':fontcolor=white:fontsize=24:"
            f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
        )

    # 各 format 行の hstack
    row_labels: list[str] = []
    for r in range(n_fmt):
        row_in = "".join(f"[c{r * n_frm + c}]" for c in range(n_frm))
        row_label = f"row{r}"
        if n_frm == 1:
            filter_parts.append(f"{row_in}copy[{row_label}]")
        else:
            filter_parts.append(f"{row_in}hstack=inputs={n_frm}[{row_label}]")
        row_labels.append(f"[{row_label}]")

    # vstack
    if n_fmt == 1:
        filter_parts.append(f"{row_labels[0]}copy[grid]")
    else:
        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")

    cmd = (
        ["ffmpeg", "-y"]
        + inputs
        + [
            "-filter_complex",
            ";".join(filter_parts),
            "-map",
            "[grid]",
            "-frames:v",
            "1",
            str(grid_out),
        ]
    )
    subprocess.check_call(cmd)


def cli() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--formats",
        default="youtube,short,square",
        help="検証対象 format (カンマ区切り、default 全 3 種)",
    )
    ap.add_argument(
        "--frames",
        default="30,90",
        help="検証 frame 番号 (カンマ区切り、default 30,90)",
    )
    ap.add_argument("--out-dir", default=str(SMOKE_OUT), help="出力ディレクトリ")
    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
    args = ap.parse_args()

    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
    for f in formats:
        if f not in FORMAT_DIMS:
            print(f"ERROR: 未知の format: {f} (許容: {','.join(FORMAT_DIMS)})", file=sys.stderr)
            return 4
    frames = [int(x) for x in args.frames.split(",") if x.strip()]

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # 環境チェック
    for tool in ("npx", "ffprobe", "ffmpeg"):
        if shutil.which(tool) is None:
            print(f"ERROR: {tool} コマンドが PATH にない", file=sys.stderr)
            return 3

    # videoConfig.ts 原本保持
    if not VIDEO_CONFIG.exists():
        print(f"ERROR: videoConfig.ts が無い: {VIDEO_CONFIG}", file=sys.stderr)
        return 4
    original = VIDEO_CONFIG.read_text(encoding="utf-8")

    results: list[dict] = []
    stills: list[Path] = []
    failed = 0

    try:
        for fmt in formats:
            try:
                patched = patch_format(original, fmt)
            except ValueError as e:
                print(f"ERROR: {e}", file=sys.stderr)
                return 4
            VIDEO_CONFIG.write_text(patched, encoding="utf-8")
            print(f"\n[smoke] format={fmt} に切替て still を出力します")
            for frame in frames:
                png = out_dir / f"smoke_{fmt}_f{frame:04d}.png"
                try:
                    render_still(PROJ, frame, png)
                except subprocess.CalledProcessError as e:
                    print(
                        f"  ERROR: remotion still failed (fmt={fmt}, frame={frame}): {e}",
                        file=sys.stderr,
                    )
                    failed += 1
                    results.append(
                        {"format": fmt, "frame": frame, "ok": False, "error": "still_failed"}
                    )
                    continue
                try:
                    w, h = probe_dim(png)
                except subprocess.CalledProcessError as e:
                    print(f"  ERROR: ffprobe failed for {png}: {e}", file=sys.stderr)
                    failed += 1
                    results.append(
                        {"format": fmt, "frame": frame, "ok": False, "error": "probe_failed"}
                    )
                    continue
                expected = FORMAT_DIMS[fmt]
                ok = (w, h) == expected
                if not ok:
                    failed += 1
                results.append(
                    {
                        "format": fmt,
                        "frame": frame,
                        "ok": ok,
                        "expected": list(expected),
                        "actual": [w, h],
                        "png": str(png),
                    }
                )
                stills.append(png)
                marker = "OK" if ok else "MISMATCH"
                print(
                    f"  [{marker}] {png.name}: expected={expected[0]}x{expected[1]}, "
                    f"actual={w}x{h}"
                )
    finally:
        VIDEO_CONFIG.write_text(original, encoding="utf-8")
        print(f"\n[smoke] videoConfig.ts を原本に restore しました")

    if not args.no_grid and stills:
        grid_out = out_dir / "grid.png"
        try:
            make_grid(stills, grid_out, formats, frames)
            print(f"\n[smoke] grid: {grid_out}")
        except subprocess.CalledProcessError as e:
            print(f"WARN: ffmpeg grid 合成失敗: {e}", file=sys.stderr)

    summary_path = out_dir / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "formats": formats,
                "frames": frames,
                "results": results,
                "failed": failed,
                "total": len(results),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nsummary: {summary_path}")
    print(f"  total={len(results)}, failed={failed}")

    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(cli())
