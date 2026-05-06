import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import type { SlideSegment } from './types';

interface SlideProps {
  segment: SlideSegment;
}

export const Slide: React.FC<SlideProps> = ({ segment }) => {
  const frame = useCurrentFrame();
  // segment 内 local frame: Sequence 子要素は 0 基準 (Remotion 仕様)。
  // SlideSequence が <Sequence from={startFrame}> でラップするので
  // ここでは frame そのものを使う。
  const duration = segment.endFrame - segment.startFrame;

  const opacity = interpolate(
    frame,
    [0, 12, duration - 12, duration],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' },
  );

  const align = segment.align ?? 'center';
  const bg = segment.backgroundColor ?? 'rgba(20, 26, 44, 0.92)';
  const fg = segment.textColor ?? '#ffffff';

  const justify = align === 'center' ? 'center' : 'flex-start';
  const textAlign = align === 'center' ? ('center' as const) : ('left' as const);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bg,
        opacity,
        display: 'flex',
        alignItems: 'center',
        justifyContent: justify,
        padding: '8% 6%',
        boxSizing: 'border-box',
      }}
    >
      <div style={{ color: fg, textAlign, maxWidth: '90%' }}>
        <h1
          style={{
            fontSize: 96,
            fontWeight: 800,
            lineHeight: 1.2,
            margin: 0,
            letterSpacing: '0.02em',
          }}
        >
          {segment.title}
        </h1>
        {segment.subtitle && (
          <p style={{ fontSize: 44, opacity: 0.8, marginTop: 24 }}>{segment.subtitle}</p>
        )}
        {segment.bullets && segment.bullets.length > 0 && (
          <ul
            style={{
              marginTop: 48,
              paddingLeft: align === 'left' ? 32 : 0,
              listStyle: align === 'left' ? 'disc' : 'none',
              fontSize: 52,
              lineHeight: 1.5,
            }}
          >
            {segment.bullets.map((b, i) => (
              <li
                key={i}
                style={{
                  color: b.emphasis ? '#ffd166' : fg,
                  fontWeight: b.emphasis ? 700 : 500,
                  marginBottom: 12,
                }}
              >
                {b.text}
              </li>
            ))}
          </ul>
        )}
      </div>
    </AbsoluteFill>
  );
};
