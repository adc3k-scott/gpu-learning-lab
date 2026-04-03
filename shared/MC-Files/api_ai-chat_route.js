import { NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

// In-memory rate limiting (upgrade to Redis/Upstash in Week 2)
const rateLimitMap = new Map();

const SYSTEM_PROMPTS = {
  harley: `You are Mission Control's Harley-Davidson diagnostic expert. You help riders diagnose issues with their Harley-Davidson motorcycles. You know DTC codes (P-codes, B-codes, U-codes), common problems by model year, service intervals, fluid capacities, torque specs, wiring diagrams concepts, and troubleshooting flowcharts. Be specific about Harley models (Sportster, Softail, Touring, etc.) and reference Twin Cam, Milwaukee-Eight, Evolution, and Revolution Max engines as appropriate. Always recommend safety precautions.`,

  auto: `You are Mission Control's automotive diagnostic expert. You help car owners understand OBD-II codes, diagnose check engine lights, interpret live data PIDs, understand recalls and TSBs, identify fluid leaks by color, and plan maintenance schedules. Cover all major makes and models. Reference specific systems (EVAP, EGR, catalytic converter, O2 sensors, etc.) and provide clear repair guidance. Always mention when a professional mechanic should be consulted.`,

  trucking: `You are Mission Control's CDL trucking expert. You help commercial drivers with Hours of Service regulations (FMCSA), pre-trip/post-trip inspections, IFTA fuel tax reporting, axle weight distribution, load planning, DOT compliance, ELD requirements, and profit/cost-per-mile calculations. Know the difference between property and passenger carrier rules. Reference current FMCSA regulations and common roadside inspection items.`,

  ebike: `You are Mission Control's e-bike expert. You help e-bike riders with error codes (Bosch, Shimano, Bafang, and generic), battery health and range optimization, motor diagnostics, controller issues, display problems, and state-by-state classification laws (Class 1/2/3). Cover both hub motors and mid-drive systems. Help with build calculations for custom e-bikes. Always mention safety and local regulations.`,

  scooter: `You are Mission Control's electric scooter expert. You help scooter riders diagnose error codes, plan maintenance schedules, troubleshoot common issues (battery, motor, controller, brakes, tires), and compare scooter models. Cover popular brands like Segway Ninebot, Xiaomi, Apollo, Kaabo, VSETT, and others. Discuss range, speed, waterproofing, tire types, and safety gear.`,
};

// Rate limit check: 10 requests per minute per IP
function checkIPRateLimit(ip) {
  const now = Date.now();
  const windowMs = 60 * 1000; // 1 minute
  const limit = 10;

  if (!rateLimitMap.has(ip)) {
    rateLimitMap.set(ip, []);
  }

  const timestamps = rateLimitMap.get(ip).filter((t) => now - t < windowMs);
  rateLimitMap.set(ip, timestamps);

  if (timestamps.length >= limit) {
    return false;
  }

  timestamps.push(now);
  return true;
}

// Clean up old entries every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [ip, timestamps] of rateLimitMap.entries()) {
    const recent = timestamps.filter((t) => now - t < 60000);
    if (recent.length === 0) {
      rateLimitMap.delete(ip);
    } else {
      rateLimitMap.set(ip, recent);
    }
  }
}, 5 * 60 * 1000);

export async function POST(request) {
  try {
    // Check API key
    if (!process.env.ANTHROPIC_API_KEY) {
      return NextResponse.json(
        { error: 'AI chat is not configured. Please add ANTHROPIC_API_KEY.' },
        { status: 503 }
      );
    }

    // IP rate limiting
    const ip = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown';
    if (!checkIPRateLimit(ip)) {
      return NextResponse.json(
        { error: 'Too many requests. Please wait a moment and try again.' },
        { status: 429 }
      );
    }

    const body = await request.json();
    const { message, platform = 'harley', history = [] } = body;

    // Validation
    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Message is required.' },
        { status: 400 }
      );
    }

    if (message.length > 2000) {
      return NextResponse.json(
        { error: 'Message is too long. Maximum 2,000 characters.' },
        { status: 400 }
      );
    }

    const systemPrompt = SYSTEM_PROMPTS[platform] || SYSTEM_PROMPTS.harley;

    // Build messages array from history
    const messages = [];
    if (Array.isArray(history)) {
      history.slice(-10).forEach((msg) => {
        if (msg.role && msg.content) {
          messages.push({
            role: msg.role === 'user' ? 'user' : 'assistant',
            content: String(msg.content).slice(0, 2000),
          });
        }
      });
    }
    messages.push({ role: 'user', content: message });

    const startTime = Date.now();

    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      system: systemPrompt,
      messages,
    });

    const latencyMs = Date.now() - startTime;
    const reply = response.content[0]?.text || 'I apologize, but I was unable to generate a response.';

    return NextResponse.json({
      reply,
      platform,
      tokens: {
        input: response.usage?.input_tokens || 0,
        output: response.usage?.output_tokens || 0,
      },
      latencyMs,
    });
  } catch (error) {
    console.error('AI Chat error:', error);

    if (error?.status === 429) {
      return NextResponse.json(
        { error: 'AI service is busy. Please try again in a moment.' },
        { status: 429 }
      );
    }

    return NextResponse.json(
      { error: 'Something went wrong with the AI chat. Please try again.' },
      { status: 500 }
    );
  }
}
