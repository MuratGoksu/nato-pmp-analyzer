#!/bin/bash
# NATO PMP Analyzer - Automated Server Installation Script
# For Ubuntu 20.04/22.04 LTS

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_USER="nato-pmp"
APP_DIR="/opt/nato-pmp-analyzer"
APP_PORT="8501"
PYTHON_VERSION="3.10"

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}NATO PMP Analyzer - Server Installation${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root (use sudo)${NC}"
   exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    OS_VERSION=$VERSION_ID
else
    echo -e "${RED}Cannot detect OS version${NC}"
    exit 1
fi

echo -e "${YELLOW}Detected OS: $OS $OS_VERSION${NC}"

# Check if Ubuntu
if [ "$OS" != "ubuntu" ]; then
    echo -e "${YELLOW}Warning: This script is designed for Ubuntu. Continue? (y/n)${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}Step 1: Updating system packages${NC}"
apt update
apt upgrade -y

echo ""
echo -e "${GREEN}Step 2: Installing essential packages${NC}"
apt install -y \
    git \
    curl \
    wget \
    vim \
    ufw \
    build-essential \
    software-properties-common \
    nginx \
    certbot \
    python3-certbot-nginx \
    fail2ban

echo ""
echo -e "${GREEN}Step 3: Installing Python $PYTHON_VERSION${NC}"
if ! command -v python$PYTHON_VERSION &> /dev/null; then
    add-apt-repository -y ppa:deadsnakes/ppa
    apt update
    apt install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-dev
fi

# Verify Python installation
python$PYTHON_VERSION --version

echo ""
echo -e "${GREEN}Step 4: Creating application user${NC}"
if id "$APP_USER" &>/dev/null; then
    echo -e "${YELLOW}User $APP_USER already exists${NC}"
else
    useradd -r -m -s /bin/bash $APP_USER
    echo -e "${GREEN}Created user: $APP_USER${NC}"
fi

echo ""
echo -e "${GREEN}Step 5: Creating application directory${NC}"
mkdir -p $APP_DIR
chown $APP_USER:$APP_USER $APP_DIR

echo ""
echo -e "${YELLOW}Application directory created: $APP_DIR${NC}"
echo -e "${YELLOW}You need to:${NC}"
echo -e "  1. Copy application files to: $APP_DIR"
echo -e "  2. Or clone from Git repository"
echo ""
echo -e "${YELLOW}Continue with Git clone? (y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Enter Git repository URL:${NC}"
    read -r GIT_REPO

    if [ ! -z "$GIT_REPO" ]; then
        cd $APP_DIR
        sudo -u $APP_USER git clone "$GIT_REPO" .
        echo -e "${GREEN}Repository cloned successfully${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Step 6: Setting up Python virtual environment${NC}"
cd $APP_DIR
sudo -u $APP_USER python$PYTHON_VERSION -m venv venv
echo -e "${GREEN}Virtual environment created${NC}"

if [ -f "$APP_DIR/requirements.txt" ]; then
    echo -e "${GREEN}Installing Python dependencies...${NC}"
    sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
    sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt
    echo -e "${GREEN}Dependencies installed${NC}"
else
    echo -e "${YELLOW}requirements.txt not found. Skipping dependency installation.${NC}"
fi

echo ""
echo -e "${GREEN}Step 7: Creating .env file${NC}"
if [ ! -f "$APP_DIR/.env" ]; then
    cat > $APP_DIR/.env << EOF
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
OPENAI_MODEL=gpt-4-turbo-preview

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Application Settings
STREAMLIT_SERVER_PORT=$APP_PORT
STREAMLIT_SERVER_ADDRESS=127.0.0.1
EOF
    chown $APP_USER:$APP_USER $APP_DIR/.env
    chmod 600 $APP_DIR/.env
    echo -e "${GREEN}.env file created${NC}"
    echo -e "${YELLOW}IMPORTANT: Edit $APP_DIR/.env and add your API keys!${NC}"
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi

echo ""
echo -e "${GREEN}Step 8: Creating necessary directories${NC}"
sudo -u $APP_USER mkdir -p $APP_DIR/chroma_db
sudo -u $APP_USER mkdir -p $APP_DIR/logs
sudo -u $APP_USER mkdir -p $APP_DIR/data

echo ""
echo -e "${GREEN}Step 9: Installing systemd service${NC}"
if [ -f "$APP_DIR/nato-pmp-analyzer.service" ]; then
    cp $APP_DIR/nato-pmp-analyzer.service /etc/systemd/system/
    systemctl daemon-reload
    echo -e "${GREEN}Systemd service installed${NC}"
else
    echo -e "${YELLOW}Service file not found. Creating default service...${NC}"
    cat > /etc/systemd/system/nato-pmp-analyzer.service << 'EOF'
[Unit]
Description=NATO PMP Analyzer
After=network.target

[Service]
Type=simple
User=nato-pmp
WorkingDirectory=/opt/nato-pmp-analyzer
EnvironmentFile=/opt/nato-pmp-analyzer/.env
ExecStart=/opt/nato-pmp-analyzer/venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1 --server.headless=true
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
fi

echo ""
echo -e "${GREEN}Step 10: Configuring Nginx${NC}"
if [ -f "$APP_DIR/nginx.conf" ]; then
    echo -e "${YELLOW}Enter your domain name (or press Enter to skip):${NC}"
    read -r DOMAIN_NAME

    if [ ! -z "$DOMAIN_NAME" ]; then
        cp $APP_DIR/nginx.conf /etc/nginx/sites-available/nato-pmp-analyzer
        sed -i "s/your-domain.com/$DOMAIN_NAME/g" /etc/nginx/sites-available/nato-pmp-analyzer

        # Temporarily comment out SSL lines (will be added by Certbot)
        sed -i 's/ssl_certificate/#ssl_certificate/g' /etc/nginx/sites-available/nato-pmp-analyzer
        sed -i 's/listen 443/#listen 443/g' /etc/nginx/sites-available/nato-pmp-analyzer

        ln -sf /etc/nginx/sites-available/nato-pmp-analyzer /etc/nginx/sites-enabled/

        # Test Nginx configuration
        nginx -t

        systemctl reload nginx
        echo -e "${GREEN}Nginx configured for domain: $DOMAIN_NAME${NC}"
    else
        echo -e "${YELLOW}Skipping Nginx configuration${NC}"
    fi
else
    echo -e "${YELLOW}Nginx config file not found. Skipping.${NC}"
fi

echo ""
echo -e "${GREEN}Step 11: Configuring firewall (UFW)${NC}"
ufw --force enable
ufw allow ssh
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw status verbose

echo ""
echo -e "${GREEN}Step 12: Starting services${NC}"
systemctl enable nato-pmp-analyzer
systemctl start nato-pmp-analyzer
systemctl enable nginx

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Check service status
if systemctl is-active --quiet nato-pmp-analyzer; then
    echo -e "${GREEN}✓ NATO PMP Analyzer is running${NC}"
else
    echo -e "${RED}✗ NATO PMP Analyzer failed to start${NC}"
    echo -e "${YELLOW}Check logs: sudo journalctl -u nato-pmp-analyzer -xe${NC}"
fi

echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. Edit configuration: sudo nano $APP_DIR/.env"
echo -e "  2. Add your OpenAI API key"
echo -e "  3. Restart service: sudo systemctl restart nato-pmp-analyzer"
echo -e "  4. Check status: sudo systemctl status nato-pmp-analyzer"
echo -e "  5. View logs: sudo journalctl -u nato-pmp-analyzer -f"
echo ""

if [ ! -z "$DOMAIN_NAME" ]; then
    echo -e "${YELLOW}SSL Setup:${NC}"
    echo -e "  Run: sudo certbot --nginx -d $DOMAIN_NAME"
    echo -e "  Then access: https://$DOMAIN_NAME"
    echo ""
fi

echo -e "${YELLOW}Access Application:${NC}"
echo -e "  Local: http://localhost:$APP_PORT"
if [ ! -z "$DOMAIN_NAME" ]; then
    echo -e "  Domain: http://$DOMAIN_NAME"
fi
echo ""

echo -e "${GREEN}Installation script completed!${NC}"
