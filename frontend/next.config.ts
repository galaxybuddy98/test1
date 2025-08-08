import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async headers() {
    return [
      {
        source: '/(user|health|docs|assessment|auth|chatbot|monitoring|report|request|response)/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,DELETE,PATCH,POST,PUT' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version' },
        ],
      },
    ];
  },
  async rewrites() {
    return [
      // 사용자 관련
      {
        source: '/api/login',
        destination: `${process.env.NEXT_PUBLIC_GATEWAY_URL || 'https://api.eripotter.com'}/login`,
      },
      {
        source: '/api/signup', 
        destination: `${process.env.NEXT_PUBLIC_GATEWAY_URL || 'https://api.eripotter.com'}/signup`,
      },
      // 기본 API
      {
        source: '/health',
        destination: `${process.env.NEXT_PUBLIC_GATEWAY_URL || 'https://api.eripotter.com'}/health`,
      },
      {
        source: '/docs',
        destination: `${process.env.NEXT_PUBLIC_GATEWAY_URL || 'https://api.eripotter.com'}/docs`,
      },
      // 마이크로서비스들
      {
        source: '/(assessment|auth|chatbot|monitoring|report|request|response)/:path*',
        destination: `${process.env.NEXT_PUBLIC_GATEWAY_URL || 'https://api.eripotter.com'}/:match*`,
      },
    ];
  },
  env: {
    NEXT_PUBLIC_GATEWAY_URL: process.env.NEXT_PUBLIC_GATEWAY_URL || 'https://api.eripotter.com',
  },
};

export default nextConfig;
