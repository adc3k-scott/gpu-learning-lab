# RunPod API Integration Notes
*Notion backup — 2026-03-28*

> Mission Control manages RunPod cloud GPU pods via GraphQL API. IntegrationAgent dispatches via runpod skill. When MARLIE I goes live, on-prem racks replace RunPod cloud as primary.
---
## Current Setup — RunPod Cloud
- Endpoint: https://api.runpod.io/graphql
- Auth: Bearer token — RUNPOD_API_KEY in .venv/.env
- Skill: skills/builtin/runpod.py — list / start / stop / terminate
- Planner patterns: list pods | pod status | start pod | stop pod | terminate pod
---
## GraphQL Operations
### List Pods
```graphql
query {
  myself {
    pods {
      id name status
      runtime { uptimeInSeconds gpus { id gpuUtilPercent } }
      machine { gpuDisplayName }
    }
  }
}
```
### Start Pod
```graphql
mutation {
  podResume(input: { podId: "POD_ID", gpuCount: 1 }) {
    id status
  }
}
```
### Stop Pod
```graphql
mutation {
  podStop(input: { podId: "POD_ID" }) {
    id status
  }
}
```
---
## Mission Control Flow
- Chat trigger: "list pods" / "start pod XYZ" / "stop pod XYZ"
- Planner: Regex fast-path -> IntegrationAgent -> runpod skill
- SSE stream: /tasks/{id}/stream — live step events during pod ops
- Dashboard: Mission Control HQ at http://localhost:8000
---
## MARLIE I Transition Plan (H2 2026)
> When NVL72 racks go live, on-prem becomes primary. RunPod cloud is overflow. Mission Control routes by cost/latency/availability.
- Phase 1 (now): RunPod cloud — dev/test workloads
- Phase 2 (H2 2026): MARLIE I on-prem — production inference + training
- Phase 3: Hybrid routing — Mission Control schedules across on-prem + cloud
---
## On-Prem API Design (Future)
- Protocol: OpenAI-compatible REST — drop-in for cloud providers
- Auth: API key per customer — managed by Mission Control
- Billing: Per-GPU-hour metering via PDU current sensors
- Scheduler: OrchestratorAgent — job queue, priority, multi-tenant isolation
```plain text
POST /v1/chat/completions    -- inference
POST /v1/embeddings         -- embeddings
GET  /v1/models             -- available models
GET  /v1/pods               -- active compute pods (internal)
POST /v1/jobs               -- batch job submission
```
---
> UPDATED 2026-03-23 -- POST-GTC REWRITE
RunPod remains the cloud GPU provider for Phase 0 (pre-facility). The existing GraphQL integration and Mission Control planner patterns are still valid.
### Current Status:
- RunPod balance: ~$184
- Network volume: aido-workspace (250GB, US-TX-3)
- Active pod: ml4cl3icn37ys1 (L40S, EXITED)
- Image gen endpoints: FLUX Schnell + Kontext (live on RunPod Hub)
### Transition Plan (unchanged):
- Phase 0: RunPod cloud (NOW)
- Phase 1: On-prem at MARLIE I (H2 2026 when Vera Rubin ships Dec 2026)
- Phase 2: Hybrid (Willow Glen primary + RunPod overflow)
- Phase 3: Full on-prem fleet (Willow Glen + MARLIE I + pods)
### Fleet Management Stack:
- NVIDIA Run:AI -- workload orchestration across all on-prem nodes
- NVIDIA Dynamo 1.0 -- inference optimization (7x performance boost)
- NVIDIA Base Command Manager -- cluster lifecycle management
- Mission Control AI (ADC-built) -- autonomous operations, monitoring, SSE dashboard
- NVIDIA Mission Control (HPE offering) -- available 2026, evaluate for integration