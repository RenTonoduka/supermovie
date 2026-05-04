/**
 * Phase 3-T (Codex CODEX_REVIEW_PHASE3S_AND_3T 推奨): chunks mode 経路の
 * useNarrationMode test。useNarrationMode.test.tsx は narrationData mock 空
 * 固定 (legacy / none 経路のみ) なので、chunks 経路を別 file で分離して mock
 * の競合を避ける (vitest 各 test file は独立 module cache)。
 *
 * 検証経路 (Codex review 重点):
 *   - mode "chunks" when narrationData non-empty + 全 chunk file が存在
 *   - chunks 経路は legacy より優先
 *   - incomplete chunks (一部 chunk file 不在) → legacy fallback
 *   - 1 + chunk 数の watcher 登録 + unmount 全 cancel
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';

vi.mock('remotion', () => {
  const watchers: Map<string, Set<() => void>> = new Map();
  let staticFiles: Array<{ name: string }> = [];

  const watchStaticFile = (name: string, callback: () => void) => {
    if (!watchers.has(name)) watchers.set(name, new Set());
    watchers.get(name)!.add(callback);
    return {
      cancel: () => {
        watchers.get(name)?.delete(callback);
        if (watchers.get(name)?.size === 0) watchers.delete(name);
      },
    };
  };

  return {
    watchStaticFile,
    getStaticFiles: () => staticFiles,
    __setStaticFiles: (files: Array<{ name: string }>) => {
      staticFiles = files;
    },
    __triggerWatch: (name: string) => {
      watchers.get(name)?.forEach((cb) => cb());
    },
    __getWatcherCount: () => {
      let total = 0;
      watchers.forEach((set) => (total += set.size));
      return total;
    },
    __resetWatchers: () => {
      watchers.clear();
    },
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

import * as remotion from 'remotion';
import { useNarrationMode } from './useNarrationMode';
import { invalidateNarrationMode } from './mode';

const remotionMock = remotion as unknown as {
  __setStaticFiles: (files: Array<{ name: string }>) => void;
  __triggerWatch: (name: string) => void;
  __getWatcherCount: () => number;
  __resetWatchers: () => void;
};

describe('useNarrationMode (chunks mode)', () => {
  beforeEach(() => {
    invalidateNarrationMode();
    remotionMock.__setStaticFiles([]);
    remotionMock.__resetWatchers();
  });

  afterEach(() => {
    invalidateNarrationMode();
  });

  it('returns mode "chunks" when narrationData populated + all chunk files exist', () => {
    remotionMock.__setStaticFiles([
      { name: 'narration/chunk_000.wav' },
      { name: 'narration/chunk_001.wav' },
    ]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('chunks');
    if (result.current.kind === 'chunks') {
      expect(result.current.segments).toHaveLength(2);
    }
  });

  it('chunks mode takes precedence over legacy when both exist', () => {
    remotionMock.__setStaticFiles([
      { name: 'narration.wav' },
      { name: 'narration/chunk_000.wav' },
      { name: 'narration/chunk_001.wav' },
    ]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('chunks');
  });

  it('falls back to legacy when narrationData populated but a chunk is missing', () => {
    remotionMock.__setStaticFiles([
      { name: 'narration.wav' },
      { name: 'narration/chunk_000.wav' },
      // chunk_001.wav は不在
    ]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('legacy');
  });

  it('falls back to none when chunks incomplete + legacy absent', () => {
    remotionMock.__setStaticFiles([
      { name: 'narration/chunk_000.wav' },
      // chunk_001.wav 不在 + narration.wav 不在
    ]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('none');
  });

  it('registers 1 + chunk count watchers, all canceled on unmount', () => {
    const { unmount } = renderHook(() => useNarrationMode());
    // narration.wav (1) + chunk_000.wav + chunk_001.wav (2) = 3 watchers
    expect(remotionMock.__getWatcherCount()).toBe(3);
    unmount();
    expect(remotionMock.__getWatcherCount()).toBe(0);
  });

  it('chunk watch trigger re-evaluates mode (incomplete → complete chunks)', () => {
    // 初期: chunk_000.wav のみ → narrationData 完全じゃないので none
    remotionMock.__setStaticFiles([{ name: 'narration/chunk_000.wav' }]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('none');
    // chunk_001.wav 出現 → trigger watch on chunk_001.wav
    act(() => {
      remotionMock.__setStaticFiles([
        { name: 'narration/chunk_000.wav' },
        { name: 'narration/chunk_001.wav' },
      ]);
      remotionMock.__triggerWatch('narration/chunk_001.wav');
    });
    expect(result.current.kind).toBe('chunks');
  });
});
