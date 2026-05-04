# SuperMovie Phase 3 Progress (2026-05-04)

Phase 3-A 〜 Phase 3-O の commit 集約と Codex review 履歴。次セッション着手前の状態把握用。

`docs/PHASE3_PROGRESS.md` は `scripts/regen_phase3_progress.sh` で commit chain
section が auto-gen される。本文 (Phase 別 deliverable / Codex review 履歴 / 残候補)
は手動メンテ。`git log roku/phase3i-transcript-alignment..HEAD --oneline` を一次 source。

## Branch chain

```
main
 ├─ roku/phase3f-asset-gate    : Phase 3-F BGM/Narration asset gate
 ├─ roku/phase3g-visual-smoke  : Phase 3-F hotfix + Phase 3-G visual_smoke 初版 + 8 件 fix
 ├─ roku/phase3h-narration-sequence
 │     : Phase 3-H per-segment <Sequence> + 9 件 fix + vstack letterbox
 ├─ roku/phase3i-transcript-alignment
 │     : Phase 3-I transcript timing alignment + cut-aware mapping
 └─ roku/phase3j-timeline (HEAD)
       : Phase 3-J timeline.py 共通化 + 6 件 fix
       : Phase 3-K core 1 integration smoke test
       : Phase 3-K core 2 build_slide / build_telop transcript validation
       : Phase 3-J review 4 件 fix (P1 partial 含む)
       : Phase 3-L core require_timing strict mode
       : Phase 3-L vi build_slide e2e test + P1 partial fix
       : Phase 3-M core 1 build_telop e2e test (call_budoux stub)
       : Phase 3-M ii build_telop ms_to_playback_frame timeline 統合
       : Phase 3-M iii generate_slide_plan skip + missing inputs test
```

## Phase 別 deliverable サマリ

### Phase 3-F (asset gate, branch: roku/phase3f-asset-gate)
- `template/src/SoundEffects/BGM.tsx` + `Narration/NarrationAudio.tsx`:
  `getStaticFiles()` で public 配下 asset 有無検出、不在時 null
- 不在 OK → render 失敗しない (BGM/narration は optional)

### Phase 3-G (visual smoke, branch: roku/phase3g-visual-smoke)
- `template/scripts/visual_smoke.py`: 3 format × 2 frame の still + ffprobe + grid
- vstack letterbox fix (Codex bg 中の investigation で発見、新規 P1)
- Phase 3-F hotfix: base Video volume 自動 mute when narration.wav present

### Phase 3-H (per-segment Sequence, branch: roku/phase3h-narration-sequence)
- `template/src/Narration/types.ts`: NarrationSegment 型定義
- `template/src/Narration/narrationData.ts`: placeholder (script で all-or-nothing 上書き)
- `template/src/Narration/mode.ts`: getNarrationMode() (chunks / legacy / none 三経路)
- `voicevox_narration.py`: chunk 保持 + wave duration 測定 + atomic 書き込み
  + cleanup_stale_all + StaleCleanupError + wave.Error catch
- `MainVideo.tsx` + `NarrationAudio.tsx`: getNarrationMode() 経由

### Phase 3-I (transcript timing, branch: roku/phase3i-transcript-alignment)
- collect_chunks() を {text, sourceStartMs, sourceEndMs} dict 返しに変更
- write_narration_data() で transcript start_ms から videoConfig.FPS で frame 化
- vad_result.json があれば cut-aware mapping (build_cut_segments_from_vad +
  ms_to_playback_frame)
- 隣接 chunk overlap 検出 + WARN

### Phase 3-J (timeline 共通化, branch: roku/phase3j-timeline)
- `template/scripts/timeline.py`: 4 helper + 2 validation
  - read_video_config_fps / build_cut_segments_from_vad / ms_to_playback_frame /
    load_cut_segments / VadSchemaError / validate_vad_schema /
    TranscriptSegmentError / validate_transcript_segment(s)
- 3 script (voicevox / build_slide / build_telop) で FPS / cut helper を統一
- VAD 部分破損 fail-fast、transcript start>end / 型不正 fail-fast

### Phase 3-K (smoke test, on roku/phase3j-timeline)
- `template/scripts/test_timeline_integration.py`: 14 test ケース
- `template/package.json`: `test:timeline` script、`test = lint + test:timeline`
- `CLAUDE.md` に Visual Smoke + Timeline Test 節
- transcript validation を build_slide / build_telop にも展開 (require_timing=True)

