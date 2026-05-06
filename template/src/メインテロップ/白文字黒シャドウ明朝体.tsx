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

interface WhiteShadowProps {
  subtitleData: SubtitleData;
  fontSize?: number;
  fontColor?: string;
  bottomOffset?: number;
  fontFamily?: string;
}

export const WhiteShadow: React.FC<WhiteShadowProps> = ({
  subtitleData,
  fontSize = 100,
  fontColor = "white",
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
          color: fontColor,
          fontSize,
          fontFamily,
          fontWeight: 600,
          lineHeight: 1.3,
          textAlign: "center",
          textShadow: "0 0 5px rgba(0,0,0,1), 0 0 5px rgba(0,0,0,1), 0 0 10px rgba(0,0,0,1), 0 0 10px rgba(0,0,0,1), 0 0 15px rgba(0,0,0,1), 0 0 15px rgba(0,0,0,1), 0 0 22px rgba(0,0,0,1), 0 0 30px rgba(0,0,0,1), 0 0 40px rgba(0,0,0,1), 0 0 50px rgba(0,0,0,1), 0 0 62px rgba(0,0,0,1), 0 0 75px rgba(0,0,0,1), 0 0 90px rgba(0,0,0,1), 0 0 105px rgba(0,0,0,1), 0 0 120px rgba(0,0,0,1), 0 0 140px rgba(0,0,0,1), 0 0 160px rgba(0,0,0,0.9), 0 0 180px rgba(0,0,0,0.7), 0 0 200px rgba(0,0,0,0.4)",
        }}
      >
        {currentSubtitle.lines.map((line, i) => (
          <React.Fragment key={i}>
            {i > 0 && <br />}
            {line}
          </React.Fragment>
        ))}
      </div>
    </AbsoluteFill>
  );
};
