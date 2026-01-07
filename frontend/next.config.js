/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'standalone',
    eslint: {
        // Ignore updates during deploy for speed
        ignoreDuringBuilds: true,
    },
};

module.exports = nextConfig;
