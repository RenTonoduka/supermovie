import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  Easing,
} from "remotion";

// 字幕データの型定義
export interface SubtitleItem {
  text: string;
  lines: string[];
  start: number;
  end: number;
  startFrame: number;
  endFrame: number;
}

export interface SubtitleData {
  fps: number;
  subtitles: SubtitleItem[];
}

interface BlueGoldProps {
  subtitleData: SubtitleData;
  fontSize?: number;
  strokeColor?: string;
  strokeWidth?: number;
  bottomOffset?: number;
  fontFamily?: string;
}

export const BlueGold: React.FC<BlueGoldProps> = ({
  subtitleData,
  fontSize = 85,
  strokeColor = "#F5E6A3",
  strokeWidth = 12,
  bottomOffset = 80,
  fontFamily = "'Noto Sans JP', sans-serif",
}) => {
  const frame = useCurrentFrame();

  // 現在のフレームに対応する字幕を検索
  const currentSubtitle = subtitleData.subtitles.find(
    (sub) => frame >= sub.startFrame && frame <= sub.endFrame
  );

  if (!currentSubtitle) {
    return null;
  }

  // テロップの表示時間
  const duration = currentSubtitle.endFrame - currentSubtitle.startFrame;

  // フェードイン/アウトアニメーション
  const maxFadeDuration = Math.floor(duration / 3);
  const fadeInDuration = Math.min(3, maxFadeDuration);
  const fadeOutDuration = Math.min(3, maxFadeDuration);

  let opacity = 1;

  if (duration > 6) {
    const fadeInEnd = currentSubtitle.startFrame + fadeInDuration;
    const fadeOutStart = currentSubtitle.endFrame - fadeOutDuration;

    if (fadeInEnd < fadeOutStart) {
      opacity = interpolate(
        frame,
        [currentSubtitle.startFrame, fadeInEnd, fadeOutStart, currentSubtitle.endFrame],
        [0, 1, 1, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
      );
    } else {
      const midPoint = (currentSubtitle.startFrame + currentSubtitle.endFrame) / 2;
      opacity = interpolate(
        frame,
        [currentSubtitle.startFrame, midPoint, currentSubtitle.endFrame],
        [0, 1, 0],
        { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
      );
    }
  }

  // スケールアニメーション
  const scale = fadeInDuration > 0 ? interpolate(
    frame,
    [currentSubtitle.startFrame, currentSubtitle.startFrame + fadeInDuration],
    [0.95, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }
  ) : 1;

  // SVGサイズ計算
  const lineHeightPx = fontSize * 1.3;
  const svgHeight = currentSubtitle.lines.length * lineHeightPx;
  const maxLineLength = Math.max(...currentSubtitle.lines.map(line => line.length));
  const svgWidth = maxLineLength * fontSize + 60;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: bottomOffset,
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
        }}
      >
        <svg
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          width={svgWidth}
          height={svgHeight}
          style={{
            display: "block",
            overflow: "visible",
            filter: `
              drop-shadow(2px 3px 0 rgba(0,0,0,0.8))
              drop-shadow(4px 6px 0 #9A8448)
              drop-shadow(0 0 15px rgba(255,255,255,0.9))
              drop-shadow(0 0 25px rgba(255,255,255,0.6))
            `,
          }}
        >
          <defs>
            <linearGradient
              id="blueGoldVerticalGrad"
              gradientUnits="objectBoundingBox"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >
              <stop offset="0%" stopColor="#0033AA" />
              <stop offset="50%" stopColor="#0088FF" />
              <stop offset="100%" stopColor="#0033AA" />
            </linearGradient>
          </defs>
          {currentSubtitle.lines.map((line, i) => (
            <text
              key={i}
              x={svgWidth / 2}
              y={fontSize + i * lineHeightPx}
              textAnchor="middle"
              stroke={strokeColor}
              strokeWidth={strokeWidth}
              strokeLinejoin="round"
              strokeLinecap="round"
              fill="url(#blueGoldVerticalGrad)"
              paintOrder="stroke fill"
              style={{
                fontSize,
                fontFamily,
                fontWeight: 900,
              }}
            >
              {line}
            </text>
          ))}
        </svg>
      </div>
    </AbsoluteFill>
  );
};
