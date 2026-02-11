# 🧰 Post-Format Console Configuration Manual

Guide to restoring and customizing your work environment on Windows with support for WSL, PowerShell, CMD, and Oh-My-Posh. Ideal for developers and enthusiasts who want an efficient and visually appealing setup.

> [Return](README.md)

---

## 📦 Installation Order

### 1. Install PowerShell 7
- Download from [GitHub Releases](https://github.com/PowerShell/PowerShell/releases) or Use winget
  Search Version
  ```bash
  winget search Microsoft.PowerShell
  ```
  Select version with ID and install
  ```bash
  winget install --id Microsoft.PowerShell --source winget
  ```
- Verify with:
  ```bash
  pwsh
  ```

  🚫 Hide Windows PowerShell (v5) from Windows Terminal
  1. Open Windows Terminal.
  2. Click the dropdown arrow (˅) next to the tab bar and select Settings.
  3. In Startup > Default Profile, set it to PowerShell 7 (or your preferred shell).
  4. Go to Profiles > Windows PowerShell (this is version 5).
  5. Scroll down and enable Hide profile from dropdown.
  6. Save the changes and close the settings.

### 2. Install Python
- Download from [python.org](https://www.python.org/downloads/)
- Check the "Add Python to PATH" option during installation
- Verify the installation:
  ```bash
  python --version
  ```
  
### 3. Install Git
- Download from [git-scm.com](https://git-scm.com/) or Winget
  ```powershell
  winget install --id Git.Git -e --source winget
  ```
- During setup:
  - "Use Git from the command line and also from 3rd-party software"
  - "Checkout as-is, commit Unix-style line endings"

- Configure Git:
  1. Open Windows Terminal.
  2. Click the dropdown arrow (˅) next to the tab bar and select GitBash.
     
  ```bash
  git config --global user.name "YourName"
  git config --global user.email "youremail@example.com"
  ```
- Verify config:
  ```bash
  git config list
  ``` 

### 4. Install Miniconda (optional)
- Download from [anaconda.com](https://www.anaconda.com/)
- Create virtual environments using `conda` or use `venv` for a lighter setup

> install Conda:
> ```cmd
> curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe --output .\Miniconda3-latest-Windows-x86_64.exe
> ```

  ➕ Add Anaconda PowerShell Prompt to Windows Terminal (Manual Method)
  1. Search for Anaconda PowerShell Prompt in the Windows Start Menu.
  2. Right-click > Open file location.
  3. In the File Explorer window, right-click on the shortcut > Properties.
  4. Go to he Shortcut tab:
    - Copy the content from Target (this is your launch command).
    - Click Change Icon and copy the path of the icon shown there.
  5. Now open Windows Terminal > Settings.
  6. Add a New Profile:
    - Name: Anaconda PowerShell
    - Command line: Paste the value copied from the Target field.
    - Icon: Paste the path from the Change Icon window.
  7. Save the changes and you're done!
  
  > Repeat the same steps for the Anaconda Prompt (CMD version) if desired.

#### ➕ Initialize Conda for ZSH
  1. Download Miniconda in your home directory (`~/Download/`).
     ```bash
     wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
     ```
  2. Install Miniconda
      ```bash
      bash Miniconda3-latest-Linux-x86_64.sh
      ```

      During installation:
      - Accept the license
      - Install path: ~/miniconda3
      - Initialize Conda → YES
  2. Initialize Conda for ZSH:
     ```bash
     conda init zsh
     ```
  3. Reload the shell:
     ```bash
     source ~/.zshrc
     ```
  4. Verify installation:
     ```bash
     conda --version
     ```

  ➕ Create and use a Conda environment
  ```bash
  conda create -n lab python=3.12
  conda activate lab
  ```

### 5. WSL and Linux Distribution Setup

**Prerequisites**

  1. Enable WSL from "Turn Windows features on or off":
    - Check the box: Windows Subsystem for Linux
    - Check the box: Virtual Machine Platform
  2. Restart your PC.
  3. Open Task Manager > Performance and check that Virtualization is enabled in your system.

  Install WSL with Your prefer distribution

  ```powershell
  wsl --list --online
  wsl --install -d kali-linux
  ```
  > Make sure to restart and open Linux Distribution at least once to complete the installation.
  
  ### _Troubleshooting:_
  If you get the error `Wsl/CallMsi/Install/REGDB_E_CLASSNOTREG`:
  1. Visit the [WSL releases page](https://github.com/microsoft/WSL/releases/)
  2. Download and install the **latest version** for your system
  3. Verify installation with:
  ```powershell
  wsl --list --online
  ```

  ### _Win-Kex On Kali-Linux:_
  Win-KeX provides a GUI desktop experience for Kali Linux in Windows Subsystem for Linux (WSL 2)
  1. Visit the [Win-Kex](https://www.kali.org/docs/wsl/win-kex/#install-win-kex).
  2. Install Win-Kex and include large Kali-linux and shortcut on Terminal. 
  ```powershell
 kali@kali:~$ sudo apt update
 kali@kali:~$
 kali@kali:~$ sudo apt install -y kali-win-kex
  ```

---

## 💻 Consoles and Customization

### 6. Verify if Windows Terminal was installed (recommended)
- From Microsoft Store or [GitHub](https://github.com/microsoft/terminal)

### 7. Install Clink (for CMD)
- Download from [chrisant996/clink](https://github.com/chrisant996/clink/releases)
> Enhances CMD experience and allows the use of Oh-My-Posh

### 8. Install Oh-My-Posh PowerShell
- [Oh-My-Posh Page](https://ohmyposh.dev/docs/installation/windows)
  
```powershell
winget install JanDeDobbeleer.OhMyPosh -s winget
```
- After installation, **close** the console
- **Run as Administrator**, then execute:
```powershell
oh-my-posh font install
```
- Select your preferred font (e.g., FiraCode)
- Open Windows Terminal > Settings > Defaults > Appearance:
  - **Font face**: select preferred font (e.g., `FiraCode Nerd Font Mono`)
  > Mono fonts are recommended to maintain correct spacing
- Try open
   ```powershell
  notepad $PROFILE
  ```
  When the above command gives an error, make sure to create the profile first and add the oh-my-posh init above.
  
  ```powershell
  New-Item -Path $PROFILE -Type File -Force
  ```
  add next line, save and rebbot terminal
  ```text
  oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/craver.omp.json" | Invoke-Expression
  ```
  > use comand `set` on CMD for search environment variables
  Now install Terminals-Icons 
  ```powershell
  Install-Module -Name Terminal-Icons -Repository PSGallery
  ```
  Now add this line to `$PROFILE` this use icons and can use ListView
  
  ```powershell
  Import-Module Terminal-Icons
  Set-PSReadLineOption -PredictionViewStyle ListView
  ```
#### CMD + Clink:
  1. In CMD, check if `oh-my-posh` works.
  2. Run `clink info` and locate the scripts folder.
  3. Copy the path to your `%LocalAppData%\clink\scripts` folder.
  4. Create a file named `oh-my-posh.lua` in that folder.
  5. Add this line (update `<YourUser>` accordingly):
  ```lua
  load(io.popen('oh-my-posh init cmd --config "C:/Users/<YourUser>/AppData/Local/Programs/oh-my-   posh/themes/craver_edit.omp.json"'):read("*a"))()
  ```
  6. To find the correct path, use `set` in CMD and search for `oh-my-posh` theme paths.
  7. Restart CMD and execute:
  ```bash
  clink set prompt.transient always
  ```
  > This ensures a clean one-line prompt each time.

---

#### WSL (bash):
```bash
eval "$(oh-my-posh init bash --config ~/.poshthemes/craver-style.omp.json)"
```
---

## 🎯 Final Recommendations

I prefer Transient style!, then I add this lines on `.omp.json`:
```bash
  {
  "transient_prompt": {
    "background": "transparent",
    "foreground": "#ffffff",
    "template": "{{ .Shell }}> "
  }
}
```

- Keep this file updated and synced with your GitHub
- Use VSCode's cloud sync feature by signing in
- Store your `.omp.json` theme in a backup repo

---

> Created with ❤️ by [YourName] for developers who love having a clean and productive environment.