### Phase 3-L (require_timing + Phase 3-J review fix, on roku/phase3j-timeline)
- timeline.validate_transcript_segment(require_timing) + validate_transcript_segments
- voicevox は optional 維持 (Phase 3-I 累積 fallback 互換)
- VAD load synthesis 前移動 + NARRATION_DIR.mkdir() 順序 fix (P1 partial)
- collect_chunks の validate を `.get(...).strip()` 前に移動 (P2 #1)
- build_telop で validate_vad_schema 経由 (P2 #2)
- SKILL.md に exit 3 / exit 8 追記 (P3)
- assert → RuntimeError raise (`python -O` safe)

### Phase 3-M (cut helper 完全統合 + smoke 拡張, on roku/phase3j-timeline)
- build_telop ms_to_playback_frame を timeline 経由 (find_cut_segment_for_ms 残置)
- build_telop e2e test (call_budoux stub)
- generate_slide_plan skip + missing inputs test
- docs/PHASE3_PROGRESS.md + docs/reviews/ 9 件 commit (Codex artifact)

### Phase 3-N (Studio hot-reload + API mock 完成, on roku/phase3j-timeline)
- generate_slide_plan API mock test (urllib monkey-patch、success / HTTP error / invalid JSON)
- Codex Phase 3-M review P2×3 fix (PHASE3_PROGRESS 更新 / API key save+restore /
  test isolation 強化)
- src/Narration/useNarrationMode.ts 新規 (watchStaticFile + invalidateNarrationMode +
  React state、Player/render では try/catch で no-op fallback)
- mode.ts に invalidateNarrationMode export 追加
- MainVideo / NarrationAudio が hook 経由に統一

### Phase 3-O (validation + auto-gen + race fix, on roku/phase3j-timeline)
- build_slide_data --plan validation 経路 test (Codex P2 #3 解消、fallback / strict 両 path)
- scripts/regen_phase3_progress.sh: PHASE3_PROGRESS commit chain 自動再生成 helper
- voicevox_narration.py write 順序を chunks → narrationData.ts → narration.wav に
  変更 (Codex Phase 3-N P2 hot-reload race 解消、Studio で chunks 経路が先に
  成立して legacy fallback が一瞬鳴る window を消す)

## Codex review 履歴

| review file | 対象 commit | verdict |
|---|---|---|
| CODEX_REVIEW_PHASE3F_20260504T205513 | Phase 3-F | P1×3 + P2×2 + P3×3、Phase 3-G で全 fix |
| CODEX_PHASE3G_NEXT_20260504T205513 | Phase 3-G design | visual_smoke + temp project + ffprobe |
| CODEX_REVIEW_PHASE3G_20260504T211444 | Phase 3-G 初版 | P1×3 + P2×3 + P3×2、Phase 3-G fix で全 close |
| CODEX_REVIEW_PHASE3G_FIX_20260504T212554 | Phase 3-G fix | token 切れで verdict 不完全、investigation で vstack バグ実証 |
| CODEX_REVIEW_PHASE3H_20260504T213301 | Phase 3-H | P1×2 + P2×4 + P3×3、Phase 3-H fix で全 close |
| CODEX_REVIEW_PHASE3H_FIX_AND_NEXT_20260504T214514 | Phase 3-H fix | 7/9 ✅ + ⚠️ partial 2 件 + 新規 P2/P3×3、residual 5 fix |
| CODEX_REVIEW_PHASE3I_AND_NEXT_20260504T215824 | Phase 3-I | P1×2 + P2×2 + P3×2、Phase 3-J で全 fix |
| CODEX_REVIEW_PHASE3J_AND_NEXT_20260504T221120 | Phase 3-J | P1×1 + P2×2 + P3×1、Phase 3-J review fix で close |
| CODEX_REVIEW_PHASE3J_FIX_AND_3L_20260504T222048 | Phase 3-J fix | 4/5 ✅ + P1 partial (NARRATION_DIR.mkdir 順序)、即 fix 済 |
| CODEX_REVIEW_PHASE3L_AND_3M_20260504T222846 | Phase 3-L vi + P1 partial fix | P2 #1 (cleanup contract コメント) + P2 #2 (test isolation)、94bc3d5 で全 fix |
| CODEX_REVIEW_PHASE3M_AND_3N_20260504T223552 | Phase 3-M comprehensive | P0/P1 なし、P2×3 (PHASE3_PROGRESS 不正確 / API key restore / API mock schema validation 未踏)、Phase 3-N 推奨 ii Studio hot-reload、f34abf3 で P2 #1+#2 / 6c8fb00 で P2 #3 fix |
| CODEX_REVIEW_PHASE3N_AND_3O_20260504T224734 | Phase 3-N + 3-O i/ii | P2 #1 (hot-reload race) + P3 #1 (PHASE3_PROGRESS body stale)、本 commit で全 fix |

## 未着手 / 残候補

### 自走可
- any 警告ゼロ化 (TS-side、eslint-config-flat 4.x、telopTemplate 30 個全 typing 必要、
  npm install 走らせる必要あり)
- Phase 3-O ii (PHASE3_PROGRESS auto-gen) は Phase 別 deliverable / Codex review 履歴 /
  残候補 sections も auto-gen するなら拡張余地あり
- voicevox_narration.py の sentinel 化 (現行 race fix で十分でも、より厳密な
  signal file を narrationData.ts 後に書く形も Codex 言及)

### Roku 判断領域 (deploy / 段取り / 課金 / 法的)
- ★ PR / merge 戦略 (roku/phase3j-timeline は phase3i / phase3h / phase3g / phase3f を
  順次 merge する必要あり、複数分岐を 1 PR に潰すか段階 merge にするか)
- Phase 3-G visual_smoke を実 project で end-to-end 検証 (main.mp4 fixture 必要)
- CI 整備 (GitHub Actions / 別 CI provider、test:timeline + lint 自動化)
- slide_plan.v2 + scene_plan 統合 (Anthropic API 課金)
- supermovie-image-gen 統合 (Gemini API 課金)
- supermovie-se 統合 (素材判断)
- SadTalker / HeyGen / Kling 統合 (法的 / モラルリスク + API 課金)

## 全 commit count (roku/phase3j-timeline branch、最新 33 件)

```
155f396 chore(gitignore): __pycache__/ + *.pyc 追加
5dc2fb7 docs(phase3): regen commit chain to 31
a1c615e feat(release): check_release_ready.sh に optional lint gate (Codex 最終推奨)
b2f8974 docs(phase3): regen commit chain to 29
e31eafe feat(release): check_release_ready.sh composite gate (Phase 3-Q)
c40ed7f docs(phase3): regen commit chain to 27
f9bd729 docs(phase3): release-ready note + final Codex verify artifact
d71c503 docs(phase3): regen commit chain to 25 + release-readiness artifact
5a10f21 docs(reviews): Codex Phase 3-P review + 3-Q consult artifact
bce03e0 feat(docs): regen_phase3_progress.sh --verify mode + self-reference doc (Phase 3-Q ii)
32a6bfa docs(phase3): regen commit chain to 22 commits
d41ec9c fix(narration): Codex Phase 3-O fix re-review P1 + P2 #2 actual code fix
b70b592 fix(narration): Codex Phase 3-O fix re-review P1 + P2×2 + P3 全 fix
aacc5dc test(narration): write 順序 race fix の regression test (Phase 3-O follow-up)
9876e61 docs(phase3): regen commit chain section to 18 commits
a5fcb80 fix(narration): Studio hot-reload race + PHASE3_PROGRESS body update (Phase 3-N review fix)
d10cd92 feat(docs): PHASE3_PROGRESS.md auto-gen helper (Phase 3-O ii)
6c8fb00 test(timeline): build_slide_data --plan validation 経路 (Phase 3-O i / Codex P2 #3)
1d27892 feat(narration): Studio hot-reload via watchStaticFile (Phase 3-N ii)
f34abf3 fix(timeline): Codex Phase 3-M review P2 #1 + #2 fix
ae3d2e8 test(timeline): generate_slide_plan API HTTP error + invalid JSON path (Phase 3-N i+)
8abdb2b test(timeline): generate_slide_plan Anthropic API mock test (Phase 3-N i)
94bc3d5 fix(timeline): Codex Phase 3-L re-review P2 2 件 fix
47e6c39 docs(phase3): Phase 3 progress note + Codex review artifacts (Phase 3-M v)
bed46b7 test(timeline): generate_slide_plan skip + missing inputs subtest (Phase 3-M iii)
350dff7 refactor(telop): ms_to_playback_frame を timeline 経由に統一 (Phase 3-M ii)
3c765e3 test(timeline): build_telop_data e2e + bad transcript subtest (Phase 3-M core 1)
96e5215 fix(narration): P1 partial NARRATION_DIR.mkdir 順序 + Phase 3-L vi 展開
a9019c7 feat(timeline): require_timing strict mode + validate_transcript_segments helper (Phase 3-L core)
e2a1a39 fix(timeline): Codex Phase 3-J review 4 件 fix (P1×1 + P2×2 + P3×1)
41b5ef2 fix(timeline): transcript validation を build_slide / build_telop にも展開 (Phase 3-K core 2)
398ea94 test(timeline): pure python integration smoke test (Phase 3-K core 1)
66e2aeb feat(timeline): timeline.py 共通化 + Phase 3-I review 6 件 fix (Phase 3-J)
```

(更新: 2026-05-04_23:57、source=HEAD、`scripts/regen_phase3_progress.sh` で auto-gen。
本 script で regen → docs commit する形のため、docs 上の commit chain は
docs commit を作る前の HEAD を反映する設計 (off-by-one は intrinsic、
`--verify` mode で count drift を CI 検査可)。)

## Test gates

```bash
cd <PROJECT> (template から copy された実 project)
npm run test           # eslint + tsc + pure python integration smoke
npm run test:timeline  # pure python integration smoke 単独 (engine 不要、CI 高頻度可)
npm run visual-smoke   # 実 main.mp4 + node_modules 必要、3 format × 2 frame still
```

`test:timeline` は **20 test ケース** (Phase 3-A〜3-O 累積、最新 aacc5dc 時点) で
timeline.py / 4 script の連鎖を engine 不要で高速検証 (新規 commit 後の regression
早期検出用)。test 一覧は `scripts/test_timeline_integration.py` の `main()` 末尾参照。
