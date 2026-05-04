import { useEffect, useState } from 'react';
import { watchStaticFile } from 'remotion';
import { narrationData } from './narrationData';
import {
  NARRATION_LEGACY_FILE,
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
 *   2) `watchStaticFile` で narration.wav と narrationData 内の各 chunk file
 *      を監視 (Remotion 公式 API、Studio 限定で発火、Player / render は
 *      no-op、出典: https://www.remotion.dev/docs/watchstaticfile)
 *   3) 任意の watch event で `invalidateNarrationMode()` + setMode で
 *      React tree を再評価
 *   4) cleanup で全 watch を cancel (memory leak 防止)
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
 * (Cmd+R) が安全。
 */
export const useNarrationMode = (): NarrationMode => {
  const [mode, setMode] = useState<NarrationMode>(() => getNarrationMode());

  useEffect(() => {
    const cancels: Array<() => void> = [];
    const updateMode = () => {
      invalidateNarrationMode();
      setMode(getNarrationMode());
    };

    // legacy narration.wav の変更監視
    try {
      const watchLegacy = watchStaticFile(NARRATION_LEGACY_FILE, updateMode);
      if (watchLegacy && typeof watchLegacy.cancel === 'function') {
        cancels.push(watchLegacy.cancel);
      }
    } catch {
      // Player / render context など watchStaticFile が動かない場合は no-op
    }

    // chunk wav の変更監視 (narrationData 内 file 全部)
    for (const seg of narrationData) {
      try {
        const watchChunk = watchStaticFile(seg.file, updateMode);
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
