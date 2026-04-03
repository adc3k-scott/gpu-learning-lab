import { NextResponse } from 'next/server';
import { createServerClient } from '@supabase/ssr';

// Routes that require authentication
const PROTECTED_ROUTES = ['/dashboard', '/garage', '/ai-chat', '/account', '/onboarding'];

// Routes only for guests (redirect to dashboard if logged in)
const GUEST_ONLY_ROUTES = ['/login'];

export async function middleware(request) {
  let response = NextResponse.next({
    request: { headers: request.headers },
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          response = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh session
  const { data: { user } } = await supabase.auth.getUser();
  const pathname = request.nextUrl.pathname;

  // Protected routes — redirect to login if not authenticated
  const isProtected = PROTECTED_ROUTES.some(route => pathname.startsWith(route));
  if (isProtected && !user) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Guest-only routes — redirect to dashboard if already logged in
  const isGuestOnly = GUEST_ONLY_ROUTES.some(route => pathname.startsWith(route));
  if (isGuestOnly && user) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Inject user tier into headers for downstream use
  if (user) {
    response.headers.set('x-user-id', user.id);
    // Tier would be fetched from profile in actual implementation
  }

  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|robots.txt|sitemap.xml|og-image.png|icon-.*\\.png|apple-touch-icon.png|site\\.webmanifest|api/).*)',
  ],
};
