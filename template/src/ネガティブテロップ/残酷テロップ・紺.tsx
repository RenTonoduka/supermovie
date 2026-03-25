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

interface NavyBlueRiitegakiProps {
  subtitleData: SubtitleData;
  fontSize?: number;
  bottomOffset?: number;
  fontFamily?: string;
}

export const NavyBlueRiitegaki: React.FC<NavyBlueRiitegakiProps> = ({
  subtitleData,
  fontSize = 110,
  bottomOffset = 80,
  fontFamily = "'りいてがき筆', cursive",
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
  const svgWidth = maxLineLength * fontSize + 80;

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
              drop-shadow(0 0 8px rgba(0,0,0,0.4))
              drop-shadow(0 0 15px rgba(0,0,0,0.2))
            `,
          }}
        >
          {currentSubtitle.lines.map((line, i) => (
            <React.Fragment key={i}>
              {/* 外側縁取り：濃い青 */}
              <text
                x={svgWidth / 2}
                y={fontSize + i * lineHeightPx}
                textAnchor="middle"
                stroke="#1e3a5f"
                strokeWidth={32}
                strokeLinejoin="round"
                strokeLinecap="round"
                fill="none"
                style={{
                  fontSize,
                  fontFamily,
                  fontWeight: 400,
                }}
              >
                {line}
              </text>
              {/* 内側縁取り：白 + 濃い紺色塗り */}
              <text
                x={svgWidth / 2}
                y={fontSize + i * lineHeightPx}
                textAnchor="middle"
                stroke="white"
                strokeWidth={15}
                strokeLinejoin="round"
                strokeLinecap="round"
                fill="#1a237e"
                paintOrder="stroke fill"
                style={{
                  fontSize,
                  fontFamily,
                  fontWeight: 400,
                }}
              >
                {line}
              </text>
            </React.Fragment>
          ))}
        </svg>
      </div>
    </AbsoluteFill>
  );
};
