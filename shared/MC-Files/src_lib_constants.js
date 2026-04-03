// ============================================
// MISSION CONTROL — Constants
// ============================================

export const SITE_NAME = 'Mission Control';
export const SITE_DESCRIPTION = 'AI-powered vehicle intelligence for every rider and driver.';
export const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';

// --- Platforms ---
export const PLATFORMS = {
  harley: {
    id: 'harley',
    name: 'Harley-Davidson',
    shortName: 'Harley',
    color: '#E8720E',
    icon: '🏍️',
    description: 'DTC codes, diagnostic flowcharts, service reference, torque specs, wiring diagrams, and more.',
    toolCount: 7,
    route: '/harley',
  },
  auto: {
    id: 'auto',
    name: 'Automotive',
    shortName: 'Auto',
    color: '#8B5CF6',
    icon: '🚗',
    description: 'OBD-II codes, diagnostic flowcharts, recall database, fluid guide, and morning briefs.',
    toolCount: 5,
    route: '/auto',
  },
  trucking: {
    id: 'trucking',
    name: 'Trucking',
    shortName: 'Trucking',
    color: '#FF6F00',
    icon: '🚛',
    description: 'HOS tracker, pre-trip checklists, profit calculator, IFTA generator, axle weight, and more.',
    toolCount: 7,
    route: '/trucking',
  },
  ebike: {
    id: 'ebike',
    name: 'E-Bike',
    shortName: 'E-Bike',
    color: '#22C55E',
    icon: '🚲',
    description: 'Error codes, battery health, class/law reference, wiring diagrams, build calculator.',
    toolCount: 7,
    route: '/ebike',
  },
  scooter: {
    id: 'scooter',
    name: 'Scooter',
    shortName: 'Scooter',
    color: '#06B6D4',
    icon: '🛴',
    description: 'Error codes, diagnostic flowcharts, maintenance guide, comparison calculator.',
    toolCount: 5,
    route: '/scooter',
  },
};

export const PLATFORM_LIST = Object.values(PLATFORMS);

// --- Universal Tools ---
export const UNIVERSAL_TOOLS = [
  { id: 'parts', name: 'Parts Locator', route: '/tools/parts', icon: '🔍', gate: 'free' },
  { id: 'converter', name: 'Unit Converter', route: '/tools/converter', icon: '🔄', gate: 'free' },
  { id: 'fuel-log', name: 'Fuel Log Tracker', route: '/tools/fuel-log', icon: '⛽', gate: 'free' },
  { id: 'tire-calc', name: 'Tire Size Calculator', route: '/tools/tire-calc', icon: '🛞', gate: 'free' },
  { id: 'maintenance-cost', name: 'Maintenance Cost Estimator', route: '/tools/maintenance-cost', icon: '💰', gate: 'free' },
  { id: 'fuel-economy', name: 'Fuel Economy Calculator', route: '/tools/fuel-economy', icon: '📊', gate: 'free' },
  { id: 'obd-reference', name: 'OBD Live Data Reference', route: '/tools/obd-reference', icon: '📡', gate: 'free' },
  { id: 'emergency', name: 'Emergency Roadside Guide', route: '/tools/emergency', icon: '🆘', gate: 'free' },
  { id: 'schedule-builder', name: 'Maintenance Schedule Builder', route: '/tools/schedule-builder', icon: '📅', gate: 'free' },
  { id: 'service-export', name: 'Service History Export', route: '/tools/service-export', icon: '📤', gate: 'pro' },
  { id: 'ai-chat', name: 'AI Diagnostic Chat', route: '/ai-chat', icon: '🤖', gate: 'free', badge: 'AI Powered' },
];

// --- Tiers ---
export const TIERS = {
  free: {
    id: 'free',
    name: 'Free',
    price: 0,
    aiLimit: 3,
    vehicleLimit: 1,
    features: [
      'All 41 diagnostic tools',
      'AI Chat — 3 queries/day',
      '1 vehicle in garage',
      'Community forum access',
      'Blog access',
    ],
  },
  premium: {
    id: 'premium',
    name: 'Premium',
    monthlyPrice: 9.99,
    annualPrice: 7.99,
    aiLimit: 20,
    vehicleLimit: 3,
    trialDays: 7,
    color: '#8B5CF6',
    features: [
      'Everything in Free',
      'AI Chat — 20 queries/day',
      '3 vehicles in garage',
      'Morning brief emails',
      'PREMIUM forum badge',
      '7-day free trial',
    ],
  },
  pro: {
    id: 'pro',
    name: 'Pro',
    monthlyPrice: 19.99,
    annualPrice: 15.99,
    aiLimit: Infinity,
    vehicleLimit: Infinity,
    color: '#F59E0B',
    features: [
      'Everything in Premium',
      'AI Chat — Unlimited',
      'Unlimited vehicles',
      'Wiring diagrams',
      'Torque sequences',
      'Service history export',
      'PRO forum badge',
    ],
  },
};

// --- Gated Routes (require specific tier) ---
export const GATED_ROUTES = {
  '/harley/wiring': 'pro',
  '/harley/torque': 'pro',
  '/ebike/wiring': 'pro',
  '/tools/service-export': 'pro',
};

// --- Theme ---
export const THEME = {
  background: '#0A0A0B',
  surface: '#111113',
  border: '#1E1E21',
  textPrimary: '#F5F5F6',
  textSecondary: '#C4C4CE',
  textMuted: '#8E8E9A',
  textDim: '#6B6B76',
  textFaint: '#4A4A55',
};

