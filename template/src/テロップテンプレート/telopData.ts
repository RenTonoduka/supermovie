import type { TelopSegment } from './telopTypes';
import { FPS as CONFIG_FPS, SOURCE_DURATION_FRAMES } from '../videoConfig';

// ===== テロップデータ =====
// /supermovie-subtitles で自動生成されます
// cut phase 完了後、TOTAL_FRAMES は cutData.CUT_TOTAL_FRAMES に切り替えること

export const FPS = CONFIG_FPS;
export const TOTAL_FRAMES = SOURCE_DURATION_FRAMES;

export const telopData: TelopSegment[] = [
  // サンプル:
  // {
  //   id: 1,
  //   startFrame: 0,
  //   endFrame: 100,
  //   text: "サンプルテキスト",
  //   style: "normal",
  //   highlight: "",
  //   animation: "fadeOnly",
  //   template: 2
  // },
];
