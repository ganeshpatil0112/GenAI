# 📦 Windows to H100 GPU Transfer Guide

Complete guide to transfer your fine-tuned models from Windows to H100 GPU server

---

## 🎯 What You Need to Transfer

### **Essential Files** (Must transfer):
```
✅ models/                    # Your trained models (~2-5 GB)
✅ api_server.py              # API server code
✅ Dockerfile                 # Docker configuration
✅ docker-compose.yml         # Docker Compose config
✅ requirements.txt           # Python dependencies
✅ requirements_api.txt       # API dependencies
```

### **Optional but Recommended**:
```
📄 datasets/                  # Training datasets (if needed)
📄 start_api.py              # Quick start script
📄 test_api.py               # Testing script
📄 client_example.py         # Python client
📄 README.md                 # Documentation
📄 API_README.md             # API docs
```

### **NOT Needed on Server**:
```
❌ finetuning/               # Training scripts (not needed for inference)
❌ test_*.py                 # Local test scripts
❌ *.md                      # Documentation files (except API_README.md)
```

---

## 🚀 Transfer Methods (Choose One)

### **Method 1: PowerShell Script** (Automated) ⭐ Recommended
### **Method 2: WinSCP** (GUI) ⭐ Easiest
### **Method 3: Manual SCP** (Command Line)
### **Method 4: FTP/SFTP Client**

---

## 📝 Method 1: PowerShell Script (Automated)

I've created an automated script for you!

### Step 1: Configure the Script

Edit `transfer_to_h100.ps1` and change these lines:

```powershell
# Line 5-7: Update with your H100 server details
$SERVER_IP = "192.168.1.100"        # Your H100 server IP
$SERVER_USER = "username"            # Your username
$SERVER_PATH = "~/finetuningfinal"  # Destination path
```

### Step 2: Run the Script

```powershell
# In PowerShell, navigate to your project
cd D:\finetuningfinal

# Run the transfer script
.\transfer_to_h100.ps1
```

### Step 3: Follow On-Screen Instructions

The script will:
1. ✅ Check which files exist
2. ✅ Create a compressed archive
3. ✅ Transfer to H100 server
4. ✅ Show next steps

**Expected output:**
```
========================================
Transfer to H100 GPU Server
========================================

1. Preparing files for transfer...
  ✓ models
  ✓ api_server.py
  ✓ Dockerfile
  ...

Total size: 2.5 GB
Server: user@192.168.1.100

Proceed with transfer? (y/n): y

2. Creating compressed archive...
✓ Archive created successfully!

3. Transferring to H100 server...
[Progress bar]

✓ Transfer completed successfully!
```

---

## 🖥️ Method 2: WinSCP (GUI - Easiest)

### Step 1: Install WinSCP

```powershell
# Download from: https://winscp.net/eng/download.php
# Or install via winget:
winget install WinSCP.WinSCP
```

### Step 2: Connect to H100 Server

1. Open WinSCP
2. Enter connection details:
   - **Host name**: Your H100 server IP (e.g., 192.168.1.100)
   - **User name**: Your username
   - **Password**: Your password
   - **Port**: 22
3. Click **Login**

### Step 3: Transfer Files

1. **Left panel**: Navigate to `D:\finetuningfinal`
2. **Right panel**: Navigate to `/home/username/`
3. **Select folders to transfer**:
   - `models/`
   - `api_server.py`
   - `Dockerfile`
   - `docker-compose.yml`
   - `requirements*.txt`
4. **Drag and drop** from left to right
5. Wait for transfer to complete

### Step 4: Verify Transfer

Check file sizes match on both sides.

---

## 💻 Method 3: Manual SCP (Command Line)

### Prerequisites:

Install OpenSSH (if not installed):
```powershell
# Check if installed
ssh -V

# If not installed:
Add-WindowsCapability -Online -Name OpenSSH.Client
```

