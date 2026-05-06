/**
 * Phase 3-H/I: per-segment narration timeline 用の型定義。
 * voicevox_narration.py が wave 実測 duration から narrationData.ts を生成する
 * (https://www.remotion.dev/docs/sequence)。
 */
export interface NarrationSegment {
  /** chunk index (0-based、生成順) */
  id: number;
  /**
   * timeline 上での開始 frame.
   * Phase 3-I: transcript_fixed.json の sourceStartMs を videoConfig.FPS で frame 化。
   * cut 後動画 (vad_result.json) がある場合は cut-aware mapping、cut で除外された
   * 箇所は累積 frame fallback。--script / --script-json は累積。
   */
  startFrame: number;
  /** WAV 実 duration を frame 換算した値 (FPS は voicevox_narration.py 引数) */
  durationInFrames: number;
  /** public/ 配下からの相対 path (例 'narration/chunk_000.wav') */
  file: string;
  /** debug 用に元 transcript text を保持 (省略可) */
  text?: string;
  /** Phase 3-I: 元 transcript の start ms (timing alignment 元、debug 用) */
  sourceStartMs?: number;
  /** Phase 3-I: 元 transcript の end ms (debug 用) */
  sourceEndMs?: number;
}
