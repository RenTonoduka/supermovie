/**
 * Phase 3-R (Codex CODEX_RESUME_PHASE3R 推奨 B4): Telop.tsx の `any` 警告 9 件を
 * 解消するための共通型定義。telopStyles.ts の各 template / animation を構造的
 * type で表現し、`(font as any).fillGradient` のような escape を排除する。
 *
 * 各 template の font/textStroke/animation は heterogeneous (一部 template
 * のみ fillGradient / opacity / charDelay 等を持つ) ため、interface 側で
 * `?` optional で表現し、タグ無しで安全アクセスする。
 */

export interface TelopFontConfig {
  size: number;
  weight: number;
  family: string;
  /** 'italic' or 'normal'、telopStyles.ts では `as const` で literal */
  style: string;
  lineHeight: number;
  letterSpacing: number;
  color: string;
  /** SVG グラデーション fill (template3 / template6 のみ持つ) */
  fillGradient?: {
    enabled: boolean;
    start: string;
    end: string;
  };
  /** 不透明度 (template3 / template6 のみ持つ、default 1) */
  opacity?: number;
}

export interface TelopTextShadowConfig {
  offsetX: number;
  offsetY: number;
  blur: number;
  color: string;
}

export interface TelopTextStrokeConfig {
  width: number;
  gradient?: {
    start: string;
    end: string;
  };
}

export interface TelopBackgroundConfig {
  enabled: boolean;
  gradient?: string;
  padding?: string;
  borderRadius?: number | string;
  backdropFilter?: string;
  boxShadow?: string;
  border?: string;
}

export interface TelopPositionConfig {
  bottom: number;
  maxWidth: string;
  containerPadding: string;
}

export interface TelopHighlightConfig {
  color: string;
  glowOpacity: string;
}

export interface TelopStyleConfig {
  name: string;
  font: TelopFontConfig;
  textShadow: TelopTextShadowConfig;
  textStroke: TelopTextStrokeConfig;
  background: TelopBackgroundConfig;
  position: TelopPositionConfig;
  highlight?: TelopHighlightConfig;
}

export interface TelopAnimationSpring {
  damping: number;
  stiffness: number;
  mass: number;
}

export interface TelopAnimationConfig {
  name: string;
  fadeInDuration: number;
  fadeOutDuration: number;
  slideInDistance: number;
  /** 全 animation が持つ ('up' / 'down' / 'left' / 'right'、telopStyles.ts では `as const`) */
  slideDirection: string;
  /** charByChar 系のみ持つ、各文字の遅延 frame */
  charDelay?: number;
  spring: TelopAnimationSpring;
}
