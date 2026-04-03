# NVIDIA Run:AI -- Real Product UI Screenshots Reference

Compiled: 2026-03-25
Purpose: Real product screenshots for ADC investor materials and operations pages.
All images are from official NVIDIA sources. Use with proper attribution.

---

## 1. NVIDIA Run:AI Documentation Screenshots (docs.run.ai v2.20)

Base URL for relative paths: `https://docs.run.ai/v2.20/platform-admin/performance/`

### Dashboard Analysis Page
Source: https://docs.run.ai/v2.20/platform-admin/performance/dashboard-analysis/
Also available at: https://docs.run.ai/v2.17/admin/admin-ui-setup/dashboard-analysis/

| # | Image Path (relative to page) | Full URL (v2.17) | What It Shows | Type |
|---|-------------------------------|-------------------|---------------|------|
| 1 | `../img/node-downtime.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/node-downtime.png | **Node Downtime** -- Overall available resources per node, uptime/downtime visualization | Real UI screenshot |
| 2 | `../img/gpu-allocation.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/gpu-allocation.png | **GPU Allocation** -- Cluster-wide GPU allocation and utilization vs time chart | Real UI screenshot |
| 3 | `../img/gpu-utilization.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/gpu-utilization.png | **GPU Utilization** -- Tracks researcher GPU utilization efficiency over time | Real UI screenshot |
| 4 | `../img/training-interactive.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/training-interactive.png | **Training vs Interactive** -- Breakdown of running workloads by type (training, interactive, CPU-only) | Real UI screenshot |
| 5 | `../img/pending-jobs.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/pending-jobs.png | **Pending Queue Size** -- Workload scheduling queue showing pending jobs over time | Real UI screenshot |
| 6 | `../img/cpu-utilization.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/cpu-utilization.png | **CPU & Memory Utilization** -- Node-level CPU and memory usage metrics | Real UI screenshot |
| 7 | `../img/multi-cluster-overview.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/multi-cluster-overview.png | **Multi-Cluster Overview** -- Aggregated dashboard showing all connected clusters at a glance | Real UI screenshot |
| 8 | `../img/consumption-dashboard.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/consumption-dashboard.png | **Consumption Dashboard** -- Resource consumption tracking for cost/chargeback analysis | Real UI screenshot |
| 9 | `../img/consumption-dashboard-time-picker.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/consumption-dashboard-time-picker.png | **Time Range Picker** -- Dashboard time selection controls | Real UI screenshot |
| 10 | `../img/consumption-dashboard-gpu-over-time.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/consumption-dashboard-gpu-over-time.png | **GPU Over Time** -- GPU allocation timeline visualization for consumption tracking | Real UI screenshot |
| 11 | `../img/consumption-dashboard-project-over-quota-graph.png` | https://docs.run.ai/v2.17/admin/admin-ui-setup/img/consumption-dashboard-project-over-quota-graph.png | **Project Over-Quota** -- Per-project GPU consumption showing quota exceeded periods | Real UI screenshot |

### Workloads Management Page
Source: https://docs.run.ai/v2.20/Researcher/workloads/overviews/managing-workloads/

| # | Image Path | Full URL (v2.17) | What It Shows | Type |
|---|-----------|-------------------|---------------|------|
| 12 | `../img/workload-table.png` | https://docs.run.ai/v2.20/Researcher/workloads/overviews/img/workload-table.png | **Workloads Table** -- Full list of scheduled workloads with name, project, user, type, status, GPU allocation, runtime, and utilization columns | Real UI screenshot |

### Departments / Org Management
Source: https://docs.run.ai/v2.20/platform-admin/aiinitiatives/org/departments/

| # | Image Path | What It Shows | Type |
|---|-----------|---------------|------|
| 13 | `../img/department-list.png` | **Departments Table** -- Organizational hierarchy showing departments, node pools, GPU quotas, projects, allocated GPUs, allocation ratio | Real UI screenshot |
| 14 | `../img/quota-mgmt.png` | **Quota Management** -- Configuration panel for GPU devices, CPU cores, and memory allocation per department | Real UI screenshot |

### Nodes / Cluster Resources
Source: https://docs.run.ai/v2.20/platform-admin/aiinitiatives/resources/nodes/

| # | Image Path | What It Shows | Type |
|---|-----------|---------------|------|
| 15 | `../img/node-list.png` | **Nodes Table** -- List of cluster nodes with GPU types, status, and resource metrics | Real UI screenshot |

### Multi-Cluster Architecture
Source: https://docs.run.ai/v2.20/home/overview/

