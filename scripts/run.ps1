# research-assistant 一键启动脚本
# 功能：环境检查 → 构建前端（如需要）→ 启动后端
# 用法：powershell -ExecutionPolicy Bypass -File scripts/run.ps1

# 切换到项目根目录（脚本所在目录的上一级）
Set-Location (Split-Path -Parent $PSScriptRoot)

# 显示启动横幅
Write-Host ""
Write-Host "=== research-assistant 启动 ===" -ForegroundColor Cyan
Write-Host ""

# 第 1 步：环境检查
Write-Host "[1/3] 环境检查..." -ForegroundColor Yellow
# 运行 check_env.py，失败则中止
uv run python scripts/check_env.py
# $LASTEXITCODE 是上条命令的退出码，非 0 = 失败
if ($LASTEXITCODE -ne 0) {
    # 环境有问题，停止启动
    Write-Host "环境检查未通过，请先修复上述问题。" -ForegroundColor Red
    exit 1
}

# 第 2 步：检查前端是否已构建（dist 存在与否）
Write-Host "[2/3] 检查前端构建..." -ForegroundColor Yellow
$webDist = "web/dist/index.html"
if (-not (Test-Path $webDist)) {
    # dist 不存在 = 前端没构建过，需要构建
    Write-Host "前端未构建，正在构建（首次运行需要）..." -ForegroundColor Yellow
    # 进入 web 目录
    Push-Location web
    # 先确认依赖装了（node_modules 在就跳过 install）
    if (-not (Test-Path "node_modules")) {
        Write-Host "  npm install..." -ForegroundColor Yellow
        npm install
    }
    # 构建前端
    Write-Host "  npm run build..." -ForegroundColor Yellow
    npm run build
    # 回到项目根
    Pop-Location
} else {
    Write-Host "前端已构建 ✓" -ForegroundColor Green
}

# 第 3 步：启动后端
Write-Host "[3/3] 启动后端..." -ForegroundColor Yellow
Write-Host "访问 http://127.0.0.1:8000，按 Ctrl+C 停止" -ForegroundColor Green
Write-Host ""
# 启动 uvicorn（前台运行，Ctrl+C 停止）
uv run uvicorn research_assistant.main:app --reload