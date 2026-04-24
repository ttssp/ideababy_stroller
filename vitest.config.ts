// Vitest 最小配置(T002 范围)
// include 仅指 tests/**/*.test.ts;db / coverage / 阈值由 T008 task 增强
// 首跑无测试时 vitest 退出码 0,符合 T002 verification §2
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    globals: false,
    include: ['tests/**/*.test.ts'],
    exclude: ['tests/e2e/**', 'node_modules/**', '.next/**', 'dist/**'],
    passWithNoTests: true,
  },
});
