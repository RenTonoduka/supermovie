import { Audio, getStaticFiles, staticFile } from 'remotion';

interface BGMProps {
  volume?: number;
}

const BGM_FILE = 'BGM/bgm.mp3';

/**
 * Phase 3-F asset gate: public/BGM/bgm.mp3 が無い時は null を返して render を
 * 失敗させない。getStaticFiles() は public/ 以下の asset 一覧を返す Remotion 公式 API
 * (https://www.remotion.dev/docs/get-static-files)。
 */
export const BGM: React.FC<BGMProps> = ({ volume = 0.3 }) => {
  const hasFile = getStaticFiles().some((f) => f.name === BGM_FILE);
  if (!hasFile) {
    return null;
  }
  return <Audio src={staticFile(BGM_FILE)} volume={() => volume} loop />;
};
