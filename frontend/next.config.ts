import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  basePath: "/CIVIO",
  reactStrictMode: true,
  images: {
    domains: ["localhost", "api.citizenai.in", "tile.openstreetmap.org"],
    unoptimized: true,
  },
  transpilePackages: ["lucide-react"],
};

export default nextConfig;
