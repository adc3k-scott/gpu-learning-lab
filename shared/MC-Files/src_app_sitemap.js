import { ALL_ROUTES, SITE_URL } from '@/lib/constants';

export default function sitemap() {
  const now = new Date().toISOString();

  // Priority mapping
  const getPriority = (route) => {
    if (route === '/') return 1.0;
    if (route === '/pricing' || route === '/blog') return 0.9;
    if (route.split('/').length === 2 && !route.includes('tools')) return 0.8; // Platform index pages
    if (route === '/tools') return 0.8;
    return 0.6; // Individual tool pages
  };

  // Change frequency mapping
  const getChangeFrequency = (route) => {
    if (route === '/' || route === '/blog') return 'daily';
    if (route === '/pricing') return 'weekly';
    return 'monthly';
  };

  return ALL_ROUTES.map((route) => ({
    url: `${SITE_URL}${route}`,
    lastModified: now,
    changeFrequency: getChangeFrequency(route),
    priority: getPriority(route),
  }));
}
