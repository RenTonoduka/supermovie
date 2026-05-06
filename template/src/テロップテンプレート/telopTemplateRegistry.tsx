// 自動生成可能 (現在は手書き): 30 telop テンプレートを registry で一元管理
// Codex Phase 2 design (2026-05-04) 推奨: B + registry
// templateId = registry のキー (= 各 .tsx の export 名)

import type React from 'react';

// ===== Main (落ち着いた・通常字幕) =====
import { BlackWhite as KuroMoji } from '../メインテロップ/黒文字';
import { BlueTextWhiteBg } from '../メインテロップ/青文字白背景';
import { WhiteBlackTeleop } from '../メインテロップ/白黒テロップ';
import { WhiteBlue } from '../メインテロップ/白青テロップ';
import { WhiteBlueTeleopV2 } from '../メインテロップ/白青テロップver2';
import { WhiteBgGradText } from '../メインテロップ/白背景グラデ';
import { WhiteTextBlackShadow } from '../メインテロップ/白文字黒シャドウ';
import { WhiteTextBlackShadowGothic } from '../メインテロップ/白文字黒シャドウゴシック';
import { WhiteShadow as WhiteShadowMincho } from '../メインテロップ/白文字黒シャドウ明朝体';
import { WhiteBlackBackground } from '../メインテロップ/白文字黒背景';
import { WhitePinkBlueGradation } from '../メインテロップ/白文字青ピンク背景グラデ';
import { GreenTextWhiteBg } from '../メインテロップ/緑文字白背景';

// ===== Emphasis (注目・強調) =====
import { OrangeGradation } from '../強調テロップ/オレンジグラデーション';
import { YellowShadow } from '../強調テロップ/黄色シャドウ';
import { YellowTextBlackShadow } from '../強調テロップ/黄色文字黒シャドウ';
import { GoldGradNavyBg } from '../強調テロップ/金グラデ・紺背景';
import { BlackTextYellowBg } from '../強調テロップ/黒文字黄色背景';
import { BlueGold } from '../強調テロップ/青文字金枠';
import { RedWhite as AkaMoji } from '../強調テロップ/赤文字';
import { RedTextWhiteBg } from '../強調テロップ/赤文字白背景';
import { WhiteRed } from '../強調テロップ/白赤テロップ';
import { WhiteRedTeleopV2 } from '../強調テロップ/白赤テロップver2';
import { WhiteRedShadow } from '../強調テロップ/白文字赤シャドウ';
import { WhiteGreen } from '../強調テロップ/白緑テロップ';
import { GreenGradation } from '../強調テロップ/緑グラデ金シャドウ';

// ===== Negative (警告・否定) =====
import { BlackPurpleGradation } from '../ネガティブテロップ/黒紫グラデ';
import { BlackWhiteBackground } from '../ネガティブテロップ/黒文字白背景';
import { NavyBlueRiitegaki } from '../ネガティブテロップ/残酷テロップ・紺';
import { PurpleTextWhiteBg } from '../ネガティブテロップ/紫文字白背景';
import { WhitePurpleShadow } from '../ネガティブテロップ/白文字紫シャドウ';

// テロップコンポーネントの共通 props 型 (各 .tsx は subtitleData を必須で受ける)
export interface SubtitleItem {
  text: string;
  lines: string[];
  start: number;
  end: number;
  startFrame: number;
  endFrame: number;
}
export interface SubtitleData {
  fps: number;
  subtitles: SubtitleItem[];
}
export type TelopComponent = React.FC<{ subtitleData: SubtitleData }>;

export type TelopCategory = 'main' | 'emphasis' | 'negative';

export interface TelopTemplateEntry {
  category: TelopCategory;
  displayName: string;
  Component: TelopComponent;
}

