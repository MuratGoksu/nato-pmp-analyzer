# Deploying NATO PMP Analyzer to Streamlit Cloud

## Prerequisites

- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- OpenAI API key

## Step 1: Prepare Your GitHub Repository

### 1.1 Initialize Git Repository (if not already done)

```bash
cd /Users/muratgoksu/Desktop/nato-pmp-analyzer
git init
git add .
git commit -m "Initial commit: NATO PMP Analyzer"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `nato-pmp-analyzer`)
3. **DO NOT** initialize with README (we already have files)
4. Click "Create repository"

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/nato-pmp-analyzer.git
git branch -M main
git push -u origin main
```

## Step 2: Configure Streamlit Cloud

### 2.1 Sign in to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Authorize Streamlit to access your repositories

### 2.2 Deploy New App

1. Click "New app" button
2. Select your repository: `YOUR_USERNAME/nato-pmp-analyzer`
3. Select branch: `main`
4. Main file path: `app.py`
5. Click "Deploy"

### 2.3 Configure Secrets

Before the app works, you need to add your API keys:

1. In Streamlit Cloud dashboard, click your app
2. Click "Settings" (⚙️ icon)
3. Click "Secrets" in the left sidebar
4. Add the following in TOML format:

```toml
# OpenAI Configuration
OPENAI_API_KEY = "sk-proj-YOUR-ACTUAL-OPENAI-API-KEY-HERE"
OPENAI_MODEL = "gpt-4-turbo-preview"

# Email Configuration (Optional - only if you want email notifications)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password-here"
FROM_EMAIL = "your-email@gmail.com"
```

5. Click "Save"
6. The app will automatically reboot with the new secrets

## Step 3: Update Code to Use Streamlit Secrets

The app is already configured to use Streamlit secrets in production. The code automatically detects if it's running on Streamlit Cloud and uses `st.secrets` instead of `.env` file.

## Step 4: Verify Deployment

### 4.1 Check App Status

1. Wait for deployment to complete (usually 2-5 minutes)
2. You'll see "Your app is live!" when ready
3. Click the URL to open your app

### 4.2 Test Functionality

1. **Upload a PDF** document
2. **Check Dashboard** for visualizations
3. **Test Chatbot** with a question
4. **Verify RAG initialization** (should happen automatically)

## Important Notes

### Data Persistence

**Warning**: Streamlit Cloud uses ephemeral storage. This means:

- Uploaded documents will be lost when the app restarts
- The `chroma_db/` vector database will be cleared on restart
- `processed_documents.json` will not persist

**Solution for Production**:
- Use external storage (AWS S3, Google Cloud Storage)
- Use managed vector database (Pinecone, Weaviate)
- Implement database persistence (PostgreSQL, MongoDB)

### Resource Limits

Streamlit Cloud free tier has limitations:
- 1 GB RAM
- 1 CPU core
- 1 GB storage

For production use with many documents, consider:
- Upgrading to Streamlit Cloud paid tier
- Using Docker deployment on cloud VMs
- Deploying to internal servers

### Security Considerations

1. **Never commit secrets** to GitHub
2. **Use environment variables** for all sensitive data
3. **Enable authentication** if handling sensitive NATO documents
4. **Use HTTPS** (automatic with Streamlit Cloud)

## Troubleshooting

### App Won't Start

**Check logs**: In Streamlit Cloud dashboard → Your App → "Manage app" → View logs

Common issues:
1. **Missing dependencies**: Check `requirements.txt`
2. **Missing secrets**: Verify all required secrets are added
3. **File path issues**: Ensure all paths are relative

### OpenAI API Errors

1. Verify API key is correct in Secrets
2. Check OpenAI account has available credits
3. Ensure API key has not expired

### Slow Performance

1. Reduce number of documents processed
2. Decrease embedding chunk size
3. Consider upgrading Streamlit Cloud tier

## Custom Domain (Optional)

1. Go to App Settings → General
2. Click "Custom subdomain"
3. Enter your desired subdomain (e.g., `nato-pmp-analyzer.streamlit.app`)
4. Save changes

## Updating Your App

When you push updates to GitHub:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically detect changes and redeploy within minutes.

## Support

- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Community: https://discuss.streamlit.io/
- Project Issues: https://github.com/YOUR_USERNAME/nato-pmp-analyzer/issues

## Next Steps

After successful Streamlit Cloud deployment:
1. Test all features thoroughly
2. Configure email notifications (if needed)
3. Set up monitoring and logging
4. Plan for Docker deployment (see DEPLOYMENT_DOCKER.md)
5. Plan for internal server deployment (see DEPLOYMENT_SERVER.md)
