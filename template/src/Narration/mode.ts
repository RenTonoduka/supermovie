import { getStaticFiles } from 'remotion';
import { narrationData } from './narrationData';
import type { NarrationSegment } from './types';

export const NARRATION_LEGACY_FILE = 'narration.wav';

/**
 * Phase 3-H Codex review P1 #1 反映:
 * NarrationAudio と MainVideo が narration の状態を別々に判定すると、
 * chunk 不足 + legacy 存在で「narration も base 元音声も無音」になる
 * 矛盾モードが発生する。本 helper を両者から呼ぶことで mode を一元化する。
 */
export type NarrationMode =
  | { kind: 'chunks'; segments: readonly NarrationSegment[] }
  | { kind: 'legacy'; file: string }
  | { kind: 'none' };

/**
 * narration の有効モードを返す。優先順位:
 *   1) narrationData が non-empty + 全 chunk file が public/ 配下に存在 → chunks
 *   2) public/narration.wav 存在 → legacy
 *   3) どちらも不在 → none
 *
 * getStaticFiles() の結果を一度 Set 化して O(1) lookup
 * (Codex P3 #8 反映、毎 frame の some() 重複を防ぐ)。
 *
 * Codex re-review 新規 P3 反映: module-level memo で 1 render 内の
 * 重複呼出 (MainVideo + NarrationAudio が両方 call) を 1 回に集約。
 * Remotion は 1 render で 1 JS context を使うため、context-fresh で
 * 自然に memo が消える (Studio hot-reload 時も module 再評価で reset)。
 *
 * Phase 3-N (Codex Phase 3-M 推奨 ii): Studio hot-reload に対応するため
 * `invalidateNarrationMode()` を追加、`useNarrationMode()` hook が
 * `watchStaticFile` callback で invalidate + React state 更新する。
 * Player / render は従来通り pure helper で動作。
 *
 * 出典: https://www.remotion.dev/docs/getstaticfiles
 */
let _modeCache: NarrationMode | undefined;

export const getNarrationMode = (): NarrationMode => {
  if (_modeCache !== undefined) {
    return _modeCache;
  }
  const names = new Set(getStaticFiles().map((f) => f.name));
  if (
    narrationData.length > 0 &&
    narrationData.every((seg) => names.has(seg.file))
  ) {
    _modeCache = { kind: 'chunks', segments: narrationData };
  } else if (names.has(NARRATION_LEGACY_FILE)) {
    _modeCache = { kind: 'legacy', file: NARRATION_LEGACY_FILE };
  } else {
    _modeCache = { kind: 'none' };
  }
  return _modeCache;
};

/**
 * Phase 3-N: Studio hot-reload で _modeCache を無効化するための export。
 * useNarrationMode hook (`src/Narration/useNarrationMode.ts`) が
 * watchStaticFile callback から呼ぶ。Player / render path は呼ばない (memo
 * を maintain するほうが速い)。
 */
export const invalidateNarrationMode = (): void => {
  _modeCache = undefined;
};
