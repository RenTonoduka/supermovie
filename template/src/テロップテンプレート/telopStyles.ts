// ===== アニメーションテンプレート =====

// アニメーションなし
export const animation_none = {
  name: 'アニメーションなし',
  fadeInDuration: 0,
  fadeOutDuration: 0,
  slideInDistance: 0,
  slideDirection: 'up' as const,
  spring: {
    damping: 20,
    stiffness: 100,
    mass: 0.5,
  },
};

// 左からスライドイン
export const animation_slideFromLeft = {
  name: '左からスライドイン',
  fadeInDuration: 8,
  fadeOutDuration: 8,
  slideInDistance: 50,
  slideDirection: 'left' as const,
  spring: {
    damping: 20,
    stiffness: 100,
    mass: 0.5,
  },
};

// 不透明度+ブラー_下から
export const animation_fadeBlurFromBottom = {
  name: '不透明度+ブラー_下から',
  fadeInDuration: 10,
  fadeOutDuration: 10,
  slideInDistance: 30,
  slideDirection: 'up' as const,
  spring: {
    damping: 15,
    stiffness: 120,
    mass: 0.5,
  },
};

// スライドイン + フェード（上から）
export const animation_slideIn = {
  name: 'スライドイン',
  fadeInDuration: 8,
  fadeOutDuration: 8,
  slideInDistance: 30,
  slideDirection: 'up' as const,
  spring: {
    damping: 20,
    stiffness: 100,
    mass: 0.5,
  },
};

// フェードのみ
export const animation_fadeOnly = {
  name: 'フェードのみ',
  fadeInDuration: 8,
  fadeOutDuration: 8,
  slideInDistance: 0,
  slideDirection: 'up' as const,
  spring: {
    damping: 20,
    stiffness: 100,
    mass: 0.5,
  },
};

// 左からスライドイン + 不透明度 + ブラー（複合）
export const animation_slideLeftFadeBlur = {
  name: '左スライド+フェード+ブラー',
  fadeInDuration: 10,
  fadeOutDuration: 10,
  slideInDistance: 50,
  slideDirection: 'left' as const,
  spring: {
    damping: 15,
    stiffness: 120,
    mass: 0.5,
  },
};

// 右からフェードイン
export const animation_fadeFromRight = {
  name: '右からフェードイン',
  fadeInDuration: 10,
  fadeOutDuration: 10,
  slideInDistance: 40,
  slideDirection: 'right' as const,
  spring: {
    damping: 18,
    stiffness: 100,
    mass: 0.5,
  },
};

// 左からフェードイン（スライド小さめ）
export const animation_fadeFromLeft = {
  name: '左からフェードイン',
  fadeInDuration: 10,
  fadeOutDuration: 10,
  slideInDistance: 40,
  slideDirection: 'left' as const,
  spring: {
    damping: 18,
    stiffness: 100,
    mass: 0.5,
  },
};

// 一文字ずつ上からスライドイン
export const animation_charByChar = {
  name: '一文字ずつ上から',
  fadeInDuration: 0,
  fadeOutDuration: 8,
  slideInDistance: 25,
  slideDirection: 'down' as const,
  charDelay: 2, // 各文字の遅延フレーム数
  spring: {
    damping: 15,
    stiffness: 200,
    mass: 0.4,
  },
};

// ===== スタイルテンプレート集 =====

// テンプレート1: グラデーション背景スタイル
export const template1_gradient = {
  name: 'グラデーション背景',
  font: {
    size: 80,
    weight: 800,
    family: '"Noto Sans JP", sans-serif',
    style: 'italic' as const,
    lineHeight: 1.2,
    letterSpacing: 0,
    color: '#ffffff',
  },
  textShadow: {
    offsetX: -5,
    offsetY: 5,
    blur: 25,
    color: 'rgba(0, 0, 0, 0.92)',
  },
  textStroke: {
    width: 0,
    gradient: {
      start: 'transparent',
      end: 'transparent',
    },
  },
  background: {
    enabled: true,
    gradient: 'linear-gradient(90deg, #CE4BFF 0%, #4C82E5 100%)',
    padding: '0 10px',
    borderRadius: 0,
    backdropFilter: 'blur(10px)',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
  },
  position: {
    bottom: 100,
    maxWidth: '85%',
    containerPadding: '0 60px',
  },
  highlight: {
    color: '#FFD700',
    glowOpacity: '40',
  },
};

// テンプレート2: 紫ストローク（背景なし）
export const template2_purpleStroke = {
  name: '紫ストローク（背景なし）',
  font: {
    size: 80,
    weight: 800,
    family: '"Noto Sans JP", sans-serif',
    style: 'italic' as const,
    lineHeight: 1.2,
    letterSpacing: 0,
    color: '#ffffff',
  },
  textShadow: {
    offsetX: -8,
    offsetY: 8,
    blur: 35,
    color: 'rgba(0, 0, 0, 0.95)',
  },
  textStroke: {
    width: 14,
    gradient: {
      start: '#9420D6',
      end: '#3835EC',
    },
  },
  background: {
    enabled: false,
    gradient: 'transparent',
    padding: '0',
    borderRadius: 0,
    backdropFilter: 'none',
    boxShadow: 'none',
    border: 'none',
  },
  position: {
    bottom: 100,
    maxWidth: '85%',
    containerPadding: '0 60px',
  },
  highlight: {
    color: '#FFD700',
    glowOpacity: '40',
  },
};

