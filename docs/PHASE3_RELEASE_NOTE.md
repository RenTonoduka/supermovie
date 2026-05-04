# SuperMovie Phase 3 Release Note (2026-05-04)

`roku/phase3j-timeline` HEAD: `d71c503` (Codex CODEX_FINAL_VERIFY_20260504T231638
で release-ready 判定)

Phase 3-A 〜 Phase 3-Q の自走実装結果。本 note は Roku 不在モード中に Claude+Codex
協働で 26 commit を積んだ成果物の release assertion を固定する目的。

## Release-readiness statement (2026-05-04 時点、技術 readiness のみ)

| 項目 | 状態 |
|---|---|
| code 側 P0/P1 (Codex 14 review 通過) | ✅ ゼロ |
| pure python integration smoke (`test:timeline`) | ✅ 20/20 pass |
| docs vs git log drift (`regen_phase3_progress.sh --verify`) | ✅ exit 0 (drift 1 = self-reference 許容内) |
| worktree clean | ✅ untracked なし |
| TypeScript lint / tsc | [未検証] (npm install permission issue で sandbox 内検証不可、Roku 環境で再実行推奨) |
| 実 project visual-smoke / render e2e | [未検証] (Roku 判断領域、main.mp4 fixture 必要) |

Roku 判断領域 (release blocker 候補):
- ★ PR / merge 戦略: phase3f→g→h→i→j は ancestry 連結済み、技術的に階層 merge
  不要。Codex 推奨は `roku/phase3j-timeline` を 1 PR / squash merge。`main..HEAD`
  は 43 commits、PR diff は 26 commits 表示より大きく見える点に注意。
- 実 project (main.mp4 + node_modules + remotion installed) で
  `npm run test:visual-smoke` と `npm run render` を 1 周通すことが推奨。
- 5/13 リリース予定なら本 branch を Roku の最終 e2e 後に main へ。

## 主要 deliverable (Phase 3-F 〜 3-Q)

### 1. 基盤 (Phase 3-F〜H)
- BGM/Narration optional asset gate (`getStaticFiles()` で不在 OK、render 失敗しない)
- visual_smoke.py (3 format × 2 frame の still + ffprobe + grid)
- per-segment narration `<Sequence>` (chunk wav 保持 + wave duration 測定 +
  `narrationData.ts` all-or-nothing 生成 + atomic write)

### 2. timeline 共通化 (Phase 3-I/J)
- `template/scripts/timeline.py`: 4 helper + 2 validation 集約
  (`read_video_config_fps` / `build_cut_segments_from_vad` /
  `ms_to_playback_frame` / `load_cut_segments` / `validate_vad_schema` /
  `validate_transcript_segment(s)`)
- 3 script (voicevox / build_slide / build_telop) で FPS / cut helper /
  transcript validation を一元化
- VAD 部分破損 + transcript start>end / 型不正の fail-fast 早期検出

### 3. integration smoke + Studio hot-reload (Phase 3-K/N)
- 20 test ケース (`test_timeline_integration.py`、engine 不要、CI 高頻度可)
- `useNarrationMode()` hook (watchStaticFile + invalidateNarrationMode +
  React state、Studio で Cmd+R 不要、Player/render は no-op fallback)

### 4. write 順序 race fix + rollback 強化 (Phase 3-N/O/P)
- voicevox_narration.py write 順序を **chunks → narrationData.ts → narration.wav** に
  変更 (Studio hot-reload で legacy fallback が一瞬鳴る race を解消)
- concat_wavs_atomic 周辺の rollback catch を `Exception` 全般に拡張
  (旧 `wave.Error / EOFError` 限定だと `os.replace` / 権限 / disk full で
  all-or-nothing 破れ)
- regression test (`test_voicevox_write_order_narrationdata_before_wav`) で
  call order を mock 経由で verify (旧順序に戻れば必ず fail)

### 5. doc + verify infra (Phase 3-M/O/Q)
- `docs/PHASE3_PROGRESS.md`: branch chain / Phase 別 deliverable / Codex
  review 履歴 / 残候補 を 1 file に集約
