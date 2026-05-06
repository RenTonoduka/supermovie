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

interface WhitePurpleShadowProps {
  subtitleData: SubtitleData;
  fontSize?: number;
  fontColor?: string;
  strokeColor?: string;
  strokeWidth?: number;
  bottomOffset?: number;
  fontFamily?: string;
}

export const WhitePurpleShadow: React.FC<WhitePurpleShadowProps> = ({
  subtitleData,
  fontSize = 100,
  fontColor = "white",
  strokeColor = "#6A0DAD",
  strokeWidth = 12,
  bottomOffset = 80,
  fontFamily = "'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif JP', serif",
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
              drop-shadow(0 0 10px rgba(106,13,173,1))
              drop-shadow(0 0 20px rgba(106,13,173,0.8))
              drop-shadow(0 0 35px rgba(106,13,173,0.5))
            `,
          }}
        >
          <text
            x={svgWidth / 2}
            textAnchor="middle"
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeLinejoin="round"
            strokeLinecap="round"
            fill={fontColor}
            paintOrder="stroke fill"
            style={{
              fontSize,
              fontFamily,
              fontWeight: 600,
            }}
          >
            {currentSubtitle.lines.map((line, i) => (
              <tspan
                key={i}
                x={svgWidth / 2}
                y={fontSize + i * lineHeightPx}
              >
                {line}
              </tspan>
            ))}
          </text>
        </svg>
      </div>
    </AbsoluteFill>
  );
};
