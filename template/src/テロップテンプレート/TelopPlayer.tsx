import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { Telop } from './Telop';
import { telopData } from './telopData';

export const TelopPlayer: React.FC = () => {
  const frame = useCurrentFrame();

  const current = telopData.find(
    (s) => frame >= s.startFrame && frame < s.endFrame
  );

  return (
    <AbsoluteFill>
      {current && <Telop segment={current} />}
    </AbsoluteFill>
  );
};
