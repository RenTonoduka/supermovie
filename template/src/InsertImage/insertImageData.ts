import type { ImageSegment } from './types';

const FPS = 30;
const toFrame = (seconds: number) => Math.round(seconds * FPS);

// ==== 挿入画像データ ====
// 画像ファイルは public/images/ に配置
export const insertImageData: ImageSegment[] = [
  // 例: { id: 1, startFrame: toFrame(5), endFrame: toFrame(10), file: 'example.png', type: 'infographic' },
];
