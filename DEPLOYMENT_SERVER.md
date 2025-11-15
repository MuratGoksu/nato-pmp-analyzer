# 🖥️ Internal Server Deployment Guide - NATO PMP Analyzer

## Overview

This guide covers deploying the NATO PMP Analyzer on an internal server for production use. This deployment method provides full control, security, and is suitable for NATO classified networks.

**Deployment Time:** 1-2 hours
**Difficulty:** ⭐⭐⭐ Advanced
**Best For:** Production NATO deployments, classified networks, on-premise infrastructure

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Preparation](#server-preparation)
3. [Application Installation](#application-installation)
4. [Systemd Service Setup](#systemd-service-setup)
5. [Nginx Reverse Proxy](#nginx-reverse-proxy)
6. [SSL/TLS Configuration](#ssltls-configuration)
7. [Security Hardening](#security-hardening)
8. [Monitoring & Maintenance](#monitoring--maintenance)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Server Requirements

**Minimum Specifications:**
- **OS:** Ubuntu 20.04 LTS / 22.04 LTS (or RHEL 8+)
- **CPU:** 2 cores
- **RAM:** 4GB
- **Storage:** 20GB SSD
- **Network:** Static IP address

**Recommended Specifications:**
- **OS:** Ubuntu 22.04 LTS
- **CPU:** 4 cores
- **RAM:** 8GB
- **Storage:** 50GB SSD
- **Network:** Static IP, domain name

### Access Requirements

- SSH access with sudo privileges
- Domain name (optional, for HTTPS)
- Firewall access (ports 80, 443)
- OpenAI API key
- SMTP credentials (optional)

---

## Server Preparation

### Step 1: Update System

```bash
# Update package lists
sudo apt update

# Upgrade existing packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget vim ufw build-essential
```

### Step 2: Install Python 3.10+

```bash
# Check Python version
python3 --version

# If Python 3.10+ not available, install:
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Verify installation
python3.10 --version
```

### Step 3: Create Application User

```bash
# Create dedicated user for security
sudo useradd -r -m -s /bin/bash nato-pmp
sudo usermod -aG sudo nato-pmp  # Optional: if user needs sudo

# Create application directory
sudo mkdir -p /opt/nato-pmp-analyzer
sudo chown nato-pmp:nato-pmp /opt/nato-pmp-analyzer
```

### Step 4: Configure Firewall

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH (important!)
sudo ufw allow ssh
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status verbose
```

---

## Application Installation

### Step 1: Clone Repository

```bash
# Switch to application user
sudo su - nato-pmp

# Navigate to application directory
cd /opt/nato-pmp-analyzer

# Clone repository
git clone https://github.com/YOUR_USERNAME/nato-pmp-analyzer.git .

# Or upload files manually if no internet access
# Use: scp -r nato-pmp-analyzer/ user@server:/opt/nato-pmp-analyzer/
```

### Step 2: Create Virtual Environment

```bash
# Create Python virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 3: Install Dependencies

```bash
# Install application dependencies
pip install -r requirements.txt

# Verify installation
pip list

# Test import
python3 -c "import streamlit; print(streamlit.__version__)"
```

### Step 4: Configure Environment

```bash
# Create .env file
nano .env

# Add configuration:
```

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE
OPENAI_MODEL=gpt-4-turbo-preview

# Email Configuration (Optional)
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=nato-pmp@example.com
SMTP_PASSWORD=your-smtp-password
FROM_EMAIL=nato-pmp@example.com

# Application Settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=127.0.0.1
```

```bash
# Secure .env file
chmod 600 .env
chown nato-pmp:nato-pmp .env
```

### Step 5: Create Necessary Directories

```bash
# Create data directories
mkdir -p chroma_db logs

# Set permissions
chmod 755 chroma_db logs
chown -R nato-pmp:nato-pmp /opt/nato-pmp-analyzer

# Exit from nato-pmp user
exit
```

### Step 6: Test Application

```bash
# Test run as nato-pmp user
sudo su - nato-pmp
cd /opt/nato-pmp-analyzer
source venv/bin/activate
streamlit run app.py --server.port=8501

# Access from browser: http://SERVER_IP:8501
# If works, press Ctrl+C to stop
exit
```

---

## Systemd Service Setup

### Step 1: Copy Service File

```bash
# Copy service file to systemd
sudo cp nato-pmp-analyzer.service /etc/systemd/system/

# Or create manually:
sudo nano /etc/systemd/system/nato-pmp-analyzer.service
```

(Service file content is in `nato-pmp-analyzer.service`)

### Step 2: Enable and Start Service

```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable nato-pmp-analyzer

# Start service
sudo systemctl start nato-pmp-analyzer

# Check status
sudo systemctl status nato-pmp-analyzer
```

### Step 3: Verify Service

```bash
# Check if service is running
sudo systemctl is-active nato-pmp-analyzer

# View logs
sudo journalctl -u nato-pmp-analyzer -f

# Test access
curl http://127.0.0.1:8501
```

---

## Nginx Reverse Proxy

### Step 1: Install Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

### Step 2: Configure Nginx

```bash
# Copy Nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/nato-pmp-analyzer

# Or create manually:
sudo nano /etc/nginx/sites-available/nato-pmp-analyzer
```

(Nginx configuration content is in `nginx.conf`)

**Edit the configuration:**
```bash
# Replace placeholders
sudo sed -i 's/your-domain.com/actual-domain.com/g' /etc/nginx/sites-available/nato-pmp-analyzer
```

### Step 3: Enable Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/nato-pmp-analyzer /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## SSL/TLS Configuration

### Option 1: Let's Encrypt (Public Domain)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow prompts:
# - Enter email address
# - Agree to Terms of Service
# - Choose: Redirect HTTP to HTTPS (option 2)

# Test automatic renewal
sudo certbot renew --dry-run

# Renewal is automatic via cron/systemd timer
```

### Option 2: Self-Signed Certificate (Internal Use)

```bash
# Generate self-signed certificate
sudo mkdir -p /etc/ssl/private
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nato-pmp.key \
  -out /etc/ssl/certs/nato-pmp.crt

# Update Nginx configuration to use self-signed cert
sudo nano /etc/nginx/sites-available/nato-pmp-analyzer

# Change SSL paths:
# ssl_certificate /etc/ssl/certs/nato-pmp.crt;
# ssl_certificate_key /etc/ssl/private/nato-pmp.key;

# Reload Nginx
sudo systemctl reload nginx
```

### Option 3: Organization Certificate

```bash
# Copy your organization's certificate and key
sudo cp /path/to/your-cert.crt /etc/ssl/certs/nato-pmp.crt
sudo cp /path/to/your-key.key /etc/ssl/private/nato-pmp.key

# Secure key file
sudo chmod 600 /etc/ssl/private/nato-pmp.key

# Update Nginx configuration (see Option 2)
# Reload Nginx
sudo systemctl reload nginx
```

---

## Security Hardening

### 1. SSH Security

```bash
# Disable password authentication (use SSH keys only)
sudo nano /etc/ssh/sshd_config

# Set:
# PasswordAuthentication no
# PermitRootLogin no
# PubkeyAuthentication yes

# Restart SSH
sudo systemctl restart sshd
```

### 2. Fail2Ban (Brute Force Protection)

```bash
# Install Fail2Ban
sudo apt install -y fail2ban

# Configure for Nginx
sudo nano /etc/fail2ban/jail.local
```

```ini
[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
```

```bash
# Start Fail2Ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Check status
sudo fail2ban-client status
```

### 3. AppArmor/SELinux

```bash
# For Ubuntu (AppArmor)
sudo apt install -y apparmor apparmor-utils

# Create profile for Streamlit (advanced)
# See: https://gitlab.com/apparmor/apparmor/-/wikis/QuickProfileLanguage

# For RHEL (SELinux)
# Configure SELinux policies as needed
```

### 4. Regular Updates

```bash
# Enable automatic security updates
sudo apt install -y unattended-upgrades

# Configure
sudo dpkg-reconfigure -plow unattended-upgrades

# Manual updates
sudo apt update && sudo apt upgrade -y
```

### 5. File Permissions

```bash
# Secure application directory
sudo chown -R nato-pmp:nato-pmp /opt/nato-pmp-analyzer
sudo find /opt/nato-pmp-analyzer -type d -exec chmod 755 {} \;
sudo find /opt/nato-pmp-analyzer -type f -exec chmod 644 {} \;
sudo chmod 700 /opt/nato-pmp-analyzer/.env
sudo chmod +x /opt/nato-pmp-analyzer/venv/bin/*
```

---

## Monitoring & Maintenance

### 1. Log Management

```bash
# View application logs
sudo journalctl -u nato-pmp-analyzer -f

# View Nginx access logs
sudo tail -f /var/log/nginx/nato-pmp-analyzer.access.log

# View Nginx error logs
sudo tail -f /var/log/nginx/nato-pmp-analyzer.error.log

# Configure log rotation
sudo nano /etc/logrotate.d/nato-pmp-analyzer
```

```
/opt/nato-pmp-analyzer/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nato-pmp nato-pmp
    sharedscripts
    postrotate
        systemctl reload nato-pmp-analyzer > /dev/null 2>&1 || true
    endscript
}
```

### 2. Backup Strategy

```bash
# Create backup script
sudo nano /opt/nato-pmp-analyzer/backup.sh
```

```bash
#!/bin/bash
# NATO PMP Analyzer Backup Script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/nato-pmp-analyzer/$DATE"
APP_DIR="/opt/nato-pmp-analyzer"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
tar -czf "$BACKUP_DIR/chroma_db.tar.gz" -C "$APP_DIR" chroma_db/

# Backup configuration
cp "$APP_DIR/.env" "$BACKUP_DIR/.env"

# Backup processed documents
cp "$APP_DIR/processed_documents.json" "$BACKUP_DIR/" 2>/dev/null || true

# Cleanup old backups (keep last 7 days)
find /backup/nato-pmp-analyzer/ -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null || true

echo "Backup completed: $BACKUP_DIR"
```

```bash
# Make executable
sudo chmod +x /opt/nato-pmp-analyzer/backup.sh

# Schedule with cron (daily at 2 AM)
sudo crontab -e
# Add:
# 0 2 * * * /opt/nato-pmp-analyzer/backup.sh >> /var/log/nato-pmp-backup.log 2>&1
```

### 3. Monitoring with Systemd

```bash
# Check service status
sudo systemctl status nato-pmp-analyzer

# View recent logs
sudo journalctl -u nato-pmp-analyzer -n 50

# Monitor resources
htop  # or install: sudo apt install htop

# Check disk usage
df -h
du -sh /opt/nato-pmp-analyzer/*
```

### 4. Uptime Monitoring (Optional)

```bash
# Install monitoring tool
# Example: Netdata
bash <(curl -Ss https://my-netdata.io/kickstart.sh)

# Access dashboard: http://SERVER_IP:19999
```

---

## Updating the Application

### Manual Update

```bash
# 1. Backup current version
sudo su - nato-pmp
cd /opt/nato-pmp-analyzer
./backup.sh

# 2. Pull latest changes
git pull origin main

# 3. Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# 4. Restart service
exit
sudo systemctl restart nato-pmp-analyzer

# 5. Check status
sudo systemctl status nato-pmp-analyzer
```

### Automated Updates (Optional)

```bash
# Create update script
sudo nano /opt/nato-pmp-analyzer/update.sh
```

```bash
#!/bin/bash
# NATO PMP Analyzer Update Script

set -e

APP_DIR="/opt/nato-pmp-analyzer"
cd "$APP_DIR"

# Backup
./backup.sh

# Pull updates
sudo -u nato-pmp git pull origin main

# Update dependencies
sudo -u nato-pmp /opt/nato-pmp-analyzer/venv/bin/pip install --upgrade -r requirements.txt

# Restart service
systemctl restart nato-pmp-analyzer

echo "Update completed successfully"
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status nato-pmp-analyzer

# View detailed logs
sudo journalctl -u nato-pmp-analyzer -xe

# Check if port is in use
sudo netstat -tlnp | grep 8501

# Test manual start
sudo su - nato-pmp
cd /opt/nato-pmp-analyzer
source venv/bin/activate
streamlit run app.py
```

### Nginx Errors

```bash
# Test Nginx configuration
sudo nginx -t

# View error logs
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx

# Check if Streamlit is running
curl http://127.0.0.1:8501
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R nato-pmp:nato-pmp /opt/nato-pmp-analyzer

# Fix permissions
sudo chmod -R 755 /opt/nato-pmp-analyzer
sudo chmod 600 /opt/nato-pmp-analyzer/.env
```

### SSL Certificate Issues

```bash
# Test certificate
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Check certificate validity
openssl x509 -in /etc/letsencrypt/live/your-domain.com/fullchain.pem -noout -dates
```

### High Memory Usage

```bash
# Check memory usage
free -h

# Check application memory
sudo systemctl status nato-pmp-analyzer

# Restart service to clear memory
sudo systemctl restart nato-pmp-analyzer

# Consider increasing swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Advanced Configuration

### Custom Domain Configuration

1. **Update DNS records:**
   - Add A record: `nato-pmp.your-domain.com` → `SERVER_IP`

2. **Update Nginx configuration:**
   ```bash
   sudo nano /etc/nginx/sites-available/nato-pmp-analyzer
   # Change server_name to: nato-pmp.your-domain.com
   ```

3. **Obtain SSL certificate:**
   ```bash
   sudo certbot --nginx -d nato-pmp.your-domain.com
   ```

### Load Balancing (Multiple Instances)

```bash
# Run multiple Streamlit instances
# Instance 1: Port 8501
# Instance 2: Port 8502
# Instance 3: Port 8503

# Update Nginx for load balancing
sudo nano /etc/nginx/sites-available/nato-pmp-analyzer
```

```nginx
upstream streamlit_backend {
    least_conn;
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    # ... existing config ...
    location / {
        proxy_pass http://streamlit_backend;
        # ... existing proxy settings ...
    }
}
```

### Database Migration (PostgreSQL)

For production with persistent data needs:

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE nato_pmp_db;
CREATE USER nato_pmp WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE nato_pmp_db TO nato_pmp;
\q

# Update application to use PostgreSQL
# (Requires code changes)
```

---

## Performance Optimization

### 1. Enable Caching

```bash
# Add to .env
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### 2. Increase File Descriptors

```bash
# Edit limits
sudo nano /etc/security/limits.conf

# Add:
nato-pmp soft nofile 65536
nato-pmp hard nofile 65536
```

### 3. Optimize Nginx

```bash
sudo nano /etc/nginx/nginx.conf
```

```nginx
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    # ... existing config ...

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
}
```

---

## Uninstall

```bash
# Stop and disable service
sudo systemctl stop nato-pmp-analyzer
sudo systemctl disable nato-pmp-analyzer

# Remove service file
sudo rm /etc/systemd/system/nato-pmp-analyzer.service
sudo systemctl daemon-reload

# Remove Nginx configuration
sudo rm /etc/nginx/sites-enabled/nato-pmp-analyzer
sudo rm /etc/nginx/sites-available/nato-pmp-analyzer
sudo systemctl reload nginx

# Remove SSL certificate (if Let's Encrypt)
sudo certbot delete --cert-name your-domain.com

# Remove application
sudo rm -rf /opt/nato-pmp-analyzer

# Remove user (optional)
sudo userdel -r nato-pmp
```

---

## Additional Resources

- **Ubuntu Server Guide:** https://ubuntu.com/server/docs
- **Systemd Documentation:** https://systemd.io/
- **Nginx Documentation:** https://nginx.org/en/docs/
- **Let's Encrypt:** https://letsencrypt.org/docs/
- **Security Hardening:** https://www.cisecurity.org/

---

## Next Steps

After successful server deployment:

1. ✅ Configure automated backups
2. ✅ Set up monitoring and alerting
3. ✅ Perform security audit
4. ✅ Document admin procedures
5. ✅ Train users
6. ✅ Create disaster recovery plan

---

**Last Updated:** November 15, 2025
**Deployment Type:** Production Internal Server
**Security Level:** NATO-Ready
