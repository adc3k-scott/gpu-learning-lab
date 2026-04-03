import './globals.css';
import { AuthProvider } from '@/components/AuthProvider';

export const metadata = {
  title: {
    default: 'Mission Control — AI-Powered Vehicle Intelligence',
    template: '%s | Mission Control',
  },
  description:
    'Free diagnostic tools, AI chat, and vehicle management for Harley-Davidson, cars, trucks, e-bikes, and scooters. 41 tools across 5 platforms.',
  keywords: [
    'vehicle diagnostics',
    'Harley-Davidson DTC codes',
    'OBD-II scanner',
    'truck HOS tracker',
    'e-bike battery health',
    'scooter maintenance',
    'AI mechanic',
    'diagnostic tools',
  ],
  authors: [{ name: 'Mission Control' }],
  creator: 'Mission Control',
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: '/',
    siteName: 'Mission Control',
    title: 'Mission Control — AI-Powered Vehicle Intelligence',
    description:
      'Free diagnostic tools, AI chat, and vehicle management for Harley-Davidson, cars, trucks, e-bikes, and scooters.',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Mission Control — 41 tools across 5 platforms',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Mission Control — AI-Powered Vehicle Intelligence',
    description:
      'Free diagnostic tools, AI chat, and vehicle management across 5 platforms.',
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
    },
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
};

export const viewport = {
  themeColor: '#0A0A0B',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebApplication',
              name: 'Mission Control',
              description:
                'AI-powered vehicle intelligence for Harley-Davidson, cars, trucks, e-bikes, and scooters.',
              url: process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000',
              applicationCategory: 'UtilityApplication',
              operatingSystem: 'Web',
              offers: [
                {
                  '@type': 'Offer',
                  price: '0',
                  priceCurrency: 'USD',
                  description: 'Free tier — 41 tools, 3 AI queries/day',
                },
                {
                  '@type': 'Offer',
                  price: '9.99',
                  priceCurrency: 'USD',
                  description: 'Premium — 20 AI queries/day, 3 vehicles',
                },
                {
                  '@type': 'Offer',
                  price: '19.99',
                  priceCurrency: 'USD',
                  description: 'Pro — Unlimited AI, unlimited vehicles, wiring diagrams',
                },
              ],
            }),
          }}
        />
      </head>
      <body className="min-h-screen bg-background text-text-primary font-sans antialiased">
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
