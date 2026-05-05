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
  // Codex P5 review P2 #2 反映: callback 引数を StaticFileMeta 対応に。
  // 旧 signature `() => void` は引数なしで呼ばれていたが、本実装の sentinel
  // null guard と lastModified:sizeInBytes dedup は metadata/null が来た時だけ
  // 動くため、mock 側でも file param を渡せる形に拡張する。
  type StaticFileMeta =
    | {
        lastModified?: number;
        sizeInBytes?: number;
      }
    | null
    | undefined;
  const watchers: Map<string, Set<(file?: StaticFileMeta) => void>> = new Map();
  let staticFiles: Array<{ name: string }> = [];

  const watchStaticFile = (
    name: string,
    callback: (file?: StaticFileMeta) => void,
  ) => {
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
    __triggerWatch: (name: string, file?: StaticFileMeta) => {
      watchers.get(name)?.forEach((cb) => cb(file));
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

type TestStaticFileMeta =
  | {
      lastModified?: number;
      sizeInBytes?: number;
    }
  | null
  | undefined;

const remotionMock = remotion as unknown as {
  __setStaticFiles: (files: Array<{ name: string }>) => void;
  __triggerWatch: (name: string, file?: TestStaticFileMeta) => void;
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

  it('registers 2 + chunk count watchers (sentinel + legacy + chunks), all canceled on unmount', () => {
    const { unmount } = renderHook(() => useNarrationMode());
    // Phase 3-V P5: narration.ready.json sentinel (1) + narration.wav (1) +
    // chunk_000.wav + chunk_001.wav (2) = 4 watchers
    expect(remotionMock.__getWatcherCount()).toBe(4);
    unmount();
    expect(remotionMock.__getWatcherCount()).toBe(0);
  });

  it('sentinel trigger re-evaluates mode (chunks visible after ready signal)', async () => {
    // 初期: chunk file 不在で none
    remotionMock.__setStaticFiles([]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('none');
    // chunks + sentinel が現れた後、sentinel trigger で再評価
    // Phase 3-V P5 review P2 #1 反映: scheduleUpdate が queueMicrotask 経由なので
    // act() を async にして microtask flush を待つ
    await act(async () => {
      remotionMock.__setStaticFiles([
        { name: 'narration/chunk_000.wav' },
        { name: 'narration/chunk_001.wav' },
        { name: 'narration.ready.json' },
      ]);
      remotionMock.__triggerWatch('narration.ready.json');
      await Promise.resolve();
    });
    expect(result.current.kind).toBe('chunks');
  });

  it('chunk watch trigger re-evaluates mode (incomplete → complete chunks)', async () => {
    // 初期: chunk_000.wav のみ → narrationData 完全じゃないので none
    remotionMock.__setStaticFiles([{ name: 'narration/chunk_000.wav' }]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('none');
    // chunk_001.wav 出現 → trigger watch on chunk_001.wav
    // Phase 3-V P5 review P2 #1 反映: scheduleUpdate が queueMicrotask 経由なので
    // act() を async にして microtask flush を待つ
    await act(async () => {
      remotionMock.__setStaticFiles([
        { name: 'narration/chunk_000.wav' },
        { name: 'narration/chunk_001.wav' },
      ]);
      remotionMock.__triggerWatch('narration/chunk_001.wav');
      await Promise.resolve();
    });
    expect(result.current.kind).toBe('chunks');
  });

  it('sentinel null event (delete) is ignored, mode stays at chunks', async () => {
    // Phase 3-V P5 review P2 #2 反映: sentinel callback の null guard 仕様 verify
    remotionMock.__setStaticFiles([
      { name: 'narration/chunk_000.wav' },
      { name: 'narration/chunk_001.wav' },
      { name: 'narration.ready.json' },
    ]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('chunks');
    // sentinel 削除 event (null) → ready signal として扱わない (mode 不変期待)
    await act(async () => {
      remotionMock.__triggerWatch('narration.ready.json', null);
      await Promise.resolve();
    });
    // chunks file がまだ全部 staticFiles にあるので mode 維持
    expect(result.current.kind).toBe('chunks');
  });

  it('same metadata on legacy watcher → second trigger no-op (per-key dedup)', async () => {
    // Phase 3-V P5 review P2 #2 反映: lastModified:sizeInBytes per-key dedup verify
    remotionMock.__setStaticFiles([{ name: 'narration.wav' }]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('legacy');
    const meta = { lastModified: 12345, sizeInBytes: 678 };
    await act(async () => {
      remotionMock.__triggerWatch('narration.wav', meta);
      await Promise.resolve();
    });
    expect(result.current.kind).toBe('legacy');
    // 同一 metadata の 2 回目 trigger → dedup で no-op (mode 不変、再 invalidate 起きない)
    await act(async () => {
      remotionMock.__triggerWatch('narration.wav', meta);
      await Promise.resolve();
    });
    expect(result.current.kind).toBe('legacy');
    // 異なる metadata は再 evaluation 走る (signal change → 通過)
    remotionMock.__setStaticFiles([
      { name: 'narration.wav' },
      { name: 'narration/chunk_000.wav' },
      { name: 'narration/chunk_001.wav' },
    ]);
    await act(async () => {
      remotionMock.__triggerWatch('narration.wav', {
        lastModified: 99999,
        sizeInBytes: 1024,
      });
      await Promise.resolve();
    });
    expect(result.current.kind).toBe('chunks');
  });

  it('cross-file burst coalesced into 1 update (queueMicrotask batching)', async () => {
    // Phase 3-V P5 review P2 #1 反映: cross-file burst を 1 microtask に集約
    remotionMock.__setStaticFiles([]);
    const { result } = renderHook(() => useNarrationMode());
    expect(result.current.kind).toBe('none');
    // sentinel + legacy + 2 chunk の event を burst で発火
    await act(async () => {
      remotionMock.__setStaticFiles([
        { name: 'narration/chunk_000.wav' },
        { name: 'narration/chunk_001.wav' },
        { name: 'narration.wav' },
        { name: 'narration.ready.json' },
      ]);
      remotionMock.__triggerWatch('narration/chunk_000.wav');
      remotionMock.__triggerWatch('narration/chunk_001.wav');
      remotionMock.__triggerWatch('narration.wav');
      remotionMock.__triggerWatch('narration.ready.json');
      // microtask flush
      await Promise.resolve();
    });
    // burst 後の最終 mode は chunks (4 event でも 1 invalidate に集約されて到達)
    expect(result.current.kind).toBe('chunks');
  });
});
