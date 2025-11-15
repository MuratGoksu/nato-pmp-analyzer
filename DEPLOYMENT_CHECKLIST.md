# 🚀 NATO PMP Analyzer - Deployment Checklist

## Quick Deployment Options

| Option | Difficulty | Time | Best For |
|--------|-----------|------|----------|
| **Streamlit Cloud** | ⭐ Easy | 10 min | Quick demos, testing |
| **Docker** | ⭐⭐ Medium | 30 min | Local/cloud deployment |
| **Internal Server** | ⭐⭐⭐ Advanced | 1-2 hrs | Production, NATO networks |

---

## 1️⃣ Streamlit Cloud Deployment (Recommended for Quick Start)

### Prerequisites Checklist
- [ ] GitHub account created
- [ ] OpenAI API key obtained
- [ ] Git repository initialized

### Step-by-Step

#### A. Prepare Repository
```bash
cd /Users/muratgoksu/Desktop/nato-pmp-analyzer
git add .
git commit -m "feat: prepare for Streamlit Cloud deployment"
git push origin main
```

#### B. Deploy to Streamlit Cloud
1. [ ] Go to https://share.streamlit.io/
2. [ ] Sign in with GitHub
3. [ ] Click "New app"
4. [ ] Select repository: `nato-pmp-analyzer`
5. [ ] Main file: `app.py`
6. [ ] Click "Deploy"

#### C. Configure Secrets
1. [ ] Click Settings ⚙️ → Secrets
2. [ ] Add secrets (TOML format):
```toml
OPENAI_API_KEY = "sk-proj-YOUR-KEY-HERE"
OPENAI_MODEL = "gpt-4-turbo-preview"

# Optional: Email notifications
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
FROM_EMAIL = "your-email@gmail.com"
```
3. [ ] Save and wait for reboot

#### D. Verify Deployment
- [ ] Upload a test PDF
- [ ] Check dashboard loads
- [ ] Test chatbot query
- [ ] Verify RAG responses

**Estimated Time:** 10-15 minutes
**Cost:** FREE (Streamlit Community Cloud)
**URL:** `https://[your-app-name].streamlit.app`

**See:** [DEPLOYMENT_STREAMLIT_CLOUD.md](DEPLOYMENT_STREAMLIT_CLOUD.md) for details

---

## 2️⃣ Docker Deployment

### Prerequisites Checklist
- [ ] Docker installed
- [ ] Docker Compose installed (optional)
- [ ] OpenAI API key

### Step-by-Step

#### A. Build Docker Image
```bash
cd /Users/muratgoksu/Desktop/nato-pmp-analyzer
docker build -t nato-pmp-analyzer:latest .
```

#### B. Run Container
```bash
# Option 1: Using environment variables
docker run -d \
  -p 8501:8501 \
  -e OPENAI_API_KEY="your-key-here" \
  -e OPENAI_MODEL="gpt-4-turbo-preview" \
  --name nato-pmp-analyzer \
  nato-pmp-analyzer:latest

# Option 2: Using .env file
docker run -d \
  -p 8501:8501 \
  --env-file .env \
  --name nato-pmp-analyzer \
  nato-pmp-analyzer:latest
```

#### C. Verify Container
```bash
docker ps
docker logs nato-pmp-analyzer
```

#### D. Access Application
- [ ] Open browser: http://localhost:8501
- [ ] Test upload functionality
- [ ] Verify all features work

**Estimated Time:** 30 minutes
**Cost:** FREE (local) or cloud VM pricing
**URL:** `http://localhost:8501` or `http://[server-ip]:8501`

**See:** [DEPLOYMENT_DOCKER.md](DEPLOYMENT_DOCKER.md) for details

---

## 3️⃣ Internal Server Deployment

### Prerequisites Checklist
- [ ] Ubuntu/Debian server (20.04+ recommended)
- [ ] SSH access to server
- [ ] sudo privileges
- [ ] Domain name (optional)
- [ ] SSL certificate (for HTTPS)

### Step-by-Step

#### A. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip -y

# Install Nginx (reverse proxy)
sudo apt install nginx -y

# Install Certbot (SSL)
sudo apt install certbot python3-certbot-nginx -y
```

#### B. Deploy Application
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/nato-pmp-analyzer.git
cd nato-pmp-analyzer

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

#### C. Create Systemd Service
```bash
sudo nano /etc/systemd/system/nato-pmp-analyzer.service
```

Add service configuration (see DEPLOYMENT_SERVER.md)

#### D. Configure Nginx Reverse Proxy
```bash
sudo nano /etc/nginx/sites-available/nato-pmp-analyzer
```

Add Nginx configuration (see DEPLOYMENT_SERVER.md)

#### E. Enable SSL (Optional)
```bash
sudo certbot --nginx -d your-domain.com
```

#### F. Start Services
```bash
sudo systemctl enable nato-pmp-analyzer
sudo systemctl start nato-pmp-analyzer
sudo systemctl enable nginx
sudo systemctl restart nginx
```

#### G. Verify Deployment
- [ ] Check service status: `sudo systemctl status nato-pmp-analyzer`
- [ ] Access via domain: https://your-domain.com
- [ ] Test all functionality
- [ ] Check logs: `sudo journalctl -u nato-pmp-analyzer -f`

**Estimated Time:** 1-2 hours
**Cost:** Server hosting costs
**URL:** `https://your-domain.com`

