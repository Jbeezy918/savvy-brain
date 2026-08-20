# Savvy Brain Dashboard - Deployment Guide

## Production Deployment Options

### Option 1: Streamlit Cloud (Easiest)
```bash
# Push to GitHub (if not already)
git add .
git commit -m "Dashboard production ready"
git push

# Then deploy via https://streamlit.io/cloud
# Connect your GitHub repo and select /dashboard/app.py as entry point
```

### Option 2: Self-Hosted (Recommended for you)
Deploy on your own server (savvytechautomations.com infrastructure):

```bash
# 1. SSH into your server
ssh user@savvytechautomations.com

# 2. Clone the repo
git clone <your-repo-url> /var/www/savvy-brain

# 3. Install dependencies
cd /var/www/savvy-brain/dashboard
pip install -r requirements.txt

# 4. Start with systemd or supervisor
# Create /etc/systemd/system/savvy-brain-dashboard.service:
[Unit]
Description=Savvy Brain Dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/savvy-brain/dashboard
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port 8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable savvy-brain-dashboard
sudo systemctl start savvy-brain-dashboard

# 5. Add nginx reverse proxy
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name dashboard.savvytechautomations.com;
    
    location / {
        proxy_pass http://streamlit;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Option 3: Docker (Scalable)
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app
COPY dashboard/requirements.txt .
RUN pip install -r requirements.txt

COPY dashboard/ .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# Build and run
docker build -t savvy-brain-dashboard .
docker run -p 8501:8501 savvy-brain-dashboard
```

## Pre-Deployment Checklist

- [ ] Database connection tested (local SQLite or remote)
- [ ] All environment variables set (.env file)
- [ ] Theme colors validated in production browser
- [ ] Navigation links tested
- [ ] KPI cards pulling live data
- [ ] Approvals workflow tested
- [ ] Agent controls working
- [ ] File upload pipeline tested

## Environment Variables

Create `.env` file:
```
DATABASE_URL=sqlite:///savvy_brain.db
STREAMLIT_SERVER_PORT=8501
LOG_LEVEL=error
```

## Monitoring

```bash
# Check logs
tail -f /var/log/savvy-brain-dashboard.log

# Check uptime
systemctl status savvy-brain-dashboard

# Restart if needed
sudo systemctl restart savvy-brain-dashboard
```

## URL After Deployment
- Streamlit Cloud: `https://savvy-brain-<username>.streamlit.app`
- Self-Hosted: `https://dashboard.savvytechautomations.com`
- Docker: `http://localhost:8501`