### Step 1: Create Archive Manually

```powershell
cd D:\finetuningfinal

# Compress files
Compress-Archive -Path models,api_server.py,Dockerfile,docker-compose.yml,requirements.txt,requirements_api.txt -DestinationPath h100_transfer.zip
```

### Step 2: Transfer via SCP

```powershell
# Transfer archive
scp h100_transfer.zip username@192.168.1.100:~/

# Or transfer individual directories
scp -r models username@192.168.1.100:~/finetuningfinal/
scp api_server.py Dockerfile docker-compose.yml username@192.168.1.100:~/finetuningfinal/
```

### Step 3: Extract on Server

```bash
# SSH to server
ssh username@192.168.1.100

# Extract files
unzip ~/h100_transfer.zip -d ~/finetuningfinal/

# Or create directory if needed
mkdir -p ~/finetuningfinal
cd ~/finetuningfinal
```

---

## 🌐 Method 4: FTP/SFTP Client

### Using FileZilla:

1. **Download**: https://filezilla-project.org/
2. **Install and open**
3. **Connect**:
   - Host: `sftp://192.168.1.100`
   - Username: Your username
   - Password: Your password
   - Port: 22
4. **Transfer files** via drag-and-drop

---

## 📊 Transfer Time Estimates

Based on file sizes and network speed:

| Network Speed | 2 GB Models | 5 GB Models |
|---------------|-------------|-------------|
| **1 Gbps (LAN)** | 2-3 minutes | 5-7 minutes |
| **100 Mbps** | 3-5 minutes | 7-10 minutes |
| **10 Mbps** | 30 minutes | 60-90 minutes |
| **1 Mbps (slow)** | 4-5 hours | 10-12 hours |

💡 **Tip**: Transfer during off-peak hours for faster speeds

---

## 🔧 On H100 Server (After Transfer)

### Step 1: SSH to Server

```bash
ssh username@192.168.1.100
```

### Step 2: Extract Files (if compressed)

```bash
# Navigate to home directory
cd ~

# Extract archive
unzip h100_transfer.zip -d ~/finetuningfinal

# Or if using finetuning_h100_*.zip
unzip finetuning_h100_*.zip -d ~/finetuningfinal
```

### Step 3: Navigate to Directory

```bash
cd ~/finetuningfinal

# Verify files transferred
ls -lh
```

Expected output:
```
drwxr-xr-x 5 user user 4.0K models/
-rw-r--r-- 1 user user  15K api_server.py
-rw-r--r-- 1 user user 1.2K Dockerfile
-rw-r--r-- 1 user user  450 docker-compose.yml
-rw-r--r-- 1 user user  238 requirements.txt
-rw-r--r-- 1 user user  156 requirements_api.txt
```

### Step 4: Verify Models

```bash
# Check models directory
ls -lh models/

# Should see:
# hr_full_finetuned/
# sales_peft_finetuned/
# healthcare_lora_finetuned/
# marketing_qlora_finetuned/
```

### Step 5: Deploy with Docker

```bash
# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify GPU is detected
docker-compose exec llm-api python -c "import torch; print(f'GPU: {torch.cuda.is_available()}')"
```

---

## ✅ Verification Checklist

After transfer, verify on H100 server:

```bash
# Check files exist
ls ~/finetuningfinal/api_server.py      # Should exist
ls ~/finetuningfinal/Dockerfile         # Should exist
ls ~/finetuningfinal/models/            # Should exist

# Check file sizes
du -sh ~/finetuningfinal/models         # Should be ~2-5 GB

# Check models
ls ~/finetuningfinal/models/            # Should show model directories

# Test Python imports
python3 -c "import torch; print(torch.__version__)"
python3 -c "import transformers; print(transformers.__version__)"
```

---

## 🐛 Troubleshooting

### Problem: SSH Connection Refused

