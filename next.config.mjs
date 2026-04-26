// 最小 Next.js 15 配置 · App Router · React strict 开启
// 不引入 custom webpack / experimental 项;后续如需 image domain / headers 再 patch
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

export default nextConfig;
