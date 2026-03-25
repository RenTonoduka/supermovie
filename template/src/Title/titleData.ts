import type { TitleSegment } from './Title';

const FPS = 30;
const toFrame = (seconds: number) => Math.round(seconds * FPS);

// ==== タイトル（セグメント見出し）データ ====
export const titleData: TitleSegment[] = [
  // 例: { id: 1, startFrame: toFrame(0), endFrame: toFrame(15), text: 'イントロダクション' },
];