| # | Image Path | What It Shows | Type |
|---|-----------|---------------|------|
| 16 | `../img/multi-cluster.png` | **Architecture Diagram** -- Control plane and cluster relationship topology | Architecture diagram |

---

## 2. NVIDIA Run:AI on SaaS Docs (run-ai-docs.nvidia.com)

### Workloads Table (Newer UI)
Source: https://run-ai-docs.nvidia.com/saas/workloads-in-nvidia-run-ai/workloads

| # | Full URL | What It Shows | Type |
|---|----------|---------------|------|
| 17 | https://3278325112-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FLiY1aIqfxD3a58ufUYOM%2Fuploads%2FuUGaSJjxXAw2t2YnoGtL%2Fvia-Yaml-submission.png?alt=media&token=a705e239-1301-4b43-9409-96594cfc55ca | **Workloads Table (SaaS version)** -- Latest UI showing scheduled workloads on the Run:AI scheduler | Real UI screenshot |

---

## 3. NVIDIA Developer Blog -- Azure Integration (January 2026)

Source: https://developer.nvidia.com/blog/streamline-ai-infrastructure-with-nvidia-runai-on-microsoft-azure
**HIGH VALUE -- These are the best control-room-style screenshots.**

| # | Full URL | What It Shows | Type |
|---|----------|---------------|------|
| 18 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/10/image7-2-png.webp | **Overview Dashboard** -- Real-time cluster metrics: GPU availability, active workloads, pending tasks, node resources. THE "control room" view. | Real UI screenshot |
| 19 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/10/image5-2-png.webp | **Node Management** -- AKS cluster nodes showing heterogeneous GPU environment (H100 + A100 in same cluster) | Real UI screenshot |
| 20 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/10/image2-2-png.webp | **Node Pools** -- Node pool configuration aligned with scale sets for contextual workload scheduling | Real UI screenshot |
| 21 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/10/image8-png.webp | **Team GPU Allocation** -- GPU resource distribution across teams using projects/quotas with baseline guarantees and burst capabilities | Real UI screenshot |
| 22 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/10/image4-4-png.webp | **Workload Management** -- Running workloads with type, status, and GPU allocation metrics | Real UI screenshot |
| 23 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/10/figure-6-runai-png.webp | **Usage Analytics** -- GPU utilization graphs over time for chargeback and capacity planning | Real UI screenshot |

---

## 4. NVIDIA Developer Blog -- AWS Integration (July 2025)

Source: https://developer.nvidia.com/blog/accelerate-ai-model-orchestration-with-nvidia-runai-on-aws

| # | Full URL | What It Shows | Type |
|---|----------|---------------|------|
| 24 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/run-aws-1-png.webp | **Architecture Diagram** -- System components of Run:AI integration with AWS (EC2, EKS, control plane) | Architecture diagram |
| 25 | https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/run-aws-2-png.webp | **Run:AI Dashboard on AWS** -- GPU utilization metrics and visibility into consumption across workloads/teams | Real UI screenshot |

---

## 5. NVIDIA Product Pages (nvidia.com)

### Run:AI Product Page
Source: https://www.nvidia.com/en-us/software/run-ai/

| # | Full URL | What It Shows | Type |
|---|----------|---------------|------|
| 26 | https://www.nvidia.com/content/nvidiaGDC/us/en_US/software/run-ai/_jcr_content/root/responsivegrid/nv_container_1738623837/nv_image.coreimg.jpeg/1773320652870/run-ai-ui-1920x1455.jpeg | **Hero Dashboard Screenshot** -- Primary Run:AI platform interface showing centralized management, workflow visualization, orchestration controls. HIGH RESOLUTION (1920x1455). | Real UI screenshot / marketing render |

### NVIDIA Mission Control Product Page
Source: https://www.nvidia.com/en-us/data-center/mission-control/

| # | Full URL | What It Shows | Type |
|---|----------|---------------|------|
| 27 | https://www.nvidia.com/content/nvidiaGDC/us/en_US/data-center/mission-control/_jcr_content/root/responsivegrid/nv_container_284191847/nv_image.coreimg.jpeg/1773696358366/mission-control-dashboard-ari.jpeg | **Mission Control 2.3 Dashboard** -- Cluster-level operations and workload management visualization | Real UI screenshot / marketing render |

### NVIDIA Mission Control Blog
Source: https://blogs.nvidia.com/blog/mission-control-software/

| # | Full URL | What It Shows | Type |
|---|----------|---------------|------|
| 28 | https://blogs.nvidia.com/wp-content/uploads/2025/03/gtc25-corp-blog-nvidia-mission-control-1280x680-1.jpg | **Mission Control Hero** -- Blog header image for Mission Control announcement | Marketing graphic |

