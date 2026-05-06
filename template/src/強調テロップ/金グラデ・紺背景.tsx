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

interface GoldGradNavyBgProps {
  subtitleData: SubtitleData;
  fontSize?: number;
  bgColor?: string;
  gradientFrom?: string;
  gradientMiddle?: string;
  gradientTo?: string;
  bottomOffset?: number;
  fontFamily?: string;
}

export const GoldGradNavyBg: React.FC<GoldGradNavyBgProps> = ({
  subtitleData,
  fontSize = 90,
  bgColor = "#1a1f4e",
  gradientFrom = "#B8A472",
  gradientMiddle = "#E8DCC0",
  gradientTo = "#B8A472",
  bottomOffset = 80,
  fontFamily = "'Noto Serif JP', 'Hiragino Mincho ProN', 'Yu Mincho', serif",
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
          padding: "12px 28px",
          fontSize,
          fontFamily,
          fontWeight: 900,
          lineHeight: 1.3,
          textAlign: "center",
        }}
      >
        <span
          style={{
            background: `linear-gradient(180deg, ${gradientFrom} 0%, ${gradientMiddle} 50%, ${gradientTo} 100%)`,
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            backgroundClip: "text",
          }}
        >
          {currentSubtitle.lines.map((line, i) => (
            <React.Fragment key={i}>
              {i > 0 && <br />}
              {line}
            </React.Fragment>
          ))}
        </span>
      </div>
    </AbsoluteFill>
  );
};
