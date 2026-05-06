import "./index.css";
import { Composition } from "remotion";
import { MainVideo } from "./MainVideo";
import { FPS, SOURCE_DURATION_FRAMES, RESOLUTION } from "./videoConfig";

// cut phase 完了後は cutData の CUT_TOTAL_FRAMES に切替: import { CUT_TOTAL_FRAMES } from "./cutData";
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MainVideo"
        component={MainVideo}
        durationInFrames={SOURCE_DURATION_FRAMES}
        fps={FPS}
        width={RESOLUTION.width}
        height={RESOLUTION.height}
      />
    </>
  );
};
