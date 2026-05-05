import { useEffect, useRef, useState } from 'react';
import { watchStaticFile } from 'remotion';
import { narrationData } from './narrationData';
import {
  NARRATION_LEGACY_FILE,
  NARRATION_READY_FILE,
  type NarrationMode,
  getNarrationMode,
  invalidateNarrationMode,
} from './mode';

/**
 * Phase 3-N (Codex Phase 3-M consultation 推奨 ii): Studio hot-reload 用の
 * React hook。voicevox_narration.py 実行で `narrationData.ts` / chunk wav /
 * narration.wav が更新された時、Studio で Cmd+R (reload) なしに UI を
 * 再評価する。
 *
 * 動作:
 *   1) 初回 render 時 `getNarrationMode()` で current mode を取得
 *   2) `watchStaticFile` で sentinel (Phase 3-V P5: `narration.ready.json`)、
 *      legacy `narration.wav`、narrationData 内の各 chunk file を監視
 *      (Remotion 公式 API、Studio 限定で発火、Player / render は no-op、出典:
 *      https://www.remotion.dev/docs/watchstaticfile)
 *   3) 任意の watch event で `invalidateNarrationMode()` + setMode で
 *      React tree を再評価
 *   4) cleanup で全 watch を cancel (memory leak 防止)
 *
 * Phase 3-V post-freeze P5 (Codex CODEX_P5_VOICEVOX_SENTINEL_DESIGN §2):
 * sentinel watcher を追加。watcher 数は 1 (sentinel) + 1 (legacy) + chunkCount
 * になる。dedup は 2 層:
 *   (a) sentinel callback は `StaticFile === null` (削除 event) を ready signal
 *       として扱わない (publish 完了の signal は file 出現 / 内容更新のみ)
 *   (b) `lastModified:sizeInBytes` を `useRef` Map に保持し、同一 signal key の
 *       重複 callback は no-op (Codex 設計 §2)
 * Map は per-key で保持するため、複数 file の event は独立に dedup される。
 *
 * Render path との互換性: `watchStaticFile` は render context で no-op の
 * 設計なので、本 hook を全 path で使っても render が壊れない。
 * mode helper の memo は Player / render では maintain される (毎 frame
 * 再構築のコストを回避)、Studio では invalidate で fresh 反映。
 *
 * 注意: `narrationData` は build-time 静的 data。途中で `narrationData.ts`
 * 自体が書き換わった場合は Vite/HMR が module を再評価し、本 hook も
 * 自然に新しい segments を見るが、Studio が module reload を発火するかは
 * Remotion 内部実装に依存。確実な反映が欲しい場合は Studio reload
 * (Cmd+R) が安全。P5 sentinel は public asset 完了 signal の厳密化であり、
 * `narrationData.ts` の HMR 完全独立化ではない (Codex 設計 §2 caveat)。
 */
type StaticFileMeta =
  | { lastModified?: number; sizeInBytes?: number }
  | null
  | undefined;

export const useNarrationMode = (): NarrationMode => {
  const [mode, setMode] = useState<NarrationMode>(() => getNarrationMode());
  const lastSignalRef = useRef<Map<string, string>>(new Map());
  const pendingRef = useRef<boolean>(false);

  useEffect(() => {
    const cancels: Array<() => void> = [];
    const dedupSignal = lastSignalRef.current;

    // Codex P5 review P2 #1 反映: cross-file burst coalescing
    // (sentinel + legacy + chunks の event が近接した時、各 callback で個別に
    // invalidate + setMode するのではなく queueMicrotask で 1 回に集約)。
    const scheduleUpdate = () => {
      if (pendingRef.current) {
        return;
      }
      pendingRef.current = true;
      queueMicrotask(() => {
        pendingRef.current = false;
        invalidateNarrationMode();
        setMode(getNarrationMode());
      });
    };

    const makeUpdate =
      (key: string, isSentinel: boolean) => (file?: StaticFileMeta) => {
        // Sentinel-specific: 削除 event (StaticFile === null) は ready signal にしない
        // (publish 完了 signal は file 出現 / 内容更新のみで意味を持つ、Codex 設計 §2)
        if (isSentinel && file === null) {
          return;
        }
        // file metadata が取れる場合のみ per-key dedup engage
        // (test mock など callback が arg なしで呼ぶ context は always update)
        if (
          file &&
          (file.lastModified !== undefined || file.sizeInBytes !== undefined)
        ) {
          const signal = `${file.lastModified ?? 'na'}:${file.sizeInBytes ?? 'na'}`;
          if (dedupSignal.get(key) === signal) {
            return;
          }
          dedupSignal.set(key, signal);
        }
        scheduleUpdate();
      };

    // sentinel watcher (Phase 3-V P5: narration.ready.json publish 完了 signal)
    try {
      const watchReady = watchStaticFile(
        NARRATION_READY_FILE,
        makeUpdate(NARRATION_READY_FILE, true),
      );
      if (watchReady && typeof watchReady.cancel === 'function') {
        cancels.push(watchReady.cancel);
      }
    } catch {
      // Player / render context など watchStaticFile が動かない場合は no-op
    }

    // legacy narration.wav の変更監視
    try {
      const watchLegacy = watchStaticFile(
        NARRATION_LEGACY_FILE,
        makeUpdate(NARRATION_LEGACY_FILE, false),
      );
      if (watchLegacy && typeof watchLegacy.cancel === 'function') {
        cancels.push(watchLegacy.cancel);
      }
    } catch {
      // 同上
    }

    // chunk wav の変更監視 (narrationData 内 file 全部)
    for (const seg of narrationData) {
      try {
        const watchChunk = watchStaticFile(
          seg.file,
          makeUpdate(seg.file, false),
        );
        if (watchChunk && typeof watchChunk.cancel === 'function') {
          cancels.push(watchChunk.cancel);
        }
      } catch {
        // 同上
      }
    }

    return () => {
      for (const cancel of cancels) {
        try {
          cancel();
        } catch {
          // cleanup 中の例外は飲む (cancel 戻り値仕様揺れ吸収)
        }
      }
    };
  }, []);

  return mode;
};
