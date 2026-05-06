/**
 * Phase 3 SlideSequence 用 schema (Codex Phase 3 推奨: 別レイヤー、画像扱いと分離).
 *
 * 1 Slide = タイトル + 箇条書き or 自由 React content。frame 範囲で表示制御。
 *
 * SuperMovie の他レイヤー (TelopPlayer / ImageSequence / TitleSequence) と同じく
 * data 駆動で、後段 skill (将来の supermovie-slides) が slideData.ts を生成する想定。
 */

export type SlideAlignment = 'center' | 'left';

export interface SlideBullet {
  text: string;
  /** highlighted bullet は色違いで強調 (Codex 推奨: skill 側で word→bullet 抽出時に true 設定) */
  emphasis?: boolean;
}

export interface SlideSegment {
  id: number;
  startFrame: number;
  endFrame: number;
  /** スライドのメインタイトル */
  title: string;
  /** 副題 (任意) */
  subtitle?: string;
  /** 箇条書き (任意) */
  bullets?: SlideBullet[];
  /** 配置 */
  align?: SlideAlignment;
  /** 背景色 (CSS color、省略時はテーマ既定) */
  backgroundColor?: string;
  /** テキスト色 (CSS color、省略時はテーマ既定) */
  textColor?: string;
  /** 表示中の動画レイヤー (画面 0 透過 / dimmed / hidden) */
  videoLayer?: 'visible' | 'dimmed' | 'hidden';
}
