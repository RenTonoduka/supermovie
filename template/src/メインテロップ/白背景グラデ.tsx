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

interface WhiteBgGradTextProps {
  subtitleData: SubtitleData;
  fontSize?: number;
  gradientColorFrom?: string;
  gradientColorTo?: string;
  bgColor?: string;
  bgOpacity?: number;
  bottomOffset?: number;
  fontFamily?: string;
}

export const WhiteBgGradText: React.FC<WhiteBgGradTextProps> = ({
  subtitleData,
  fontSize = 80,
  gradientColorFrom = "#d926e8",
  gradientColorTo = "#0c43e8",
  bgColor = "rgba(255, 255, 255, 0.7)",
  bottomOffset = 80,
  fontFamily = "'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif",
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
  const svgWidth = maxLineLength * fontSize + 40;

  // 45°グラデーション座標計算
  const halfDiag = (svgWidth + svgHeight) / 4;
  const cx = svgWidth / 2;
  const cy = svgHeight / 2;

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
          backgroundColor: bgColor,
          padding: "6px 12px",
          display: "inline-block",
        }}
      >
        <svg
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          width={svgWidth}
          height={svgHeight}
          style={{
            display: "block",
            overflow: "visible",
            filter: "drop-shadow(2px 2px 4px rgba(0,0,0,0.3))",
          }}
        >
          <defs>
            <linearGradient
              id="whiteBgGradTextGrad"
              gradientUnits="userSpaceOnUse"
              x1={cx - halfDiag}
              y1={cy + halfDiag}
              x2={cx + halfDiag}
              y2={cy - halfDiag}
            >
              <stop offset="0%" stopColor={gradientColorFrom} />
              <stop offset="100%" stopColor={gradientColorTo} />
            </linearGradient>
          </defs>
          <text
            x={svgWidth / 2}
            textAnchor="middle"
            fill="url(#whiteBgGradTextGrad)"
            style={{
              fontSize,
              fontFamily,
              fontWeight: 900,
              fontStyle: "italic",
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