// --- Navigation Sections ---
export const NAV_SECTIONS = [
  {
    title: 'Home',
    items: [
      { name: 'Dashboard', route: '/dashboard', icon: '📊' },
      { name: 'AI Chat', route: '/ai-chat', icon: '🤖' },
      { name: 'My Garage', route: '/garage', icon: '🏠' },
    ],
  },
  {
    title: 'Harley-Davidson',
    platform: 'harley',
    items: [
      { name: 'DTC Database', route: '/harley/dtc', icon: '🔧' },
      { name: 'Diagnostic Flowcharts', route: '/harley/flowcharts', icon: '🔀' },
      { name: 'Service Reference', route: '/harley/service', icon: '📋' },
      { name: 'Common Problems', route: '/harley/problems', icon: '⚠️' },
      { name: 'Wiring Diagrams', route: '/harley/wiring', icon: '⚡', gate: 'pro' },
      { name: 'Torque Sequences', route: '/harley/torque', icon: '🔩', gate: 'pro' },
      { name: 'Morning Brief', route: '/harley/morning-brief', icon: '☀️' },
    ],
  },
  {
    title: 'Automotive',
    platform: 'auto',
    items: [
      { name: 'DTC Database', route: '/auto/dtc', icon: '🔧' },
      { name: 'Diagnostic Flowcharts', route: '/auto/flowcharts', icon: '🔀' },
      { name: 'Recalls & TSBs', route: '/auto/recalls', icon: '📢' },
      { name: 'Fluid Color Guide', route: '/auto/fluid-guide', icon: '🎨' },
      { name: 'Morning Brief', route: '/auto/morning-brief', icon: '☀️' },
    ],
  },
  {
    title: 'Trucking',
    platform: 'trucking',
    items: [
      { name: 'HOS Tracker', route: '/trucking/hos', icon: '⏱️' },
      { name: 'Pre-Trip Checklist', route: '/trucking/pretrip', icon: '✅' },
      { name: 'Profit Calculator', route: '/trucking/profit', icon: '💵' },
      { name: 'IFTA Generator', route: '/trucking/ifta', icon: '📄' },
      { name: 'Axle Weight Calc', route: '/trucking/axle-weight', icon: '⚖️' },
      { name: 'Calculator Suite', route: '/trucking/calculators', icon: '🧮' },
      { name: 'Morning Brief', route: '/trucking/morning-brief', icon: '☀️' },
    ],
  },
  {
    title: 'E-Bike',
    platform: 'ebike',
    items: [
      { name: 'Error Codes', route: '/ebike/errors', icon: '🔧' },
      { name: 'Diagnostic Flowcharts', route: '/ebike/flowcharts', icon: '🔀' },
      { name: 'Battery & Range', route: '/ebike/battery', icon: '🔋' },
      { name: 'Class & Law Ref', route: '/ebike/laws', icon: '📜' },
      { name: 'Wiring Diagrams', route: '/ebike/wiring', icon: '⚡', gate: 'pro' },
      { name: 'Build Calculator', route: '/ebike/build', icon: '🛠️' },
      { name: 'Morning Brief', route: '/ebike/morning-brief', icon: '☀️' },
    ],
  },
  {
    title: 'Scooter',
    platform: 'scooter',
    items: [
      { name: 'Error Codes', route: '/scooter/errors', icon: '🔧' },
      { name: 'Diagnostic Flowcharts', route: '/scooter/flowcharts', icon: '🔀' },
      { name: 'Maintenance Guide', route: '/scooter/maintenance', icon: '🔧' },
      { name: 'Comparison Calc', route: '/scooter/compare', icon: '⚖️' },
      { name: 'Morning Brief', route: '/scooter/morning-brief', icon: '☀️' },
    ],
  },
  {
    title: 'Universal Tools',
    items: UNIVERSAL_TOOLS.filter(t => t.id !== 'ai-chat').map(t => ({
      name: t.name,
      route: t.route,
      icon: t.icon,
      gate: t.gate !== 'free' ? t.gate : undefined,
    })),
  },
];

// --- All Routes (for sitemap) ---
export const ALL_ROUTES = [
  '/',
  '/pricing',
  '/blog',
  '/community',
  '/tools',
  '/harley',
  '/harley/dtc',
  '/harley/flowcharts',
  '/harley/service',
  '/harley/problems',
  '/harley/wiring',
  '/harley/torque',
  '/harley/morning-brief',
  '/auto',
  '/auto/dtc',
  '/auto/flowcharts',
  '/auto/recalls',
  '/auto/fluid-guide',
  '/auto/morning-brief',
  '/trucking',
  '/trucking/hos',
  '/trucking/pretrip',
  '/trucking/profit',
  '/trucking/ifta',
  '/trucking/axle-weight',
  '/trucking/calculators',
  '/trucking/morning-brief',
  '/ebike',
  '/ebike/errors',
  '/ebike/flowcharts',
  '/ebike/battery',
  '/ebike/laws',
  '/ebike/wiring',
  '/ebike/build',
  '/ebike/morning-brief',
  '/scooter',
  '/scooter/errors',
  '/scooter/flowcharts',
  '/scooter/maintenance',
  '/scooter/compare',
  '/scooter/morning-brief',
  '/tools/parts',
  '/tools/converter',
  '/tools/fuel-log',
  '/tools/tire-calc',
  '/tools/maintenance-cost',
  '/tools/fuel-economy',
  '/tools/obd-reference',
  '/tools/emergency',
  '/tools/schedule-builder',
  '/tools/service-export',
];