- `scripts/regen_phase3_progress.sh`:
  - 通常 mode: commit chain section auto-gen
  - `--verify` mode: docs vs git log drift 検査 (CI guard、drift > 1 で exit 3)
  - `--source <SHA>`: HEAD ではなく指定 SHA まで
  - self-reference off-by-one を intrinsic 設計として明文化

## test gate コマンド

```bash
cd <PROJECT>  # template から copy された実 project
npm run test:timeline                    # pure python 20 test (engine 不要)
npm run test                             # eslint + tsc + test:timeline
npm run visual-smoke                     # 実 main.mp4 + node_modules で 3 format
                                         # × 2 frame still + dimension regression 検査
bash scripts/regen_phase3_progress.sh --verify  # docs drift 検査
```

## Codex review 履歴 (14 件)

`docs/reviews/CODEX_*.md` に全 artifact 保存。各 review の対象 commit + verdict +
fix commit の対応は `docs/PHASE3_PROGRESS.md` の Codex review 履歴 table 参照。
最新 review (`CODEX_FINAL_VERIFY_20260504T231638`) で release-ready 判定。

## 既知の限界 / 後続 phase 候補

### 自走可 (npm install 不要、低リスク)
- `regen_phase3_progress.sh` の Phase 別 deliverable / 残候補 sections も
  auto-gen 拡張 (commit message から推測する危険を Codex 過去 review で
  指摘済み、慎重設計必要)
- timeline.py / test_timeline_integration.py edge case 強化
- voicevox_narration.py の signal file による hot-reload 厳密化 (現行 race fix で
  実用十分でも、より厳密な sentinel が欲しい場面用)

### 自走可 (npm install / dev dep 必要)
- any 警告ゼロ化 (eslint no-explicit-any error 化、telopTemplate 30 個実型化)
- React component test (jsdom + React Testing Library 追加、useNarrationMode
  hook の watchStaticFile mock + invalidation 検証)

### Roku 判断領域 (deploy / 段取り / 課金 / 法的)
- PR / merge 戦略 (1 PR squash vs 階層 merge)
- 実 project での visual-smoke / render e2e (main.mp4 fixture 必要)
- CI 整備 (GitHub Actions / 別 CI provider)
- slide_plan.v2 + scene_plan 統合 (Anthropic API 課金)
- supermovie-image-gen 統合 (Gemini API 課金)
- supermovie-se 統合 (素材判断)
- SadTalker / HeyGen / Kling 統合 (法的 / モラルリスク + API 課金)

## 実装ファイル一覧 (Phase 3 で新規 / 大幅変更)

```
template/scripts/
├── timeline.py                      [新規 Phase 3-J、共通 helper 集約]
├── voicevox_narration.py            [大幅、Phase 3-D/H/I/J/L/M/N/O/P]
├── visual_smoke.py                  [新規 Phase 3-G]
├── test_timeline_integration.py     [新規 Phase 3-K、20 test]
├── build_slide_data.py              [Phase 3-J で timeline 統合]
├── build_telop_data.py              [Phase 3-J/M で timeline 統合]
└── generate_slide_plan.py           [Phase 3-C、Phase 3-N で API mock test]

template/src/Narration/
├── types.ts                         [新規 Phase 3-H、NarrationSegment 型]
├── narrationData.ts                 [新規 Phase 3-H、placeholder]
├── mode.ts                          [新規 Phase 3-H、getNarrationMode helper]
├── useNarrationMode.ts              [新規 Phase 3-N、Studio hot-reload hook]
├── NarrationAudio.tsx               [Phase 3-H/N で hook 経由に統一]
└── index.ts                         [export 集約]

template/src/MainVideo.tsx           [Phase 3-F/H/N で base mute + hook 経由]

scripts/regen_phase3_progress.sh     [新規 Phase 3-O、Phase 3-Q で --verify mode]

docs/
├── PHASE3_PROGRESS.md               [新規 Phase 3-M、auto-gen]
├── PHASE3_RELEASE_NOTE.md           [本 file、Phase 3-Q 末尾 release assertion]
└── reviews/                         [Codex 14 artifact、git tracked]
```

---

(本 note は Roku 不在モード中の Claude+Codex 協働 self-review で作成、Roku 戻り
時の handoff 起点。release decision / merge 順序 / 公開タイミングは Roku 判断領域。)
