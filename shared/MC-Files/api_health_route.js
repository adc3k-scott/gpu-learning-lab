import { NextResponse } from 'next/server';

export async function GET() {
  const status = {
    status: 'ok',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    services: {
      anthropic: !!process.env.ANTHROPIC_API_KEY,
      supabase: !!process.env.NEXT_PUBLIC_SUPABASE_URL,
      stripe: !!process.env.STRIPE_SECRET_KEY,
      kit: !!process.env.KIT_API_KEY,
    },
  };

  return NextResponse.json(status);
}
