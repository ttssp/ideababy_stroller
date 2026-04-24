// 根路由占位页 · T002 仅返回标题
// Phase 1 task 会把 "/" 改为 302 → /today(或 /login),见 directory-layout §1
export default function Page() {
  return (
    <main>
      <h1>PI Briefing Console · v0.1</h1>
    </main>
  );
}
