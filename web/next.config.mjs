/** @type {import('next').NextConfig} */
const nextConfig = {
  // packages/shared is plain ESM sitting outside web/ (an npm workspace); compile it with the app.
  transpilePackages: ["@aruvi/shared"],
};
export default nextConfig;
