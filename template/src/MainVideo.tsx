import { AbsoluteFill, Video, staticFile } from 'remotion';
import { TelopPlayer } from './テロップテンプレート';
import { SESequence } from './SoundEffects/SESequence';
import { BGM } from './SoundEffects/BGM';
import { ImageSequence } from './InsertImage';
import { TitleSequence } from './Title';
import { SlideSequence } from './Slides';
import { VIDEO_FILE } from './videoConfig';

export const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {/* ベース動画 */}
      <Video
        src={staticFile(VIDEO_FILE)}
        volume={1.0}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'contain',
        }}
      />

      {/* スライド (Phase 3-A、別レイヤーで動画の上に被せる) */}
      <SlideSequence />

      {/* 挿入画像 */}
      <ImageSequence />

      {/* テロップ */}
      <TelopPlayer />

      {/* タイトル */}
      <TitleSequence />

      {/* BGM */}
      <BGM volume={0.08} />

      {/* 効果音 */}
      <SESequence />
    </AbsoluteFill>
  );
};
