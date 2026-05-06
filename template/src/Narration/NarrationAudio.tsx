import React from 'react';
import { Audio, Sequence, staticFile } from 'remotion';
import { useNarrationMode } from './useNarrationMode';
import type { NarrationMode } from './mode';

interface NarrationAudioProps {
  volume?: number;
}

interface NarrationAudioWithModeProps {
  volume?: number;
  mode: NarrationMode;
}

/**
 * Phase 3-V (Codex CODEX_REVIEW_PHASE3U_AND_3V 推奨): mode を prop で受ける
 * pure component。MainVideo 側で `useNarrationMode()` を 1 回呼んで両方に
 * mode を流す経路で watcher 二重登録を解消する。
 *
 * Render only、hook 呼出なし。`useNarrationMode` を持つ component から
 * mode を受け取り、chunks / legacy / none で表示分岐するだけ。
 */
export const NarrationAudioWithMode: React.FC<NarrationAudioWithModeProps> = ({
  volume = 1.0,
  mode,
}) => {
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

/**
 * Phase 3-H: getNarrationMode() で chunks / legacy / none の三経路を分岐。
 * MainVideo の hasNarration 判定とロジック共有 (Codex P1 #1 反映)。
 * Phase 3-N: useNarrationMode() hook 経由 (Studio hot-reload 対応、
 * Player / render では従来通りの pure 動作にフォールバック)。
 * Phase 3-V: hook 呼出を内部に保持しつつ pure 部分は NarrationAudioWithMode に
 * 分離。MainVideo 側で mode 共有する構成では `NarrationAudioWithMode` を使う。
 *
 * volume はコールバック形式 (Remotion lint 警告回避、
 * https://www.remotion.dev/docs/audio/volume)。
 */
export const NarrationAudio: React.FC<NarrationAudioProps> = ({
  volume = 1.0,
}) => {
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
