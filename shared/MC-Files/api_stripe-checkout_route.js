import { NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const PRICE_IDS = {
  premium_monthly: process.env.STRIPE_PREMIUM_MONTHLY_PRICE_ID,
  premium_annual: process.env.STRIPE_PREMIUM_ANNUAL_PRICE_ID,
  pro_monthly: process.env.STRIPE_PRO_MONTHLY_PRICE_ID,
  pro_annual: process.env.STRIPE_PRO_ANNUAL_PRICE_ID,
};

export async function POST(request) {
  try {
    if (!process.env.STRIPE_SECRET_KEY) {
      return NextResponse.json(
        { error: 'Payments are not configured.' },
        { status: 503 }
      );
    }

    const body = await request.json();
    const { tier, interval = 'monthly', userId, email, promoCode } = body;

    // Validate tier
    if (!tier || !['premium', 'pro'].includes(tier)) {
      return NextResponse.json(
        { error: 'Invalid subscription tier.' },
        { status: 400 }
      );
    }

    // Validate interval
    if (!['monthly', 'annual'].includes(interval)) {
      return NextResponse.json(
        { error: 'Invalid billing interval.' },
        { status: 400 }
      );
    }

    const priceKey = `${tier}_${interval}`;
    const priceId = PRICE_IDS[priceKey];

    if (!priceId) {
      return NextResponse.json(
        { error: 'Price not configured. Please contact support.' },
        { status: 500 }
      );
    }

    const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';

    // Build checkout session params
    const sessionParams = {
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${siteUrl}/account?checkout=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${siteUrl}/pricing?checkout=cancelled`,
      metadata: {
        userId: userId || '',
        tier,
        interval,
      },
    };

    // Add email if provided
    if (email) {
      sessionParams.customer_email = email;
    }

    // 7-day free trial on Premium monthly only
    if (tier === 'premium' && interval === 'monthly') {
      sessionParams.subscription_data = {
        trial_period_days: 7,
      };
    }

    // Add promo code support
    if (promoCode) {
      sessionParams.discounts = [{ promotion_code: promoCode }];
    } else {
      sessionParams.allow_promotion_codes = true;
    }

    const session = await stripe.checkout.sessions.create(sessionParams);

    return NextResponse.json({ url: session.url, sessionId: session.id });
  } catch (error) {
    console.error('Stripe checkout error:', error);
    return NextResponse.json(
      { error: 'Failed to create checkout session. Please try again.' },
      { status: 500 }
    );
  }
}
