<#
.SYNOPSIS
  Dev setup script for Windows (PowerShell)
#>

Set-StrictMode -Version Latest

Write-Host "Setting up dev environment (Windows)..."

# Ensure running as admin for Docker/WSL/Hyper-V operations if needed.
# Install Python (suggest manual install), then run:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r agents/requirements.txt
pip install -r web-app/backend/requirements.txt

Write-Host "Dev environment setup complete."