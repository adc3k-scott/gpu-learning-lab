import { NextResponse } from 'next/server';
import { createAdminSupabaseClient } from '@/lib/supabase';

// In-memory cooldown: 30 seconds per IP
const cooldownMap = new Map();

function checkCooldown(ip) {
  const now = Date.now();
  const lastRequest = cooldownMap.get(ip);

  if (lastRequest && now - lastRequest < 30000) {
    return false;
  }

  cooldownMap.set(ip, now);
  return true;
}

// Clean up old cooldowns every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [ip, timestamp] of cooldownMap.entries()) {
    if (now - timestamp > 60000) {
      cooldownMap.delete(ip);
    }
  }
}, 5 * 60 * 1000);

export async function POST(request) {
  try {
    const ip = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';

    // Cooldown check
    if (!checkCooldown(ip)) {
      return NextResponse.json(
        { error: 'Please wait a moment before signing up again.' },
        { status: 429 }
      );
    }

    const body = await request.json();
    const { email, platform, source = 'landing', utm_source, utm_medium, utm_campaign } = body;

    // Email validation
    if (!email || typeof email !== 'string') {
      return NextResponse.json(
        { error: 'Email is required.' },
        { status: 400 }
      );
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Please enter a valid email address.' },
        { status: 400 }
      );
    }

    // Save to Supabase
    const supabase = createAdminSupabaseClient();

    if (supabase && process.env.NEXT_PUBLIC_SUPABASE_URL) {
      const { error: dbError } = await supabase
        .from('email_signups')
        .upsert(
          {
            email: email.toLowerCase().trim(),
            platform_interest: platform || null,
            source,
            utm_source: utm_source || null,
            utm_medium: utm_medium || null,
            utm_campaign: utm_campaign || null,
          },
          { onConflict: 'email' }
        );

      if (dbError) {
        console.error('Supabase email signup error:', dbError);
      }
    }

    // Subscribe to Kit (ConvertKit)
    if (process.env.KIT_API_KEY) {
      try {
        const kitResponse = await fetch('https://api.convertkit.com/v3/forms/YOUR_FORM_ID/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: process.env.KIT_API_KEY,
            email: email.toLowerCase().trim(),
            tags: platform ? [platform] : [],
          }),
        });

        if (!kitResponse.ok) {
          console.error('Kit subscription error:', await kitResponse.text());
        }
      } catch (kitError) {
        console.error('Kit API error:', kitError);
        // Don't fail the request if Kit is down
      }
    }

    return NextResponse.json({
      success: true,
      message: "You're in! Check your email for a welcome message.",
    });
  } catch (error) {
    console.error('Email signup error:', error);
    return NextResponse.json(
      { error: 'Something went wrong. Please try again.' },
      { status: 500 }
    );
  }
}
