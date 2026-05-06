import type { ImageSegment } from './types';
import { FPS } from '../videoConfig';

/**
 * 秒を frame 番号に変換する helper。
 * 例コメント (insertImageData[] 内) で参照する想定で export し、
 * ユーザがデータ追加時にも import 経由で使える形にする
 * (export しないと tsc noUnusedLocals で error TS6133)。
 */
export const toFrame = (seconds: number) => Math.round(seconds * FPS);

// ==== 挿入画像データ ====
// /supermovie-image-gen で自動生成されます
export const insertImageData: ImageSegment[] = [
  // 例: { id: 1, startFrame: toFrame(5), endFrame: toFrame(10), file: 'generated/example.png', type: 'infographic' },
];
