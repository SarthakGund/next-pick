# Git Setup and Push to GitHub
# Run this script in a NEW PowerShell window after closing the current one

cd C:\Users\Admin\Desktop\movie_eccomender

# Configure Git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init

# Add all files (respecting .gitignore)
git add .

# Check what will be committed
Write-Host "`n=== Files to be committed ===" -ForegroundColor Cyan
git status

# Show total size
Write-Host "`n=== Repository size ===" -ForegroundColor Cyan
$size = (git ls-files -s | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "$([math]::Round($size, 2)) MB"

Write-Host "`n=== Next Steps ===" -ForegroundColor Green
Write-Host "1. Review the files above"
Write-Host "2. If everything looks good, run: git commit -m 'Initial commit'"
Write-Host "3. Create a new GitHub repo at: https://github.com/new"
Write-Host "4. Then run:"
Write-Host "   git branch -M main"
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
Write-Host "   git push -u origin main"
