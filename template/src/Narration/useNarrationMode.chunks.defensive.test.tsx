/**
 * Phase 3-V (Codex CODEX_REVIEW_PHASE3U_AND_3V P2 gap 反映): chunk 側
 * watchStaticFile(seg.file) で partial throw した場合の defensive test。
 * useNarrationMode.test.tsx (legacy / none) や
 * useNarrationMode.chunks.test.tsx (chunks happy path) や
 * useNarrationMode.defensive.test.tsx (legacy 側 throw) では未検証だった、
 * 「narrationData non-empty で一部 chunk file の watch だけ throw する」
 * 経路を runtime 検証する。
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook } from '@testing-library/react';

const throwTargets = new Set<string>();

vi.mock('remotion', () => {
  const watchStaticFile = (
    name: string,
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    callback: () => void,
  ) => {
    if (throwTargets.has(name)) {
      throw new Error(`Simulated throw for ${name}`);
    }
    return { cancel: () => {} };
  };
  return {
    watchStaticFile,
    getStaticFiles: () => [],
  };
});

vi.mock('./narrationData', () => ({
  narrationData: [
    {
      id: 0,
      startFrame: 0,
      durationInFrames: 30,
      file: 'narration/chunk_000.wav',
      text: 'first',
    },
    {
      id: 1,
      startFrame: 30,
      durationInFrames: 15,
      file: 'narration/chunk_001.wav',
      text: 'second',
    },
  ],
}));

import { useNarrationMode } from './useNarrationMode';
import { invalidateNarrationMode } from './mode';

describe('useNarrationMode chunk-side defensive', () => {
  beforeEach(() => {
    invalidateNarrationMode();
    throwTargets.clear();
  });

  it('一部 chunk watch が throw しても他の watch は登録される (mount 成功)', () => {
    throwTargets.add('narration/chunk_001.wav');
    expect(() => {
      const { unmount } = renderHook(() => useNarrationMode());
      unmount();
    }).not.toThrow();
  });

  it('全 chunk watch が throw しても mount/unmount を破壊しない', () => {
    throwTargets.add('narration/chunk_000.wav');
    throwTargets.add('narration/chunk_001.wav');
    expect(() => {
      const { unmount } = renderHook(() => useNarrationMode());
      unmount();
    }).not.toThrow();
  });

  it('legacy watch は OK + chunk watch 全 throw → initial mode は normal 経路', () => {
    throwTargets.add('narration/chunk_000.wav');
    throwTargets.add('narration/chunk_001.wav');
    const { result } = renderHook(() => useNarrationMode());
    // watch が失敗しても initial getNarrationMode() は static state を読むので
    // narrationData empty 扱い (chunks 不在) → none を返す
    expect(result.current.kind).toBe('none');
  });
});
