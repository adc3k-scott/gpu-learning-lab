// ROXY Agent Job Manager
// Every agent task gets a lifecycle: QUEUED → RUNNING → COMPLETED | FAILED | PROMOTED | ARCHIVED
// Prevents runaway processes, tracks everything, enforces boundaries.

const MAX_CONCURRENT_JOBS = 3;
const DEFAULT_TIMEOUT_MS = 25000; // 25s (leaves 5s buffer in Vercel 30s limit)

// In-memory job store (upgrade to Vercel KV later)
const jobs = new Map();
let jobCounter = 0;

const JOB_STATES = {
  QUEUED: "QUEUED",
  RUNNING: "RUNNING",
  COMPLETED: "COMPLETED",
  FAILED: "FAILED",
  PROMOTED: "PROMOTED",
  ARCHIVED: "ARCHIVED",
};

/**
 * Create a new job
 */
function createJob({ type, tools, sessionId, metadata = {} }) {
  const id = `job_${++jobCounter}_${Date.now()}`;
  const job = {
    id,
    type, // "tool_call", "training", "merge", "search"
    state: JOB_STATES.QUEUED,
    tools: tools || [],
    sessionId,
    metadata,
    createdAt: Date.now(),
    startedAt: null,
    completedAt: null,
    duration: null,
    result: null,
    error: null,
    retries: 0,
    maxRetries: metadata.maxRetries || 1,
    timeout: metadata.timeout || DEFAULT_TIMEOUT_MS,
  };
  jobs.set(id, job);
  return job;
}

/**
 * Start a job — enforces concurrency limit
 */
function startJob(jobId) {
  const job = jobs.get(jobId);
  if (!job) return null;

  // Check concurrency
  const running = Array.from(jobs.values()).filter((j) => j.state === JOB_STATES.RUNNING);
  if (running.length >= MAX_CONCURRENT_JOBS) {
    job.error = `Concurrency limit reached (${MAX_CONCURRENT_JOBS} jobs running)`;
    job.state = JOB_STATES.FAILED;
    return job;
  }

  job.state = JOB_STATES.RUNNING;
  job.startedAt = Date.now();
  return job;
}

/**
 * Complete a job
 */
function completeJob(jobId, result) {
  const job = jobs.get(jobId);
  if (!job) return null;

  job.state = JOB_STATES.COMPLETED;
  job.completedAt = Date.now();
  job.duration = job.completedAt - job.startedAt;
  job.result = result;
  return job;
}

/**
 * Fail a job — auto-retry if retries remain
 */
function failJob(jobId, error) {
  const job = jobs.get(jobId);
  if (!job) return null;

  job.retries++;
  if (job.retries < job.maxRetries) {
    // Reset to queued for retry
    job.state = JOB_STATES.QUEUED;
    job.error = `Retry ${job.retries}/${job.maxRetries}: ${error}`;
    return job;
  }

  job.state = JOB_STATES.FAILED;
  job.completedAt = Date.now();
  job.duration = job.completedAt - (job.startedAt || job.createdAt);
  job.error = error;
  return job;
}

/**
 * Run a function with job lifecycle management
 * @param {Object} opts - Job options
 * @param {Function} fn - Async function to execute
 * @returns {Object} Job result
 */
async function runWithLifecycle({ type, tools, sessionId, metadata }, fn) {
  const job = createJob({ type, tools, sessionId, metadata });
  const started = startJob(job.id);

  if (started.state === JOB_STATES.FAILED) {
    return { job: started, result: null, error: started.error };
  }

  try {
    // Race between the function and a timeout
    const result = await Promise.race([
      fn(),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error(`Job ${job.id} timed out after ${job.timeout}ms`)), job.timeout)
      ),
    ]);

    const completed = completeJob(job.id, result);
    return { job: completed, result, error: null };
  } catch (err) {
    const failed = failJob(job.id, err.message);

    // If retried, try again
    if (failed.state === JOB_STATES.QUEUED) {
      return runWithLifecycle({ type, tools, sessionId, metadata }, fn);
    }

    return { job: failed, result: null, error: err.message };
  }
}

/**
 * Get job stats for analytics
 */
function getJobStats() {
  const allJobs = Array.from(jobs.values());
  return {
    total: allJobs.length,
    queued: allJobs.filter((j) => j.state === JOB_STATES.QUEUED).length,
    running: allJobs.filter((j) => j.state === JOB_STATES.RUNNING).length,
    completed: allJobs.filter((j) => j.state === JOB_STATES.COMPLETED).length,
    failed: allJobs.filter((j) => j.state === JOB_STATES.FAILED).length,
    avgDuration: allJobs.filter((j) => j.duration).reduce((sum, j) => sum + j.duration, 0) /
      (allJobs.filter((j) => j.duration).length || 1),
    recentJobs: allJobs.slice(-10).map((j) => ({
      id: j.id,
      type: j.type,
      state: j.state,
      tools: j.tools,
      duration: j.duration,
      error: j.error,
    })),
  };
}

/**
 * Clean up old jobs (prevent memory leak)
 */
function cleanup() {
  const cutoff = Date.now() - 30 * 60 * 1000; // 30 minutes
  for (const [id, job] of jobs) {
    if (job.completedAt && job.completedAt < cutoff) {
      jobs.delete(id);
    }
    // Kill stuck running jobs
    if (job.state === JOB_STATES.RUNNING && job.startedAt < cutoff) {
      failJob(id, "Job timed out (stuck for 30+ minutes)");
    }
  }
}

// Auto-cleanup every 5 minutes
setInterval(cleanup, 5 * 60 * 1000);

module.exports = {
  JOB_STATES,
  createJob,
  startJob,
  completeJob,
  failJob,
  runWithLifecycle,
  getJobStats,
  cleanup,
};
