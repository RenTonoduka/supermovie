import React from 'react';
import { Audio, Sequence, staticFile } from 'remotion';
import { useNarrationMode } from './useNarrationMode';

interface NarrationAudioProps {
  volume?: number;
}

/**
 * Phase 3-H: getNarrationMode() で chunks / legacy / none の三経路を分岐。
 * MainVideo の hasNarration 判定とロジック共有 (Codex P1 #1 反映)。
 * Phase 3-N: useNarrationMode() hook 経由 (Studio hot-reload 対応、
 * Player / render では従来通りの pure 動作にフォールバック)。
 *
 * volume はコールバック形式 (Remotion lint 警告回避、
 * https://www.remotion.dev/docs/audio/volume)。
 */
export const NarrationAudio: React.FC<NarrationAudioProps> = ({ volume = 1.0 }) => {
  const mode = useNarrationMode();

  if (mode.kind === 'chunks') {
    return (
      <>
        {mode.segments.map((seg) => (
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

  if (mode.kind === 'legacy') {
    return <Audio src={staticFile(mode.file)} volume={() => volume} />;
  }

  return null;
};
