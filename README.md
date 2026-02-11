# 🐍 Python Cybersecurity Tools

This repository contains **small, focused Python tools** used for **cybersecurity analysis, automation, and incident response support**.

The scripts included here are practical utilities developed for real-world scenarios such as:
- Email and header analysis
- Basic forensic and log processing
- File and data manipulation
- Security-related automation tasks

All scripts are compatible with **Python 3.12+** unless stated otherwise.

---

## 📂 Repository Structure

The tools are organized by use case to keep the repository clear and easy to navigate:

- **Email & Messaging Security**
- **File & Data Processing**
- **Threat Intelligence & Analysis**
- **Automation & Utilities**
- **PowerShell scripts for Windows environments**
- **Documentation and operational notes**

This repository is intended as a **toolbox**, not as a single application or framework.

---

## 🔧 Featured Tools

### 🔹 LCM & GCD Calculator
📁 `tools/file_processing/mcm_MCD.py`

**Functionality:**
- Generates prime numbers from 1 to *n*
- Performs prime factorization
- Calculates:
  - Least Common Multiple (LCM)
  - Greatest Common Divisor (GCD)

---

### 🔹 Mouse Automation Script (Windows)
📁 `tools/misc/clic.py`

Automates repetitive mouse actions on Windows systems.

**Highlights:**
- Progress bar and colored output
- Clipboard interaction
- Useful for repetitive operational tasks

---

### 🔹 Image URL Overlay Tool
📁 `tools/file_processing/mezclarImg.py`

Adds a URL overlay to an image and combines it with another image.

**Process:**
- Accepts a user-provided URL
- Writes the URL onto an image
- Resizes images to a common width
- Vertically concatenates them into a single output image

---

### 🔹 Email Header Extraction
📁 `tools/log_analysis/header_mail.py`

Extracts and copies email headers for analysis.

**Steps:**
1. Select a `.eml` file via file dialog
2. Parse the email headers
3. Copy headers to clipboard
4. Display a temporary confirmation label

Useful for **email analysis and incident response**.

---
## 🔐 Endpoint Hygiene & Automation
📁 `tools/endpoint_hygiene`

- **endpoint_hygiene/**
  - Windows endpoint hygiene checks and safe remediation
  - PowerShell + Python automation
  - Focused on security, stability, and transparency
---

## 📄 Documentation

Additional guides and notes can be found in the `docs/` directory, including:
- [Commands List](/docs/Comands.md)
- [OpenVAS installation notes](/docs/instalar_OpenVas.md) 
- [Kali Linux maintenance tips](/docs/kali-mantenimiento.md)
- [Exchange and Active Directory connection guides](/docs/Guia_conexion_Exchange_y_AD.md)
- [Post-Format Console Configuration Manual](/docs/Manual_Config.md)
- [Fish Shell + Oh My Posh](/docs/fish-shell-setup.md)

---

## ⚠️ Notes

- Some scripts are **Windows-specific** (PowerShell or GUI-based).
- Executable files (`.exe`) are provided for convenience but **source code is always available**.
- This repository focuses on **utility and clarity**, not on enterprise-scale tooling.

---

## 📜 License

This project is licensed under the **MIT License**.
