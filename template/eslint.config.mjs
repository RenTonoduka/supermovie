// @remotion/eslint-config-flat 4.x は default export を提供せず、named exports
// (config / makeConfig) を提供する。default import すると `does not provide an
// export named 'default'` で fail するため、named import に切り替える。
import { config } from "@remotion/eslint-config-flat";

// telop-templates-30.zip 由来の component が `any` を使っているため、
// no-explicit-any は warning に緩和。型を厳密化するのは別 issue。
export default [
  ...config,
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "warn",
    },
  },
];
