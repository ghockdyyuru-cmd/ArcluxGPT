#!/bin/bash

# Warna Terminal untuk Estetika
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}     ARCLUX CORE INTEGRATION v1.0 - INSTALLER       ${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e "Preparing environment for independent architecture..."
echo ""

# 1. Update dan Upgrade Repositori Termux
echo -e "${GREEN}[*]${NC} Updating packages..."
pkg update -y && pkg upgrade -y

# 2. Install Python dan Git jika belum ada
echo -e "${GREEN}[*]${NC} Checking core dependencies..."
pkg install python git -y

# 3. Install modul Python yang dibutuhkan
echo -e "${GREEN}[*]${NC} Installing required Python libraries..."
pip install --upgrade pip
pip install requests scapy

# 4. Memberikan izin eksekusi pada file utama
if [ -f "arclux.py" ]; then
    chmod +x arclux.py
fi

echo ""
echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}  INSTALLATION SUCCESSFUL! UNRESTRICTED CORE READY  ${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e "To start the machine, run: ${GREEN}python arclux.py${NC}"
echo ""

