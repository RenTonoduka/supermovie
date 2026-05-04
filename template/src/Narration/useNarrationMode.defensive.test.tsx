/**
 * Phase 3-U (Codex CODEX_REVIEW_PHASE3T_AND_3U 推奨): useNarrationMode の
 * defensive path test。useNarrationMode.ts の try/catch (line 47, 69) で
 * watchStaticFile throw / cancel throw / cancel なし戻り値の経路を吸収する
 * 実装、その防御経路が unmount で落ちないことを runtime 検証する。
 *
 * Remotion 4.0.403 の watch-static-file.js では v5 flag 時 throw 経路あり
 * (Codex review に記載)、そこも mount/unmount が安全であることを保証する。
 *
 * 検証経路 (Codex review 重点):
 *   - watchStaticFile throw → useEffect 内で catch、mount は成功、watcher 0
 *   - cancel throw → unmount cleanup で catch、unmount 成功、leak 0
 *   - cancel なし戻り値 (return undefined) → cancel 関数取得失敗、unmount で
 *     try/catch が typeof check で吸収
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook } from '@testing-library/react';

// remotion mock — watchStaticFile が指定されたパターンで throw / 異常戻り値を返す
const mockState = {
  shouldThrow: false as boolean,
  cancelShouldThrow: false as boolean,
  returnNullCancel: false as boolean,
};

vi.mock('remotion', () => {
  const watchStaticFile = (name: string, callback: () => void) => {
    if (mockState.shouldThrow) {
      throw new Error('Simulated watchStaticFile failure');
    }
    if (mockState.returnNullCancel) {
      // cancel なしの戻り値を模擬 (typeof watchChunk.cancel !== 'function')
      return null as unknown as { cancel: () => void };
    }
    return {
      cancel: () => {
        if (mockState.cancelShouldThrow) {
          throw new Error('Simulated cancel failure');
        }
      },
    };
  };
  return {
    watchStaticFile,
    getStaticFiles: () => [],
  };
});

vi.mock('./narrationData', () => ({
  narrationData: [],
}));

import { useNarrationMode } from './useNarrationMode';
import { invalidateNarrationMode } from './mode';

describe('useNarrationMode defensive paths', () => {
  beforeEach(() => {
    invalidateNarrationMode();
    mockState.shouldThrow = false;
    mockState.cancelShouldThrow = false;
    mockState.returnNullCancel = false;
  });

  afterEach(() => {
    invalidateNarrationMode();
  });

  it('survives watchStaticFile throw without crashing mount', () => {
    mockState.shouldThrow = true;
    expect(() => {
      const { unmount } = renderHook(() => useNarrationMode());
      // mount 成功 + initial mode (none) を返す
      // unmount も throw しない
      unmount();
    }).not.toThrow();
  });

  it('survives cancel throw on unmount', () => {
    mockState.cancelShouldThrow = true;
    expect(() => {
      const { unmount } = renderHook(() => useNarrationMode());
      unmount();
    }).not.toThrow();
  });

  it('survives null/undefined return from watchStaticFile (no cancel function)', () => {
    mockState.returnNullCancel = true;
    expect(() => {
      const { unmount } = renderHook(() => useNarrationMode());
      unmount();
    }).not.toThrow();
  });

  it('initial mode falls back to "none" when watchStaticFile throws', () => {
    mockState.shouldThrow = true;
    const { result } = renderHook(() => useNarrationMode());
    // watch 失敗しても initial getNarrationMode() は動く
    expect(result.current.kind).toBe('none');
  });
});