**See:** [DEPLOYMENT_SERVER.md](DEPLOYMENT_SERVER.md) for details

---

## 📊 Deployment Comparison

### Streamlit Cloud ⭐
**Pros:**
- ✅ Fastest deployment (10 min)
- ✅ Zero infrastructure management
- ✅ Automatic HTTPS
- ✅ Auto-deploys on git push
- ✅ Free tier available

**Cons:**
- ❌ Limited resources (1GB RAM)
- ❌ Ephemeral storage (resets on restart)
- ❌ Public internet required
- ❌ May not meet NATO security requirements

**Best for:** Quick demos, PoC, public testing

---

### Docker ⭐⭐
**Pros:**
- ✅ Consistent environment
- ✅ Easy to scale
- ✅ Portable across platforms
- ✅ Can run on-premise
- ✅ Persistent storage

**Cons:**
- ❌ Requires Docker knowledge
- ❌ Need to manage infrastructure
- ❌ Manual SSL setup

**Best for:** Cloud VMs (AWS, Azure, GCP), development environments

---

### Internal Server ⭐⭐⭐
**Pros:**
- ✅ Full control over environment
- ✅ Can meet NATO security requirements
- ✅ On-premise deployment
- ✅ Persistent storage
- ✅ Production-ready

**Cons:**
- ❌ Complex setup
- ❌ Requires server management
- ❌ Manual updates needed

**Best for:** Production NATO deployments, classified networks

---

## 🔒 Security Checklist (All Deployments)

### Before Going Live
- [ ] All API keys stored in environment variables (never in code)
- [ ] `.env` file added to `.gitignore`
- [ ] HTTPS enabled (SSL/TLS)
- [ ] Authentication implemented (if handling sensitive data)
- [ ] Rate limiting configured
- [ ] Input validation enabled
- [ ] Error messages don't expose sensitive info
- [ ] Logs configured (but not logging secrets)
- [ ] Backup strategy in place
- [ ] Monitoring/alerting configured

### NATO-Specific Security
- [ ] Deployed on approved infrastructure
- [ ] Network isolation configured
- [ ] Access controls implemented
- [ ] Audit logging enabled
- [ ] Data encryption at rest
- [ ] Compliance requirements met
- [ ] Security review completed

---

## 🧪 Testing Checklist (All Deployments)

### Functional Testing
- [ ] Upload PDF document (small, <1MB)
- [ ] Upload DOCX document
- [ ] Upload multiple documents (batch)
- [ ] View dashboard metrics
- [ ] Test chatbot with sample questions
- [ ] Generate timeline visualization
- [ ] Export to Excel
- [ ] Export to PDF
- [ ] Send test email notification
- [ ] Generate AI insights

### Performance Testing
- [ ] Upload 10+ documents
- [ ] Check response time (<5 sec)
- [ ] Verify memory usage
- [ ] Test concurrent users (if applicable)

### Error Handling
- [ ] Upload invalid file (non-PDF/DOCX)
- [ ] Upload corrupted PDF
- [ ] Test without API key configured
- [ ] Test with invalid API key
- [ ] Test network disconnection

---

## 📈 Post-Deployment

### Monitoring
- [ ] Set up uptime monitoring
- [ ] Configure error alerting
- [ ] Track API usage/costs
- [ ] Monitor resource usage (RAM, CPU)

### Maintenance
- [ ] Schedule regular backups
- [ ] Plan for updates/patches
- [ ] Document admin procedures
- [ ] Create user guide/training materials

### Scaling (if needed)
- [ ] Identify bottlenecks
- [ ] Plan for increased load
- [ ] Consider database migration
- [ ] Implement caching

---

## 🆘 Troubleshooting

### Common Issues

**App won't start:**
1. Check logs for errors
2. Verify all dependencies installed
3. Confirm API keys are set
4. Check port availability (8501)

**Slow performance:**
1. Check API rate limits
2. Reduce document count
3. Increase server resources
4. Enable caching

**API errors:**
1. Verify API key is valid
2. Check OpenAI account credits
3. Review rate limits
4. Check internet connectivity

---

## 📞 Support Resources

- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **Docker:** https://docs.docker.com/
- **Nginx:** https://nginx.org/en/docs/
- **OpenAI:** https://platform.openai.com/docs

---

## ✅ Quick Start Recommendation

**For immediate demo:** Choose **Streamlit Cloud** ⭐
**For testing/development:** Choose **Docker** ⭐⭐
**For production NATO use:** Choose **Internal Server** ⭐⭐⭐

---

**Last Updated:** November 15, 2025
**Version:** 0.5
