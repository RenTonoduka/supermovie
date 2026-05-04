import type { TitleSegment } from './Title';
import { FPS } from '../videoConfig';

/**
 * 秒を frame 番号に変換する helper。
 * 例コメント (titleData[] 内) で参照する想定で export し、
 * ユーザがデータ追加時にも import 経由で使える形にする
 * (export しないと tsc noUnusedLocals で error TS6133)。
 */
export const toFrame = (seconds: number) => Math.round(seconds * FPS);

// ==== タイトル（セグメント見出し）データ ====
// /supermovie-subtitles で自動生成されます
export const titleData: TitleSegment[] = [
  // 例: { id: 1, startFrame: toFrame(0), endFrame: toFrame(15), text: 'イントロダクション' },
];