// registry: テンプレート ID (= キー) → メタ情報 + Component
// 命名は各 .tsx の export 名を尊重 (一部はファイル名と異なるため alias で同名衝突を回避)
export const telopTemplateRegistry = {
  // --- main 12 ---
  WhiteBlue: { category: 'main', displayName: '白青テロップ', Component: WhiteBlue as TelopComponent },
  WhiteBlueTeleopV2: { category: 'main', displayName: '白青テロップver2', Component: WhiteBlueTeleopV2 as TelopComponent },
  KuroMoji: { category: 'main', displayName: '黒文字', Component: KuroMoji as TelopComponent },
  BlueTextWhiteBg: { category: 'main', displayName: '青文字白背景', Component: BlueTextWhiteBg as TelopComponent },
  WhiteBlackTeleop: { category: 'main', displayName: '白黒テロップ', Component: WhiteBlackTeleop as TelopComponent },
  WhiteBgGradText: { category: 'main', displayName: '白背景グラデ', Component: WhiteBgGradText as TelopComponent },
  WhiteTextBlackShadow: { category: 'main', displayName: '白文字黒シャドウ', Component: WhiteTextBlackShadow as TelopComponent },
  WhiteTextBlackShadowGothic: { category: 'main', displayName: '白文字黒シャドウゴシック', Component: WhiteTextBlackShadowGothic as TelopComponent },
  WhiteShadowMincho: { category: 'main', displayName: '白文字黒シャドウ明朝体', Component: WhiteShadowMincho as TelopComponent },
  WhiteBlackBackground: { category: 'main', displayName: '白文字黒背景', Component: WhiteBlackBackground as TelopComponent },
  WhitePinkBlueGradation: { category: 'main', displayName: '白文字青ピンク背景グラデ', Component: WhitePinkBlueGradation as TelopComponent },
  GreenTextWhiteBg: { category: 'main', displayName: '緑文字白背景', Component: GreenTextWhiteBg as TelopComponent },

  // --- emphasis 13 ---
  OrangeGradation: { category: 'emphasis', displayName: 'オレンジグラデーション', Component: OrangeGradation as TelopComponent },
  AkaMoji: { category: 'emphasis', displayName: '赤文字', Component: AkaMoji as TelopComponent },
  YellowShadow: { category: 'emphasis', displayName: '黄色シャドウ', Component: YellowShadow as TelopComponent },
  YellowTextBlackShadow: { category: 'emphasis', displayName: '黄色文字黒シャドウ', Component: YellowTextBlackShadow as TelopComponent },
  GoldGradNavyBg: { category: 'emphasis', displayName: '金グラデ・紺背景', Component: GoldGradNavyBg as TelopComponent },
  BlackTextYellowBg: { category: 'emphasis', displayName: '黒文字黄色背景', Component: BlackTextYellowBg as TelopComponent },
  BlueGold: { category: 'emphasis', displayName: '青文字金枠', Component: BlueGold as TelopComponent },
  RedTextWhiteBg: { category: 'emphasis', displayName: '赤文字白背景', Component: RedTextWhiteBg as TelopComponent },
  WhiteRed: { category: 'emphasis', displayName: '白赤テロップ', Component: WhiteRed as TelopComponent },
  WhiteRedTeleopV2: { category: 'emphasis', displayName: '白赤テロップver2', Component: WhiteRedTeleopV2 as TelopComponent },
  WhiteRedShadow: { category: 'emphasis', displayName: '白文字赤シャドウ', Component: WhiteRedShadow as TelopComponent },
  WhiteGreen: { category: 'emphasis', displayName: '白緑テロップ', Component: WhiteGreen as TelopComponent },
  GreenGradation: { category: 'emphasis', displayName: '緑グラデ金シャドウ', Component: GreenGradation as TelopComponent },

  // --- negative 5 ---
  BlackPurpleGradation: { category: 'negative', displayName: '黒紫グラデ', Component: BlackPurpleGradation as TelopComponent },
  BlackWhiteBackground: { category: 'negative', displayName: '黒文字白背景', Component: BlackWhiteBackground as TelopComponent },
  NavyBlueRiitegaki: { category: 'negative', displayName: '残酷テロップ・紺', Component: NavyBlueRiitegaki as TelopComponent },
  PurpleTextWhiteBg: { category: 'negative', displayName: '紫文字白背景', Component: PurpleTextWhiteBg as TelopComponent },
  WhitePurpleShadow: { category: 'negative', displayName: '白文字紫シャドウ', Component: WhitePurpleShadow as TelopComponent },
} as const satisfies Record<string, TelopTemplateEntry>;

export type TelopTemplateId = keyof typeof telopTemplateRegistry;

// project-config.json telopStyle.{main,emphasis,negative} 既定値の displayName とのマップ:
//   "白青テロップver2" → 'WhiteBlueTeleopV2'
//   "オレンジグラデーション" → 'OrangeGradation'
//   "黒紫グラデ" → 'BlackPurpleGradation'
// supermovie-init / supermovie-subtitles から逆引きする時はこの helper を使う
export function findTemplateIdByDisplayName(displayName: string): TelopTemplateId | undefined {
  const entries = Object.entries(telopTemplateRegistry) as [TelopTemplateId, TelopTemplateEntry][];
  return entries.find(([, v]) => v.displayName === displayName)?.[0];
}

export function listTemplatesByCategory(category: TelopCategory): TelopTemplateId[] {
  const entries = Object.entries(telopTemplateRegistry) as [TelopTemplateId, TelopTemplateEntry][];
  return entries.filter(([, v]) => v.category === category).map(([k]) => k);
}
