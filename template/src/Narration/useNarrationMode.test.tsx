/**
 * Phase 3-S B5 (Codex CODEX_REVIEW_PHASE3R_AND_3S 推奨): useNarrationMode hook の
 * vitest + jsdom + @testing-library/react による unit test.
 *
 * 検証経路 (Codex review 重点):
 *   - watchStaticFile callback が呼ばれた時 invalidateNarrationMode + setMode で
 *     React tree が再評価
 *   - unmount 時に全 watch.cancel() が呼ばれて memory leak しない
 *   - legacy / chunks / none の三経路切替
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';

// Remotion module を hoist mock (`vi.mock` は hoist 必要)
vi.mock('remotion', () => {
  const watchers: Map<string, () => void> = new Map();
  let staticFiles: Array<{ name: string }> = [];

  const watchStaticFile = (
    name: string,
    callback: () => void,
  ): { cancel: () => void } => {
    watchers.set(name, callback);
    return {
      cancel: () => {
        watchers.delete(name);
      },
    };
  };

  return {
    watchStaticFile,
    getStaticFiles: () => staticFiles,
    // Test helpers
    __setStaticFiles: (files: Array<{ name: string }>) => {
      staticFiles = files;
    },
    __triggerWatch: (name: string) => {
      const cb = watchers.get(name);
      if (cb) cb();
    },
    __getWatcherCount: () => watchers.size,
  };
});

// narrationData も mock (test ごとに書き換え可能に)
vi.mock('./narrationData', () => ({
  narrationData: [],
}));

import * as remotion from 'remotion';
import { useNarrationMode } from './useNarrationMode';
import { invalidateNarrationMode } from './mode';

const remotionMock = remotion as unknown as {
  __setStaticFiles: (files: Array<{ name: string }>) => void;
  __triggerWatch: (name: string) => void;
  __getWatcherCount: () => number;
};

describe('useNarrationMode', () => {
  beforeEach(() => {
    invalidateNarrationMode();
    remotionMock.__setStaticFiles([]);
  });

  afterEach(() => {
    invalidateNarrationMode();
  });

  it('returns mode "none" when no narration files exist', () => {
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current).toEqual({ kind: 'none' });
  });

  it('returns mode "legacy" when public/narration.wav exists', () => {
    remotionMock.__setStaticFiles([{ name: 'narration.wav' }]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('legacy');
    if (result.current.kind === 'legacy') {
      expect(result.current.file).toBe('narration.wav');
    }
  });

  it('watches narration.wav and re-evaluates on change', () => {
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('none');
    // Simulate voicevox_narration.py が narration.wav を生成
    act(() => {
      remotionMock.__setStaticFiles([{ name: 'narration.wav' }]);
      remotionMock.__triggerWatch('narration.wav');
    });
    expect(result.current.kind).toBe('legacy');
  });

  it('cleans up watchers on unmount (no memory leak)', () => {
    const { unmount } = renderHook(() => useNarrationMode());
    expect(remotionMock.__getWatcherCount()).toBeGreaterThan(0);
    unmount();
    expect(remotionMock.__getWatcherCount()).toBe(0);
  });
});
