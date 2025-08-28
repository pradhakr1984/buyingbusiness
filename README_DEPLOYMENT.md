# 🚀 Deployment Guide: GitHub → Vercel

## 📱 **Files to Open the HTML Dashboard**

To view your dashboard, open either of these files in your browser:

1. **`index.html`** - Main dashboard file (used for Vercel deployment)
2. **`dashboard_20250828.html`** - Dated backup version

**Double-click either file to open in your default browser!**

---

## 🌐 **Deploy to Vercel (Mobile Access)**

Follow these steps to deploy your dashboard so you can view it on your phone while traveling:

### Step 1: Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit initial version
git commit -m "Initial commit: Business Acquisition Tracker"

# Add your GitHub repository (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/business-acquisition-tracker.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Sign up/Login** with your GitHub account
3. **Import Project**: Click "New Project" 
4. **Select Repository**: Choose your `business-acquisition-tracker` repo
5. **Deploy**: Click "Deploy" (Vercel auto-detects static files)

**That's it!** Vercel will give you a URL like: `https://business-acquisition-tracker.vercel.app`

---

## 📁 **Key Files for Deployment**

### Essential Files (Already Created):
- ✅ `index.html` - Main dashboard (auto-generated)
- ✅ `sample_business_listings.json` - Sample data
- ✅ `vercel.json` - Vercel configuration
- ✅ `.gitignore` - Git ignore file

### Production Files:
- ✅ `api_integration.py` - Real API integration
- ✅ `dashboard_generator.py` - Dashboard generator
- ✅ `requirements.txt` - Python dependencies

---

## 🔄 **Updating Your Dashboard**

### For Real Data (with API):
```bash
# Set your API key
export ZYLA_API_KEY="your_real_api_key"

# Generate new dashboard with real data
python3 api_integration.py
python3 dashboard_generator.py

# Commit and push updates
git add index.html
git commit -m "Update dashboard with latest business listings"
git push

# Vercel auto-deploys the changes!
```

### For Sample Data Updates:
```bash
# Update sample data
python3 create_sample_dashboard.py

# Push to GitHub
git add index.html sample_business_listings.json
git commit -m "Update sample dashboard"
git push
```

---

## 📱 **Mobile Viewing Features**

Your dashboard is mobile-responsive and includes:

- 📊 **Touch-friendly cards** for each business listing
- 🔍 **Readable text** on small screens  
- 📈 **Responsive stats grid** that adapts to phone screens
- 🔗 **Clickable links** to original business listings
- 🎨 **Modern design** that looks great on any device

---

## 🛠 **GitHub Repository Setup**

### Create Repository on GitHub:
1. Go to https://github.com
2. Click "New repository"
3. Name: `business-acquisition-tracker`
4. Description: "Daily business acquisition tracking with beautiful dashboard"
5. Make it **Private** (recommended for business use)
6. Click "Create repository"

### Repository Structure:
```
business-acquisition-tracker/
├── index.html                    # Main dashboard (for Vercel)
├── sample_business_listings.json # Sample data
├── dashboard_generator.py        # Dashboard generator
├── api_integration.py           # Production API integration
├── requirements.txt             # Python dependencies
├── vercel.json                  # Vercel config
├── .gitignore                   # Git ignore
├── README.md                    # Main documentation
└── PRODUCTION_SETUP.md          # Production setup guide
```

---

## ⚡ **Quick Commands**

### Initialize and Deploy:
```bash
# One-time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/business-acquisition-tracker.git
git push -u origin main

# Then deploy on Vercel (web interface)
```

### Daily Updates (when you have real data):
```bash
# Update dashboard
python3 api_integration.py && python3 dashboard_generator.py

# Deploy updates
git add index.html && git commit -m "Daily update" && git push
```

---

## 🔗 **What You'll Get**

- **GitHub Repository**: Version-controlled code and dashboard
- **Vercel URL**: `https://your-project.vercel.app` 
- **Mobile Access**: View on phone/tablet anywhere
- **Auto-Deployment**: Push to GitHub → Automatic Vercel update
- **Fast Loading**: Static files served from CDN

---

## ✅ **Next Steps**

1. **Test Locally**: Open `index.html` in your browser
2. **Create GitHub Repo**: Follow the GitHub setup above  
3. **Deploy to Vercel**: Import from GitHub
4. **Test Mobile**: Visit your Vercel URL on your phone
5. **Set Up API** (optional): Add real business data

**Your dashboard will be accessible anywhere you have internet! 📱**
