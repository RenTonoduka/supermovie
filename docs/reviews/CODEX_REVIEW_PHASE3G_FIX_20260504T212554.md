Reading additional input from stdin...
2026-05-04T12:25:54.667569Z ERROR codex_core::session: failed to load skill /Users/rokumasuda/.claude/skills/script-sheet-output/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 83
OpenAI Codex v0.128.0 (research preview)
--------
workdir: /Users/rokumasuda/.claude/plugins/supermovie
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019df2f3-c2ec-75f3-996c-36255f3638c5
--------
user
SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。

照合手順:
1. `git log roku/phase3f-asset-gate..HEAD --oneline` で 3 commit 確認
2. `git show 7d0698b --stat` で fix commit の範囲把握
3. 各指摘について before/after を点検

検査チェックリスト (前回指摘番号 → 解消確認):

P1
- #1 visual_smoke.py: render/probe 失敗 → exit 3 経路、main.mp4/REMOTION_BIN 事前検査追加されているか
- #2 visual_smoke.py: drawtext filter 不在検査 + label fallback、grid 失敗 → exit 3 へ昇格、特殊文字 escape も
- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置

P2
- #4 visual_smoke.py docstring: --keep-stills 行削除
- #5 full matrix 時のみ grid (env_error / 部分失敗時 skip)
- #6 空 formats / 空 frames / 負数 frames で exit 4

P3
- #7 supermovie-narration SKILL.md: 連携マップ末尾の旧手順表記置換
- #8 MainVideo.tsx: getStaticFiles Studio cache 仕様の docs

regression / 新たな問題:
- ロジック分岐ミス (`break` 使用で外側 fmt loop の続行可否、env_error フラグ動作)
- 旧 exit 体系 (exit 2 only) 想定の caller があるか
- summary.json schema 変更で既存依存があるか
- escape 処理 (drawtext text=...) で他の特殊文字漏れ
- patch_format restore が SIGINT で走るか (try/finally なので走るはず)

出力フォーマット:
- 全 8 件: ✅ closed / ❌ remaining / ⚠️ partial の三段階で verdict
- 新規発見の P0/P1/P2/P3 があれば追加
- LGTM 禁止、最低 1 件 (軽微でも) 追加観察点を出す

短く決定的に (verdict 表 + 新規指摘のみ)。
2026-05-04T12:25:54.843737Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
2026-05-04T12:25:54.855046Z ERROR rmcp::transport::worker: worker quit with fatal: Transport channel closed, when AuthRequired(AuthRequiredError { www_authenticate_header: "Bearer error=\"invalid_token\", error_description=\"Authentication failed. The provided bearer token is invalid, expired, or no longer recognized by the server. To resolve: clear authentication tokens in your MCP client and reconnect. Your client should automatically re-register and obtain new tokens.\", resource_metadata=\"https://api.kashika-20mile.com/.well-known/oauth-protected-resource/mcp\"" })
hook: SessionStart
hook: SessionStart
hook: SessionStart
hook: SessionStart
hook: SessionStart Completed
hook: SessionStart Completed
hook: SessionStart Completed
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
hook: UserPromptSubmit Completed
codex
確認します。指定の `git log` / `git show` から差分範囲を実測し、その後に対象ファイルと既存 caller を読む順で見ます。
  → 指定 git log / show で差分範囲を確認
  • 8件の指摘ごとに該当コードを照合
  • regression と既存依存を検索
  • verdict 表と新規指摘をまとめる
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'git log roku/phase3f-asset-gate..HEAD --oneline' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-7oeAB6y2' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-GgMmHuQs' (errno=Operation not permitted)
7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
30a5094 fix(asset-gate): base video auto-mute when narration.wav present (Phase 3-F hotfix)

exec
/bin/zsh -lc 'git show 7d0698b --stat' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'git status --short --branch' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-U0ewm0qy' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-JFBUjGqe' (errno=Operation not permitted)
## roku/phase3g-visual-smoke
?? docs/

 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-Cw1LCjxp' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ljkrXQxc' (errno=Operation not permitted)
