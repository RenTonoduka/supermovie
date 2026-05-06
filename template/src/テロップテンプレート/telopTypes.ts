import type { TelopTemplateId } from './telopTemplateRegistry';

export interface TelopSegment {
  id: number;
  startFrame: number;
  endFrame: number;
  text: string;
  highlight?: string;
  style?: 'normal' | 'emphasis' | 'warning' | 'success';
  // legacy: 既存 Telop.tsx (template={1..6} で switch する旧 API) と互換のため残す
  template?: 1 | 2 | 3 | 4 | 5 | 6;
  // 新: telopTemplateRegistry に登録された templateId (registry のキー)
  // templateId が指定されると Telop.tsx の legacy 分岐より優先される
  templateId?: TelopTemplateId;
  animation?: 'none' | 'slideIn' | 'fadeOnly' | 'slideFromLeft' | 'fadeBlurFromBottom' | 'slideLeftFadeBlur' | 'fadeFromRight' | 'fadeFromLeft' | 'charByChar';
}
