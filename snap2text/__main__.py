#!/usr/bin/env python3
"""
Snap2Text - OCR tool using Gemini AI for text extraction from screenshots.

This module provides functionality to capture screen areas and extract text
using Google's Gemini AI API. Supports various screenshot, clipboard, and
notification tools.
"""

import sys
import os
import base64
import json
import urllib.request
import urllib.error
import subprocess
import shutil

# ==========================================
# Configuration
# ==========================================
# 1. Try to get from environment variable
API_KEY = os.getenv('MY_GEMINI_API_KEY')

# 2. Fallback: Read from secrets file if not in environment
if not API_KEY:
    SECRET_PATH = os.path.expanduser("~/.secrets/MY_GEMINI_API_KEY")
    if os.path.exists(SECRET_PATH):
        with open(SECRET_PATH, 'r') as f:
            API_KEY = f.read().strip()

# Use an available Gemini model variant
MODEL = "gemini-2.5-flash-lite"
TEMP_IMG = "/tmp/snap_capture.png"
# ==========================================

# Tool priority lists (in order of preference)
SCREENSHOT_TOOLS = ["maim", "scrot", "gnome-screenshot"]
CLIPBOARD_TOOLS = ["xclip", "xsel", "wl-paste"]
NOTIFICATION_TOOLS = ["notify-send", "kdialog"]

# Detected tools (populated at runtime)
detected_screenshot_tool = None
detected_clipboard_tool = None
detected_notification_tool = None


def detect_tools():
    """Detect available system tools using shutil.which()."""
    global detected_screenshot_tool, detected_clipboard_tool, detected_notification_tool

    # Detect screenshot tool
    for tool in SCREENSHOT_TOOLS:
        if shutil.which(tool):
            detected_screenshot_tool = tool
            break

    # Detect clipboard tool
    for tool in CLIPBOARD_TOOLS:
        if shutil.which(tool):
            detected_clipboard_tool = tool
            break

    # Detect notification tool
    for tool in NOTIFICATION_TOOLS:
        if shutil.which(tool):
            detected_notification_tool = tool
            break


def notify(title, message):
    """Send a desktop notification using the detected notification tool."""
    if detected_notification_tool == "notify-send":
        subprocess.run(["notify-send", title, message, "-i", "camera-photo"])
    elif detected_notification_tool == "kdialog":
        subprocess.run(["kdialog", "--passivepopup", f"{title}: {message}", "5"])
    else:
        # Fallback: print to stderr
        print(f"{title}: {message}", file=sys.stderr)


def copy_to_clipboard(text):
    """Copy text to clipboard using the detected clipboard tool."""
    if detected_clipboard_tool == "xclip":
        # Copy to clipboard (Ctrl+V)
        process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        # Also to primary selection (middle click)
        process = subprocess.Popen(['xclip', '-selection', 'primary'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
    elif detected_clipboard_tool == "xsel":
        # Copy to clipboard (Ctrl+V)
        process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        # Also to primary selection (middle click)
        process = subprocess.Popen(['xsel', '--primary', '--input'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
    elif detected_clipboard_tool == "wl-paste":
        # Wayland clipboard
        process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))


def capture_screenshot(output_path):
    """Capture screenshot using the detected screenshot tool.
    
    Args:
        output_path: Path where the screenshot will be saved
        
    Returns:
        bool: True if successful, False if user cancelled
        
    Raises:
        subprocess.CalledProcessError: If screenshot capture fails
    """
    if detected_screenshot_tool == "maim":
        # -s: select area, -u: hide cursor
        subprocess.run(["maim", "-s", "-u", output_path], check=True)
    elif detected_screenshot_tool == "scrot":
        # -s: select area, -f: freeze screen
        subprocess.run(["scrot", "-s", output_path], check=True)
    elif detected_screenshot_tool == "gnome-screenshot":
        # -a: area selection, -f: output file
        subprocess.run(["gnome-screenshot", "-a", "-f", output_path], check=True)
    return True


def check_required_tools():
    """Check if required tools are available and show error if not.
    
    Returns:
        bool: True if all required tools are available, False otherwise
    """
    errors = []

    if not detected_screenshot_tool:
        errors.append(f"No screenshot tool found. Install one of: {', '.join(SCREENSHOT_TOOLS)}")

    if not detected_clipboard_tool:
        errors.append(f"No clipboard tool found. Install one of: {', '.join(CLIPBOARD_TOOLS)}")

    if errors:
        error_message = "Missing required tools:\n" + "\n".join(errors)
        if detected_notification_tool:
            notify("Snap2Text Error", error_message)
        print(error_message, file=sys.stderr)
        return False

    return True


def main():
    """Main entry point for the Snap2Text application."""
    # Detect available tools
    detect_tools()

    # Check for required tools
    if not check_required_tools():
        sys.exit(1)

    if not API_KEY:
        notify("Snap2Text Error", "API key not found in environment or ~/.secrets/MY_GEMINI_API_KEY")
        sys.exit(1)

    try:
        # 1. Capture screenshot area
        capture_screenshot(TEMP_IMG)
    except subprocess.CalledProcessError:
        sys.exit(0)  # User cancelled (Esc)

    notify("Snap2Text", "Processing image with Gemini...")

    try:
        # 2. Encode image to Base64
        with open(TEMP_IMG, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        # 3. Prepare API request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}

        prompt_text = (
            "Extract all text from this image. Rules:\n"
            "1. Maintain formatting (lists, indentation).\n"
            "2. If it is a table, use Markdown syntax.\n"
            "3. If it is code, return ONLY the code.\n"
            "4. Return ONLY the extracted text, no explanations."
        )

        data = {
            "contents": [{
                "parts": [
                    {"text": prompt_text},
                    {"inline_data": {
                        "mime_type": "image/png",
                        "data": img_data
                    }}
                ]
            }]
        }

        json_data = json.dumps(data).encode('utf-8')

        # 4. Execute API request
        req = urllib.request.Request(url, data=json_data, headers=headers, method='POST')

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))

        # 5. Extract text and copy to clipboard
        try:
            extracted_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
            copy_to_clipboard(extracted_text)

            preview = extracted_text[:40].replace('\n', ' ') + "..."
            notify("OCR Successful", f"Copied: {preview}")

        except (KeyError, IndexError):
            notify("OCR Error", "Model did not return any text.")

    except urllib.error.HTTPError as e:
        notify("API Error", f"Code {e.code}")
    except Exception as e:
        notify("Unexpected Error", str(e))
    finally:
        if os.path.exists(TEMP_IMG):
            os.remove(TEMP_IMG)


if __name__ == "__main__":
    main()
