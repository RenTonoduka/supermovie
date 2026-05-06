import type { SlideSegment } from './types';

// ==== スライドデータ (Phase 3-A) ====
// 将来の supermovie-slides skill で transcript 段落タイトル + Outline から自動生成。
// 現時点は placeholder 空配列。サンプルはコメントアウトで残す。

export const slideData: SlideSegment[] = [
  // 例 (cut 後 frame 0-180 でフルスクリーンタイトル):
  // {
  //   id: 1,
  //   startFrame: 0,
  //   endFrame: 180,
  //   title: 'Claude Code 完全自動編集',
  //   subtitle: 'SuperMovie Phase 3 PoC',
  //   align: 'center',
  // },
  // 例 (箇条書きスライド):
  // {
  //   id: 2,
  //   startFrame: 600,
  //   endFrame: 900,
  //   title: 'パイプラインの強み',
  //   bullets: [
  //     { text: '文字起こし → 誤字修正 → カット → テロップ' },
  //     { text: '30 templates から自動選択', emphasis: true },
  //     { text: 'BudouX で意味境界を保つ改行' },
  //   ],
  //   align: 'left',
  //   backgroundColor: '#101a2c',
  // },
];
