# POS CX Voice Assistant - Deployment Script
# This script helps you deploy your custom LLM to the cloud

Write-Host "🚀 POS CX Voice Assistant - Deployment Helper" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "✅ Git is available: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit: POS CX Voice Assistant"
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Already in a git repository" -ForegroundColor Green
}

# Check if we have a remote origin
$remoteOrigin = git remote get-url origin 2>$null
if (-not $remoteOrigin) {
    Write-Host "🌐 No remote repository configured." -ForegroundColor Yellow
    Write-Host "Please create a GitHub repository and add it as origin:" -ForegroundColor Yellow
    Write-Host "git remote add origin https://github.com/yourusername/your-repo-name.git" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or if you already have a repository:" -ForegroundColor Yellow
    Write-Host "git remote add origin YOUR_REPOSITORY_URL" -ForegroundColor Cyan
} else {
    Write-Host "✅ Remote origin configured: $remoteOrigin" -ForegroundColor Green
    
    # Commit and push changes
    Write-Host "📤 Committing and pushing changes..." -ForegroundColor Yellow
    git add .
    git commit -m "Update POS CX Voice Assistant for deployment"
    git push origin main
    Write-Host "✅ Changes pushed to GitHub" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Green
Write-Host "==============" -ForegroundColor Green
Write-Host ""
Write-Host "1. Deploy to Railway (Recommended):" -ForegroundColor Yellow
Write-Host "   - Go to https://railway.app" -ForegroundColor Cyan
Write-Host "   - Sign up with GitHub" -ForegroundColor Cyan
Write-Host "   - Click 'New Project' → 'Deploy from GitHub repo'" -ForegroundColor Cyan
Write-Host "   - Select your repository" -ForegroundColor Cyan
Write-Host "   - Railway will auto-detect and deploy" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Or deploy to Render:" -ForegroundColor Yellow
Write-Host "   - Go to https://render.com" -ForegroundColor Cyan
Write-Host "   - Create Web Service" -ForegroundColor Cyan
Write-Host "   - Connect your GitHub repository" -ForegroundColor Cyan
Write-Host "   - Set build command: pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host "   - Set start command: uvicorn main:app --host 0.0.0.0 --port `$PORT" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Configure in Retell:" -ForegroundColor Yellow
Write-Host "   - Get your deployment URL (e.g., https://your-app.railway.app)" -ForegroundColor Cyan
Write-Host "   - Go to Retell Dashboard → Create New Agent" -ForegroundColor Cyan
Write-Host "   - Select 'Custom LLM' as AI provider" -ForegroundColor Cyan
Write-Host "   - Enter endpoint: https://your-app.railway.app/chat" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Test your voice agent!" -ForegroundColor Yellow
Write-Host ""
Write-Host "📚 For detailed instructions, see DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host "📋 For setup summary, see SETUP_COMPLETE.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 Good luck with your deployment!" -ForegroundColor Green 