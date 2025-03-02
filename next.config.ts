/** @type {import('next').NextConfig} */
const config = {
  swcMinify: true,
  reactStrictMode: true,
  experimental: {
    serverActions: true,
  },
}

export default config 