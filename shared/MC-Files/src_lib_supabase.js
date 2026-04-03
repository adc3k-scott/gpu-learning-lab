import { createBrowserClient } from '@supabase/ssr';
import { createClient } from '@supabase/supabase-js';

// ============================================
// BROWSER CLIENT (client components)
// ============================================
export function createBrowserSupabaseClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  );
}

// ============================================
// SERVER CLIENT (server components, API routes)
// ============================================
export function createServerSupabaseClient() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    }
  );
}

// ============================================
// ADMIN CLIENT (service role — server only, bypasses RLS)
// ============================================
export function createAdminSupabaseClient() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    }
  );
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Get the current authenticated user's profile
 */
export async function getCurrentUser(supabase) {
  try {
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) return null;

    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.id)
      .single();

    if (profileError) return { ...user, tier: 'free' };
    return { ...user, ...profile };
  } catch {
    return null;
  }
}

/**
 * Check if a user has access to a specific tier level
 */
export function hasTierAccess(userTier, requiredTier) {
  const tierLevel = { free: 0, premium: 1, pro: 2 };
  return (tierLevel[userTier] || 0) >= (tierLevel[requiredTier] || 0);
}

/**
 * Check AI rate limit for a user
 */
export async function checkAIRateLimit(supabase, userId, tier) {
  const limits = { free: 3, premium: 20, pro: Infinity };
  const dailyLimit = limits[tier] || 3;

  if (dailyLimit === Infinity) return { allowed: true, remaining: Infinity };

  const today = new Date().toISOString().split('T')[0];
  const { count, error } = await supabase
    .from('ai_chat_usage')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId)
    .eq('query_date', today);

  if (error) return { allowed: false, remaining: 0 };

  const used = count || 0;
  return {
    allowed: used < dailyLimit,
    remaining: dailyLimit - used,
    used,
    limit: dailyLimit,
  };
}

/**
 * Check if a user can add another vehicle
 */
export async function canAddVehicle(supabase, userId, tier) {
  const limits = { free: 1, premium: 3, pro: Infinity };
  const vehicleLimit = limits[tier] || 1;

  if (vehicleLimit === Infinity) return { allowed: true, remaining: Infinity };

  const { count, error } = await supabase
    .from('vehicles')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId);

  if (error) return { allowed: false, remaining: 0 };

  const current = count || 0;
  return {
    allowed: current < vehicleLimit,
    remaining: vehicleLimit - current,
    current,
    limit: vehicleLimit,
  };
}
