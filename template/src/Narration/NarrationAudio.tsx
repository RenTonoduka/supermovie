import React from 'react';
import { Audio, staticFile } from 'remotion';

interface NarrationAudioProps {
  /** ファイル名 (public/ 配下、省略時 'narration.wav') */
  file?: string;
  volume?: number;
}

/**
 * Phase 3-D: VOICEVOX で生成した narration.wav を再生する layer.
 * `public/narration.wav` が存在する想定。voicevox_narration.py で engine 不在時は
 * 生成されず、代わりに base video の元音声 (Video volume=1.0) が維持される。
 *
 * 呼び出し側 (MainVideo.tsx) は narration.wav の有無に関わらずこの component を
 * 配置できるが、ファイル不在で render が失敗するため、有無を build script から
 * project-config.json などに記録するか、render 前に存在確認するのが安全.
 */
export const NarrationAudio: React.FC<NarrationAudioProps> = ({
  file = 'narration.wav',
  volume = 1.0,
}) => {
  return <Audio src={staticFile(file)} volume={volume} />;
};
