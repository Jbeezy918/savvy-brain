#!/usr/bin/env python3
"""
Bob v2.1 - Smart Computer Control Agent
- Uses vision to SEE the screen
- Uses Playwright for smart web automation
- Can find buttons by text, fill forms, navigate sites
- Handles complex multi-step commands
"""

import os
import sys
import json
import time
import base64
import subprocess
import pyautogui
import requests
from pathlib import Path
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Ollama settings
OLLAMA_URL = "http://localhost:11434"
TEXT_MODEL = "deepseek-r1:7b"
VISION_MODEL = "llava:7b"

class SmartBobAgent:
    def __init__(self):
        self.verbose = True
        self.history = []

    def speak(self, text):
        """Use macOS TTS"""
        subprocess.run(['say', '-v', 'Samantha', '-r', '170', text], check=False)

    def take_screenshot(self, path="/tmp/bob_screen.png"):
        """Take screenshot and return path"""
        subprocess.run(['screencapture', '-x', path], check=False)
        return path

    def get_screenshot_base64(self):
        """Get screenshot as base64 for vision model"""
        path = self.take_screenshot()
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def ask_vision(self, prompt, image_base64=None):
        """Ask the vision model what it sees on screen"""
        if image_base64 is None:
            image_base64 = self.get_screenshot_base64()

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": VISION_MODEL,
                    "prompt": prompt,
                    "images": [image_base64],
                    "stream": False
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            return f"Vision error: {response.status_code}"
        except Exception as e:
            return f"Vision error: {e}"

    def ask_ollama(self, prompt, system_prompt=None):
        """Query text model for planning"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": TEXT_MODEL,
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json()["message"]["content"]
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"

    def web_goto(self, url):
        """Navigate to URL using Chrome via AppleScript"""
        if not url.startswith('http'):
            url = 'https://' + url

        # Use AppleScript to control Chrome (no threading issues)
        script = f'''
        tell application "Google Chrome"
            activate
            if (count of windows) = 0 then
                make new window
            end if
            set URL of active tab of front window to "{url}"
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', script], check=True, capture_output=True)
            time.sleep(2)  # Wait for page load
            return f"Opened {url} in Chrome"
        except Exception as e:
            # Fallback to default browser
            subprocess.run(['open', url], check=False)
            return f"Opened {url} in default browser"

    def web_click(self, text_or_selector):
        """Click element using vision + pyautogui"""
        return self.find_and_click_on_screen(text_or_selector)

    def web_fill(self, field_name, text):
        """Click on field and type text"""
        # First try to click the field
        click_result = self.find_and_click_on_screen(field_name)
        time.sleep(0.3)
        # Then type the text
        pyautogui.typewrite(text, interval=0.03)
        return f"Filled '{field_name}' with text"

    def web_type(self, text):
        """Type text using pyautogui"""
        # Handle special characters that typewrite can't do
        try:
            pyautogui.typewrite(text, interval=0.03)
        except:
            # Fallback: use clipboard
            subprocess.run(['pbcopy'], input=text.encode(), check=True)
            pyautogui.hotkey('command', 'v')
        return f"Typed: {text}"

    def web_press(self, key):
        """Press keyboard key"""
        key_lower = key.lower().strip()
        pyautogui.press(key_lower)
        return f"Pressed: {key}"

    def find_and_click_on_screen(self, description):
        """Use vision to find something on screen and click it"""
        screenshot_b64 = self.get_screenshot_base64()

        prompt = f"""Look at this screenshot. I need to click on: "{description}"

Find this element and tell me its approximate X,Y coordinates on the screen.
The screen is 1920x1080 (or similar). Give me coordinates in this format:
CLICK: x, y

