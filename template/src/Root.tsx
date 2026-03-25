import "./index.css";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";

// ==== ここを編集 ====
// /supermovie-init が自動設定します
const VIDEO_DURATION_FRAMES = 1500; // placeholder
const FPS = 30;
const VIDEO_FILE = 'main.mp4';
// ====================

export const VIDEO_CONFIG = {
  durationInFrames: VIDEO_DURATION_FRAMES,
  fps: FPS,
  videoFile: VIDEO_FILE,
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MainVideo"
        component={MainVideo}
        durationInFrames={VIDEO_DURATION_FRAMES}
        fps={FPS}
        width={1920}
        height={1080}
      />
    </>
  );
};
