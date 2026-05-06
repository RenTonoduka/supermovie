import React from 'react';
import { Sequence } from 'remotion';
import { Slide } from './Slide';
import { slideData } from './slideData';

/**
 * Phase 3-A SlideSequence: slideData の各 SlideSegment を frame 範囲に従って描画.
 * ImageSequence と同型。MainVideo の <video> レイヤーの上に被せる想定。
 *
 * 現状 slideData は空配列 (placeholder)。supermovie-slides skill が将来生成する。
 */
export const SlideSequence: React.FC = () => {
  return (
    <>
      {slideData.map((segment) => (
        <Sequence
          key={segment.id}
          from={segment.startFrame}
          durationInFrames={segment.endFrame - segment.startFrame}
        >
          <Slide segment={segment} />
        </Sequence>
      ))}
    </>
  );
};
