/**
 * Phase 3-S B5 (Codex CODEX_REVIEW_PHASE3R_AND_3S 推奨): React component test 基盤.
 *
 * vitest + jsdom + @testing-library/react で useNarrationMode hook の
 * watchStaticFile callback / invalidateNarrationMode / cleanup を unit test。
 *
 * lint と分離する理由: vitest は eslint/tsc とは別の test runner 経路、
 * `npm run test:react` で個別実行 + `npm run test` で連結実行。
 */
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
  },
});
