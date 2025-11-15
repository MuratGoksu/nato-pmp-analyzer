# 🐳 Docker Deployment Guide - NATO PMP Analyzer

## Overview

This guide covers deploying the NATO PMP Analyzer using Docker containers. Docker provides a consistent, portable deployment solution that works across different environments.

**Deployment Time:** ~30 minutes
**Difficulty:** ⭐⭐ Medium
**Best For:** Cloud VMs, on-premise servers, development environments

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Deployment Options](#deployment-options)
4. [Configuration](#configuration)
5. [Advanced Usage](#advanced-usage)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Docker** (version 20.10+)
   ```bash
   # Install on Ubuntu/Debian
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Install on macOS
   # Download Docker Desktop from https://www.docker.com/products/docker-desktop

   # Verify installation
   docker --version
   ```

2. **Docker Compose** (version 2.0+)
   ```bash
   # Usually included with Docker Desktop
   # For Linux, install separately:
   sudo apt install docker-compose-plugin

   # Verify installation
   docker compose version
   ```

### Required Configuration

- OpenAI API key (required for AI features)
- SMTP credentials (optional, for email notifications)
- 2GB+ RAM available
- 5GB+ disk space

---

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# 1. Clone repository (or navigate to project directory)
cd /Users/muratgoksu/Desktop/nato-pmp-analyzer

# 2. Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
OPENAI_MODEL=gpt-4-turbo-preview

# Optional: Email configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
EOF

# 3. Build and start container
docker compose up -d

# 4. Check logs
docker compose logs -f

# 5. Access application
# Open browser to: http://localhost:8501
```

### Option 2: Using Docker CLI

```bash
# 1. Build image
docker build -t nato-pmp-analyzer:latest .

# 2. Run container
docker run -d \
  -p 8501:8501 \
  -e OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE" \
  -e OPENAI_MODEL="gpt-4-turbo-preview" \
  --name nato-pmp-analyzer \
  --restart unless-stopped \
  nato-pmp-analyzer:latest

# 3. Check status
docker ps

# 4. View logs
docker logs -f nato-pmp-analyzer

# 5. Access application
# Open browser to: http://localhost:8501
```

---

## Deployment Options

### 1. Local Development

Perfect for testing and development on your local machine.

```bash
# Start container
docker compose up

# Access at: http://localhost:8501

# Stop container (Ctrl+C or)
docker compose down
```

**Features:**
- Hot reloading (if volumes mounted)
- Easy debugging
- Quick iteration

---

### 2. Cloud VM Deployment

Deploy to AWS EC2, Azure VM, Google Cloud Compute, etc.

```bash
# On your cloud VM:

# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# 2. Clone repository
git clone https://github.com/YOUR_USERNAME/nato-pmp-analyzer.git
cd nato-pmp-analyzer

# 3. Configure environment
nano .env  # Add your API keys

# 4. Deploy
docker compose up -d

# 5. Configure firewall (allow port 8501)
# AWS: Add inbound rule in Security Group
# Azure: Add NSG rule
# GCP: Add firewall rule

# 6. Access via public IP
http://YOUR_VM_PUBLIC_IP:8501
```

**Cloud Provider Examples:**

**AWS EC2:**
```bash
# Security Group: Allow TCP 8501 from your IP
# Instance type: t3.medium or larger (2 vCPU, 4GB RAM)
```

**Azure VM:**
```bash
# VM Size: Standard_B2s or larger
# NSG: Allow inbound 8501
```

**Google Cloud:**
```bash
# Machine type: e2-medium or larger
# Firewall rule: tcp:8501
```

---

### 3. Production Deployment with Nginx

Use Nginx as reverse proxy for HTTPS and better security.

```bash
# 1. Install Nginx
sudo apt install nginx certbot python3-certbot-nginx

# 2. Create Nginx configuration
sudo nano /etc/nginx/sites-available/nato-pmp-analyzer

# Add configuration (see below)

# 3. Enable site
sudo ln -s /etc/nginx/sites-available/nato-pmp-analyzer /etc/nginx/sites-enabled/

# 4. Get SSL certificate
sudo certbot --nginx -d your-domain.com

# 5. Start services
docker compose up -d
sudo systemctl restart nginx
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeouts for large file uploads
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }
}
```

---

## Configuration

### Environment Variables

All configuration is done via environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key for GPT-4 |
| `OPENAI_MODEL` | No | `gpt-4-turbo-preview` | Model to use |
| `SMTP_SERVER` | No | `smtp.gmail.com` | Email server |
| `SMTP_PORT` | No | `587` | Email port |
| `SMTP_USERNAME` | No | - | Email username |
| `SMTP_PASSWORD` | No | - | Email password |
| `FROM_EMAIL` | No | - | Sender email address |

### Persistent Storage

Docker volumes are used to persist data across container restarts:

```yaml
volumes:
  chroma_data:        # Vector database
  processed_data:     # Document metadata
```

**Backup volumes:**
```bash
# Backup
docker run --rm \
  -v nato-pmp-analyzer_chroma_data:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/chroma_backup.tar.gz /data

# Restore
docker run --rm \
  -v nato-pmp-analyzer_chroma_data:/data \
  -v $(pwd):/backup \
  ubuntu tar xzf /backup/chroma_backup.tar.gz -C /
```

---

## Advanced Usage

### Building Custom Image

```bash
# Build with custom tag
docker build -t nato-pmp-analyzer:v0.5 .

# Build for specific platform
docker build --platform linux/amd64 -t nato-pmp-analyzer:latest .

# Build with build arguments
docker build --build-arg PYTHON_VERSION=3.10 -t nato-pmp-analyzer:latest .
```

### Running Multiple Instances

```bash
# Instance 1
docker run -d -p 8501:8501 --name nato-pmp-1 nato-pmp-analyzer:latest

# Instance 2
docker run -d -p 8502:8501 --name nato-pmp-2 nato-pmp-analyzer:latest

# Instance 3
docker run -d -p 8503:8501 --name nato-pmp-3 nato-pmp-analyzer:latest
```

### Resource Limits

```bash
# Limit CPU and memory
docker run -d \
  --cpus="1.5" \
  --memory="2g" \
  --memory-swap="2g" \
  -p 8501:8501 \
  --name nato-pmp-analyzer \
  nato-pmp-analyzer:latest
```

### Logging Configuration

```bash
# JSON log driver with rotation
docker run -d \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  -p 8501:8501 \
  --name nato-pmp-analyzer \
  nato-pmp-analyzer:latest

# View logs
docker logs -f nato-pmp-analyzer

# View last 100 lines
docker logs --tail 100 nato-pmp-analyzer
```

---

## Production Deployment

### Docker Compose Production Configuration

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  nato-pmp-analyzer:
    image: nato-pmp-analyzer:latest
    container_name: nato-pmp-analyzer-prod
    restart: always

    ports:
      - "127.0.0.1:8501:8501"  # Only localhost (use Nginx reverse proxy)

    env_file:
      - .env.production

    volumes:
      - chroma_data:/app/chroma_db
      - processed_data:/app/data
      - ./logs:/app/logs

    networks:
      - nato-pmp-network

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 1G

    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"

volumes:
  chroma_data:
    driver: local
  processed_data:
    driver: local

networks:
  nato-pmp-network:
    driver: bridge
```

**Deploy:**
```bash
docker compose -f docker-compose.prod.yml up -d
```

### Monitoring & Health Checks

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' nato-pmp-analyzer

# Auto-restart on failure
docker update --restart=always nato-pmp-analyzer

# Monitor resource usage
docker stats nato-pmp-analyzer
```

### Security Best Practices

1. **Run as non-root user** (already configured in Dockerfile)
2. **Use secrets management:**
   ```bash
   # Docker secrets (Swarm mode)
   echo "sk-proj-YOUR-KEY" | docker secret create openai_key -
   ```
3. **Scan for vulnerabilities:**
   ```bash
   docker scan nato-pmp-analyzer:latest
   ```
4. **Enable firewall:**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs nato-pmp-analyzer

# Check container status
docker ps -a

# Restart container
docker restart nato-pmp-analyzer

# Remove and recreate
docker compose down
docker compose up -d
```

### Port Already in Use

```bash
# Find process using port 8501
sudo lsof -i :8501
# or
sudo netstat -tulpn | grep 8501

# Kill process or use different port
docker run -p 8502:8501 nato-pmp-analyzer:latest
```

### Out of Memory

```bash
# Check container memory usage
docker stats nato-pmp-analyzer

# Increase memory limit
docker update --memory 4g nato-pmp-analyzer

# Check system memory
free -h
```

### Build Failures

```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker build --no-cache -t nato-pmp-analyzer:latest .

# Check Docker disk space
docker system df
docker system prune -a
```

### OpenAI API Errors

```bash
# Verify environment variable is set
docker exec nato-pmp-analyzer env | grep OPENAI

# Check API key in logs
docker logs nato-pmp-analyzer 2>&1 | grep -i "openai\|api"
```

---

## Maintenance

### Updating the Application

```bash
# 1. Pull latest code
git pull origin main

# 2. Rebuild image
docker compose build

# 3. Restart with new image
docker compose up -d

# 4. Remove old images
docker image prune
```

### Backup Strategy

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup volumes
docker run --rm \
  -v nato-pmp-analyzer_chroma_data:/data \
  -v $(pwd)/$BACKUP_DIR:/backup \
  ubuntu tar czf /backup/chroma_data.tar.gz /data

# Backup processed documents
docker cp nato-pmp-analyzer:/app/processed_documents.json $BACKUP_DIR/

echo "Backup completed: $BACKUP_DIR"
EOF

chmod +x backup.sh

# Run backup
./backup.sh

# Schedule with cron (daily at 2 AM)
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

---

## Performance Optimization

### Increase Resources

```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '4.0'
      memory: 8G
```

### Use tmpfs for Temporary Files

```yaml
volumes:
  - type: tmpfs
    target: /tmp
    tmpfs:
      size: 1000000000  # 1GB
```

### Enable BuildKit

```bash
# Better caching and parallel builds
export DOCKER_BUILDKIT=1
docker build -t nato-pmp-analyzer:latest .
```

---

## Uninstall

```bash
# Stop and remove containers
docker compose down

# Remove images
docker rmi nato-pmp-analyzer:latest

# Remove volumes (WARNING: deletes all data)
docker volume rm nato-pmp-analyzer_chroma_data
docker volume rm nato-pmp-analyzer_processed_data

# Remove all (complete cleanup)
docker compose down -v --rmi all
```

---

## Additional Resources

- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose:** https://docs.docker.com/compose/
- **Best Practices:** https://docs.docker.com/develop/dev-best-practices/
- **Security:** https://docs.docker.com/engine/security/

---

## Next Steps

After successful Docker deployment:

1. ✅ Test all functionality
2. ✅ Configure monitoring and alerts
3. ✅ Set up automated backups
4. ✅ Configure Nginx reverse proxy (for production)
5. ✅ Enable SSL/TLS with Let's Encrypt
6. ⏭️ Proceed to internal server deployment (see DEPLOYMENT_SERVER.md)

---

**Last Updated:** November 15, 2025
**Docker Image:** `nato-pmp-analyzer:latest`
**Supported Platforms:** linux/amd64, linux/arm64
