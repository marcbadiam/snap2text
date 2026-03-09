# Snap2Text

Screenshot OCR tool using Google Gemini AI - extracts text from screenshots directly to clipboard.

## Description

Snap2Text is a lightweight command-line tool that allows you to capture any area of your screen and instantly extract text from it using Google's Gemini AI. The extracted text is automatically copied to your clipboard, ready to be pasted wherever you need it.

## Features

- **Select screen area and get text in clipboard** - Draw a selection rectangle around any text on your screen
- **Auto-detects available system tools** - Works out of the box with whatever tools you have installed
- **Works with multiple screenshot tools** - Supports maim, scrot, and gnome-screenshot
- **Multiple clipboard tools supported** - Compatible with xclip, xsel, and wl-paste
- **Supports notification tools** - Optional notifications via notify-send or kdialog

## Model Information

This package uses **`gemini-2.5-flash-lite`** as the hardcoded model. This model was chosen for its optimal balance of speed, cost-efficiency, and OCR accuracy for screenshot text extraction tasks.

### Changing the Model (Advanced Users)

To use a different Gemini model, edit the source code:

```bash
# Locate the package installation
python -c "import snap2text; print(snap2text.__file__)"

# Edit the __main__.py file and change the MODEL variable
# Default: MODEL = "gemini-2.5-flash-lite"
# Alternatives: "gemini-2.5-flash", "gemini-2.0-flash-lite", etc.
```

Available models can be found at: https://ai.google.dev/gemini-api/docs/models/gemini

## Requirements

- Python 3.8+
- At least one screenshot tool: maim, scrot, or gnome-screenshot
- At least one clipboard tool: xclip, xsel, or wl-paste
- Optional: notify-send or kdialog for notifications

## API Key Setup

This package is designed to work with **Google AI Studio** API keys.

### Free Tier Limits

- **250 requests per day**
- **10 requests per minute**
- Results are more than adequate for screenshot OCR tasks

### Getting Your API Key

1. Visit [Google AI Studio API Keys](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

## Installation

```bash
pip install snap2text
```

## Configuration

Set your Google AI Studio API key using one of the following methods:

### Method 1: Environment Variable

```bash
export MY_GEMINI_API_KEY="your-api-key-here"
```

Add this line to your `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration file to make it persistent.

### Method 2: Secrets File

Create `~/.secrets/MY_GEMINI_API_KEY` containing only your API key:

```bash
mkdir -p ~/.secrets
echo "your-api-key-here" > ~/.secrets/MY_GEMINI_API_KEY
chmod 600 ~/.secrets/MY_GEMINI_API_KEY
```

## Usage

### Command Line

Run the command directly:

```bash
snap2text
```

Then select the area of your screen containing the text you want to extract. The text will be automatically copied to your clipboard.

### Keyboard Shortcut (Recommended)

The recommended way to use Snap2Text is by binding it to a keyboard shortcut:

- **Recommended shortcut**: `Ctrl+PrintScreen` (most logical for screenshot tools)
- **Alternative**: `Super+Shift+S` or any combination you prefer

#### Setting up a keyboard shortcut:

**Linux Mint / Cinnamon:**
1. Open System Settings → Keyboard → Shortcuts → Custom Shortcuts
2. Click "Add custom shortcut"
3. Name: "Snap2Text"
4. Command: `snap2text`
5. Assign your preferred key combination

**Ubuntu / GNOME:**
1. Open Settings → Keyboard → Custom Shortcuts
2. Click "+" to add new shortcut
3. Name: "Snap2Text"
4. Command: `snap2text`
5. Set your preferred keybinding

**KDE Plasma:**
1. Open System Settings → Shortcuts → Custom Shortcuts
2. Edit → New → Global Shortcut → Command/URL
3. Name: "Snap2Text"
4. Command: `snap2text`
5. Assign your preferred trigger

## System Dependencies

Install the required screenshot and clipboard tools for your distribution:

### Ubuntu / Debian

```bash
sudo apt install maim xclip
```

### Arch Linux

```bash
sudo pacman -S maim xclip
```

### Fedora

```bash
sudo dnf install maim xclip
```

## Optional Dependencies

For desktop notifications when text is copied:

```bash
# Ubuntu / Debian
sudo apt install libnotify-bin

# Arch Linux
sudo pacman -S libnotify

# Fedora
sudo dnf install libnotify
```

For KDE users who prefer kdialog:

```bash
# Ubuntu / Debian
sudo apt install kdialog

# Arch Linux
sudo pacman -S kdialog

# Fedora
sudo dnf install kdialog
```

## Alternative Screenshot Tools

If you prefer other screenshot tools, Snap2Text will automatically detect and use them:

```bash
# Using scrot (Ubuntu/Debian)
sudo apt install scrot

# Using gnome-screenshot (Ubuntu/Debian)
sudo apt install gnome-screenshot
```

## Alternative Clipboard Tools

Similarly, you can use alternative clipboard tools:

```bash
# Using xsel instead of xclip (Ubuntu/Debian)
sudo apt install xsel

# For Wayland users (Ubuntu/Debian)
sudo apt install wl-clipboard
```

## Legal Disclaimer

**This software is provided "AS IS" without warranty of any kind, express or implied.**

By using Snap2Text, you acknowledge and agree to the following:

- **API Usage**: You are solely responsible for your Google AI Studio API usage, including but not limited to:
  - Staying within free tier limits
  - Monitoring your API consumption
  - Any charges incurred from exceeding free tier limits or using paid plans
  - Compliance with Google's Terms of Service and API usage policies

- **No Liability**: The authors and contributors of this package assume no responsibility for:
  - API misuse or abuse
  - Costs or charges from Google AI Studio
  - Data privacy or security issues related to API usage
  - Any damages arising from the use of this software

- **User Responsibility**: It is your responsibility to:
  - Understand Google's AI Studio pricing and limits
  - Monitor your API usage
  - Secure your API key appropriately
  - Use the tool in compliance with all applicable laws and regulations

For the most current information about API limits and pricing, visit: https://ai.google.dev/pricing

## General Disclaimer

**The authors and contributors of this project are not responsible for any damage, data loss, or any other issues that may arise from the use of this software.** Use it at your own risk. This software is provided under the MIT License without any warranty of any kind, express or implied. See the [LICENSE](LICENSE) file for full details.

## ⚠️ Beta Version Notice

**This is a beta release (v0.2.0b1).** This version may contain incomplete implementations and significant undocumented bugs. It is strongly recommended to **avoid using this software in a real production or development environment**. Features may change, break, or be removed without prior notice in future releases.
