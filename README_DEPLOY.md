# Deploying Manna AI to Vercel

## Prerequisites
1. Install Vercel CLI: `npm i -g vercel`
2. Have a Vercel account (sign up at vercel.com)

## Deployment Steps

### Option 1: Using Vercel CLI
```bash
# Login to Vercel
vercel login

# Deploy (first time)
vercel

# Deploy to production
vercel --prod
```

### Option 2: Using GitHub
1. Push your code to a GitHub repository
2. Go to vercel.com and import your repository
3. Vercel will automatically detect the Python project and deploy it

## Important Notes

⚠️ **Environment Variables:**
- Add your OpenAI API key in Vercel dashboard:
  - Go to Project Settings → Environment Variables
  - Add: `OPENAI_API_KEY` = `your-api-key-here`
  - Or it will use the hardcoded key in `chatbot.py`

⚠️ **Package Limitations:**
- Some packages like `pyttsx3` and `SpeechRecognition` may not work in serverless environment
- Voice features will be limited to browser-based speech recognition
- Code execution features should work fine

⚠️ **Build Time:**
- First deployment may take 5-10 minutes due to package installations
- Subsequent deployments are faster

## After Deployment
Your app will be available at: `https://your-project-name.vercel.app`

## Troubleshooting
- If build fails, check Vercel logs in dashboard
- Some packages may need to be removed if they're not compatible with serverless
- Static files are served from the `/static` directory

