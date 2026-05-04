import React from 'react';
import { Audio, staticFile } from 'remotion';

interface NarrationAudioProps {
  /** ファイル名 (public/ 配下、省略時 'narration.wav') */
  file?: string;
  volume?: number;
}

/**
 * Phase 3-D: VOICEVOX で生成した narration.wav を再生する layer.
 *
 * 重要: `public/narration.wav` が存在する場合のみ MainVideo.tsx で有効化する。
 * 不在時に <Audio src=...> を render すると Remotion がエラーで停止するため、
 * MainVideo 側でコメントアウト保持 → voicevox_narration.py 走行後に有効化、
 * という運用にする (BGM 同パターン)。
 *
 * volume はコールバック形式 ((frame) => volume) を使う。Remotion の lint が
 * 静的 number 値の volume を警告するため (https://www.remotion.dev/docs/audio/volume)。
 */
export const NarrationAudio: React.FC<NarrationAudioProps> = ({
  file = 'narration.wav',
  volume = 1.0,
}) => {
  return <Audio src={staticFile(file)} volume={() => volume} />;
};
