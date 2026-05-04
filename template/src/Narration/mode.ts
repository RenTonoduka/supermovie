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
 * 出典: https://www.remotion.dev/docs/getstaticfiles
 */
export const getNarrationMode = (): NarrationMode => {
  const names = new Set(getStaticFiles().map((f) => f.name));
  if (
    narrationData.length > 0 &&
    narrationData.every((seg) => names.has(seg.file))
  ) {
    return { kind: 'chunks', segments: narrationData };
  }
  if (names.has(NARRATION_LEGACY_FILE)) {
    return { kind: 'legacy', file: NARRATION_LEGACY_FILE };
  }
  return { kind: 'none' };
};
