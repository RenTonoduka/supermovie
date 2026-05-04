/**
 * Phase 3-H: per-segment narration timeline 用の型定義。
 * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
 * (https://www.remotion.dev/docs/sequence)。
 */
export interface NarrationSegment {
  /** chunk index (0-based、生成順) */
  id: number;
  /** timeline 上での開始 frame (前 chunk の累積 duration) */
  startFrame: number;
  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
  durationInFrames: number;
  /** public/ 配下からの相対 path (例 'narration/chunk_000.wav') */
  file: string;
  /** debug 用に元 transcript text を保持 (省略可) */
  text?: string;
}
