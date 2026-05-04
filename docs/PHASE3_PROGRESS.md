# SuperMovie Phase 3 Progress (2026-05-04)

Phase 3-A 〜 Phase 3-M の commit 集約と Codex review 履歴。次セッション着手前の状態把握用。

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
- (残置) generate_slide_plan API mock test (urllib monkey-patch 必要)

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
| CODEX_REVIEW_PHASE3L_AND_3M_20260504T222846 | Phase 3-L vi + P1 partial fix | (進行中) |

## 未着手 / 残候補

### 自走可
- Phase 3-M iii API mock test (urllib.request.urlopen monkey-patch)
- Phase 3-M iv any 警告ゼロ化 (TS-side、eslint-config-flat 4.x)
- Phase 3-M vi Studio hot-reload (watchStaticFile、Studio 限定で Player 非影響)

### Roku 判断領域
- Phase 3-G visual_smoke を実 project で end-to-end 検証 (main.mp4 fixture 必要)
- slide_plan.v2 + scene_plan 統合 (Anthropic API 課金)
- supermovie-image-gen 統合 (Gemini API 課金)
- supermovie-se 統合 (素材判断)
- SadTalker / HeyGen / Kling 統合 (法的 / モラルリスク + API 課金)

## 全 commit count (roku/phase3j-timeline branch、9 件)

```
bed46b7 test(timeline): generate_slide_plan skip + missing inputs subtest (Phase 3-M iii)
350dff7 refactor(telop): ms_to_playback_frame を timeline 経由に統一 (Phase 3-M ii)
3c765e3 test(timeline): build_telop_data e2e + bad transcript subtest (Phase 3-M core 1)
96e5215 fix(narration): P1 partial NARRATION_DIR.mkdir 順序 + Phase 3-L vi 展開
a9019c7 feat(timeline): require_timing strict mode + validate_transcript_segments helper
e2a1a39 fix(timeline): Codex Phase 3-J review 4 件 fix
41b5ef2 fix(timeline): transcript validation を build_slide / build_telop にも展開
398ea94 test(timeline): pure python integration smoke test
66e2aeb feat(timeline): timeline.py 共通化 + Phase 3-I review 6 件 fix
```

## Test gates

```bash
cd <PROJECT> (template から copy された実 project)
npm run test           # eslint + tsc + pure python integration smoke
npm run test:timeline  # pure python integration smoke 単独 (engine 不要、CI 高頻度可)
npm run visual-smoke   # 実 main.mp4 + node_modules 必要、3 format × 2 frame still
```

`test:timeline` は 14 test ケースで timeline.py / 4 script の連鎖を engine 不要で
高速検証 (新規 commit 後の regression 早期検出用)。
