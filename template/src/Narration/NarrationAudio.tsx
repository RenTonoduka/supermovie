import React from 'react';
import { Audio, getStaticFiles, staticFile } from 'remotion';

interface NarrationAudioProps {
  /** ファイル名 (public/ 配下、省略時 'narration.wav') */
  file?: string;
  volume?: number;
}

/**
 * Phase 3-D: VOICEVOX で生成した narration.wav を再生する layer.
 * Phase 3-F asset gate: public/narration.wav が無い時は null を返して render を
 * 失敗させない (BGM 同パターン)。
 *
 * これにより MainVideo.tsx で常時マウントしておいて、voicevox_narration.py が
 * 生成された後に自動で再生される。生成されていない時は静かに skip。
 *
 * volume はコールバック形式 ((frame) => volume) を使う。Remotion の lint が
 * 静的 number 値の volume を警告するため (https://www.remotion.dev/docs/audio/volume)。
 */
export const NarrationAudio: React.FC<NarrationAudioProps> = ({
  file = 'narration.wav',
  volume = 1.0,
}) => {
  const hasFile = getStaticFiles().some((f) => f.name === file);
  if (!hasFile) {
    return null;
  }
  return <Audio src={staticFile(file)} volume={() => volume} />;
};