---

## 6. DGX Cloud + Run:AI Documentation

Source: https://docs.nvidia.com/dgx-cloud/run-ai/latest/overview.html

| # | Image Path | What It Shows | Type |
|---|-----------|---------------|------|
| 29 | `_images/stack1.png` | **DGX Cloud Stack Diagram** -- Layered architecture of Run:AI on DGX Cloud | Architecture diagram |
| 30 | `_images/arch-diag.png` | **Architecture & Management Model** -- Kubernetes cluster, CSP infrastructure, NVIDIA SaaS control plane relationships | Architecture diagram |
| 31 | `_images/dept-projects1.png` | **Departments & Projects** -- Organizational hierarchy with departments, projects, and user access assignments | Real UI diagram |

---

## 7. NVIDIA Mission Control Observability -- Grafana Dashboards

Source: https://docs.nvidia.com/mission-control/docs/systems-administration-guide/2.2.0/observability.html
Base URL: `https://docs.nvidia.com/mission-control/docs/systems-administration-guide/2.2.0/`

These are animated GIFs showing actual Grafana dashboard configuration for GPU cluster monitoring.

| # | Image Path | What It Shows | Type |
|---|-----------|---------------|------|
| 32 | `_images/grafana-login-screen.gif` | **Grafana Login** -- Authentication interface | Real UI (animated) |
| 33 | `_images/grafana-explore-interface.gif` | **Grafana Explore** -- Query editor running "memorytotal" metric | Real UI (animated) |
| 34 | `_images/grafana-metric-browser.gif` | **Metric Browser** -- GPU metrics labeled with BCM exporter job values | Real UI (animated) |
| 35 | `_images/grafana-new-dashboard.gif` | **Create Dashboard** -- Creating a new GPU monitoring dashboard | Real UI (animated) |
| 36 | `_images/grafana-select-prometheus.gif` | **Prometheus Data Source** -- Selecting Prometheus for GPU metrics | Real UI (animated) |
| 37 | `_images/grafana-status-history.gif` | **Device Status History** -- Status history visualization with devicestatus metric (GPU health over time) | Real UI (animated) |
| 38 | `_images/grafana-value-mappings.gif` | **Value Mappings** -- Green=healthy, red=fault GPU status indicators | Real UI (animated) |

---

## Priority Picks for ADC Investor Materials

### Tier 1 -- Must Use (the money shots)
1. **#26** -- Run:AI hero dashboard (1920x1455, highest resolution, shows the full platform)
2. **#18** -- Overview Dashboard from Azure blog (real-time cluster metrics, "control room" feel)
3. **#27** -- Mission Control 2.3 dashboard (the full operations picture)
4. **#22** -- Workload Management (jobs running with GPU allocation)
5. **#21** -- Team GPU Allocation (projects, quotas, burst -- shows governance)

### Tier 2 -- Strong Supporting
6. **#23** -- Usage Analytics (GPU utilization over time -- proves efficiency)
7. **#19** -- Node Management (heterogeneous GPU fleet -- H100 + A100)
8. **#7** -- Multi-Cluster Overview (shows scale across locations)
9. **#2** -- GPU Allocation chart (utilization vs time)
10. **#12** -- Workloads Table (the scheduler in action)

### Tier 3 -- Technical Depth
11. **#37** -- Grafana device status history (GPU health monitoring)
12. **#5** -- Pending Queue (shows demand management)
13. **#8** -- Consumption Dashboard (chargeback/billing)
14. **#13** -- Departments Table (enterprise org structure)

---

## Attribution Template

When using these screenshots in investor materials:

> Screenshot from NVIDIA Run:AI GPU orchestration platform.
> Source: [URL]. Used with attribution per NVIDIA documentation terms.

For Mission Control screenshots:

> Screenshot from NVIDIA Mission Control AI factory management software.
> Source: [URL]. Used with attribution per NVIDIA documentation terms.

---

## Notes

- All URLs verified accessible as of 2026-03-25
- docs.run.ai image paths are relative -- full URLs constructed by prepending the page base URL
- developer-blogs.nvidia.com images are absolute URLs (direct access)
- nvidia.com product page images use JCR content paths (direct access)
- GitBook-hosted images (run-ai-docs.nvidia.com) use signed URLs that may expire
- The v2.17 documentation URLs are the most stable for the dashboard analysis screenshots
- Mission Control Grafana GIFs are animated -- may need to extract frames for print materials
- NetApp has Run:AI dashboard docs but returned 403 (may need direct browser access)
