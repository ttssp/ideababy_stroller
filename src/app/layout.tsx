// 根 layout · App Router · zh-CN
// T002 范围:仅占位 shell;真正的 (main) shell 由 Phase 1 task 落地
import type { ReactNode } from 'react';

export const metadata = {
  title: 'PI Briefing Console',
  description: 'PI Briefing Console · v0.1',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
