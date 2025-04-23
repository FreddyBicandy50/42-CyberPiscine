# Makefile for the inquisitor project

# Variables
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip
SCRIPT=inquisitor.py
SYMLINK=/usr/local/bin/inquisitor

# Default target
all: install

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)

# Install Python & system dependencies
install: venv
	@echo "Installing Python dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install scapy pycryptodome
	@echo "Installing system packages..."
	sudo apt-get update
	sudo apt-get install -y tcpdump libpcap-dev
	@echo "Making script executable..."
	chmod +x $(SCRIPT)
	@echo "Creating symlink..."
	sudo mkdir -p /usr/local/bin
	sudo ln -sf "$(CURDIR)/$(SCRIPT)" "$(SYMLINK)"
	@echo "Installation complete."

# Clean everything
clean:
	@echo "Cleaning virtual environment and symlink..."
	rm -rf $(VENV_DIR)
	sudo rm -f $(SYMLINK)
	@echo "Cleanup complete."

.PHONY: all install clean venv
