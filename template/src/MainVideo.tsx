import { AbsoluteFill, Video, staticFile } from 'remotion';
import { TelopPlayer } from './テロップテンプレート';
import { SESequence } from './SoundEffects/SESequence';
import { BGM } from './SoundEffects/BGM';
import { ImageSequence } from './InsertImage';
import { TitleSequence } from './Title';
import { SlideSequence } from './Slides';
import { NarrationAudio } from './Narration';
import { getNarrationMode } from './Narration/mode';
import { VIDEO_FILE } from './videoConfig';

export const MainVideo: React.FC = () => {
  // Phase 3-F asset gate + Phase 3-H per-segment Sequence の mode helper を共有
  // (Codex Phase 3-H review P1 #1 反映)。chunks / legacy / none のいずれでも
  // narration が「鳴る」状態なら base 元音声を mute、'none' なら 1.0 で再生する。
  // これで NarrationAudio と判定が一致し、無音バグ (chunk 不足 + legacy 存在で
  // 両方消える) を防ぐ。
  // 注意: Studio 起動後に narration を生成した場合、Studio reload (Cmd+R / `r` キー)
  // で getStaticFiles cache を再生成する必要がある
  // (https://www.remotion.dev/docs/getstaticfiles)。
  const narrationMode = getNarrationMode();
  const baseVolume = narrationMode.kind === 'none' ? 1.0 : 0;

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
