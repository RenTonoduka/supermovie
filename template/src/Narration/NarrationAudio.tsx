import React from 'react';
import { Audio, Sequence, getStaticFiles, staticFile } from 'remotion';
import { narrationData } from './narrationData';

interface NarrationAudioProps {
  /** legacy 単一ファイル名 (public/ 配下、省略時 'narration.wav') */
  file?: string;
  volume?: number;
}

/**
 * Phase 3-H: per-segment narration timeline (voicevox_narration.py が
 * narrationData.ts を生成する経路)。
 *
 * 動作優先順位:
 *   1) narrationData が non-empty かつ 全 chunk file が public/ に存在
 *      → 各 chunk を <Sequence from={startFrame} durationInFrames={...}>
 *        + <Audio /> でループ再生 (https://www.remotion.dev/docs/sequence)
 *   2) narrationData が空 + public/narration.wav 存在
 *      → legacy 単一 wav (Phase 3-D 互換、deterministic test 用)
 *   3) どちらも不在 → null (asset gate、Phase 3-F 互換)
 *
 * MainVideo.tsx の hasNarration 判定 (base mute 切替) と整合させること:
 * narrationData.length > 0 || public/narration.wav 存在 のどちらかで mute。
 *
 * volume はコールバック形式 ((frame) => volume) で Remotion lint 警告を回避
 * (https://www.remotion.dev/docs/audio/volume)。
 */
export const NarrationAudio: React.FC<NarrationAudioProps> = ({
  file = 'narration.wav',
  volume = 1.0,
}) => {
  const staticFiles = getStaticFiles();

  if (narrationData.length > 0) {
    const allChunksExist = narrationData.every((seg) =>
      staticFiles.some((f) => f.name === seg.file),
    );
    if (!allChunksExist) {
      return null;
    }
    return (
      <>
        {narrationData.map((seg) => (
          <Sequence
            key={seg.id}
            from={seg.startFrame}
            durationInFrames={seg.durationInFrames}
          >
            <Audio src={staticFile(seg.file)} volume={() => volume} />
          </Sequence>
        ))}
      </>
    );
  }

  const hasFile = staticFiles.some((f) => f.name === file);
  if (!hasFile) {
    return null;
  }
  return <Audio src={staticFile(file)} volume={() => volume} />;
};
