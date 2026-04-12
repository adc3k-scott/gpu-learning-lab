// ROXY Rate Limiter — In-memory, per-IP, 20 req/min

const rateMap = new Map();
const RATE_LIMIT = 20;
const RATE_WINDOW = 60 * 1000;

function isRateLimited(ip) {
  const now = Date.now();
  if (!rateMap.has(ip)) {
    rateMap.set(ip, []);
  }
  const timestamps = rateMap.get(ip).filter((t) => now - t < RATE_WINDOW);
  rateMap.set(ip, timestamps);
  if (timestamps.length >= RATE_LIMIT) {
    return true;
  }
  timestamps.push(now);
  return false;
}

// Clean up stale entries every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [ip, timestamps] of rateMap.entries()) {
    const fresh = timestamps.filter((t) => now - t < RATE_WINDOW);
    if (fresh.length === 0) {
      rateMap.delete(ip);
    } else {
      rateMap.set(ip, fresh);
    }
  }
}, 5 * 60 * 1000);

module.exports = { isRateLimited };
