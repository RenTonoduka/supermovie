import { AbsoluteFill, Video, getStaticFiles, staticFile } from 'remotion';
import { TelopPlayer } from './テロップテンプレート';
import { SESequence } from './SoundEffects/SESequence';
import { BGM } from './SoundEffects/BGM';
import { ImageSequence } from './InsertImage';
import { TitleSequence } from './Title';
import { SlideSequence } from './Slides';
import { NarrationAudio } from './Narration';
import { VIDEO_FILE } from './videoConfig';

const NARRATION_FILE = 'narration.wav';

export const MainVideo: React.FC = () => {
  // Phase 3-F asset gate と連動: narration.wav が存在すれば base 元音声を mute、
  // 不在なら 1.0 で再生 (二重音声防止)。getStaticFiles は public/ 配下を返す
  // Remotion 公式 API (https://www.remotion.dev/docs/get-static-files)。
  const hasNarration = getStaticFiles().some((f) => f.name === NARRATION_FILE);
  const baseVolume = hasNarration ? 0 : 1.0;

  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {/* ベース動画 (narration.wav 存在時は自動 mute) */}
      <Video
        src={staticFile(VIDEO_FILE)}
        volume={() => baseVolume}
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

      {/* ナレーション (Phase 3-F asset gate、narration.wav 不在で null) */}
      <NarrationAudio volume={1.0} />

      {/* BGM (Phase 3-F asset gate、bgm.mp3 不在で null) */}
      <BGM volume={0.08} />

      {/* 効果音 */}
      <SESequence />
    </AbsoluteFill>
  );
};
