// @remotion/eslint-config-flat 4.x は default export を提供せず、named exports
// (config / makeConfig) を提供する。default import すると `does not provide an
// export named 'default'` で fail するため、named import に切り替える。
import { config } from "@remotion/eslint-config-flat";

// Phase 3-R で telop component の any を 0 化済み (telopConfigTypes.ts 9 interface
// + Telop.tsx escape 全削除 + literal narrowing)、Phase 3-V FINAL verdict 後に warn → error
// に固定し any-free contract を機械 gate 化 (template/src の any 使用 0、Bash grep 実測)。
export default [
  ...config,
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
];
