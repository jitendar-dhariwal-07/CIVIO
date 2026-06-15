import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  images: {
    domains: ["localhost", "api.citizenai.in", "tile.openstreetmap.org"],
    unoptimized: false,
  },
  transpilePackages: ["lucide-react"],
};

export default nextConfig;
