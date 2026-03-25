import type { ImageSegment } from './types';
import { FPS } from '../videoConfig';

const toFrame = (seconds: number) => Math.round(seconds * FPS);

// ==== 挿入画像データ ====
// /supermovie-image-gen で自動生成されます
export const insertImageData: ImageSegment[] = [
  // 例: { id: 1, startFrame: toFrame(5), endFrame: toFrame(10), file: 'generated/example.png', type: 'infographic' },
];
