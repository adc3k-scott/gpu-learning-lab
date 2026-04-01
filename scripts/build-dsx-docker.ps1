# build-dsx-docker.ps1
# Builds scottay007/dsx-kit:v3 entirely inside Docker Desktop.
# No WSL required. Run this from the gpu-learning-lab directory.
#
# Usage: .\scripts\build-dsx-docker.ps1
#
# BEFORE RUNNING:
#   1. Docker Desktop must be open and running
#   2. Set Docker Desktop RAM to 16GB: Settings > Resources > Advanced > Memory
#   3. Ensure 50GB+ free disk space
#   4. You need internet access (NVIDIA CDN downloads)

$ErrorActionPreference = "Stop"
$DOCKERHUB_USER = "scottay007"
$DOCKERHUB_PASS = "SuperBugsbun4!"
$IMAGE = "scottay007/dsx-kit:v3"
$DOCKERFILE = "$PSScriptRoot\Dockerfile.dsx-build"

Write-Host "=== DSX Docker Build ===" -ForegroundColor Cyan
Write-Host "Image: $IMAGE"
Write-Host "Dockerfile: $DOCKERFILE"
Write-Host ""

# Check Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker Desktop is not running. Start it first." -ForegroundColor Red
    exit 1
}
Write-Host "Docker OK" -ForegroundColor Green

# Check memory allocation
$dockerInfo = docker system info --format "{{.MemTotal}}" 2>&1
Write-Host "Docker VM memory: $([math]::Round([long]$dockerInfo / 1GB, 1)) GB"
if ([long]$dockerInfo -lt 12GB) {
    Write-Host "WARNING: Docker has less than 12GB RAM. DSX build may fail." -ForegroundColor Yellow
    Write-Host "Set it in Docker Desktop: Settings > Resources > Advanced > Memory" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") { exit 1 }
}

Write-Host ""
Write-Host "Starting docker build — this takes 20-40 minutes..." -ForegroundColor Cyan
Write-Host "Docker layer cache means restarts are fast if it fails partway."
Write-Host ""

# Build using stdin (no build context — all source is cloned inside the container)
Get-Content $DOCKERFILE | docker build `
    --tag $IMAGE `
    --progress plain `
    -

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "BUILD FAILED. Check output above for errors." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "BUILD SUCCEEDED: $IMAGE" -ForegroundColor Green

# Test the image before pushing
Write-Host ""
Write-Host "Testing image (should stay alive, not exit in < 5 seconds)..." -ForegroundColor Yellow
$job = Start-Job -ScriptBlock {
    param($img)
    docker run --rm --name dsx-test $img sleep 10 2>&1
} -ArgumentList $IMAGE

Start-Sleep -Seconds 6
$running = docker ps --filter "name=dsx-test" --format "{{.Names}}" 2>&1
if ($running -match "dsx-test") {
    Write-Host "Container alive after 6 seconds — GOOD" -ForegroundColor Green
    docker stop dsx-test 2>&1 | Out-Null
} else {
    Write-Host "WARNING: Container exited in under 6 seconds — may be broken" -ForegroundColor Yellow
    Write-Host "Check with: docker run --rm $IMAGE"
}
Stop-Job $job | Out-Null
Remove-Job $job | Out-Null

# Push to DockerHub
Write-Host ""
Write-Host "Pushing to DockerHub..." -ForegroundColor Yellow
echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin
docker push $IMAGE

if ($LASTEXITCODE -ne 0) {
    Write-Host "PUSH FAILED." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host "Image pushed: $IMAGE"
Write-Host ""
Write-Host "Next step: Deploy to RunPod via UI"
Write-Host "  Image: $IMAGE"
Write-Host "  GPU: L40S or RTX PRO 6000"
Write-Host "  Container disk: 100GB"
Write-Host "  Volume: 150GB"
Write-Host "  Ports: 22/tcp, 49100/tcp, 8080/tcp, 8111/tcp"
Write-Host "  Env vars:"
Write-Host "    NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute"
Write-Host "    NVIDIA_API_KEY=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"
Write-Host "    USD_URL=/workspace/content/DSX_BP/Assembly/DSX_Main_BP.usda"