commit 7d0698b375c8ef92261bc5d0182d31e1348c3cb1
Author: 増田朗空 <rokumasuda@RokuMacBook-Pro-M5.local>
Date:   Mon May 4 21:24:57 2026 +0900

    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
    
    CODEX_REVIEW_PHASE3G_20260504T211444 指摘 8 件を 1 commit にまとめて反映。
    
    P1 fix:
    1. visual_smoke.py: render/probe 失敗を exit 3 (環境問題) として早期 break、
       dimension mismatch だけ exit 2 に分離。MAIN_VIDEO / REMOTION_BIN の事前
       存在検査を追加 (main.mp4 不在 / npm install 未実行 を即検知)。
    2. visual_smoke.py: ffmpeg drawtext filter 不在環境を起動時に検査し、不在
       時は label なし grid に自動 fallback。grid 合成失敗は WARN ではなく
       exit 3 へ昇格 (silent fail 防止)。drawtext text の特殊文字 (シングル
       クオート / コロン) を escape。
    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
       独立コマンドとして残す。template/ 直下の plugin repo CI で main.mp4
       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
       または `npm run test:visual-smoke` を呼ぶ運用)。
    
    P2 fix:
    4. visual_smoke.py: docstring から実装されていない `--keep-stills` 行を削除。
    5. visual_smoke.py: full matrix (len(stills) == n_fmt × n_frm) かつ env_error
       なしの時のみ grid 合成、部分失敗時は cell 対応崩れを防ぐため skip。
       summary.json に grid.status / grid.error を記録。
    6. visual_smoke.py: 空 --formats / 空 --frames / 負数 --frames を exit 4 で
       reject (旧: 空 list で total=0 のまま exit 0、誤合格)。
    
    P3 fix:
    7. supermovie-narration SKILL.md: 連携マップ末尾の旧手順「<NarrationAudio /> 有効化」
       を「MainVideo.tsx が public/narration.wav を自動検出」+ Studio reload
       注記に置換 (asset gate 整合)。
    8. MainVideo.tsx: getStaticFiles() の Studio キャッシュ仕様 (Remotion 公式
       docs https://www.remotion.dev/docs/getstaticfiles 準拠) を docstring に
       追記、Studio 実行中の新規 asset 反映には reload (Cmd+R) が必要と明記。
    
    検証 (Bash 実測):
    - `python3 visual_smoke.py --formats ""` → exit 4 / `--frames ""` → exit 4 /
      `--formats unknown` → exit 4 / `--frames -10` → exit 4 (旧 0)
    - `python3 visual_smoke.py` (template/ 直下、main.mp4 不在) → exit 3 with
      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
    - `has_drawtext_filter()` ローカル ffmpeg で False (drawtext filter 表示なし)
      → label なし grid path に fallback、env_error 起きない
    
    Codex 指摘 8/8 全カバー、自走範囲 + 段取り判断 #3 (test = lint のみで合理)。
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

 skills/supermovie-narration/SKILL.md |   9 ++-
 template/package.json                |   2 +-
 template/scripts/visual_smoke.py     | 130 +++++++++++++++++++++++++++--------
 template/src/MainVideo.tsx           |   8 ++-
 4 files changed, 117 insertions(+), 32 deletions(-)

codex
差分範囲は指定どおり 3 commit でした（`git log` Bash 実測）。次に `visual_smoke.py` と周辺 caller を行番号付きで確認し、exit code と `summary.json` 依存を検索します。
  ✓ 指定 git log / show で差分範囲を確認
  → 8件の指摘ごとに該当コードを照合
  • regression と既存依存を検索
  • verdict 表と新規指摘をまとめる
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'nl -ba template/scripts/visual_smoke.py' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'nl -ba template/package.json' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	{
     2	  "name": "supermovie-project",
     3	  "version": "1.0.0",
     4	  "description": "SuperMovie - Remotion動画プロジェクト",
     5	  "repository": {},
     6	  "license": "UNLICENSED",
     7	  "private": true,
     8	  "dependencies": {
     9	    "@remotion/cli": "4.0.403",
    10	    "@remotion/zod-types": "4.0.403",
    11	    "react": "19.2.3",
    12	    "react-dom": "19.2.3",
    13	    "remotion": "4.0.403",
    14	    "zod": "3.22.3",
    15	    "@remotion/tailwind-v4": "4.0.403",
    16	    "tailwindcss": "4.0.0",
    17	    "budoux": "^0.8.0"
    18	  },
    19	  "devDependencies": {
    20	    "@remotion/eslint-config-flat": "4.0.403",
    21	    "@types/react": "19.2.7",
    22	    "@types/web": "0.0.166",
    23	    "eslint": "9.19.0",
    24	    "prettier": "3.6.0",
    25	    "typescript": "5.9.3"
    26	  },
    27	  "scripts": {
    28	    "dev": "remotion studio",
    29	    "build": "remotion bundle",
    30	    "render": "remotion render MainVideo out/video.mp4",
    31	    "upgrade": "remotion upgrade",
    32	    "lint": "eslint src && tsc",
    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
    35	    "test": "npm run lint"
    36	  },
    37	  "sideEffects": [
    38	    "*.css"
    39	  ]
    40	}

 succeeded in 0ms:
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
     3	
     4	3 format (youtube/short/square) × N frame で `npx remotion still` を生成し、
     5	各 PNG の dimension が format 期待値と一致するか ffprobe で検証する。
     6	
     7	| format | width × height | aspect |
     8	|--------|---------------|--------|
     9	| youtube | 1920 × 1080 | 16:9 |
    10	| short   | 1080 × 1920 | 9:16 |
    11	| square  | 1080 × 1080 | 1:1 |
    12	
    13	不一致 = exit non-zero (regression として CI/Roku 視認の双方で検知)。
    14	ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
    15	
    16	Codex Phase 3G design (2026-05-04, CODEX_PHASE3G_NEXT) 推奨:
    17	- videoConfig.ts FORMAT を try/finally で in-place 切替 + restore
    18	- per-format remotion still、frame 30/90 デフォルト
    19	- 各 still を ffprobe で width/height 検証
    20	- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
    21	
    22	前提:
    23	- 対象 SuperMovie project (main.mp4 / node_modules / remotion installed)
    24	- ffprobe / ffmpeg コマンドが PATH に存在 (Phase 3-A 以降 preflight で検証済み)
    25	
    26	Usage:
    27	    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
    28	    python3 scripts/visual_smoke.py --formats youtube,short
    29	    python3 scripts/visual_smoke.py --frames 30,90,180
    30	    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
    31	
    32	Exit code:
    33	    0 = 全 still 出力 + dimension 一致
    34	    2 = 1 件以上 dimension mismatch (regression、render は成功している)
    35	    3 = 実行環境問題 (main.mp4 不在 / node_modules 不在 / remotion still failed /
    36	         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
    37	    4 = 入力 / 設定不正 (videoConfig.ts 不在 or FORMAT 行 regex 不一致 /
    38	         空 formats / 空 frames / 未知 format)
    39	"""
    40	from __future__ import annotations
    41	
    42	import argparse
    43	import json
    44	import re
    45	import shutil
    46	import subprocess
    47	import sys
    48	from pathlib import Path
    49	
    50	PROJ = Path(__file__).resolve().parent.parent
    51	VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
    52	SMOKE_OUT = PROJ / "out" / "visual_smoke"
    53	COMPOSITION_ID = "MainVideo"
    54	MAIN_VIDEO = PROJ / "public" / "main.mp4"
    55	REMOTION_BIN = PROJ / "node_modules" / ".bin" / "remotion"
    56	
    57	FORMAT_DIMS = {
    58	    "youtube": (1920, 1080),
    59	    "short": (1080, 1920),
    60	    "square": (1080, 1080),
    61	}
    62	FORMAT_LINE_RE = re.compile(
    63	    r"^(export const FORMAT: VideoFormat = ')(youtube|short|square)(';)$",
    64	    re.MULTILINE,
    65	)
    66	
    67	
    68	def patch_format(content: str, fmt: str) -> str:
    69	    """videoConfig.ts の FORMAT 行を fmt に書き換える。
    70	
    71	    一致 0 件で ValueError、複数一致でも先頭1件のみ書換 (Anchored multi-line)。
    72	    """
    73	    if not FORMAT_LINE_RE.search(content):
    74	        raise ValueError(
    75	            f"FORMAT 行が videoConfig.ts に見つからない: pattern={FORMAT_LINE_RE.pattern}"
    76	        )
    77	    return FORMAT_LINE_RE.sub(rf"\g<1>{fmt}\g<3>", content, count=1)
    78	
    79	
    80	def probe_dim(png: Path) -> tuple[int, int]:
    81	    """ffprobe で PNG の width × height を取得。"""
    82	    out = subprocess.check_output(
    83	        [
    84	            "ffprobe",
    85	            "-v",
    86	            "error",
    87	            "-select_streams",
    88	            "v:0",
    89	            "-show_entries",
    90	            "stream=width,height",
    91	            "-of",
    92	            "json",
    93	            str(png),
    94	        ],
    95	        text=True,
    96	    )
    97	    info = json.loads(out)
    98	    s = info["streams"][0]
    99	    return int(s["width"]), int(s["height"])
   100	
   101	
   102	def render_still(project: Path, frame: int, png_out: Path) -> None:
   103	    """`npx remotion still` で 1 frame の PNG 出力。"""
   104	    png_out.parent.mkdir(parents=True, exist_ok=True)
   105	    subprocess.check_call(
   106	        [
   107	            "npx",
   108	            "--no-install",
   109	            "remotion",
   110	            "still",
   111	            COMPOSITION_ID,
   112	            str(png_out),
   113	            "--frame",
   114	            str(frame),
   115	        ],
   116	        cwd=str(project),
   117	    )
   118	
   119	
   120	def has_drawtext_filter() -> bool:
   121	    """ffmpeg build に drawtext filter (libfreetype) が含まれるか確認。
   122	
   123	    Mac Homebrew 標準 build は drawtext を持つが、minimal build では落ちている
   124	    ことがあるため事前検査する (Codex Phase 3-G review P1 #2 反映)。
   125	    """
   126	    try:
   127	        out = subprocess.check_output(
   128	            ["ffmpeg", "-hide_banner", "-filters"], text=True, stderr=subprocess.STDOUT
   129	        )
   130	    except (subprocess.CalledProcessError, FileNotFoundError):
   131	        return False
   132	    for line in out.splitlines():
   133	        if " drawtext " in f" {line} ":
   134	            return True
   135	    return False
   136	
   137	
   138	def make_grid(
   139	    stills: list[Path],
   140	    grid_out: Path,
   141	    formats: list[str],
   142	    frames: list[int],
   143	    label: bool,
   144	) -> None:
   145	    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
   146	
   147	    呼び出し側で full matrix (len(stills) == n_fmt * n_frm) を保証すること
   148	    (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
   149	    label=True の時は drawtext で format/frame を焼き込み、False の時は scale のみ
   150	    (drawtext filter 不在環境向け、Codex P1 #2 反映)。
   151	    """
   152	    if not stills:
   153	        return
   154	    grid_out.parent.mkdir(parents=True, exist_ok=True)
   155	    inputs: list[str] = []
   156	    for s in stills:
   157	        inputs.extend(["-i", str(s)])
   158	
   159	    n_fmt = len(formats)
   160	    n_frm = len(frames)
   161	    filter_parts: list[str] = []
   162	    # 各 cell を thumb にスケーリング (短辺 360px に固定)、必要なら drawtext
   163	    for i, s in enumerate(stills):
   164	        fmt = formats[i // n_frm]
   165	        frm = frames[i % n_frm]
   166	        if label:
   167	            txt = f"{fmt} f{frm}".replace("'", r"\'").replace(":", r"\:")
   168	            filter_parts.append(
   169	                f"[{i}:v]scale=-2:360,"
   170	                f"drawtext=text='{txt}':fontcolor=white:fontsize=24:"
   171	                f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
   172	            )
   173	        else:
   174	            filter_parts.append(f"[{i}:v]scale=-2:360[c{i}]")
   175	
   176	    # 各 format 行の hstack
   177	    row_labels: list[str] = []
   178	    for r in range(n_fmt):
   179	        row_in = "".join(f"[c{r * n_frm + c}]" for c in range(n_frm))
   180	        row_label = f"row{r}"
   181	        if n_frm == 1:
   182	            filter_parts.append(f"{row_in}copy[{row_label}]")
   183	        else:
   184	            filter_parts.append(f"{row_in}hstack=inputs={n_frm}[{row_label}]")
   185	        row_labels.append(f"[{row_label}]")
   186	
   187	    # vstack
   188	    if n_fmt == 1:
   189	        filter_parts.append(f"{row_labels[0]}copy[grid]")
   190	    else:
   191	        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
   192	
   193	    cmd = (
   194	        ["ffmpeg", "-y"]
   195	        + inputs
   196	        + [
   197	            "-filter_complex",
   198	            ";".join(filter_parts),
   199	            "-map",
   200	            "[grid]",
   201	            "-frames:v",
   202	            "1",
   203	            str(grid_out),
   204	        ]
   205	    )
   206	    subprocess.check_call(cmd)
   207	
   208	
   209	def cli() -> int:
   210	    ap = argparse.ArgumentParser()
   211	    ap.add_argument(
   212	        "--formats",
   213	        default="youtube,short,square",
   214	        help="検証対象 format (カンマ区切り、default 全 3 種)",
   215	    )
   216	    ap.add_argument(
   217	        "--frames",
   218	        default="30,90",
   219	        help="検証 frame 番号 (カンマ区切り、default 30,90)",
   220	    )
   221	    ap.add_argument("--out-dir", default=str(SMOKE_OUT), help="出力ディレクトリ")
   222	    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
   223	    args = ap.parse_args()
   224	
   225	    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
   226	    if not formats:
   227	        print("ERROR: --formats が空です (例: --formats youtube,short)", file=sys.stderr)
   228	        return 4
   229	    for f in formats:
   230	        if f not in FORMAT_DIMS:
   231	            print(f"ERROR: 未知の format: {f} (許容: {','.join(FORMAT_DIMS)})", file=sys.stderr)
   232	            return 4
   233	    frames = [int(x) for x in args.frames.split(",") if x.strip()]
   234	    if not frames:
   235	        print("ERROR: --frames が空です (例: --frames 30,90)", file=sys.stderr)
   236	        return 4
   237	    if any(f < 0 for f in frames):
   238	        print(f"ERROR: --frames に負数: {frames}", file=sys.stderr)
   239	        return 4
   240	
   241	    out_dir = Path(args.out_dir).resolve()
   242	    out_dir.mkdir(parents=True, exist_ok=True)
   243	
   244	    # 環境チェック (Codex Phase 3-G review P1 #1 反映、render 失敗を環境問題として早期検知)
   245	    for tool in ("npx", "ffprobe", "ffmpeg"):
   246	        if shutil.which(tool) is None:
   247	            print(f"ERROR: {tool} コマンドが PATH にない", file=sys.stderr)
   248	            return 3
   249	    if not MAIN_VIDEO.exists():
   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
   251	        return 3
   252	    if not REMOTION_BIN.exists():
   253	        print(
   254	            f"ERROR: remotion CLI が無い: {REMOTION_BIN} "
   255	            f"(npm install を先に実行してください)",
   256	            file=sys.stderr,
   257	        )
   258	        return 3
   259	    grid_label = has_drawtext_filter()
   260	    if not grid_label and not args.no_grid:
   261	        print(
   262	            "INFO: ffmpeg drawtext filter なし、grid label を skip して画像のみ合成します",
   263	            file=sys.stderr,
   264	        )
   265	
   266	    # videoConfig.ts 原本保持
   267	    if not VIDEO_CONFIG.exists():
   268	        print(f"ERROR: videoConfig.ts が無い: {VIDEO_CONFIG}", file=sys.stderr)
   269	        return 4
   270	    original = VIDEO_CONFIG.read_text(encoding="utf-8")
   271	
   272	    results: list[dict] = []
   273	    stills: list[Path] = []
   274	    mismatched = 0  # dimension 不一致のみカウント (render/probe 失敗は exit 3 系で別扱い)
   275	    env_error: str | None = None
   276	
   277	    try:
   278	        for fmt in formats:
   279	            if env_error:
   280	                break
   281	            try:
   282	                patched = patch_format(original, fmt)
   283	            except ValueError as e:
   284	                print(f"ERROR: {e}", file=sys.stderr)
   285	                return 4
   286	            VIDEO_CONFIG.write_text(patched, encoding="utf-8")
   287	            print(f"\n[smoke] format={fmt} に切替て still を出力します")
   288	            for frame in frames:
   289	                png = out_dir / f"smoke_{fmt}_f{frame:04d}.png"
   290	                try:
   291	                    render_still(PROJ, frame, png)
   292	                except subprocess.CalledProcessError as e:
   293	                    # P1 #1: render 失敗は環境問題 (exit 3) として即終了
   294	                    print(
   295	                        f"  ERROR: remotion still failed (fmt={fmt}, frame={frame}): {e}",
   296	                        file=sys.stderr,
   297	                    )
   298	                    env_error = "still_failed"
   299	                    results.append(
   300	                        {"format": fmt, "frame": frame, "ok": False, "error": "still_failed"}
   301	                    )
   302	                    break
   303	                try:
   304	                    w, h = probe_dim(png)
   305	                except subprocess.CalledProcessError as e:
   306	                    print(f"  ERROR: ffprobe failed for {png}: {e}", file=sys.stderr)
   307	                    env_error = "probe_failed"
   308	                    results.append(
   309	                        {"format": fmt, "frame": frame, "ok": False, "error": "probe_failed"}
   310	                    )
   311	                    break
   312	                expected = FORMAT_DIMS[fmt]
   313	                ok = (w, h) == expected
   314	                if not ok:
   315	                    mismatched += 1
   316	                results.append(
   317	                    {
   318	                        "format": fmt,
   319	                        "frame": frame,
   320	                        "ok": ok,
   321	                        "expected": list(expected),
   322	                        "actual": [w, h],
   323	                        "png": str(png),
   324	                    }
   325	                )
   326	                stills.append(png)
   327	                marker = "OK" if ok else "MISMATCH"
   328	                print(
   329	                    f"  [{marker}] {png.name}: expected={expected[0]}x{expected[1]}, "
   330	                    f"actual={w}x{h}"
   331	                )
   332	    finally:
   333	        VIDEO_CONFIG.write_text(original, encoding="utf-8")
   334	        print(f"\n[smoke] videoConfig.ts を原本に restore しました")
   335	
   336	    grid_status = "skipped"
   337	    grid_error: str | None = None
   338	    full_matrix = len(stills) == len(formats) * len(frames) and not env_error
   339	    if not args.no_grid and full_matrix:
   340	        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
   341	        grid_out = out_dir / "grid.png"
   342	        try:
   343	            make_grid(stills, grid_out, formats, frames, label=grid_label)
   344	            print(f"\n[smoke] grid: {grid_out}")
   345	            grid_status = "ok"
   346	        except subprocess.CalledProcessError as e:
   347	            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)
   348	            print(f"ERROR: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
   349	            grid_status = "failed"
   350	            grid_error = str(e)
   351	
   352	    summary_path = out_dir / "summary.json"
   353	    summary_path.write_text(
   354	        json.dumps(
   355	            {
   356	                "formats": formats,
   357	                "frames": frames,
   358	                "results": results,
   359	                "mismatched": mismatched,
   360	                "total": len(results),
   361	                "env_error": env_error,
   362	                "grid": {"status": grid_status, "error": grid_error},
   363	            },
   364	            ensure_ascii=False,
   365	            indent=2,
   366	        ),
   367	        encoding="utf-8",
   368	    )
   369	    print(f"\nsummary: {summary_path}")
   370	    print(f"  total={len(results)}, mismatched={mismatched}, env_error={env_error}, grid={grid_status}")
   371	
   372	    if env_error or grid_status == "failed":
   373	        return 3
   374	    if mismatched:
   375	        return 2
   376	    return 0
   377	
   378	
   379	if __name__ == "__main__":
   380	    sys.exit(cli())

exec
/bin/zsh -lc 'nl -ba skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'nl -ba template/src/MainVideo.tsx' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
     1	import { AbsoluteFill, Video, getStaticFiles, staticFile } from 'remotion';
     2	import { TelopPlayer } from './テロップテンプレート';
     3	import { SESequence } from './SoundEffects/SESequence';
     4	import { BGM } from './SoundEffects/BGM';
     5	import { ImageSequence } from './InsertImage';
     6	import { TitleSequence } from './Title';
     7	import { SlideSequence } from './Slides';
     8	import { NarrationAudio } from './Narration';
     9	import { VIDEO_FILE } from './videoConfig';
    10	
    11	const NARRATION_FILE = 'narration.wav';
    12	
    13	export const MainVideo: React.FC = () => {
    14	  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
    15	  // 不在なら 1.0 で再生 (二重音声防止)。getStaticFiles は Studio/render 時に
    16	  // public/ 配下の asset 一覧を返す Remotion 公式 API
    17	  // (https://www.remotion.dev/docs/getstaticfiles)。
    18	  // 注意: Studio 起動後に narration.wav を生成した場合、Studio をリロード
    19	  // (Cmd+R / `r` キー) しないと反映されない。新規 asset 追加には watchStaticFile
    20	  // を使う選択肢もあるが、現状は単純化のため reload 方式を採用。
    21	  const hasNarration = getStaticFiles().some((f) => f.name === NARRATION_FILE);
    22	  const baseVolume = hasNarration ? 0 : 1.0;
    23	
    24	  return (
    25	    <AbsoluteFill style={{ backgroundColor: 'black' }}>
    26	      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
    27	      <Video
    28	        src={staticFile(VIDEO_FILE)}
    29	        volume={() => baseVolume}
    30	        style={{
    31	          width: '100%',
    32	          height: '100%',
    33	          objectFit: 'contain',
    34	        }}
    35	      />
    36	
    37	      {/* スライド (Phase 3-A、別レイヤーで動画の上に被せる) */}
    38	      <SlideSequence />
    39	
    40	      {/* 挿入画像 */}
    41	      <ImageSequence />
    42	
    43	      {/* テロップ */}
    44	      <TelopPlayer />
    45	
    46	      {/* タイトル */}
    47	      <TitleSequence />
    48	
    49	      {/* ナレーション (Phase 3-F asset gate、narration.wav 不在で null) */}
    50	      <NarrationAudio volume={1.0} />
    51	
    52	      {/* BGM (Phase 3-F asset gate、bgm.mp3 不在で null) */}
    53	      <BGM volume={0.08} />
    54	
    55	      {/* 効果音 */}
    56	      <SESequence />
    57	    </AbsoluteFill>
    58	  );
    59	};

 succeeded in 0ms:
     1	---
     2	name: supermovie-narration
     3	description: |
     4	  VOICEVOX (ローカル無料 TTS) で transcript_fixed.json から narration.wav を生成し、
     5	  Remotion の <NarrationAudio /> layer で再生するスキル。
     6	  「ナレーション」「TTS」「VOICEVOX」「読み上げ」と言われたときに使用。
     7	argument-hint: [プロジェクトパス] [--speaker N] [--script <path>]
     8	allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
     9	effort: medium
    10	---
    11	
    12	# SuperMovie Narration — VOICEVOX 自動ナレーション
    13	
    14	Senior video producer として、文字起こし結果から自動ナレーションを生成し、
    15	動画の元音声を差し替える形で動画コンテンツの語り直しを行う。
    16	
    17	**前提**: Phase 3-A SlideSequence、Phase 3-B/3-C supermovie-slides 完成後の運用想定。
    18	
    19	## 設計起点
    20	
    21	Codex Phase 3-D design (2026-05-04, CODEX_PHASE3D_VOICEVOX) 推奨:
    22	- engine 不在で skip (`--require-engine` 指定時のみ exit non-zero)
    23	- Phase 3-C と同じく optional 経路で deterministic フォールバックなし (engine 必須)
    24	- Anthropic API ではなく VOICEVOX ローカル engine、課金ゼロ
    25	
    26	## ワークフロー
    27	
    28	```
    29	┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    30	│ 1. engine│ → │ 2. 入力  │ → │ 3. 合成  │ → │ 4. Remotion │
    31	│   起動確認│    │   解決   │    │   結合   │    │   接合    │
    32	└──────────┘    └──────────┘    └──────────┘    └──────────┘
    33	```
    34	
    35	## Phase 1: VOICEVOX engine 起動確認
    36	
    37	VOICEVOX engine は localhost:50021 で REST API を提供する。
    38	Roku が以下のいずれかで起動した後に実行:
    39	
    40	- VOICEVOX デスクトップアプリ (https://voicevox.hiroshiba.jp/)
    41	- VOICEVOX engine Docker (https://github.com/VOICEVOX/voicevox_engine)
    42	
    43	`voicevox_narration.py` は `/version` で自動確認、不在なら skip。
    44	
    45	## Phase 2: 入力解決
    46	
    47	優先順位:
    48	1. `--script <path>` で plain-text 指定 (1 行 1 chunk)
    49	2. `--script-json <path>` で `{segments: [{text}]}` JSON 指定
    50	3. default: `<PROJECT>/transcript_fixed.json` の `segments[].text` を chunk
    51	
    52	## Phase 3: 合成 + 結合
    53	
    54	各 chunk について:
    55	1. `POST /audio_query?text=...&speaker=<id>` → query JSON
    56	2. `POST /synthesis?speaker=<id>` body=query → WAV bytes
    57	
    58	すべての chunk wav を時系列で結合し `public/narration.wav` を生成。
    59	`--keep-chunks` で chunk 個別 wav も保持 (debug)。
    60	
    61	## Phase 4: Remotion 接合 (asset gate、手動操作不要)
    62	
    63	Phase 3-F asset gate により `MainVideo.tsx` 編集は不要。
    64	`<NarrationAudio />` と base `<Video>` の両方が `getStaticFiles()` で
    65	`public/narration.wav` の有無を検出する:
    66	
    67	| narration.wav 状態 | NarrationAudio | base Video volume |
    68	|--------------------|----------------|-------------------|
    69	| 不在 | null (skip) | 1.0 (元音声再生) |
    70	| 存在 | `<Audio>` 再生 | 0 (mute、二重音声防止) |
    71	
    72	つまり `voicevox_narration.py` 成功 → `public/narration.wav` 出力 →
    73	次回 `npm run dev` / `npm run render` で自動的に narration 再生 + base mute に
    74	切り替わる。Roku の手作業ゼロ。
    75	
    76	実装参照:
    77	- `template/src/MainVideo.tsx` (`hasNarration` 判定 + `baseVolume`)
    78	- `template/src/Narration/NarrationAudio.tsx` (asset gate null フォールバック)
    79	
    80	## 実行コマンド
    81	
    82	```bash
    83	# default (transcript の segments すべて、speaker=3 = ずんだもんノーマル)
    84	python3 <PROJECT>/scripts/voicevox_narration.py
    85	
    86	# speaker 指定 (一覧は --list-speakers で確認)
    87	python3 <PROJECT>/scripts/voicevox_narration.py --speaker 1
    88	python3 <PROJECT>/scripts/voicevox_narration.py --list-speakers
    89	
    90	# 別スクリプト読み込み
    91	python3 <PROJECT>/scripts/voicevox_narration.py --script narration.txt
    92	python3 <PROJECT>/scripts/voicevox_narration.py --script-json narration.json
    93	
    94	# engine 不在で fail させる (CI 用)
    95	python3 <PROJECT>/scripts/voicevox_narration.py --require-engine
    96	```
    97	
    98	## 出力
    99	
   100	- `<PROJECT>/public/narration.wav` (本命、結合済)
   101	- (`--keep-chunks` 時) `<PROJECT>/public/narration/chunk_NNN.wav`
   102	
   103	## エラーハンドリング
   104	
   105	| エラー | 対応 |
   106	|--------|------|
   107	| engine 不在 | INFO ログ + exit 0 (skip)、`--require-engine` 時のみ exit 4 |
   108	| transcript_fixed.json 不在 | exit 3 (`--script` で迂回可) |
   109	| `/audio_query` HTTP エラー | chunk skip + WARN、全 chunk 失敗で exit 5 |
   110	| WAV 結合 format mismatch | chunk skip + WARN、可能な範囲で結合 |
   111	
   112	## 連携マップ
   113	
   114	```
   115	/supermovie-init / transcribe / transcript-fix / cut / subtitles / slides
   116	    ↓ transcript_fixed.json
   117	/supermovie-narration         ← ★ここ: VOICEVOX で narration.wav 生成
   118	    ↓ public/narration.wav
   119	MainVideo.tsx が public/narration.wav を自動検出 (asset gate)
   120	    └ NarrationAudio: <Audio src=narration.wav /> マウント
   121	    └ base Video: volume=0 に切替 (二重音声防止)
   122	    ↓
   123	npm run render
   124	```
   125	
   126	**Studio を開いたまま narration.wav を生成した場合は再読み込み推奨**:
   127	`getStaticFiles()` は Studio 起動時の asset リストをキャッシュするため、
   128	新規ファイルは Studio reload (Cmd+R / `r` キー) で反映される
   129	(出典 https://www.remotion.dev/docs/getstaticfiles)。
   130	
   131	## VOICEVOX 利用規約
   132	
   133	- 商用/非商用利用可、音声ライブラリごとにクレジット表記必須 (https://voicevox.hiroshiba.jp/term/)
   134	- 話者選定 + クレジット明記は Roku 判断領域

hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg -n \"visual-smoke|visual_smoke|test:visual-smoke|summary\\.json|mismatched|env_error|grid\" ." in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./CLAUDE.md:275:`scripts/visual_smoke.py` は `videoConfig.ts` の `FORMAT` を try/finally で
./CLAUDE.md:285:mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./CLAUDE.md:286:6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:25:- Phase 3-G (今回): visual_smoke.py + npm test scripts (3 format × 2 frame、ffprobe 検証)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:488:template/scripts/visual_smoke.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:562:    25	- Phase 3-G (今回): visual_smoke.py + npm test scripts (3 format × 2 frame、ffprobe 検証)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1357:   488	template/scripts/visual_smoke.py
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1396:/bin/zsh -lc "nl -ba template/scripts/visual_smoke.py | sed -n '1,280p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1542:    14	ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1548:    20	- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1555:    27	    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1556:    28	    python3 scripts/visual_smoke.py --formats youtube,short
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1557:    29	    python3 scripts/visual_smoke.py --frames 30,90,180
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1558:    30	    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1559:    31	    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1579:    51	SMOKE_OUT = PROJ / "out" / "visual_smoke"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1645:   117	def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: list[int]) -> None:
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1646:   118	    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1653:   125	    grid_out.parent.mkdir(parents=True, exist_ok=True)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1686:   158	        filter_parts.append(f"{row_labels[0]}copy[grid]")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1688:   160	        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1697:   169	            "[grid]",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1700:   172	            str(grid_out),
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1719:   191	    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1804:   276	    if not args.no_grid and stills:
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1805:   277	        grid_out = out_dir / "grid.png"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1807:   279	            make_grid(stills, grid_out, formats, frames)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1808:   280	            print(f"\n[smoke] grid: {grid_out}")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1815:/bin/zsh -lc "nl -ba template/scripts/visual_smoke.py | sed -n '280,420p'" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1831:   280	            print(f"\n[smoke] grid: {grid_out}")
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1833:   282	            print(f"WARN: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1835:   284	    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2257:   562	    25	- Phase 3-G (今回): visual_smoke.py + npm test scripts (3 format × 2 frame、ffprobe 検証)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2743:    15	SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2746:    18	1. roku/phase3f-asset-gate..HEAD の 2 commit (Phase 3-F hotfix + Phase 3-G visual_smoke)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2761:    33	B) Phase 3-G visual_smoke (commit 8d8b715)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2762:    34	   - template/scripts/visual_smoke.py の patch_format regex で multi-line/comment 内の偽陽性ヒットがないか
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2773:    45	   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2774:    46	   - 既存 Phase 3-A〜3-F の責務分割を crowding していないか (visual_smoke が renderer と被っている等)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2901:   173	8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2915:   187	 template/scripts/visual_smoke.py     | 306 +++++++++++++++++++++++++++++++++++
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2928:   200	roku/phase3g-visual-smoke
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3002:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3040:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3041:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3130:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3131:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3132:template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4358:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4416:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./template/scripts/visual_smoke.py:14:ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
./template/scripts/visual_smoke.py:20:- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
./template/scripts/visual_smoke.py:27:    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
./template/scripts/visual_smoke.py:28:    python3 scripts/visual_smoke.py --formats youtube,short
./template/scripts/visual_smoke.py:29:    python3 scripts/visual_smoke.py --frames 30,90,180
./template/scripts/visual_smoke.py:30:    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
./template/scripts/visual_smoke.py:36:         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
./template/scripts/visual_smoke.py:52:SMOKE_OUT = PROJ / "out" / "visual_smoke"
./template/scripts/visual_smoke.py:138:def make_grid(
./template/scripts/visual_smoke.py:140:    grid_out: Path,
./template/scripts/visual_smoke.py:145:    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
./template/scripts/visual_smoke.py:154:    grid_out.parent.mkdir(parents=True, exist_ok=True)
./template/scripts/visual_smoke.py:189:        filter_parts.append(f"{row_labels[0]}copy[grid]")
./template/scripts/visual_smoke.py:191:        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
./template/scripts/visual_smoke.py:200:            "[grid]",
./template/scripts/visual_smoke.py:203:            str(grid_out),
./template/scripts/visual_smoke.py:222:    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
./template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./template/scripts/visual_smoke.py:259:    grid_label = has_drawtext_filter()
./template/scripts/visual_smoke.py:260:    if not grid_label and not args.no_grid:
./template/scripts/visual_smoke.py:262:            "INFO: ffmpeg drawtext filter なし、grid label を skip して画像のみ合成します",
./template/scripts/visual_smoke.py:274:    mismatched = 0  # dimension 不一致のみカウント (render/probe 失敗は exit 3 系で別扱い)
./template/scripts/visual_smoke.py:275:    env_error: str | None = None
./template/scripts/visual_smoke.py:279:            if env_error:
./template/scripts/visual_smoke.py:298:                    env_error = "still_failed"
./template/scripts/visual_smoke.py:307:                    env_error = "probe_failed"
./template/scripts/visual_smoke.py:315:                    mismatched += 1
./template/scripts/visual_smoke.py:336:    grid_status = "skipped"
./template/scripts/visual_smoke.py:337:    grid_error: str | None = None
./template/scripts/visual_smoke.py:338:    full_matrix = len(stills) == len(formats) * len(frames) and not env_error
./template/scripts/visual_smoke.py:339:    if not args.no_grid and full_matrix:
./template/scripts/visual_smoke.py:340:        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
./template/scripts/visual_smoke.py:341:        grid_out = out_dir / "grid.png"
./template/scripts/visual_smoke.py:343:            make_grid(stills, grid_out, formats, frames, label=grid_label)
./template/scripts/visual_smoke.py:344:            print(f"\n[smoke] grid: {grid_out}")
./template/scripts/visual_smoke.py:345:            grid_status = "ok"
./template/scripts/visual_smoke.py:347:            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)
./template/scripts/visual_smoke.py:348:            print(f"ERROR: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
./template/scripts/visual_smoke.py:349:            grid_status = "failed"
./template/scripts/visual_smoke.py:350:            grid_error = str(e)
./template/scripts/visual_smoke.py:352:    summary_path = out_dir / "summary.json"
./template/scripts/visual_smoke.py:359:                "mismatched": mismatched,
./template/scripts/visual_smoke.py:361:                "env_error": env_error,
./template/scripts/visual_smoke.py:362:                "grid": {"status": grid_status, "error": grid_error},
./template/scripts/visual_smoke.py:370:    print(f"  total={len(results)}, mismatched={mismatched}, env_error={env_error}, grid={grid_status}")
./template/scripts/visual_smoke.py:372:    if env_error or grid_status == "failed":
./template/scripts/visual_smoke.py:374:    if mismatched:
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:25:- #1 visual_smoke.py: render/probe 失敗 → exit 3 経路、main.mp4/REMOTION_BIN 事前検査追加されているか
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:26:- #2 visual_smoke.py: drawtext filter 不在検査 + label fallback、grid 失敗 → exit 3 へ昇格、特殊文字 escape も
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:27:- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:30:- #4 visual_smoke.py docstring: --keep-stills 行削除
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:31:- #5 full matrix 時のみ grid (env_error / 部分失敗時 skip)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:39:- ロジック分岐ミス (`break` 使用で外側 fmt loop の続行可否、env_error フラグ動作)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:41:- summary.json schema 変更で既存依存があるか
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:99:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:111:## roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:128:    1. visual_smoke.py: render/probe 失敗を exit 3 (環境問題) として早期 break、
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:131:    2. visual_smoke.py: ffmpeg drawtext filter 不在環境を起動時に検査し、不在
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:132:       時は label なし grid に自動 fallback。grid 合成失敗は WARN ではなく
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:135:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:137:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:138:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:141:    4. visual_smoke.py: docstring から実装されていない `--keep-stills` 行を削除。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:142:    5. visual_smoke.py: full matrix (len(stills) == n_fmt × n_frm) かつ env_error
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:143:       なしの時のみ grid 合成、部分失敗時は cell 対応崩れを防ぐため skip。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:144:       summary.json に grid.status / grid.error を記録。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:145:    6. visual_smoke.py: 空 --formats / 空 --frames / 負数 --frames を exit 4 で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:157:    - `python3 visual_smoke.py --formats ""` → exit 4 / `--frames ""` → exit 4 /
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:159:    - `python3 visual_smoke.py` (template/ 直下、main.mp4 不在) → exit 3 with
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:160:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:162:      → label なし grid path に fallback、env_error 起きない
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:170: template/scripts/visual_smoke.py     | 130 +++++++++++++++++++++++++++--------
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:175:差分範囲は指定どおり 3 commit でした（`git log` Bash 実測）。次に `visual_smoke.py` と周辺 caller を行番号付きで確認し、exit code と `summary.json` 依存を検索します。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:189:/bin/zsh -lc 'nl -ba template/scripts/visual_smoke.py' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:225:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:226:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:248:    14	ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:254:    20	- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:261:    27	    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:262:    28	    python3 scripts/visual_smoke.py --formats youtube,short
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:263:    29	    python3 scripts/visual_smoke.py --frames 30,90,180
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:264:    30	    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:270:    36	         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:286:    52	SMOKE_OUT = PROJ / "out" / "visual_smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:372:   138	def make_grid(
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:374:   140	    grid_out: Path,
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:379:   145	    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:388:   154	    grid_out.parent.mkdir(parents=True, exist_ok=True)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:423:   189	        filter_parts.append(f"{row_labels[0]}copy[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:425:   191	        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:434:   200	            "[grid]",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:437:   203	            str(grid_out),
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:456:   222	    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:484:   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:493:   259	    grid_label = has_drawtext_filter()
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:494:   260	    if not grid_label and not args.no_grid:
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:496:   262	            "INFO: ffmpeg drawtext filter なし、grid label を skip して画像のみ合成します",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:508:   274	    mismatched = 0  # dimension 不一致のみカウント (render/probe 失敗は exit 3 系で別扱い)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:509:   275	    env_error: str | None = None
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:513:   279	            if env_error:
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:532:   298	                    env_error = "still_failed"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:541:   307	                    env_error = "probe_failed"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:549:   315	                    mismatched += 1
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:570:   336	    grid_status = "skipped"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:571:   337	    grid_error: str | None = None
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:572:   338	    full_matrix = len(stills) == len(formats) * len(frames) and not env_error
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:573:   339	    if not args.no_grid and full_matrix:
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:574:   340	        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:575:   341	        grid_out = out_dir / "grid.png"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:577:   343	            make_grid(stills, grid_out, formats, frames, label=grid_label)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:578:   344	            print(f"\n[smoke] grid: {grid_out}")
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:579:   345	            grid_status = "ok"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:581:   347	            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:582:   348	            print(f"ERROR: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:583:   349	            grid_status = "failed"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:584:   350	            grid_error = str(e)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:586:   352	    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:593:   359	                "mismatched": mismatched,
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:595:   361	                "env_error": env_error,
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:596:   362	                "grid": {"status": grid_status, "error": grid_error},
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:604:   370	    print(f"  total={len(results)}, mismatched={mismatched}, env_error={env_error}, grid={grid_status}")
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:606:   372	    if env_error or grid_status == "failed":
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:608:   374	    if mismatched:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:18:1. roku/phase3f-asset-gate..HEAD の 2 commit (Phase 3-F hotfix + Phase 3-G visual_smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:33:B) Phase 3-G visual_smoke (commit 8d8b715)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:34:   - template/scripts/visual_smoke.py の patch_format regex で multi-line/comment 内の偽陽性ヒットがないか
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:46:   - 既存 Phase 3-A〜3-F の責務分割を crowding していないか (visual_smoke が renderer と被っている等)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:187: template/scripts/visual_smoke.py     | 306 +++++++++++++++++++++++++++++++++++
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:278:template/scripts/visual_smoke.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:492:/bin/zsh -lc 'nl -ba template/scripts/visual_smoke.py' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:507:    14	ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:513:    20	- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:520:    27	    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:521:    28	    python3 scripts/visual_smoke.py --formats youtube,short
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:522:    29	    python3 scripts/visual_smoke.py --frames 30,90,180
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:523:    30	    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:524:    31	    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:544:    51	SMOKE_OUT = PROJ / "out" / "visual_smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:610:   117	def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: list[int]) -> None:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:611:   118	    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:618:   125	    grid_out.parent.mkdir(parents=True, exist_ok=True)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:651:   158	        filter_parts.append(f"{row_labels[0]}copy[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:653:   160	        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:662:   169	            "[grid]",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:665:   172	            str(grid_out),
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:684:   191	    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:769:   276	    if not args.no_grid and stills:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:770:   277	        grid_out = out_dir / "grid.png"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:772:   279	            make_grid(stills, grid_out, formats, frames)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:773:   280	            print(f"\n[smoke] grid: {grid_out}")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:775:   282	            print(f"WARN: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:777:   284	    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1078:   275	`scripts/visual_smoke.py` は `videoConfig.ts` の `FORMAT` を try/finally で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1088:   285	mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1089:   286	6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1265:変更ファイル上では `visual_smoke.py` と `MainVideo.tsx` が主な実装面です。次は整合確認のため、`videoConfig.ts`、Root、Narration/BGM の asset gate 実装を読みます。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1437:CLAUDE.md:275:`scripts/visual_smoke.py` は `videoConfig.ts` の `FORMAT` を try/finally で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1458:template/scripts/visual_smoke.py:17:- videoConfig.ts FORMAT を try/finally で in-place 切替 + restore
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1459:template/scripts/visual_smoke.py:37:    4 = videoConfig.ts 解析失敗 (FORMAT 行 regex 不一致)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1460:template/scripts/visual_smoke.py:54:FORMAT_DIMS = {
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1461:template/scripts/visual_smoke.py:59:FORMAT_LINE_RE = re.compile(
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1462:template/scripts/visual_smoke.py:60:    r"^(export const FORMAT: VideoFormat = ')(youtube|short|square)(';)$",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1463:template/scripts/visual_smoke.py:66:    """videoConfig.ts の FORMAT 行を fmt に書き換える。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1464:template/scripts/visual_smoke.py:70:    if not FORMAT_LINE_RE.search(content):
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1465:template/scripts/visual_smoke.py:72:            f"FORMAT 行が videoConfig.ts に見つからない: pattern={FORMAT_LINE_RE.pattern}"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1466:template/scripts/visual_smoke.py:74:    return FORMAT_LINE_RE.sub(rf"\g<1>{fmt}\g<3>", content, count=1)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1467:template/scripts/visual_smoke.py:196:        if f not in FORMAT_DIMS:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1468:template/scripts/visual_smoke.py:197:            print(f"ERROR: 未知の format: {f} (許容: {','.join(FORMAT_DIMS)})", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1469:template/scripts/visual_smoke.py:252:                expected = FORMAT_DIMS[fmt]
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1511:/bin/zsh -lc 'git diff roku/phase3f-asset-gate..HEAD -- template/src/MainVideo.tsx template/scripts/visual_smoke.py template/package.json README.md CLAUDE.md skills/supermovie-narration/SKILL.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1543:+`scripts/visual_smoke.py` は `videoConfig.ts` の `FORMAT` を try/finally で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1553:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1554:+6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1637:diff --git a/template/scripts/visual_smoke.py b/template/scripts/visual_smoke.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1641:+++ b/template/scripts/visual_smoke.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1656:+ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1662:+- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1669:+    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1670:+    python3 scripts/visual_smoke.py --formats youtube,short
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1671:+    python3 scripts/visual_smoke.py --frames 30,90,180
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1672:+    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1673:+    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1693:+SMOKE_OUT = PROJ / "out" / "visual_smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1759:+def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: list[int]) -> None:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1760:+    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1767:+    grid_out.parent.mkdir(parents=True, exist_ok=True)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1800:+        filter_parts.append(f"{row_labels[0]}copy[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1802:+        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1811:+            "[grid]",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1814:+            str(grid_out),
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1833:+    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1918:+    if not args.no_grid and stills:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1919:+        grid_out = out_dir / "grid.png"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1921:+            make_grid(stills, grid_out, formats, frames)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1922:+            print(f"\n[smoke] grid: {grid_out}")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1924:+            print(f"WARN: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1926:+    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2020:/bin/zsh -lc "rg -n \"@remotion/studio|getStaticFiles\\(|watchStaticFile|visual-smoke|keep-stills|summary.json|exit 2|exit 3|exit 4\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2024:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2025:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2026:./CLAUDE.md:285:mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2027:./CLAUDE.md:286:6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2035:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2036:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2037:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2041:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1559:    31	    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2042:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1835:   284	    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2052:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2053:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2054:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2057:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2058:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2059:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2060:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:524:    31	    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2061:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:777:   284	    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2062:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2063:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2064:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1088:   285	mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2065:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1089:   286	6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2078:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2079:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2080:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1553:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2081:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1554:+6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2085:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2086:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2087:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1673:+    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2088:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1926:+    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2094:./template/scripts/visual_smoke.py:31:    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2095:./template/scripts/visual_smoke.py:284:    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2097:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2098:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2099:./template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2110:/bin/zsh -lc 'python3 -B template/scripts/visual_smoke.py --help' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2112:usage: visual_smoke.py [-h] [--formats FORMATS] [--frames FRAMES]
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2113:                       [--out-dir OUT_DIR] [--no-grid]
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2120:  --no-grid          ffmpeg grid 合成 skip
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2172:8d8b715 (HEAD -> roku/phase3g-visual-smoke) feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2175: template/scripts/visual_smoke.py | 306 +++++++++++++++++++++++++++++++++++++++
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2732:/bin/zsh -lc 'git show --no-ext-diff --unified=80 --no-renames 8d8b715 -- template/scripts/visual_smoke.py template/package.json CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2742:    feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2746:    mismatch 1 件以上で exit 2、ffmpeg で 3×N grid PNG も合成して目視レビュー可。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2752:    - ffmpeg filter_complex (scale + drawtext label) で 3×2 grid 合成
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2753:    - summary.json に results / failed 統計を残す
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2756:    - template/scripts/visual_smoke.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2757:    - npm scripts: visual-smoke / test:visual-smoke / test (lint + smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2758:    - CLAUDE.md に Visual Smoke 節追加 (out/visual_smoke/grid.png / summary.json 案内)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2860:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2861:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2864:+`scripts/visual_smoke.py` は `videoConfig.ts` の `FORMAT` を try/finally で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2874:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2875:+6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2956:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2957:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2958:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2964:diff --git a/template/scripts/visual_smoke.py b/template/scripts/visual_smoke.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2968:+++ b/template/scripts/visual_smoke.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2983:+ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2989:+- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2996:+    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2997:+    python3 scripts/visual_smoke.py --formats youtube,short
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2998:+    python3 scripts/visual_smoke.py --frames 30,90,180
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2999:+    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3000:+    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3020:+SMOKE_OUT = PROJ / "out" / "visual_smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3086:+def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: list[int]) -> None:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3087:+    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3094:+    grid_out.parent.mkdir(parents=True, exist_ok=True)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3127:+        filter_parts.append(f"{row_labels[0]}copy[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3129:+        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3138:+            "[grid]",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3141:+            str(grid_out),
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3160:+    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3245:+    if not args.no_grid and stills:
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3246:+        grid_out = out_dir / "grid.png"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3248:+            make_grid(stills, grid_out, formats, frames)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3249:+            print(f"\n[smoke] grid: {grid_out}")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3251:+            print(f"WARN: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:3253:+    summary_path = out_dir / "summary.json"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4533:/bin/zsh -lc 'rg -n "HARD|必ず|禁止|Roku|判断|確認|requiresConfirmation|visual-smoke|test" CLAUDE.md skills template/scripts template/src' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4541:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4542:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4551:template/scripts/visual_smoke.py:13:不一致 = exit non-zero (regression として CI/Roku 視認の双方で検知)。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4636:/bin/zsh -lc "rg -n \"copy|template|main\\.mp4|node_modules|npm install|package.json|visual_smoke|preflight|requiresConfirmation\" skills template/scripts .claude 2>/dev/null" in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4652:template/scripts/visual_smoke.py:14:ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4653:template/scripts/visual_smoke.py:23:- 対象 SuperMovie project (main.mp4 / node_modules / remotion installed)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4654:template/scripts/visual_smoke.py:24:- ffprobe / ffmpeg コマンドが PATH に存在 (Phase 3-A 以降 preflight で検証済み)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4655:template/scripts/visual_smoke.py:27:    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4656:template/scripts/visual_smoke.py:28:    python3 scripts/visual_smoke.py --formats youtube,short
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4657:template/scripts/visual_smoke.py:29:    python3 scripts/visual_smoke.py --frames 30,90,180
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4658:template/scripts/visual_smoke.py:30:    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4659:template/scripts/visual_smoke.py:31:    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4660:template/scripts/visual_smoke.py:51:SMOKE_OUT = PROJ / "out" / "visual_smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4661:template/scripts/visual_smoke.py:151:            filter_parts.append(f"{row_in}copy[{row_label}]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4662:template/scripts/visual_smoke.py:158:        filter_parts.append(f"{row_labels[0]}copy[grid]")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5008:/bin/zsh -lc 'git ls-tree -r --name-only HEAD | rg "package-lock|public|visual_smoke|MainVideo|Narration|BGM|videoConfig|Root|CLAUDE|README|SKILL.md$"' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5027:template/scripts/visual_smoke.py
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5220:レビュー範囲は `roku/phase3f-asset-gate..HEAD` の 2 commits、変更 6 files / 368 insertions / 15 deletionsです（`git diff --stat` / `git log --oneline` Bash 実測）。実レンダーは、`visual_smoke.py` が `videoConfig.ts` と `out/visual_smoke` に書き込むため未実行です（[visual_smoke.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:201), [visual_smoke.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:227)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5223:1. [template/scripts/visual_smoke.py:233](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:233) / `remotion still` 失敗を `failed += 1` に入れて最終 exit 2 にしているため、`main.mp4` 不在・`node_modules` 不在・`remotion` 不在が regression 扱いになります。docstring は実行失敗を exit 3 と定義しています（[visual_smoke.py:35](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:35)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5226:2. [template/scripts/visual_smoke.py:139](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:139) / grid は `drawtext` 前提ですが、手元の `ffmpeg -filters` に `drawtext` は表示されず、`copy/hstack/vstack` は表示されました（Bash 実測）。さらに grid 失敗は WARN のみで exit 0 になり得ます（[visual_smoke.py:281](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:281)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5227:修正案: 起動時に `ffmpeg -filters` で `drawtext` を検査し、default grid 失敗は exit 3。もしくは label 焼き込みを optional にして docs も分ける。Effort: S / 自走可否: Claude 単独修正。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5229:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5230:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5233:4. [template/scripts/visual_smoke.py:31](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:31) / `--keep-stills` が Usage にありますが、argparse には定義がありません（`python3 -B template/scripts/visual_smoke.py --help` Bash 実測、help に `--keep-stills` なし）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5236:5. [template/scripts/visual_smoke.py:276](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:276) / 一部 still だけ失敗した場合も grid 合成を試みますが、`make_grid()` は full matrix 前提で `[cN]` を組みます（[visual_smoke.py:147](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:147)）。部分失敗時は label と cell 対応が崩れるか、grid だけ WARN で落ちます。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5237:修正案: `len(stills) == len(formats) * len(frames)` の時だけ grid、部分失敗時は grid skipped を summary に明記。Effort: S / 自走可否: Claude 単独修正。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5239:6. [template/scripts/visual_smoke.py:199](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:199) / `frames` が空でも `failed=0,total=0` で exit 0 になります（[visual_smoke.py:300](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:300)）。`formats` も空文字なら同型です（[visual_smoke.py:194](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:194)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5282:レビュー範囲は `roku/phase3f-asset-gate..HEAD` の 2 commits、変更 6 files / 368 insertions / 15 deletionsです（`git diff --stat` / `git log --oneline` Bash 実測）。実レンダーは、`visual_smoke.py` が `videoConfig.ts` と `out/visual_smoke` に書き込むため未実行です（[visual_smoke.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:201), [visual_smoke.py](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:227)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5285:1. [template/scripts/visual_smoke.py:233](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:233) / `remotion still` 失敗を `failed += 1` に入れて最終 exit 2 にしているため、`main.mp4` 不在・`node_modules` 不在・`remotion` 不在が regression 扱いになります。docstring は実行失敗を exit 3 と定義しています（[visual_smoke.py:35](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:35)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5288:2. [template/scripts/visual_smoke.py:139](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:139) / grid は `drawtext` 前提ですが、手元の `ffmpeg -filters` に `drawtext` は表示されず、`copy/hstack/vstack` は表示されました（Bash 実測）。さらに grid 失敗は WARN のみで exit 0 になり得ます（[visual_smoke.py:281](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:281)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5289:修正案: 起動時に `ffmpeg -filters` で `drawtext` を検査し、default grid 失敗は exit 3。もしくは label 焼き込みを optional にして docs も分ける。Effort: S / 自走可否: Claude 単独修正。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5291:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5292:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5295:4. [template/scripts/visual_smoke.py:31](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:31) / `--keep-stills` が Usage にありますが、argparse には定義がありません（`python3 -B template/scripts/visual_smoke.py --help` Bash 実測、help に `--keep-stills` なし）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5298:5. [template/scripts/visual_smoke.py:276](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:276) / 一部 still だけ失敗した場合も grid 合成を試みますが、`make_grid()` は full matrix 前提で `[cN]` を組みます（[visual_smoke.py:147](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:147)）。部分失敗時は label と cell 対応が崩れるか、grid だけ WARN で落ちます。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5299:修正案: `len(stills) == len(formats) * len(frames)` の時だけ grid、部分失敗時は grid skipped を summary に明記。Effort: S / 自走可否: Claude 単独修正。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5301:6. [template/scripts/visual_smoke.py:199](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:199) / `frames` が空でも `failed=0,total=0` で exit 0 になります（[visual_smoke.py:300](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:300)）。`formats` も空文字なら同型です（[visual_smoke.py:194](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:194)）。  

exec
/bin/zsh -lc 'rg -n "exit 2|exit code|npm run test|visual smoke|visual-smoke" .' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./CLAUDE.md:285:mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./skills/supermovie-init/SKILL.md:156:### 2-4. exit code の扱い
./skills/supermovie-slides/SKILL.md:103:# --strict-plan で plan 検証失敗時 exit 2 (default は warning + deterministic fallback)
./skills/supermovie-slides/SKILL.md:142:`--strict-plan` 指定時は exit 2 で停止。
./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:40:   - exit code 体系 (0/2/3/4) と Codex skill 動作手順 4 表との整合
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:495:     2	"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1088:   285	mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1553:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1644:+"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2020:/bin/zsh -lc "rg -n \"@remotion/studio|getStaticFiles\\(|watchStaticFile|visual-smoke|keep-stills|summary.json|exit 2|exit 3|exit 4\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2024:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2025:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2026:./CLAUDE.md:285:mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2028:./skills/supermovie-slides/SKILL.md:103:# --strict-plan で plan 検証失敗時 exit 2 (default は warning + deterministic fallback)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2029:./skills/supermovie-slides/SKILL.md:142:`--strict-plan` 指定時は exit 2 で停止。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2035:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2036:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2037:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2052:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2053:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2054:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2057:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2058:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2059:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2062:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2063:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2064:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1088:   285	mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2078:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2079:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2080:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1553:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2085:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2086:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2096:./template/scripts/build_slide_data.py:316:                    help="--plan の validate 失敗時に exit 2 (default は warning + deterministic fallback)")
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2097:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2098:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2099:./template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2172:8d8b715 (HEAD -> roku/phase3g-visual-smoke) feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2742:    feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2746:    mismatch 1 件以上で exit 2、ffmpeg で 3×N grid PNG も合成して目視レビュー可。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2757:    - npm scripts: visual-smoke / test:visual-smoke / test (lint + smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2860:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2861:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2874:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2956:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2957:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2958:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2971:+"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4533:/bin/zsh -lc 'rg -n "HARD|必ず|禁止|Roku|判断|確認|requiresConfirmation|visual-smoke|test" CLAUDE.md skills template/scripts template/src' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4541:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4542:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4771:   156	### 2-4. exit code の扱い
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5223:1. [template/scripts/visual_smoke.py:233](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:233) / `remotion still` 失敗を `failed += 1` に入れて最終 exit 2 にしているため、`main.mp4` 不在・`node_modules` 不在・`remotion` 不在が regression 扱いになります。docstring は実行失敗を exit 3 と定義しています（[visual_smoke.py:35](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:35)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5224:修正案: `CalledProcessError` は即 `return 3`、dimension mismatch だけ exit 2。`public/main.mp4` / `node_modules/.bin/remotion` の事前チェックも追加。Effort: S / 自走可否: Claude 単独修正。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5229:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5230:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5285:1. [template/scripts/visual_smoke.py:233](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:233) / `remotion still` 失敗を `failed += 1` に入れて最終 exit 2 にしているため、`main.mp4` 不在・`node_modules` 不在・`remotion` 不在が regression 扱いになります。docstring は実行失敗を exit 3 と定義しています（[visual_smoke.py:35](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:35)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5286:修正案: `CalledProcessError` は即 `return 3`、dimension mismatch だけ exit 2。`public/main.mp4` / `node_modules/.bin/remotion` の事前チェックも追加。Effort: S / 自走可否: Claude 単独修正。
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5291:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5292:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:27:- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:40:- 旧 exit 体系 (exit 2 only) 想定の caller があるか
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:99:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:111:## roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:129:       dimension mismatch だけ exit 2 に分離。MAIN_VIDEO / REMOTION_BIN の事前
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:135:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:137:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:138:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:160:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:175:差分範囲は指定どおり 3 commit でした（`git log` Bash 実測）。次に `visual_smoke.py` と周辺 caller を行番号付きで確認し、exit code と `summary.json` 依存を検索します。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:225:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:226:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:236:     2	"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:484:   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:826:/bin/zsh -lc "rg -n \"visual-smoke|visual_smoke|test:visual-smoke|summary\\.json|mismatched|env_error|grid\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:828:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:829:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:831:./CLAUDE.md:285:mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:833:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:834:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:838:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:839:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:840:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:868:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2743:    15	SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:872:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2773:    45	   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:874:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2901:   173	8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:876:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2928:   200	roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:877:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3002:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:878:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:879:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3040:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:880:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3041:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:881:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3130:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:882:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3131:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:883:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3132:template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:884:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4358:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:885:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4416:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:903:./template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:933:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch の最新 commit (7d0698b) を再 review。前回 review (CODEX_REVIEW_PHASE3G_20260504T211444) で指摘した 8 件 (P1×3 + P2×3 + P3×2) が全部 closed したか機械的に verify、かつ regression がないか厳しめに見て。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:936:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:27:- #3 package.json: `test` から visual-smoke 除外 (lint のみ)、test:visual-smoke 残置
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:941:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:98:7d0698b fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:942:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:99:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:943:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:111:## roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:944:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:123:    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:948:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:135:    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:949:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:137:       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:950:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:138:       または `npm run test:visual-smoke` を呼ぶ運用)。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:958:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:160:      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:961:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:175:差分範囲は指定どおり 3 commit でした（`git log` Bash 実測）。次に `visual_smoke.py` と周辺 caller を行番号付きで確認し、exit code と `summary.json` 依存を検索します。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:963:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:225:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:964:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:226:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:982:./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:484:   250	        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1012:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1016:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1018:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1020:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1022:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1023:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1024:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1048:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1051:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1088:   285	mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1068:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1069:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1071:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1553:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1073:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1074:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1075:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1100:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2020:/bin/zsh -lc "rg -n \"@remotion/studio|getStaticFiles\\(|watchStaticFile|visual-smoke|keep-stills|summary.json|exit 2|exit 3|exit 4\" ." in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1101:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2024:./CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1102:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2025:./CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1103:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2026:./CLAUDE.md:285:mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1105:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2035:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1106:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2036:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1107:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2037:./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1110:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2049:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:15:SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1111:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2052:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:45:   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1112:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2053:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:173:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1113:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2054:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:200:roku/phase3g-visual-smoke
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1114:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2057:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:482:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1115:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2058:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:483:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1116:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2059:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:484:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1119:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2062:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1074:   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1120:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2063:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1075:   272	npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1121:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2064:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1088:   285	mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1123:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2078:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1539:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1124:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2079:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1540:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1125:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2080:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1553:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1127:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2084:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1631:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1128:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2085:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1632:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1129:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2086:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:1633:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1134:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2097:./template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1135:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2098:./template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1136:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2099:./template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1141:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2172:8d8b715 (HEAD -> roku/phase3g-visual-smoke) feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1144:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2742:    feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1145:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2746:    mismatch 1 件以上で exit 2、ffmpeg で 3×N grid PNG も合成して目視レビュー可。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1149:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2757:    - npm scripts: visual-smoke / test:visual-smoke / test (lint + smoke)
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1151:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2860:+npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1152:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2861:+npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1154:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2874:+mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1156:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2956:+    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1157:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2957:+    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1158:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:2958:+    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1183:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4533:/bin/zsh -lc 'rg -n "HARD|必ず|禁止|Roku|判断|確認|requiresConfirmation|visual-smoke|test" CLAUDE.md skills template/scripts template/src' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1184:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4541:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1185:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:4542:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1202:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5223:1. [template/scripts/visual_smoke.py:233](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:233) / `remotion still` 失敗を `failed += 1` に入れて最終 exit 2 にしているため、`main.mp4` 不在・`node_modules` 不在・`remotion` 不在が regression 扱いになります。docstring は実行失敗を exit 3 と定義しています（[visual_smoke.py:35](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:35)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1205:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5229:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1206:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5230:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1212:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5285:1. [template/scripts/visual_smoke.py:233](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:233) / `remotion still` 失敗を `failed += 1` に入れて最終 exit 2 にしているため、`main.mp4` 不在・`node_modules` 不在・`remotion` 不在が regression 扱いになります。docstring は実行失敗を exit 3 と定義しています（[visual_smoke.py:35](/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py:35)）。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1215:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5291:3. [template/package.json:35](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:35) / `npm run test` が `visual-smoke` を含みますが、repo の `template/public` は存在しません（`find template/public` Bash 実測）。Plugin repo CI で template 直下の test を走らせると、fixture 不在で実行失敗します。  
./docs/reviews/CODEX_REVIEW_PHASE3G_FIX_20260504T212554.md:1216:./docs/reviews/CODEX_REVIEW_PHASE3G_20260504T211444.md:5292:修正案: `test` は lint のみに戻し、`test:visual-smoke` は generated project / fixture 専用に分離。CI 用に最小 fixture を生成するなら `.gitignore` の media ignore とセットで例外設計。Effort: M / 自走可否: 段取り判断。
./template/scripts/build_slide_data.py:316:                    help="--plan の validate 失敗時に exit 2 (default は warning + deterministic fallback)")
./template/scripts/visual_smoke.py:2:"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
./template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1097:    33	    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1098:    34	    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1099:    35	    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:1530:     2	"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2743:    15	SuperMovie Plugin の roku/phase3g-visual-smoke branch を超厳しめにレビュー。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2768:    40	   - exit code 体系 (0/2/3/4) と Codex skill 動作手順 4 表との整合
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2773:    45	   - Phase 3-G test スクリプト (npm run test = lint + visual-smoke) が CI 実行で 5 分以上かかる重さ vs 速さの妥当性
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2901:   173	8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:2928:   200	roku/phase3g-visual-smoke
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3002:8d8b715 feat(visual-smoke): Phase 3-G dimension regression detector
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3035:/bin/zsh -lc 'rg -n "no-explicit-any|any|TODO|Sequence|narration|chunk_meta|voicevox|visual-smoke|test" template skills README.md CLAUDE.md' in /Users/rokumasuda/.claude/plugins/supermovie
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3040:CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3041:CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3130:template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3131:template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3132:template/package.json:35:    "test": "npm run lint && npm run test:visual-smoke"
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3798:   103	# --strict-plan で plan 検証失敗時 exit 2 (default は warning + deterministic fallback)
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:3837:   142	`--strict-plan` 指定時は exit 2 で停止。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4358:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。
./docs/reviews/CODEX_PHASE3H_NEXT_20260504T211444.md:4416:- `npm run lint` と `npm run test:visual-smoke` が Phase 3-G の gate として通る設計か（[package.json](/Users/rokumasuda/.claude/plugins/supermovie/template/package.json:32)）。

exec
/bin/zsh -lc 'git show 7d0698b -- template/scripts/visual_smoke.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-ZTrjDfgd' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-pZQurEGk' (errno=Operation not permitted)
commit 7d0698b375c8ef92261bc5d0182d31e1348c3cb1
Author: 増田朗空 <rokumasuda@RokuMacBook-Pro-M5.local>
Date:   Mon May 4 21:24:57 2026 +0900

    fix(visual-smoke): Codex Phase 3-G review P1×3 + P2×3 + P3×2 全 fix
    
    CODEX_REVIEW_PHASE3G_20260504T211444 指摘 8 件を 1 commit にまとめて反映。
    
    P1 fix:
    1. visual_smoke.py: render/probe 失敗を exit 3 (環境問題) として早期 break、
       dimension mismatch だけ exit 2 に分離。MAIN_VIDEO / REMOTION_BIN の事前
       存在検査を追加 (main.mp4 不在 / npm install 未実行 を即検知)。
    2. visual_smoke.py: ffmpeg drawtext filter 不在環境を起動時に検査し、不在
       時は label なし grid に自動 fallback。grid 合成失敗は WARN ではなく
       exit 3 へ昇格 (silent fail 防止)。drawtext text の特殊文字 (シングル
       クオート / コロン) を escape。
    3. package.json: `npm run test` を `lint` のみに戻し、`test:visual-smoke` は
       独立コマンドとして残す。template/ 直下の plugin repo CI で main.mp4
       不在の状態で test が走る事故を回避 (実 project で `npm run visual-smoke`
       または `npm run test:visual-smoke` を呼ぶ運用)。
    
    P2 fix:
    4. visual_smoke.py: docstring から実装されていない `--keep-stills` 行を削除。
    5. visual_smoke.py: full matrix (len(stills) == n_fmt × n_frm) かつ env_error
       なしの時のみ grid 合成、部分失敗時は cell 対応崩れを防ぐため skip。
       summary.json に grid.status / grid.error を記録。
    6. visual_smoke.py: 空 --formats / 空 --frames / 負数 --frames を exit 4 で
       reject (旧: 空 list で total=0 のまま exit 0、誤合格)。
    
    P3 fix:
    7. supermovie-narration SKILL.md: 連携マップ末尾の旧手順「<NarrationAudio /> 有効化」
       を「MainVideo.tsx が public/narration.wav を自動検出」+ Studio reload
       注記に置換 (asset gate 整合)。
    8. MainVideo.tsx: getStaticFiles() の Studio キャッシュ仕様 (Remotion 公式
       docs https://www.remotion.dev/docs/getstaticfiles 準拠) を docstring に
       追記、Studio 実行中の新規 asset 反映には reload (Cmd+R) が必要と明記。
    
    検証 (Bash 実測):
    - `python3 visual_smoke.py --formats ""` → exit 4 / `--frames ""` → exit 4 /
      `--formats unknown` → exit 4 / `--frames -10` → exit 4 (旧 0)
    - `python3 visual_smoke.py` (template/ 直下、main.mp4 不在) → exit 3 with
      明示メッセージ「base 動画が無い: ... npm run visual-smoke は実 project で実行」
    - `has_drawtext_filter()` ローカル ffmpeg で False (drawtext filter 表示なし)
      → label なし grid path に fallback、env_error 起きない
    
    Codex 指摘 8/8 全カバー、自走範囲 + 段取り判断 #3 (test = lint のみで合理)。
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

diff --git a/template/scripts/visual_smoke.py b/template/scripts/visual_smoke.py
index 6fdbe99..baf5094 100644
--- a/template/scripts/visual_smoke.py
+++ b/template/scripts/visual_smoke.py
@@ -28,13 +28,14 @@ Usage:
     python3 scripts/visual_smoke.py --formats youtube,short
     python3 scripts/visual_smoke.py --frames 30,90,180
     python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
-    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
 
 Exit code:
     0 = 全 still 出力 + dimension 一致
-    2 = 1 件以上 dimension mismatch (regression)
-    3 = remotion still / ffprobe / ffmpeg 実行失敗 (環境問題)
-    4 = videoConfig.ts 解析失敗 (FORMAT 行 regex 不一致)
+    2 = 1 件以上 dimension mismatch (regression、render は成功している)
+    3 = 実行環境問題 (main.mp4 不在 / node_modules 不在 / remotion still failed /
+         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
+    4 = 入力 / 設定不正 (videoConfig.ts 不在 or FORMAT 行 regex 不一致 /
+         空 formats / 空 frames / 未知 format)
 """
 from __future__ import annotations
 
@@ -50,6 +51,8 @@ PROJ = Path(__file__).resolve().parent.parent
 VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
 SMOKE_OUT = PROJ / "out" / "visual_smoke"
 COMPOSITION_ID = "MainVideo"
+MAIN_VIDEO = PROJ / "public" / "main.mp4"
+REMOTION_BIN = PROJ / "node_modules" / ".bin" / "remotion"
 
 FORMAT_DIMS = {
     "youtube": (1920, 1080),
@@ -114,11 +117,37 @@ def render_still(project: Path, frame: int, png_out: Path) -> None:
     )
 
 
-def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: list[int]) -> None:
+def has_drawtext_filter() -> bool:
+    """ffmpeg build に drawtext filter (libfreetype) が含まれるか確認。
+
+    Mac Homebrew 標準 build は drawtext を持つが、minimal build では落ちている
+    ことがあるため事前検査する (Codex Phase 3-G review P1 #2 反映)。
+    """
+    try:
+        out = subprocess.check_output(
+            ["ffmpeg", "-hide_banner", "-filters"], text=True, stderr=subprocess.STDOUT
+        )
+    except (subprocess.CalledProcessError, FileNotFoundError):
+        return False
+    for line in out.splitlines():
+        if " drawtext " in f" {line} ":
+            return True
+    return False
+
+
+def make_grid(
+    stills: list[Path],
+    grid_out: Path,
+    formats: list[str],
+    frames: list[int],
+    label: bool,
+) -> None:
     """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
 
-    ffmpeg filter_complex で hstack (frame 軸) → vstack (format 軸) する。
-    各 cell に format/frame ラベルを drawtext で焼き込み (debug 即見可).
+    呼び出し側で full matrix (len(stills) == n_fmt * n_frm) を保証すること
+    (部分失敗時の cell 対応崩れを防ぐ、Codex Phase 3-G P2 #5 反映)。
+    label=True の時は drawtext で format/frame を焼き込み、False の時は scale のみ
+    (drawtext filter 不在環境向け、Codex P1 #2 反映)。
     """
     if not stills:
         return
@@ -130,17 +159,19 @@ def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: li
     n_fmt = len(formats)
     n_frm = len(frames)
     filter_parts: list[str] = []
-    # 各 cell をラベル付き thumb にスケーリング (短辺 360px に固定)
+    # 各 cell を thumb にスケーリング (短辺 360px に固定)、必要なら drawtext
     for i, s in enumerate(stills):
         fmt = formats[i // n_frm]
         frm = frames[i % n_frm]
-        label = f"{fmt} f{frm}"
-        # label 付きで scale
-        filter_parts.append(
-            f"[{i}:v]scale=-2:360,"
-            f"drawtext=text='{label}':fontcolor=white:fontsize=24:"
-            f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
-        )
+        if label:
+            txt = f"{fmt} f{frm}".replace("'", r"\'").replace(":", r"\:")
+            filter_parts.append(
+                f"[{i}:v]scale=-2:360,"
+                f"drawtext=text='{txt}':fontcolor=white:fontsize=24:"
+                f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
+            )
+        else:
+            filter_parts.append(f"[{i}:v]scale=-2:360[c{i}]")
 
     # 各 format 行の hstack
     row_labels: list[str] = []
@@ -192,20 +223,45 @@ def cli() -> int:
     args = ap.parse_args()
 
     formats = [f.strip() for f in args.formats.split(",") if f.strip()]
+    if not formats:
+        print("ERROR: --formats が空です (例: --formats youtube,short)", file=sys.stderr)
+        return 4
     for f in formats:
         if f not in FORMAT_DIMS:
             print(f"ERROR: 未知の format: {f} (許容: {','.join(FORMAT_DIMS)})", file=sys.stderr)
             return 4
     frames = [int(x) for x in args.frames.split(",") if x.strip()]
+    if not frames:
+        print("ERROR: --frames が空です (例: --frames 30,90)", file=sys.stderr)
+        return 4
+    if any(f < 0 for f in frames):
+        print(f"ERROR: --frames に負数: {frames}", file=sys.stderr)
+        return 4
 
     out_dir = Path(args.out_dir).resolve()
     out_dir.mkdir(parents=True, exist_ok=True)
 
-    # 環境チェック
+    # 環境チェック (Codex Phase 3-G review P1 #1 反映、render 失敗を環境問題として早期検知)
     for tool in ("npx", "ffprobe", "ffmpeg"):
         if shutil.which(tool) is None:
             print(f"ERROR: {tool} コマンドが PATH にない", file=sys.stderr)
             return 3
+    if not MAIN_VIDEO.exists():
+        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
+        return 3
+    if not REMOTION_BIN.exists():
+        print(
+            f"ERROR: remotion CLI が無い: {REMOTION_BIN} "
+            f"(npm install を先に実行してください)",
+            file=sys.stderr,
+        )
+        return 3
+    grid_label = has_drawtext_filter()
+    if not grid_label and not args.no_grid:
+        print(
+            "INFO: ffmpeg drawtext filter なし、grid label を skip して画像のみ合成します",
+            file=sys.stderr,
+        )
 
     # videoConfig.ts 原本保持
     if not VIDEO_CONFIG.exists():
@@ -215,10 +271,13 @@ def cli() -> int:
 
     results: list[dict] = []
     stills: list[Path] = []
-    failed = 0
+    mismatched = 0  # dimension 不一致のみカウント (render/probe 失敗は exit 3 系で別扱い)
+    env_error: str | None = None
 
     try:
         for fmt in formats:
+            if env_error:
+                break
             try:
                 patched = patch_format(original, fmt)
             except ValueError as e:
@@ -231,28 +290,29 @@ def cli() -> int:
                 try:
                     render_still(PROJ, frame, png)
                 except subprocess.CalledProcessError as e:
+                    # P1 #1: render 失敗は環境問題 (exit 3) として即終了
                     print(
                         f"  ERROR: remotion still failed (fmt={fmt}, frame={frame}): {e}",
                         file=sys.stderr,
                     )
-                    failed += 1
+                    env_error = "still_failed"
                     results.append(
                         {"format": fmt, "frame": frame, "ok": False, "error": "still_failed"}
                     )
-                    continue
+                    break
                 try:
                     w, h = probe_dim(png)
                 except subprocess.CalledProcessError as e:
                     print(f"  ERROR: ffprobe failed for {png}: {e}", file=sys.stderr)
-                    failed += 1
+                    env_error = "probe_failed"
                     results.append(
                         {"format": fmt, "frame": frame, "ok": False, "error": "probe_failed"}
                     )
-                    continue
+                    break
                 expected = FORMAT_DIMS[fmt]
                 ok = (w, h) == expected
                 if not ok:
-                    failed += 1
+                    mismatched += 1
                 results.append(
                     {
                         "format": fmt,
@@ -273,13 +333,21 @@ def cli() -> int:
         VIDEO_CONFIG.write_text(original, encoding="utf-8")
         print(f"\n[smoke] videoConfig.ts を原本に restore しました")
 
-    if not args.no_grid and stills:
+    grid_status = "skipped"
+    grid_error: str | None = None
+    full_matrix = len(stills) == len(formats) * len(frames) and not env_error
+    if not args.no_grid and full_matrix:
+        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
         grid_out = out_dir / "grid.png"
         try:
-            make_grid(stills, grid_out, formats, frames)
+            make_grid(stills, grid_out, formats, frames, label=grid_label)
             print(f"\n[smoke] grid: {grid_out}")
+            grid_status = "ok"
         except subprocess.CalledProcessError as e:
-            print(f"WARN: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
+            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)
+            print(f"ERROR: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
+            grid_status = "failed"
+            grid_error = str(e)
 
     summary_path = out_dir / "summary.json"
     summary_path.write_text(
@@ -288,8 +356,10 @@ def cli() -> int:
                 "formats": formats,
                 "frames": frames,
                 "results": results,
-                "failed": failed,
+                "mismatched": mismatched,
                 "total": len(results),
+                "env_error": env_error,
+                "grid": {"status": grid_status, "error": grid_error},
             },
             ensure_ascii=False,
             indent=2,
@@ -297,9 +367,13 @@ def cli() -> int:
         encoding="utf-8",
     )
     print(f"\nsummary: {summary_path}")
-    print(f"  total={len(results)}, failed={failed}")
+    print(f"  total={len(results)}, mismatched={mismatched}, env_error={env_error}, grid={grid_status}")
 
-    return 2 if failed else 0
+    if env_error or grid_status == "failed":
+        return 3
+    if mismatched:
+        return 2
+    return 0
 
 
 if __name__ == "__main__":

exec
/bin/zsh -lc 'git show 7d0698b''^:template/scripts/visual_smoke.py | nl -ba' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-N38CJFP1' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-hdXSoui6' (errno=Operation not permitted)
     1	#!/usr/bin/env python3
     2	"""SuperMovie Phase 3-G visual smoke: format dimension regression detector.
     3	
     4	3 format (youtube/short/square) × N frame で `npx remotion still` を生成し、
     5	各 PNG の dimension が format 期待値と一致するか ffprobe で検証する。
     6	
     7	| format | width × height | aspect |
     8	|--------|---------------|--------|
     9	| youtube | 1920 × 1080 | 16:9 |
    10	| short   | 1080 × 1920 | 9:16 |
    11	| square  | 1080 × 1080 | 1:1 |
    12	
    13	不一致 = exit non-zero (regression として CI/Roku 視認の双方で検知)。
    14	ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
    15	
    16	Codex Phase 3G design (2026-05-04, CODEX_PHASE3G_NEXT) 推奨:
    17	- videoConfig.ts FORMAT を try/finally で in-place 切替 + restore
    18	- per-format remotion still、frame 30/90 デフォルト
    19	- 各 still を ffprobe で width/height 検証
    20	- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
    21	
    22	前提:
    23	- 対象 SuperMovie project (main.mp4 / node_modules / remotion installed)
    24	- ffprobe / ffmpeg コマンドが PATH に存在 (Phase 3-A 以降 preflight で検証済み)
    25	
    26	Usage:
    27	    python3 scripts/visual_smoke.py                       # 3 format × 2 frame
    28	    python3 scripts/visual_smoke.py --formats youtube,short
    29	    python3 scripts/visual_smoke.py --frames 30,90,180
    30	    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
    31	    python3 scripts/visual_smoke.py --keep-stills         # PNG 残す (default 残す)
    32	
    33	Exit code:
    34	    0 = 全 still 出力 + dimension 一致
    35	    2 = 1 件以上 dimension mismatch (regression)
    36	    3 = remotion still / ffprobe / ffmpeg 実行失敗 (環境問題)
    37	    4 = videoConfig.ts 解析失敗 (FORMAT 行 regex 不一致)
    38	"""
    39	from __future__ import annotations
    40	
    41	import argparse
    42	import json
    43	import re
    44	import shutil
    45	import subprocess
    46	import sys
    47	from pathlib import Path
    48	
    49	PROJ = Path(__file__).resolve().parent.parent
    50	VIDEO_CONFIG = PROJ / "src" / "videoConfig.ts"
    51	SMOKE_OUT = PROJ / "out" / "visual_smoke"
    52	COMPOSITION_ID = "MainVideo"
    53	
    54	FORMAT_DIMS = {
    55	    "youtube": (1920, 1080),
    56	    "short": (1080, 1920),
    57	    "square": (1080, 1080),
    58	}
    59	FORMAT_LINE_RE = re.compile(
    60	    r"^(export const FORMAT: VideoFormat = ')(youtube|short|square)(';)$",
    61	    re.MULTILINE,
    62	)
    63	
    64	
    65	def patch_format(content: str, fmt: str) -> str:
    66	    """videoConfig.ts の FORMAT 行を fmt に書き換える。
    67	
    68	    一致 0 件で ValueError、複数一致でも先頭1件のみ書換 (Anchored multi-line)。
    69	    """
    70	    if not FORMAT_LINE_RE.search(content):
    71	        raise ValueError(
    72	            f"FORMAT 行が videoConfig.ts に見つからない: pattern={FORMAT_LINE_RE.pattern}"
    73	        )
    74	    return FORMAT_LINE_RE.sub(rf"\g<1>{fmt}\g<3>", content, count=1)
    75	
    76	
    77	def probe_dim(png: Path) -> tuple[int, int]:
    78	    """ffprobe で PNG の width × height を取得。"""
    79	    out = subprocess.check_output(
    80	        [
    81	            "ffprobe",
    82	            "-v",
    83	            "error",
    84	            "-select_streams",
    85	            "v:0",
    86	            "-show_entries",
    87	            "stream=width,height",
    88	            "-of",
    89	            "json",
    90	            str(png),
    91	        ],
    92	        text=True,
    93	    )
    94	    info = json.loads(out)
    95	    s = info["streams"][0]
    96	    return int(s["width"]), int(s["height"])
    97	
    98	
    99	def render_still(project: Path, frame: int, png_out: Path) -> None:
   100	    """`npx remotion still` で 1 frame の PNG 出力。"""
   101	    png_out.parent.mkdir(parents=True, exist_ok=True)
   102	    subprocess.check_call(
   103	        [
   104	            "npx",
   105	            "--no-install",
   106	            "remotion",
   107	            "still",
   108	            COMPOSITION_ID,
   109	            str(png_out),
   110	            "--frame",
   111	            str(frame),
   112	        ],
   113	        cwd=str(project),
   114	    )
   115	
   116	
   117	def make_grid(stills: list[Path], grid_out: Path, formats: list[str], frames: list[int]) -> None:
   118	    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
   119	
   120	    ffmpeg filter_complex で hstack (frame 軸) → vstack (format 軸) する。
   121	    各 cell に format/frame ラベルを drawtext で焼き込み (debug 即見可).
   122	    """
   123	    if not stills:
   124	        return
   125	    grid_out.parent.mkdir(parents=True, exist_ok=True)
   126	    inputs: list[str] = []
   127	    for s in stills:
   128	        inputs.extend(["-i", str(s)])
   129	
   130	    n_fmt = len(formats)
   131	    n_frm = len(frames)
   132	    filter_parts: list[str] = []
   133	    # 各 cell をラベル付き thumb にスケーリング (短辺 360px に固定)
   134	    for i, s in enumerate(stills):
   135	        fmt = formats[i // n_frm]
   136	        frm = frames[i % n_frm]
   137	        label = f"{fmt} f{frm}"
   138	        # label 付きで scale
   139	        filter_parts.append(
   140	            f"[{i}:v]scale=-2:360,"
   141	            f"drawtext=text='{label}':fontcolor=white:fontsize=24:"
   142	            f"box=1:boxcolor=black@0.6:boxborderw=8:x=20:y=20[c{i}]"
   143	        )
   144	
   145	    # 各 format 行の hstack
   146	    row_labels: list[str] = []
   147	    for r in range(n_fmt):
   148	        row_in = "".join(f"[c{r * n_frm + c}]" for c in range(n_frm))
   149	        row_label = f"row{r}"
   150	        if n_frm == 1:
   151	            filter_parts.append(f"{row_in}copy[{row_label}]")
   152	        else:
   153	            filter_parts.append(f"{row_in}hstack=inputs={n_frm}[{row_label}]")
   154	        row_labels.append(f"[{row_label}]")
   155	
   156	    # vstack
   157	    if n_fmt == 1:
   158	        filter_parts.append(f"{row_labels[0]}copy[grid]")
   159	    else:
   160	        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
   161	
   162	    cmd = (
   163	        ["ffmpeg", "-y"]
   164	        + inputs
   165	        + [
   166	            "-filter_complex",
   167	            ";".join(filter_parts),
   168	            "-map",
   169	            "[grid]",
   170	            "-frames:v",
   171	            "1",
   172	            str(grid_out),
   173	        ]
   174	    )
   175	    subprocess.check_call(cmd)
   176	
   177	
   178	def cli() -> int:
   179	    ap = argparse.ArgumentParser()
   180	    ap.add_argument(
   181	        "--formats",
   182	        default="youtube,short,square",
   183	        help="検証対象 format (カンマ区切り、default 全 3 種)",
   184	    )
   185	    ap.add_argument(
   186	        "--frames",
   187	        default="30,90",
   188	        help="検証 frame 番号 (カンマ区切り、default 30,90)",
   189	    )
   190	    ap.add_argument("--out-dir", default=str(SMOKE_OUT), help="出力ディレクトリ")
   191	    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
   192	    args = ap.parse_args()
   193	
   194	    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
   195	    for f in formats:
   196	        if f not in FORMAT_DIMS:
   197	            print(f"ERROR: 未知の format: {f} (許容: {','.join(FORMAT_DIMS)})", file=sys.stderr)
   198	            return 4
   199	    frames = [int(x) for x in args.frames.split(",") if x.strip()]
   200	
   201	    out_dir = Path(args.out_dir).resolve()
   202	    out_dir.mkdir(parents=True, exist_ok=True)
   203	
   204	    # 環境チェック
   205	    for tool in ("npx", "ffprobe", "ffmpeg"):
   206	        if shutil.which(tool) is None:
   207	            print(f"ERROR: {tool} コマンドが PATH にない", file=sys.stderr)
   208	            return 3
   209	
   210	    # videoConfig.ts 原本保持
   211	    if not VIDEO_CONFIG.exists():
   212	        print(f"ERROR: videoConfig.ts が無い: {VIDEO_CONFIG}", file=sys.stderr)
   213	        return 4
   214	    original = VIDEO_CONFIG.read_text(encoding="utf-8")
   215	
   216	    results: list[dict] = []
   217	    stills: list[Path] = []
   218	    failed = 0
   219	
   220	    try:
   221	        for fmt in formats:
   222	            try:
   223	                patched = patch_format(original, fmt)
   224	            except ValueError as e:
   225	                print(f"ERROR: {e}", file=sys.stderr)
   226	                return 4
   227	            VIDEO_CONFIG.write_text(patched, encoding="utf-8")
   228	            print(f"\n[smoke] format={fmt} に切替て still を出力します")
   229	            for frame in frames:
   230	                png = out_dir / f"smoke_{fmt}_f{frame:04d}.png"
   231	                try:
   232	                    render_still(PROJ, frame, png)
   233	                except subprocess.CalledProcessError as e:
   234	                    print(
   235	                        f"  ERROR: remotion still failed (fmt={fmt}, frame={frame}): {e}",
   236	                        file=sys.stderr,
   237	                    )
   238	                    failed += 1
   239	                    results.append(
   240	                        {"format": fmt, "frame": frame, "ok": False, "error": "still_failed"}
   241	                    )
   242	                    continue
   243	                try:
   244	                    w, h = probe_dim(png)
   245	                except subprocess.CalledProcessError as e:
   246	                    print(f"  ERROR: ffprobe failed for {png}: {e}", file=sys.stderr)
   247	                    failed += 1
   248	                    results.append(
   249	                        {"format": fmt, "frame": frame, "ok": False, "error": "probe_failed"}
   250	                    )
   251	                    continue
   252	                expected = FORMAT_DIMS[fmt]
   253	                ok = (w, h) == expected
   254	                if not ok:
   255	                    failed += 1
   256	                results.append(
   257	                    {
   258	                        "format": fmt,
   259	                        "frame": frame,
   260	                        "ok": ok,
   261	                        "expected": list(expected),
   262	                        "actual": [w, h],
   263	                        "png": str(png),
   264	                    }
   265	                )
   266	                stills.append(png)
   267	                marker = "OK" if ok else "MISMATCH"
   268	                print(
   269	                    f"  [{marker}] {png.name}: expected={expected[0]}x{expected[1]}, "
   270	                    f"actual={w}x{h}"
   271	                )
   272	    finally:
   273	        VIDEO_CONFIG.write_text(original, encoding="utf-8")
   274	        print(f"\n[smoke] videoConfig.ts を原本に restore しました")
   275	
   276	    if not args.no_grid and stills:
   277	        grid_out = out_dir / "grid.png"
   278	        try:
   279	            make_grid(stills, grid_out, formats, frames)
   280	            print(f"\n[smoke] grid: {grid_out}")
   281	        except subprocess.CalledProcessError as e:
   282	            print(f"WARN: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
   283	
   284	    summary_path = out_dir / "summary.json"
   285	    summary_path.write_text(
   286	        json.dumps(
   287	            {
   288	                "formats": formats,
   289	                "frames": frames,
   290	                "results": results,
   291	                "failed": failed,
   292	                "total": len(results),
   293	            },
   294	            ensure_ascii=False,
   295	            indent=2,
   296	        ),
   297	        encoding="utf-8",
   298	    )
   299	    print(f"\nsummary: {summary_path}")
   300	    print(f"  total={len(results)}, failed={failed}")
   301	
   302	    return 2 if failed else 0
   303	
   304	
   305	if __name__ == "__main__":
   306	    sys.exit(cli())

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "nl -ba CLAUDE.md | sed -n '260,292p'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
   260	|---------|-------------|
   261	| `TelopSegment` | SubtitleSegment |
   262	| `telopData` | subtitleData |
   263	| `テロップテンプレート/` | Subtitles/ |
   264	| `transcript_fixed.json` | transcript_corrected.json |
   265	| `transcript_audio.wav` | /tmp/supermovie_audio.wav |
   266	
   267	## Visual Smoke (Phase 3-G、format 切替後の dimension 検査)
   268	
   269	```bash
   270	cd <PROJECT>
   271	npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
   272	npm run test           # lint + visual-smoke を一気に
   273	```
   274	
   275	`scripts/visual_smoke.py` は `videoConfig.ts` の `FORMAT` を try/finally で
   276	youtube → short → square と切替て `npx remotion still` を 2 frame ずつ生成、
   277	各 PNG を ffprobe で検証する:
   278	
   279	| format | 期待 dimension |
   280	|--------|---------------|
   281	| youtube | 1920 × 1080 |
   282	| short   | 1080 × 1920 |
   283	| square  | 1080 × 1080 |
   284	
   285	mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
   286	6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
   287	原本 `videoConfig.ts` は finally で必ず復元される (途中 fail 安全)。
   288	
   289	## アップデート手順
   290	
   291	「アップデートして」と言われたら以下を実行:
   292	

exec
/bin/zsh -lc "python3 -B template/scripts/visual_smoke.py --formats ''" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'python3 -B template/scripts/visual_smoke.py --frames abc' in /Users/rokumasuda/.claude/plugins/supermovie
 exited 1 in 0ms:
Traceback (most recent call last):
  File "/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py", line 380, in <module>
    sys.exit(cli())
             ~~~^^
  File "/Users/rokumasuda/.claude/plugins/supermovie/template/scripts/visual_smoke.py", line 233, in cli
    frames = [int(x) for x in args.frames.split(",") if x.strip()]
              ~~~^^^
ValueError: invalid literal for int() with base 10: 'abc'

 exited 4 in 0ms:
ERROR: --formats が空です (例: --formats youtube,short)

exec
/bin/zsh -lc "python3 -B template/scripts/visual_smoke.py --frames ''" in /Users/rokumasuda/.claude/plugins/supermovie
 exited 4 in 0ms:
ERROR: --frames が空です (例: --frames 30,90)

codex
主要分岐は読めました。`env_error` は内側 frame loop の `break` 後に外側 format loop も止める実装で、`summary.json` の既存依存は `rg` 上はドキュメント以外に見当たりません（Bash 実測）。入力系だけ追加で実行確認しています。
  ✓ 指定 git log / show で差分範囲を確認
  ✓ 8件の指摘ごとに該当コードを照合
  → regression と既存依存を検索
  • verdict 表と新規指摘をまとめる
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc "rg -n \"\\bfailed\\b|\\bmismatched\\b|\\benv_error\\b|\\\"grid\\\"|summary\\.json\" template skills CLAUDE.md README.md" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
CLAUDE.md:286:6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
template/scripts/voicevox_narration.py:165:            print(f"WARN: synth failed for chunk {i}: {e}", file=sys.stderr)
template/scripts/preflight_video.py:67:        print(f"ERROR: ffprobe failed for {path}: {e}", file=sys.stderr)
template/scripts/build_slide_data.py:349:                    print("ERROR: plan validation failed:")
template/scripts/build_slide_data.py:353:                print("WARN: plan validation failed, deterministic fallback:")
template/scripts/visual_smoke.py:35:    3 = 実行環境問題 (main.mp4 不在 / node_modules 不在 / remotion still failed /
template/scripts/visual_smoke.py:36:         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
template/scripts/visual_smoke.py:274:    mismatched = 0  # dimension 不一致のみカウント (render/probe 失敗は exit 3 系で別扱い)
template/scripts/visual_smoke.py:275:    env_error: str | None = None
template/scripts/visual_smoke.py:279:            if env_error:
template/scripts/visual_smoke.py:295:                        f"  ERROR: remotion still failed (fmt={fmt}, frame={frame}): {e}",
template/scripts/visual_smoke.py:298:                    env_error = "still_failed"
template/scripts/visual_smoke.py:306:                    print(f"  ERROR: ffprobe failed for {png}: {e}", file=sys.stderr)
template/scripts/visual_smoke.py:307:                    env_error = "probe_failed"
template/scripts/visual_smoke.py:315:                    mismatched += 1
template/scripts/visual_smoke.py:338:    full_matrix = len(stills) == len(formats) * len(frames) and not env_error
template/scripts/visual_smoke.py:349:            grid_status = "failed"
template/scripts/visual_smoke.py:352:    summary_path = out_dir / "summary.json"
template/scripts/visual_smoke.py:359:                "mismatched": mismatched,
template/scripts/visual_smoke.py:361:                "env_error": env_error,
template/scripts/visual_smoke.py:362:                "grid": {"status": grid_status, "error": grid_error},
template/scripts/visual_smoke.py:370:    print(f"  total={len(results)}, mismatched={mismatched}, env_error={env_error}, grid={grid_status}")
template/scripts/visual_smoke.py:372:    if env_error or grid_status == "failed":
template/scripts/visual_smoke.py:374:    if mismatched:
template/scripts/build_telop_data.py:225:        raise RuntimeError(f"budoux_split.mjs failed: {res.stderr}")

exec
/bin/zsh -lc 'python3 -B template/scripts/visual_smoke.py --formats unknown' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'python3 -B template/scripts/visual_smoke.py --frames -10' in /Users/rokumasuda/.claude/plugins/supermovie
 exited 4 in 0ms:
ERROR: 未知の format: unknown (許容: youtube,short,square)

 exited 4 in 0ms:
ERROR: --frames に負数: [-10]

exec
/bin/zsh -lc 'python3 -B template/scripts/visual_smoke.py --help' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
usage: visual_smoke.py [-h] [--formats FORMATS] [--frames FRAMES]
                       [--out-dir OUT_DIR] [--no-grid]

options:
  -h, --help         show this help message and exit
  --formats FORMATS  検証対象 format (カンマ区切り、default 全 3 種)
  --frames FRAMES    検証 frame 番号 (カンマ区切り、default 30,90)
  --out-dir OUT_DIR  出力ディレクトリ
  --no-grid          ffmpeg grid 合成 skip

codex
追加で grid 自体の寸法条件を確認しています。`scale=-2:360` は format ごとに cell 幅が変わるため、default の mixed-format grid が `vstack` 条件を満たすかが未確認のリスク箇所です。
  ✓ 指定 git log / show で差分範囲を確認
  ✓ 8件の指摘ごとに該当コードを照合
  → regression と既存依存を検索
  • verdict 表と新規指摘をまとめる
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse Completed
exec
/bin/zsh -lc 'rg -n "scale=-2:360|vstack|hstack|drawtext|grid" template/scripts/visual_smoke.py' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
14:ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
20:- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
30:    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
36:         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
120:def has_drawtext_filter() -> bool:
121:    """ffmpeg build に drawtext filter (libfreetype) が含まれるか確認。
123:    Mac Homebrew 標準 build は drawtext を持つが、minimal build では落ちている
133:        if " drawtext " in f" {line} ":
138:def make_grid(
140:    grid_out: Path,
145:    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
149:    label=True の時は drawtext で format/frame を焼き込み、False の時は scale のみ
150:    (drawtext filter 不在環境向け、Codex P1 #2 反映)。
154:    grid_out.parent.mkdir(parents=True, exist_ok=True)
162:    # 各 cell を thumb にスケーリング (短辺 360px に固定)、必要なら drawtext
169:                f"[{i}:v]scale=-2:360,"
170:                f"drawtext=text='{txt}':fontcolor=white:fontsize=24:"
174:            filter_parts.append(f"[{i}:v]scale=-2:360[c{i}]")
176:    # 各 format 行の hstack
184:            filter_parts.append(f"{row_in}hstack=inputs={n_frm}[{row_label}]")
187:    # vstack
189:        filter_parts.append(f"{row_labels[0]}copy[grid]")
191:        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
200:            "[grid]",
203:            str(grid_out),
222:    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
259:    grid_label = has_drawtext_filter()
260:    if not grid_label and not args.no_grid:
262:            "INFO: ffmpeg drawtext filter なし、grid label を skip して画像のみ合成します",
336:    grid_status = "skipped"
337:    grid_error: str | None = None
339:    if not args.no_grid and full_matrix:
340:        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
341:        grid_out = out_dir / "grid.png"
343:            make_grid(stills, grid_out, formats, frames, label=grid_label)
344:            print(f"\n[smoke] grid: {grid_out}")
345:            grid_status = "ok"
347:            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)
348:            print(f"ERROR: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
349:            grid_status = "failed"
350:            grid_error = str(e)
362:                "grid": {"status": grid_status, "error": grid_error},
370:    print(f"  total={len(results)}, mismatched={mismatched}, env_error={env_error}, grid={grid_status}")
372:    if env_error or grid_status == "failed":

exec
/bin/zsh -lc "rg -n \"test:visual-smoke|visual-smoke|npm run test|summary\\.json|mismatched|env_error|grid\" template skills CLAUDE.md README.md .github .codex 2>/dev/null" in /Users/rokumasuda/.claude/plugins/supermovie
 exited 2 in 0ms:
CLAUDE.md:271:npm run visual-smoke   # 3 format × 2 frame の still + ffprobe + grid
CLAUDE.md:272:npm run test           # lint + visual-smoke を一気に
CLAUDE.md:285:mismatch 1 件以上で exit 2 (regression 即検知)。`out/visual_smoke/grid.png` で
CLAUDE.md:286:6 cell の目視レビュー、`summary.json` で機械可読なパス/失敗統計。
template/package.json:33:    "visual-smoke": "python3 scripts/visual_smoke.py",
template/package.json:34:    "test:visual-smoke": "python3 scripts/visual_smoke.py",
template/scripts/visual_smoke.py:14:ffmpeg で 3×N grid PNG を out/visual_smoke/grid.png に合成し、目視レビューも可。
template/scripts/visual_smoke.py:20:- ffmpeg vstack/hstack で grid 合成 (`--no-grid` で skip 可)
template/scripts/visual_smoke.py:30:    python3 scripts/visual_smoke.py --no-grid             # grid 合成 skip
template/scripts/visual_smoke.py:36:         ffprobe failed / ffmpeg drawtext filter なし / grid 合成 failed)
template/scripts/visual_smoke.py:138:def make_grid(
template/scripts/visual_smoke.py:140:    grid_out: Path,
template/scripts/visual_smoke.py:145:    """ffmpeg で N(format) × M(frame) の grid を 1 PNG に合成。
template/scripts/visual_smoke.py:154:    grid_out.parent.mkdir(parents=True, exist_ok=True)
template/scripts/visual_smoke.py:189:        filter_parts.append(f"{row_labels[0]}copy[grid]")
template/scripts/visual_smoke.py:191:        filter_parts.append(f"{''.join(row_labels)}vstack=inputs={n_fmt}[grid]")
template/scripts/visual_smoke.py:200:            "[grid]",
template/scripts/visual_smoke.py:203:            str(grid_out),
template/scripts/visual_smoke.py:222:    ap.add_argument("--no-grid", action="store_true", help="ffmpeg grid 合成 skip")
template/scripts/visual_smoke.py:250:        print(f"ERROR: base 動画が無い: {MAIN_VIDEO} (npm run visual-smoke は実 project で実行)", file=sys.stderr)
template/scripts/visual_smoke.py:259:    grid_label = has_drawtext_filter()
template/scripts/visual_smoke.py:260:    if not grid_label and not args.no_grid:
template/scripts/visual_smoke.py:262:            "INFO: ffmpeg drawtext filter なし、grid label を skip して画像のみ合成します",
template/scripts/visual_smoke.py:274:    mismatched = 0  # dimension 不一致のみカウント (render/probe 失敗は exit 3 系で別扱い)
template/scripts/visual_smoke.py:275:    env_error: str | None = None
template/scripts/visual_smoke.py:279:            if env_error:
template/scripts/visual_smoke.py:298:                    env_error = "still_failed"
template/scripts/visual_smoke.py:307:                    env_error = "probe_failed"
template/scripts/visual_smoke.py:315:                    mismatched += 1
template/scripts/visual_smoke.py:336:    grid_status = "skipped"
template/scripts/visual_smoke.py:337:    grid_error: str | None = None
template/scripts/visual_smoke.py:338:    full_matrix = len(stills) == len(formats) * len(frames) and not env_error
template/scripts/visual_smoke.py:339:    if not args.no_grid and full_matrix:
template/scripts/visual_smoke.py:340:        # P2 #5: full matrix の時のみ grid (部分失敗時は cell 対応が崩れるため)
template/scripts/visual_smoke.py:341:        grid_out = out_dir / "grid.png"
template/scripts/visual_smoke.py:343:            make_grid(stills, grid_out, formats, frames, label=grid_label)
template/scripts/visual_smoke.py:344:            print(f"\n[smoke] grid: {grid_out}")
template/scripts/visual_smoke.py:345:            grid_status = "ok"
template/scripts/visual_smoke.py:347:            # P1 #2: grid 失敗は環境問題として exit 3 (silent WARN にしない)
template/scripts/visual_smoke.py:348:            print(f"ERROR: ffmpeg grid 合成失敗: {e}", file=sys.stderr)
template/scripts/visual_smoke.py:349:            grid_status = "failed"
template/scripts/visual_smoke.py:350:            grid_error = str(e)
template/scripts/visual_smoke.py:352:    summary_path = out_dir / "summary.json"
template/scripts/visual_smoke.py:359:                "mismatched": mismatched,
template/scripts/visual_smoke.py:361:                "env_error": env_error,
template/scripts/visual_smoke.py:362:                "grid": {"status": grid_status, "error": grid_error},
template/scripts/visual_smoke.py:370:    print(f"  total={len(results)}, mismatched={mismatched}, env_error={env_error}, grid={grid_status}")
template/scripts/visual_smoke.py:372:    if env_error or grid_status == "failed":
template/scripts/visual_smoke.py:374:    if mismatched:

exec
/bin/zsh -lc 'ffmpeg -hide_banner -h filter=hstack' in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc 'ffmpeg -hide_banner -h filter=vstack' in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
Filter hstack
  Stack video inputs horizontally.
    slice threading supported
    Inputs:
        dynamic (depending on the options)
    Outputs:
       #0: default (video)
(h|v)stack AVOptions:
   inputs            <int>        ..FV....... set number of inputs (from 2 to INT_MAX) (default 2)
   shortest          <boolean>    ..FV....... force termination when the shortest input terminates (default false)


Exiting with exit code 0

 succeeded in 0ms:
Filter vstack
  Stack video inputs vertically.
    slice threading supported
    Inputs:
        dynamic (depending on the options)
    Outputs:
       #0: default (video)
(h|v)stack AVOptions:
   inputs            <int>        ..FV....... set number of inputs (from 2 to INT_MAX) (default 2)
   shortest          <boolean>    ..FV....... force termination when the shortest input terminates (default false)


Exiting with exit code 0

hook: PreToolUse
hook: PreToolUse
hook: PreToolUse Completed
hook: PreToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
exec
/bin/zsh -lc "ffmpeg -v error -f lavfi -i color=s=1280x360:d=0.1 -f lavfi -i color=s=404x360:d=0.1 -f lavfi -i color=s=720x360:d=0.1 -filter_complex '[0:v][1:v][2:v]vstack=inputs=3[out]' -map '[out]' -frames:v 1 -f null -" in /Users/rokumasuda/.claude/plugins/supermovie
exec
/bin/zsh -lc "ffmpeg -v error -f lavfi -i color=s=640x360:d=0.1 -f lavfi -i color=s=202x360:d=0.1 -f lavfi -i color=s=360x360:d=0.1 -filter_complex '[0:v][1:v][2:v]vstack=inputs=3[out]' -map '[out]' -frames:v 1 -f null -" in /Users/rokumasuda/.claude/plugins/supermovie
 exited 234 in 0ms:
[Parsed_vstack_0 @ 0x8d101da40] Input 1 width 404 does not match input 0 width 1280.
[Parsed_vstack_0 @ 0x8d101da40] Failed to configure output pad on Parsed_vstack_0
[fc#0 @ 0x8d1010000] Error reinitializing filters!
[fc#0 @ 0x8d1010000] Task finished with error code: -22 (Invalid argument)
[fc#0 @ 0x8d1010000] Terminating thread with return code -22 (Invalid argument)
[vost#0:0/wrapped_avframe @ 0x8d0c28000] [enc:wrapped_avframe @ 0x8d0c145b0] Could not open encoder before EOF
[vost#0:0/wrapped_avframe @ 0x8d0c28000] Task finished with error code: -22 (Invalid argument)
[vost#0:0/wrapped_avframe @ 0x8d0c28000] Terminating thread with return code -22 (Invalid argument)
[out#0/null @ 0x8d101ce40] Nothing was written into output file, because at least one of its streams received no packets.

 exited 234 in 0ms:
[Parsed_vstack_0 @ 0xb0700df80] Input 1 width 202 does not match input 0 width 640.
[Parsed_vstack_0 @ 0xb0700df80] Failed to configure output pad on Parsed_vstack_0
[fc#0 @ 0xb07404000] Error reinitializing filters!
[fc#0 @ 0xb07404000] Task finished with error code: -22 (Invalid argument)
[fc#0 @ 0xb07404000] Terminating thread with return code -22 (Invalid argument)
[vost#0:0/wrapped_avframe @ 0xb0683c000] [enc:wrapped_avframe @ 0xb070098f0] Could not open encoder before EOF
[vost#0:0/wrapped_avframe @ 0xb0683c000] Task finished with error code: -22 (Invalid argument)
[vost#0:0/wrapped_avframe @ 0xb0683c000] Terminating thread with return code -22 (Invalid argument)
[out#0/null @ 0xb0700d440] Nothing was written into output file, because at least one of its streams received no packets.

exec
/bin/zsh -lc "git ls-tree -r --name-only HEAD | rg '"'^(template|skills|CLAUDE|README|'"\\.github|\\.codex)'" in /Users/rokumasuda/.claude/plugins/supermovie
 succeeded in 0ms:
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-vp8VzGVY' (errno=Operation not permitted)
git: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead
git: error: couldn't create cache file '/tmp/xcrun_db-E341qqHS' (errno=Operation not permitted)
CLAUDE.md
README.md
skills/supermovie-cut/SKILL.md
skills/supermovie-image-gen/SKILL.md
skills/supermovie-init/SKILL.md
skills/supermovie-narration/SKILL.md
skills/supermovie-se/SKILL.md
skills/supermovie-skill-creator/SKILL.md
skills/supermovie-slides/SKILL.md
skills/supermovie-subtitles/SKILL.md
skills/supermovie-telop-creator/SKILL.md
skills/supermovie-transcribe/SKILL.md
skills/supermovie-transcript-fix/SKILL.md
template/.prettierrc
template/eslint.config.mjs
template/package.json
template/remotion.config.ts
template/scripts/budoux_split.mjs
template/scripts/build_slide_data.py
template/scripts/build_telop_data.py
template/scripts/compare_telop_split.py
template/scripts/generate_slide_plan.py
template/scripts/preflight_video.py
template/scripts/visual_smoke.py
template/scripts/voicevox_narration.py
template/src/InsertImage/ImageSequence.tsx
template/src/InsertImage/InsertImage.tsx
template/src/InsertImage/index.ts
template/src/InsertImage/insertImageData.ts
template/src/InsertImage/types.ts
template/src/MainVideo.tsx
template/src/Narration/NarrationAudio.tsx
template/src/Narration/index.ts
template/src/Root.tsx
template/src/Slides/Slide.tsx
template/src/Slides/SlideSequence.tsx
template/src/Slides/index.tsx
template/src/Slides/slideData.ts
template/src/Slides/types.ts
template/src/SoundEffects/BGM.tsx
template/src/SoundEffects/SEPlayer.ts
template/src/SoundEffects/SESequence.tsx
template/src/SoundEffects/seData.ts
template/src/Title/Title.tsx
template/src/Title/index.ts
template/src/Title/titleData.ts
template/src/index.css
template/src/index.ts
template/src/videoConfig.ts
template/tsconfig.json

  ✓ 指定 git log / show で差分範囲を確認
  ✓ 8件の指摘ごとに該当コードを照合
  ✓ regression と既存依存を検索
  → verdict 表と新規指摘をまとめる
  ✓ 指定 git log / show で差分範囲を確認
  ✓ 8件の指摘ごとに該当コードを照合
  ✓ regression と既存依存を検索
  ✓ verdict 表と新規指摘をまとめる
