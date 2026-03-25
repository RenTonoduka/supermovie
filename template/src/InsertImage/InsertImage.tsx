import React from 'react';
import { useCurrentFrame, interpolate, Img, staticFile } from 'remotion';
import type { ImageSegment } from './types';

interface InsertImageProps {
  segment: ImageSegment;
}

export const InsertImage: React.FC<InsertImageProps> = ({ segment }) => {
  const frame = useCurrentFrame();
  const duration = segment.endFrame - segment.startFrame;
  const localFrame = frame - segment.startFrame;

  const opacity = interpolate(
    localFrame,
    [0, 8, duration - 8, duration],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const scale = segment.type === 'photo'
    ? interpolate(localFrame, [0, duration], [1.0, 1.05], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 1;

  if (segment.type === 'overlay') {
    return (
      <div
        style={{
          position: 'absolute',
          top: 0, left: 0, width: '100%', height: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          opacity,
          zIndex: 50,
        }}
      >
        <Img
          src={staticFile(`images/${segment.file}`)}
          style={{
            maxWidth: '80%',
            maxHeight: '80%',
            objectFit: 'contain',
            transform: `scale(${segment.scale ?? 1})`,
          }}
        />
      </div>
    );
  }

  return (
    <div
      style={{
        position: 'absolute',
        top: 0, left: 0, width: '100%', height: '100%',
        opacity,
        zIndex: 50,
      }}
    >
      <Img
        src={staticFile(`images/${segment.file}`)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: segment.type === 'infographic' ? 'contain' : 'cover',
          transform: `scale(${scale * (segment.scale ?? 1)})`,
        }}
      />
    </div>
  );
};
