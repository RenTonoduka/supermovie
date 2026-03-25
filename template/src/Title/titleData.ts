import type { TitleSegment } from './Title';
import { FPS } from '../videoConfig';

const toFrame = (seconds: number) => Math.round(seconds * FPS);

// ==== タイトル（セグメント見出し）データ ====
// /supermovie-subtitles で自動生成されます
export const titleData: TitleSegment[] = [
  // 例: { id: 1, startFrame: toFrame(0), endFrame: toFrame(15), text: 'イントロダクション' },
];
