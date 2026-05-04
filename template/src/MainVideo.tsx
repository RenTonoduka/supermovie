import { AbsoluteFill, Video, getStaticFiles, staticFile } from 'remotion';
import { TelopPlayer } from './テロップテンプレート';
import { SESequence } from './SoundEffects/SESequence';
import { BGM } from './SoundEffects/BGM';
import { ImageSequence } from './InsertImage';
import { TitleSequence } from './Title';
import { SlideSequence } from './Slides';
import { NarrationAudio, narrationData } from './Narration';
import { VIDEO_FILE } from './videoConfig';

const NARRATION_FILE = 'narration.wav';
const NARRATION_CHUNK_PREFIX = 'narration/chunk_';

export const MainVideo: React.FC = () => {
  // Phase 3-F asset gate + Phase 3-H per-segment Sequence と連動:
  // - legacy: public/narration.wav 存在 → base mute
  // - phase3h: narrationData non-empty + chunk wav 存在 → base mute
  // どちらも不在なら base 元音声 1.0 で再生。getStaticFiles は Studio/render 時に
  // public/ 配下の asset 一覧を返す Remotion 公式 API
  // (https://www.remotion.dev/docs/getstaticfiles)。
  // 注意: Studio 起動後に narration を生成した場合、Studio リロード
  // (Cmd+R / `r` キー) で反映する。新規 asset 追加に watchStaticFile を使う選択肢
  // もあるが、現状は単純化のため reload 方式を採用。
  const staticFiles = getStaticFiles();
  const hasLegacyNarration = staticFiles.some((f) => f.name === NARRATION_FILE);
  const hasChunkNarration =
    narrationData.length > 0 &&
    narrationData.every((seg) =>
      staticFiles.some((f) => f.name === seg.file),
    ) &&
    staticFiles.some((f) => f.name.startsWith(NARRATION_CHUNK_PREFIX));
  const hasNarration = hasLegacyNarration || hasChunkNarration;
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