```powershell
# Solution 1: Check if SSH service is running on server
# On server:
sudo systemctl status ssh
sudo systemctl start ssh

# Solution 2: Check firewall
# On server:
sudo ufw status
sudo ufw allow 22/tcp
```

### Problem: Permission Denied

```bash
# Solution: Check SSH key or use password authentication
ssh -o PreferredAuthentications=password username@server_ip
```

### Problem: Transfer Interrupted

```powershell
# Solution: Use rsync for resumable transfer
# Install WSL or use rsync for Windows
rsync -avz --progress -e ssh ./models username@server_ip:~/finetuningfinal/
```

### Problem: Disk Space Full on Server

```bash
# Check available space
df -h

# Clean up if needed
docker system prune -a
```

### Problem: Transfer Too Slow

**Solutions**:
1. **Compress first**: Use higher compression
   ```powershell
   Compress-Archive -CompressionLevel Optimal
   ```

2. **Use rsync with compression**:
   ```bash
   rsync -avz --compress-level=9
   ```

3. **Transfer during off-peak hours**

4. **Use direct connection** (not VPN)

---

## 🚀 Quick Reference Commands

### Windows Side:

```powershell
# Navigate to project
cd D:\finetuningfinal

# Run automated script
.\transfer_to_h100.ps1

# Or manual transfer
scp -r models username@SERVER_IP:~/finetuningfinal/
```

### H100 Server Side:

```bash
# Connect
ssh username@SERVER_IP

# Navigate
cd ~/finetuningfinal

# Extract (if needed)
unzip *.zip

# Deploy
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f

# Test GPU
nvidia-smi
```

---

## 📁 Complete File Structure After Transfer

On H100 server, you should have:

```
~/finetuningfinal/
├── models/
│   ├── hr_full_finetuned/
│   ├── sales_peft_finetuned/
│   ├── healthcare_lora_finetuned/
│   └── marketing_qlora_finetuned/
├── api_server.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements_api.txt
├── start_api.py (optional)
├── test_api.py (optional)
└── client_example.py (optional)
```

---

## 🎯 Next Steps After Transfer

1. ✅ Extract files on server
2. ✅ Verify all files present
3. ✅ Deploy with Docker: `docker-compose up -d`
4. ✅ Check GPU detection: `nvidia-smi`
5. ✅ Test API: `curl http://localhost:8000/health`
6. ✅ Access from your machine: `http://SERVER_IP:8000/docs`

---

## 💡 Pro Tips

### 1. Use SSH Keys (No Password)

```powershell
# Generate SSH key
ssh-keygen -t rsa -b 4096

# Copy to server
type $env:USERPROFILE\.ssh\id_rsa.pub | ssh username@server_ip "cat >> ~/.ssh/authorized_keys"

# Now you can connect without password
ssh username@server_ip
```

### 2. Speed Up Transfers

```bash
# Use compression
scp -C archive.zip username@server_ip:~/

# Use multiple connections (if available)
# Install parallel-scp or use rsync
```

### 3. Automate with Task Scheduler

Create a scheduled task to run `transfer_to_h100.ps1` automatically.

---

## 🔒 Security Considerations

1. **Use SSH keys** instead of passwords
2. **Change default SSH port** (22 → custom)
3. **Enable firewall** on server
4. **Use VPN** for remote access
5. **Encrypt sensitive data** before transfer

---

## ✅ Transfer Checklist

- [ ] H100 server accessible via SSH
- [ ] Server IP and credentials configured
- [ ] All model files present locally
- [ ] Sufficient disk space on server (~10GB free)
- [ ] Transfer method chosen (Script/WinSCP/SCP)
- [ ] Files transferred successfully
- [ ] Files extracted on server
- [ ] Docker and NVIDIA runtime installed on server
- [ ] Ready to deploy!

---

**Ready to transfer? Run:**

```powershell
.\transfer_to_h100.ps1
```

**Or use WinSCP for GUI transfer!**

