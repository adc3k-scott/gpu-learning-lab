import { NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createAdminSupabaseClient } from '@/lib/supabase';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export async function POST(request) {
  try {
    const body = await request.text();
    const signature = request.headers.get('stripe-signature');

    if (!signature || !process.env.STRIPE_WEBHOOK_SECRET) {
      return NextResponse.json({ error: 'Missing signature or webhook secret' }, { status: 400 });
    }

    // Verify webhook signature
    let event;
    try {
      event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET);
    } catch (err) {
      console.error('Webhook signature verification failed:', err.message);
      return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
    }

    const supabase = createAdminSupabaseClient();

    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object;
        const userId = session.metadata?.userId;
        const tier = session.metadata?.tier || 'premium';

        if (userId) {
          await supabase
            .from('profiles')
            .update({
              tier,
              stripe_customer_id: session.customer,
              stripe_subscription_id: session.subscription,
              updated_at: new Date().toISOString(),
            })
            .eq('id', userId);
        }

        console.log(`✅ Checkout completed: user=${userId}, tier=${tier}`);
        break;
      }

      case 'customer.subscription.updated': {
        const subscription = event.data.object;
        const customerId = subscription.customer;

        // Determine tier from price
        const priceId = subscription.items?.data?.[0]?.price?.id;
        let tier = 'free';

        if (priceId === process.env.STRIPE_PREMIUM_MONTHLY_PRICE_ID ||
            priceId === process.env.STRIPE_PREMIUM_ANNUAL_PRICE_ID) {
          tier = 'premium';
        } else if (priceId === process.env.STRIPE_PRO_MONTHLY_PRICE_ID ||
                   priceId === process.env.STRIPE_PRO_ANNUAL_PRICE_ID) {
          tier = 'pro';
        }

        // Handle cancellation scheduled
        if (subscription.cancel_at_period_end) {
          console.log(`⚠️ Subscription cancellation scheduled: customer=${customerId}`);
          // Don't downgrade yet — they paid through the end of the period
        } else {
          await supabase
            .from('profiles')
            .update({
              tier,
              updated_at: new Date().toISOString(),
            })
            .eq('stripe_customer_id', customerId);

          console.log(`✅ Subscription updated: customer=${customerId}, tier=${tier}`);
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object;
        const customerId = subscription.customer;

        // Downgrade to free
        await supabase
          .from('profiles')
          .update({
            tier: 'free',
            stripe_subscription_id: null,
            updated_at: new Date().toISOString(),
          })
          .eq('stripe_customer_id', customerId);

        console.log(`❌ Subscription deleted: customer=${customerId} → free`);
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object;
        const customerId = invoice.customer;

        console.log(`⚠️ Payment failed: customer=${customerId}, amount=${invoice.amount_due}`);
        // Could send a notification email here
        break;
      }

      default:
        console.log(`Unhandled event: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    return NextResponse.json({ error: 'Webhook processing failed' }, { status: 500 });
  }
}
