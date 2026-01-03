# Quick Setup Script for Movie Recommender Frontend

Write-Host "🎬 Movie Recommender - Frontend Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create React app with Vite
Write-Host "Step 1: Creating React app..." -ForegroundColor Yellow
npm create vite@latest movie-recommender-frontend -- --template react

# Step 2: Navigate and install dependencies
Write-Host "`nStep 2: Installing dependencies..." -ForegroundColor Yellow
cd movie-recommender-frontend
npm install
npm install axios

# Step 3: Install Tailwind
Write-Host "`nStep 3: Installing Tailwind CSS..." -ForegroundColor Yellow
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Step 4: Configure Tailwind
Write-Host "`nStep 4: Configuring Tailwind..." -ForegroundColor Yellow

# Create tailwind.config.js
@"
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"@ | Out-File -FilePath "tailwind.config.js" -Encoding utf8

# Update index.css
@"
@tailwind base;
@tailwind components;
@tailwind utilities;
"@ | Out-File -FilePath "src/index.css" -Encoding utf8

# Copy App.jsx
Write-Host "`nStep 5: Setting up App component..." -ForegroundColor Yellow
Copy-Item "../App.jsx.template" -Destination "src/App.jsx"

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Run: npm run dev" -ForegroundColor White
Write-Host "2. Open: http://localhost:5173" -ForegroundColor White
Write-Host "3. Make sure FastAPI is running on port 8000!" -ForegroundColor White
