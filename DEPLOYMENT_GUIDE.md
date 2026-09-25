# Step-by-Step Deployment Guide for ResumeIQ

Follow these steps to deploy **ResumeIQ** for free using **Render (Backend)** and **Vercel (Frontend)**.

---

## Step 1: Push Code to GitHub

Open PowerShell in `D:\resume-matcher`:

```powershell
cd D:\resume-matcher
git init
git add .
git commit -m "Initial commit of ResumeIQ project"
git branch -M main
```

1. Create a new repository on [GitHub](https://github.com/new) called `resume-matcher`.
2. Push your code:
   ```powershell
   git remote add origin https://github.com/<your-username>/resume-matcher.git
   git push -u origin main
   ```

---

## Step 2: Deploy the Backend on Render (Free)

1. Go to [Render Dashboard](https://dashboard.render.com/) and sign in (with GitHub).
2. Click **New +** > **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your `resume-matcher` repo.
4. Fill in the settings:
   - **Name:** `resumeiq-backend` (or your choice)
   - **Region:** Closest to you (e.g., Singapore, Frankfurt, Oregon)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python -c "import nltk; nltk.download(\x27punkt\x27); nltk.download(\x27punkt_tab\x27); nltk.download(\x27stopwords\x27); nltk.download(\x27wordnet\x27)"
     ```
   - **Start Command:**
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** **Free**
5. Click **Deploy Web Service**.
6. Once deployed, copy your Render URL (e.g. `https://resumeiq-backend.onrender.com`).
   - Test it by visiting: `https://resumeiq-backend.onrender.com/api/health`

---

## Step 3: Deploy the Frontend on Vercel (Free)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) and sign in with GitHub.
2. Click **Add New...** > **Project**.
3. Import your `resume-matcher` repository.
4. Configure the project:
   - **Framework Preset:** `Vite`
   - **Root Directory:** Click Edit and select `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Expand **Environment Variables** and add:
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** `https://your-render-backend.onrender.com/api` *(replace with your real Render URL + `/api`)*
6. Click **Deploy**.
7. Vercel will give you a live production URL (e.g. `https://resumeiq-frontend.vercel.app`)!

