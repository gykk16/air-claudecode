# GitHub CLI (gh) Installation Guide

GitHub CLI is the official command-line tool for using GitHub from the terminal.

- Official site: https://cli.github.com/
- GitHub repository: https://github.com/cli/cli

---

## macOS

### Homebrew (Recommended)

```bash
brew install gh
```

Upgrade:

```bash
brew upgrade gh
```

### MacPorts

```bash
sudo port install gh
```

### Conda

```bash
conda install gh --channel conda-forge
```

---

## Windows

### WinGet (Recommended)

```powershell
winget install --id GitHub.cli
```

Upgrade:

```powershell
winget upgrade --id GitHub.cli
```

> When using Windows Terminal, you need to open a new window for PATH changes to take effect.

### Scoop

```powershell
scoop install gh
```

### Chocolatey

```powershell
choco install gh
```

---

## Linux

### Debian / Ubuntu / Raspberry Pi (apt)

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
  && sudo mkdir -p -m 755 /etc/apt/keyrings \
  && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
  && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && sudo mkdir -p -m 755 /etc/apt/sources.list.d \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && sudo apt update \
  && sudo apt install gh -y
```

### Fedora (dnf5)

```bash
sudo dnf install dnf5-plugins
sudo dnf config-manager addrepo --from-repofile=https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh --repo gh-cli
```

### Amazon Linux 2 (yum)

```bash
sudo yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo yum install gh
```

### openSUSE / SUSE (zypper)

```bash
sudo zypper addrepo https://cli.github.com/packages/rpm/gh-cli.repo
sudo zypper ref
sudo zypper install gh
```

### Arch Linux

```bash
sudo pacman -S github-cli
```

### Alpine Linux

```bash
apk add github-cli
```

### Homebrew (Linux)

```bash
brew install gh
```

---

## Verify Installation

```bash
gh --version
```

## Authentication Setup

Authenticate with your GitHub account after installation:

```bash
gh auth login
```

Check authentication status:

```bash
gh auth status
```

---

## References

- [Official Manual](https://cli.github.com/manual/)
- [Releases Page (Binary Downloads)](https://github.com/cli/cli/releases/latest)
