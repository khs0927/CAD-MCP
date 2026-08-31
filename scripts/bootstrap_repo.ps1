# CAD-MCP Repository Bootstrap & Environment Setup Script
# Sets up C:\cad-mcp structure, clones upstreams, and initializes the CAD-MCP workspace repository.

param (
    [string]$RootDir = "C:\cad-mcp",
    [switch]$SkipClone = $false
)

$ErrorActionPreference = "Continue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         CAD-MCP Repository Bootstrap & Setup               " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Directories
$WorkspaceDir = Join-Path $RootDir "workspace\CAD-MCP"
$UpstreamsDir = Join-Path $RootDir "upstreams"

Write-Host "`n[1/4] Ensuring Directory Structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $WorkspaceDir, $UpstreamsDir | Out-Null
Write-Host "  Workspace: $WorkspaceDir" -ForegroundColor Green
Write-Host "  Upstreams: $UpstreamsDir" -ForegroundColor Green

# 2. Clone Upstreams if not skipped
if (-not $SkipClone) {
    Write-Host "`n[2/4] Cloning / Updating Upstream Repositories..." -ForegroundColor Yellow
    $repos = @(
        @{ name = "multiCAD-mcp"; url = "https://github.com/AnCode666/multiCAD-mcp.git" },
        @{ name = "zwcad-standard-mcp"; url = "https://github.com/qwtao321/zwcad-standard-mcp.git" },
        @{ name = "ZWCAD-MCP"; url = "https://github.com/dalingo81/ZWCAD-MCP.git" },
        @{ name = "ZWCAD-Platform-MCP"; url = "https://github.com/Jerri-Z/ZWCAD-Platform-MCP.git" },
        @{ name = "kenchiku-mcp"; url = "https://github.com/Sora-bluesky/kenchiku-mcp.git" },
        @{ name = "ZWCAD-Mechanical-MCP"; url = "https://github.com/john0909/ZWCAD-Mechanical-MCP.git" },
        @{ name = "zwcad-mcp-server"; url = "https://github.com/petem903/zwcad-mcp-server.git" },
        @{ name = "zwcad-control-mcp"; url = "https://github.com/Whfkl/zwcad-control-mcp.git" },
        @{ name = "Autocad-MCP"; url = "https://github.com/U-C4N/Autocad-MCP.git" }
    )

    foreach ($r in $repos) {
        $target = Join-Path $UpstreamsDir $r.name
        if (Test-Path $target) {
            $sha = git -C $target rev-parse HEAD 2>$null
            Write-Host "  $($r.name): Already cloned ($($sha.Substring(0,8)))" -ForegroundColor Gray
        } else {
            Write-Host "  Cloning $($r.name)..." -ForegroundColor White
            git clone --depth 1 $r.url $target
        }
    }
}

# 3. Generate Test Fixture
Write-Host "`n[3/4] Generating Architectural Fixture..." -ForegroundColor Yellow
$fixtureScript = Join-Path $WorkspaceDir "scripts\generate_fixtures.py"
if (Test-Path $fixtureScript) {
    python $fixtureScript
}

# 4. Git Initialization in Workspace
Write-Host "`n[4/4] Verifying Git Repository in Workspace..." -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $WorkspaceDir ".git"))) {
    Write-Host "  Initializing git repository in $WorkspaceDir..." -ForegroundColor White
    git -C $WorkspaceDir init
    git -C $WorkspaceDir branch -M main
} else {
    Write-Host "  Git repository already initialized." -ForegroundColor Green
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "CAD-MCP Bootstrap Completed Successfully!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