// テンプレート3: グラデーション文字 + 白ストローク
export const template3_gradientText = {
  name: 'グラデーション文字 + 白ストローク',
  font: {
    size: 80,
    weight: 800,
    family: '"Noto Sans JP", sans-serif',
    style: 'italic' as const,
    lineHeight: 1.2,
    letterSpacing: 0,
    color: '#ffffff', // SVGでグラデーションに上書き
    fillGradient: {
      enabled: true,
      start: '#9420D6',
      end: '#3835EC',
    },
    opacity: 0.9,
  },
  textShadow: {
    offsetX: -8,
    offsetY: 8,
    blur: 35,
    color: 'rgba(0, 0, 0, 0.85)',
  },
  textStroke: {
    width: 10,
    gradient: {
      start: '#ffffff',
      end: '#ffffff',
    },
  },
  background: {
    enabled: false,
    gradient: 'transparent',
    padding: '0',
    borderRadius: 0,
    backdropFilter: 'none',
    boxShadow: 'none',
    border: 'none',
  },
  position: {
    bottom: 100,
    maxWidth: '85%',
    containerPadding: '0 60px',
  },
  highlight: {
    color: '#FFD700',
    glowOpacity: '40',
  },
};

// テンプレート4: ネガティブ（白背景・黒テキスト）
export const template4_negative = {
  name: 'ネガティブ（白背景・黒テキスト）',
  font: {
    size: 80,
    weight: 800,
    family: '"Noto Sans JP", sans-serif',
    style: 'italic' as const,
    lineHeight: 1.2,
    letterSpacing: 0,
    color: '#1a1a1a',
  },
  textShadow: {
    offsetX: 0,
    offsetY: 0,
    blur: 0,
    color: 'transparent',
  },
  textStroke: {
    width: 0,
    gradient: {
      start: 'transparent',
      end: 'transparent',
    },
  },
  background: {
    enabled: true,
    gradient: 'linear-gradient(90deg, #ffffff 0%, #f0f0f0 100%)',
    padding: '0 20px',
    borderRadius: 0,
    backdropFilter: 'none',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
    border: 'none',
  },
  position: {
    bottom: 100,
    maxWidth: '85%',
    containerPadding: '0 60px',
  },
  highlight: {
    color: '#dc2626',
    glowOpacity: '40',
  },
};

// テンプレート4v2: ネガティブ（黒背景・白テキスト）
export const template4_negative_v2 = {
  name: 'ネガティブv2（黒背景・白テキスト）',
  font: {
    size: 80,
    weight: 800,
    family: '"Noto Sans JP", sans-serif',
    style: 'italic' as const,
    lineHeight: 1.2,
    letterSpacing: 0,
    color: '#ffffff',
  },
  textShadow: {
    offsetX: 0,
    offsetY: 0,
    blur: 0,
    color: 'transparent',
  },
  textStroke: {
    width: 0,
    gradient: {
      start: 'transparent',
      end: 'transparent',
    },
  },
  background: {
    enabled: true,
    gradient: 'linear-gradient(90deg, #1a1a1a 0%, #2a2a2a 100%)',
    padding: '0 20px',
    borderRadius: 0,
    backdropFilter: 'none',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.6)',
    border: 'none',
  },
  position: {
    bottom: 100,
    maxWidth: '85%',
    containerPadding: '0 60px',
  },
  highlight: {
    color: '#dc2626',
    glowOpacity: '40',
  },
};

// テンプレート6: 白背景 + グラデーション文字（紫→青）
export const template6_whiteGradientText = {
  name: '白背景 + グラデーション文字',
  font: {
    size: 80,
    weight: 800,
    family: '"Noto Sans JP", sans-serif',
    style: 'italic' as const,
    lineHeight: 1.2,
    letterSpacing: 0,
    color: '#ffffff', // SVGでグラデーションに上書き
    fillGradient: {
      enabled: true,
      start: '#B20AFD',  // 紫
      end: '#087FFF',    // 青
    },
    opacity: 1,
  },
  textShadow: {
    offsetX: 0,
    offsetY: 0,
    blur: 0,
    color: 'transparent',
  },
  textStroke: {
    width: 0,
    gradient: {
      start: 'transparent',
      end: 'transparent',
    },
  },
  background: {
    enabled: true,
    gradient: 'linear-gradient(90deg, #ffffff 0%, #f8f8f8 100%)',
    padding: '0 20px',
    borderRadius: 0,
    backdropFilter: 'none',
    boxShadow: 'none',
    border: 'none',
  },
  position: {
    bottom: 100,
    maxWidth: '85%',
    containerPadding: '0 60px',
  },
  highlight: {
    color: '#B20AFD',
    glowOpacity: '40',
  },
};

// ===== 使用するテンプレートを選択 =====
// 使いたいテンプレートに変更してください
export const subtitleConfig = template3_gradientText;

// CSSスタイルを生成するヘルパー関数
export const getTextShadowCSS = () => {
  const { offsetX, offsetY, blur, color } = subtitleConfig.textShadow;
  return `${offsetX}px ${offsetY}px ${blur}px ${color}`;
};

export const getTextStrokeCSS = () => {
  const { width, gradient } = subtitleConfig.textStroke;
  // グラデーションストロークはSVGで実装するため、ここではwidthのみ返す
  return { width, gradient };
};