If you can't find it, say: NOT_FOUND: reason"""

        response = self.ask_vision(prompt, screenshot_b64)
        print(f"Vision response: {response}")

        if "CLICK:" in response:
            try:
                coords = response.split("CLICK:")[1].strip().split(",")
                x = int(coords[0].strip())
                y = int(coords[1].strip().split()[0])  # Handle trailing text
                pyautogui.click(x, y)
                return f"Clicked at ({x}, {y}) - {description}"
            except Exception as e:
                return f"Could not parse coordinates: {e}"

        return f"Could not find: {description}"

    def execute_command(self, command):
        """Parse and execute a natural language command"""
        command_lower = command.lower().strip()

        # Direct actions
        if command_lower.startswith("go to ") or command_lower.startswith("open "):
            url = command.split(" ", 2)[-1].strip()
            return self.web_goto(url)

        if command_lower.startswith("click "):
            target = command.split(" ", 1)[-1].strip()
            result = self.web_click(target)
            if "Could not" in result:
                # Fallback to vision
                return self.find_and_click_on_screen(target)
            return result

        if command_lower.startswith("type "):
            text = command.split(" ", 1)[-1].strip().strip('"\'')
            return self.web_type(text)

        if command_lower.startswith("fill "):
            # "fill email with test@test.com"
            parts = command.split(" with ", 1)
            if len(parts) == 2:
                field = parts[0].replace("fill ", "").strip()
                value = parts[1].strip()
                return self.web_fill(field, value)

        if command_lower.startswith("press "):
            key = command.split(" ", 1)[-1].strip()
            return self.web_press(key)

        if "scroll down" in command_lower:
            pyautogui.scroll(-3)
            return "Scrolled down"

        if "scroll up" in command_lower:
            pyautogui.scroll(3)
            return "Scrolled up"

        if "screenshot" in command_lower:
            path = self.take_screenshot()
            return f"Screenshot saved to {path}"

        if "what do you see" in command_lower or "describe" in command_lower:
            return self.ask_vision("Describe what you see on this screen. What application is open? What buttons and options are visible?")

        # Complex command - use AI to break it down
        return self.handle_complex_command(command)

    def handle_complex_command(self, command):
        """Use AI to break down complex commands into steps"""
        system_prompt = """You are Bob, a computer control agent. Break down the user's request into simple steps.

Available actions:
- go to [url] - navigate to website
- click [text/button] - click on element
- type [text] - type text
- fill [field] with [value] - fill form field
- press [key] - press keyboard key (enter, tab, escape)
- scroll up/down
- screenshot

Output a numbered list of simple actions. Be specific.
Example:
User: "Log into my email"
1. go to gmail.com
2. click Sign in
3. wait for page load

User: "Search for cats on Google"
1. go to google.com
2. type cats
3. press enter"""

        response = self.ask_ollama(command, system_prompt)
        print(f"\nPlan:\n{response}\n")

        # Extract and execute steps
        results = []
        lines = response.strip().split('\n')
        for line in lines:
            # Skip non-action lines
            line = line.strip()
            if not line or not line[0].isdigit():
                continue

            # Extract action (remove number prefix)
            action = line.split('.', 1)[-1].strip() if '.' in line else line
            action = action.split(')', 1)[-1].strip() if ')' in action else action

            # Skip meta instructions
            if any(skip in action.lower() for skip in ['wait', 'verify', 'check', 'confirm', 'observe']):
                time.sleep(1)
                continue

            print(f"  Executing: {action}")
            result = self.execute_command(action)
            results.append(f"{action} -> {result}")
            time.sleep(0.5)

        return "\n".join(results) if results else response

    def process_command(self, command):
        """Main entry point for commands"""
        print(f"\n{'='*50}")
        print(f"Command: {command}")
        print('='*50)

        result = self.execute_command(command)
        print(f"\nResult: {result}")

        return result

    def cleanup(self):
        """Clean up resources"""
        pass  # No cleanup needed for AppleScript approach


# For the web server to use
def create_agent():
    return SmartBobAgent()


if __name__ == "__main__":
    agent = SmartBobAgent()

    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        agent.process_command(command)
    else:
        agent.speak("Bob version 2.1 ready. I can now see your screen and control websites.")
        print("\nBob v2.1 - Smart Agent")
        print("Commands: type naturally, or 'quit' to exit\n")

        while True:
            try:
                cmd = input("You: ").strip()
                if cmd.lower() == 'quit':
                    break
                if cmd:
                    response = agent.process_command(cmd)
                    if len(response) < 200:
                        agent.speak(response.split('\n')[0][:100])
            except KeyboardInterrupt:
                break

        agent.cleanup()
