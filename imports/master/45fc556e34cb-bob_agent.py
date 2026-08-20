#!/usr/bin/env python3
"""
Bob v2.0 - Computer Control Agent
Uses Ollama (free local AI) to control your Mac
- Sees your screen via screenshots
- Controls mouse and keyboard
- Fills forms, clicks buttons, navigates
- Voice commands via macOS speech recognition
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
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.5  # Pause between actions

# Ollama settings
OLLAMA_URL = "http://localhost:11434"
MODEL = "deepseek-r1:7b"  # Fast model for quick responses

class BobAgent:
    def __init__(self):
        self.history = []
        self.running = True
        self.verbose = True

    def speak(self, text):
        """Use macOS TTS to speak"""
        subprocess.run(['say', '-v', 'Samantha', '-r', '170', text], check=False)

    def take_screenshot(self):
        """Take screenshot and return path"""
        path = "/tmp/bob_screen.png"
        subprocess.run(['screencapture', '-x', path], check=False)
        return path

    def get_screen_description(self):
        """Take screenshot and get AI description of what's on screen"""
        screenshot_path = self.take_screenshot()
        # For now, just return that we took a screenshot
        # Full vision would require a vision model
        return f"Screenshot saved to {screenshot_path}"

    def ask_ollama(self, prompt, system_prompt=None):
        """Query Ollama for a response"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json()["message"]["content"]
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error connecting to Ollama: {e}"

    def parse_action(self, ai_response):
        """Parse AI response for actions to take"""
        response_lower = ai_response.lower()

        actions = []

        # Look for click commands
        if "click" in response_lower:
            if "(" in ai_response and ")" in ai_response:
                # Try to extract coordinates
                try:
                    start = ai_response.index("(")
                    end = ai_response.index(")")
                    coords = ai_response[start+1:end].split(",")
                    x, y = int(coords[0].strip()), int(coords[1].strip())
                    actions.append(("click", x, y))
                except:
                    pass

        # Look for type commands
        if "type:" in response_lower or "type \"" in response_lower:
            try:
                if "type:" in response_lower:
                    start = response_lower.index("type:") + 5
                    text = ai_response[start:].strip().split("\n")[0]
                elif 'type "' in response_lower:
                    start = response_lower.index('type "') + 6
                    end = ai_response[start:].index('"')
                    text = ai_response[start:start+end]
                actions.append(("type", text))
            except:
                pass

        # Look for key press commands
        if "press " in response_lower:
            keys = ["enter", "tab", "escape", "backspace", "delete", "up", "down", "left", "right"]
            for key in keys:
                if f"press {key}" in response_lower:
                    actions.append(("press", key))
                    break

        # Look for scroll commands
        if "scroll" in response_lower:
            if "up" in response_lower:
                actions.append(("scroll", "up"))
            elif "down" in response_lower:
                actions.append(("scroll", "down"))

        # Look for open URL commands
        if "open url" in response_lower or "go to" in response_lower:
            # Try to extract URL
            import re
            urls = re.findall(r'https?://[^\s]+', ai_response)
            if urls:
                actions.append(("open_url", urls[0]))

        return actions

    def execute_action(self, action):
        """Execute a parsed action"""
        action_type = action[0]

        try:
            if action_type == "click":
                x, y = action[1], action[2]
                print(f"  → Clicking at ({x}, {y})")
                pyautogui.click(x, y)
                return True

            elif action_type == "type":
                text = action[1]
                print(f"  → Typing: {text}")
                pyautogui.typewrite(text, interval=0.05)
                return True

            elif action_type == "press":
                key = action[1]
                print(f"  → Pressing: {key}")
                pyautogui.press(key)
                return True

            elif action_type == "scroll":
                direction = action[1]
                amount = 3 if direction == "down" else -3
                print(f"  → Scrolling {direction}")
                pyautogui.scroll(amount)
                return True

            elif action_type == "open_url":
                url = action[1]
                print(f"  → Opening URL: {url}")
                subprocess.run(['open', url], check=False)
                return True

        except Exception as e:
            print(f"  ✗ Action failed: {e}")
            return False

        return False

    def process_command(self, command):
        """Process a user command"""
        print(f"\n{'='*50}")
        print(f"Command: {command}")
        print('='*50)

        # Take screenshot to see current state
        self.take_screenshot()

        # Build prompt for AI
        system_prompt = """You are Bob, a computer control agent. You help users by controlling their computer.

When given a task, respond with specific actions to take. Use these formats:
- To click: "click (x, y)" with screen coordinates
- To type text: "type: the text to type"
- To press a key: "press enter" or "press tab" etc
- To scroll: "scroll up" or "scroll down"
- To open a URL: "open url https://example.com"

Be specific and direct. Execute one step at a time.
If you need more information, ask the user.
"""

        # Get AI response
        print("\nThinking...")
        response = self.ask_ollama(command, system_prompt)
        print(f"\nBob: {response}")

        # Parse and execute actions
        actions = self.parse_action(response)

        if actions:
            print(f"\nExecuting {len(actions)} action(s):")
            for action in actions:
                self.execute_action(action)
                time.sleep(0.5)

        return response

    def run_interactive(self):
        """Run in interactive mode"""
        self.speak("Bob version 2 is ready. I can control your computer. What do you need?")

        print("\n" + "="*50)
        print("BOB v2.0 - Computer Control Agent")
        print("="*50)
        print("Commands:")
        print("  - Type any task for Bob to do")
        print("  - 'screenshot' - Take and show screenshot")
        print("  - 'quit' - Exit")
        print("="*50 + "\n")

        while self.running:
            try:
                command = input("\nYou: ").strip()

                if not command:
                    continue

                if command.lower() == 'quit':
                    self.speak("Goodbye!")
                    break

                if command.lower() == 'screenshot':
                    path = self.take_screenshot()
                    print(f"Screenshot saved to {path}")
                    subprocess.run(['open', path], check=False)
                    continue

                # Process the command
                response = self.process_command(command)

                # Speak short responses
                if len(response) < 200:
                    self.speak(response.split('\n')[0][:100])

            except KeyboardInterrupt:
                print("\n\nInterrupted by user")
                break
            except Exception as e:
                print(f"Error: {e}")

    def run_voice_mode(self):
        """Run with voice input (uses macOS dictation)"""
        self.speak("Voice mode activated. I'm listening.")
        print("\n⚠️  Voice mode requires macOS Dictation to be enabled")
        print("Press Fn Fn (function key twice) to start dictation")
        print("Or use the regular text input below\n")
        self.run_interactive()


def main():
    # Check Ollama is running
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code != 200:
            print("⚠️  Ollama doesn't seem to be running. Start it with: ollama serve")
            sys.exit(1)
    except:
        print("⚠️  Cannot connect to Ollama. Start it with: ollama serve")
        print("   Then run: ollama pull deepseek-r1:7b")
        sys.exit(1)

    agent = BobAgent()

    if len(sys.argv) > 1:
        if sys.argv[1] == '--voice':
            agent.run_voice_mode()
        else:
            # Run single command
            command = ' '.join(sys.argv[1:])
            agent.process_command(command)
    else:
        agent.run_interactive()


if __name__ == "__main__":
    main()
