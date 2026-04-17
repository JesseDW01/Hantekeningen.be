# Git LFS Setup Script for Hantekeningen.be
# This script configures LFS to handle high-res masters while keeping the web-optimized files fast.

Write-Host "Initializing Git LFS..." -ForegroundColor Cyan
git lfs install

# Track High-Res Print PDFs with LFS
# We specifically track files ending in _print.pdf so the _web.pdf stays in regular Git.
Write-Host "Tracking High-Res Print PDFs..." -ForegroundColor Yellow
git lfs track "*_print.pdf"

# Track epubs with LFS
Write-Host "Tracking EPUBs..." -ForegroundColor Yellow
git lfs track "*.epub"

# Track Processed PNG images
# These are the high-quality masters with transparency.
Write-Host "Tracking Processed Image Masters..." -ForegroundColor Yellow
git lfs track "albums/**/*.png"

# Add the configuration to Git
Write-Host "Saving Git LFS configuration..." -ForegroundColor Green
git add .gitattributes

Write-Host "`n✅ Git LFS is now configured!" -ForegroundColor Green
Write-Host "- Files like '*_print.pdf' and 'albums/**/*.png' will be stored in LFS."
Write-Host "- Small files like '*_web.pdf' and your source code remain in standard Git for speed."
Write-Host "`nYou can now commit and push your files safely."
