# GitHub Repository Setup Script
# This script helps set up the GitHub repository for the Traffic Management Agent System

Write-Host "🚀 GitHub Repository Setup for Traffic Management Agent System" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green

# Check if Git is configured
Write-Host "📋 Checking Git configuration..." -ForegroundColor Yellow
$gitUser = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitUser -or -not $gitEmail) {
    Write-Host "❌ Git not configured. Please run:" -ForegroundColor Red
    Write-Host "   git config --global user.name 'Your Name'" -ForegroundColor Cyan
    Write-Host "   git config --global user.email 'your.email@example.com'" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ Git configured: $gitUser ($gitEmail)" -ForegroundColor Green

# Check if repository is initialized
Write-Host "📋 Checking repository status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Host "📝 Uncommitted changes found. Committing..." -ForegroundColor Yellow
    git add .
    git commit -m "Update: Traffic Management Agent System with comprehensive documentation"
    Write-Host "✅ Changes committed" -ForegroundColor Green
} else {
    Write-Host "✅ Repository is clean" -ForegroundColor Green
}

# Instructions for manual GitHub setup
Write-Host "`n📋 GitHub Repository Setup Instructions:" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Yellow

Write-Host "1️⃣  Create Repository on GitHub:" -ForegroundColor Cyan
Write-Host "   • Go to: https://github.com/new" -ForegroundColor White
Write-Host "   • Repository name: curious_agents" -ForegroundColor White
Write-Host "   • Description: Traffic Management Agent System with AI-powered congestion detection and solution recommendations" -ForegroundColor White
Write-Host "   • Make it Public" -ForegroundColor White
Write-Host "   • Do NOT initialize with README (we already have one)" -ForegroundColor White
Write-Host "   • Click 'Create repository'" -ForegroundColor White

Write-Host "`n2️⃣  After creating the repository, run these commands:" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/curious_agents.git" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White

Write-Host "`n3️⃣  Verify the repository:" -ForegroundColor Cyan
Write-Host "   • Go to: https://github.com/YOUR_USERNAME/curious_agents" -ForegroundColor White
Write-Host "   • Check that all files are uploaded" -ForegroundColor White
Write-Host "   • Verify documentation is properly formatted" -ForegroundColor White

Write-Host "`n📊 Repository Contents:" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Yellow

# List key files
$keyFiles = @(
    "AGENT_DOCUMENTATION.md",
    "DEMO_DOCUMENTATION.md", 
    "demo_original_agents_with_output.py",
    "congestion_detector/agent.py",
    "context_aggregator/agent.py",
    "fix_recommender/agent.py",
    "README.md",
    "docker-compose.yml"
)

Write-Host "📁 Key files to be uploaded:" -ForegroundColor Cyan
foreach ($file in $keyFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file (missing)" -ForegroundColor Red
    }
}

Write-Host "`n🎯 Key Features:" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Yellow
Write-Host "• AI-Powered Traffic Analysis using Google Gemini API" -ForegroundColor White
Write-Host "• Real-time GPS Data Processing" -ForegroundColor White
Write-Host "• Comprehensive Documentation with Flow Charts" -ForegroundColor White
Write-Host "• Three Specialized Agents Working Together" -ForegroundColor White
Write-Host "• Enhanced Demo with Confidence Scores" -ForegroundColor White

Write-Host "`n📚 Documentation:" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Yellow
Write-Host "• AGENT_DOCUMENTATION.md - Detailed agent specifications with Mermaid flow charts" -ForegroundColor White
Write-Host "• DEMO_DOCUMENTATION.md - Demo script documentation with input/output specs" -ForegroundColor White
Write-Host "• README.md - Main project overview" -ForegroundColor White

Write-Host "`n🚀 Ready to push to GitHub!" -ForegroundColor Green
Write-Host "Follow the instructions above to create and push to the repository." -ForegroundColor Cyan 