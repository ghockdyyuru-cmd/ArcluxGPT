# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import requests
import subprocess
import getpass
from typing import Generator

# --- Dependency Management ---
def check_dependencies():
    required_packages = [
        ("colorama", "colorama"),
        ("pwinput", "pwinput"),
        ("dotenv", "python-dotenv"),
        ("rich", "rich")
    ]
    missing_pip_names = []
    for import_name, pip_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_pip_names.append(pip_name)

    if missing_pip_names:
        print(f"[\033[93m!\033[0m] Missing components: {', '.join(missing_pip_names)}")
        print("[\033[96m*\033[0m] Equipping environment automatically...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_pip_names])
            print("[\033[92m+\033[0m] Upgrades complete. Launching engine...")
            time.sleep(1)
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            print(f"[\033[91m-\033[0m] Optimization failed: {e}")
            sys.exit(1)

check_dependencies()

# --- Imports ---
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.spinner import Spinner
from rich.align import Align
from textwrap import dedent
import colorama
from pwinput import pwinput
from dotenv import load_dotenv, set_key

colorama.init(autoreset=True)

# --- Configuration ---
class Config:
    """ArcluxGPT Engine Configuration"""
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL_POOL = ["llama-3.3-70b-versatile"]
    ENV_FILE = ".Arclux"
    API_KEY_NAME = "ARCLUX-CORE-KEY"
    CODE_THEME = "monokai"
    
    # 🔐 Kunci Keamanan Akses Enkripsi Lokal
    SECURITY_KEY = "arclux2026" 

    class Colors:
        PROMPT = "magenta"
        ACCENT = "purple"

# --- Advanced UI ---
class UI:
    def __init__(self):
        self.console = Console()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def banner(self):
        self.clear()
        ascii_art = dedent("""
        [bold magenta] █████╗ ██████╗  ██████╗██╗     ██╗   ██╗██╗  ██╗[/]
        [bold magenta]██╔══██╗██╔══██╗██╔════╝██║     ██║   ██║╚██╗██╔╝[/]
        [bold magenta]███████║██████╔╝██║     ██║     ██║   ██║ ╚███╔╝ [/]
        [bold magenta]██╔══██║██╔══██╗██║     ██║     ██║   ██║ ██╔██╗ [/]
        [bold magenta]██║  ██║██║  ██║╚██████╗███████╗╚██████╔╝██╔╝ ██╗[/]
        [bold_purple]╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝[/]
        """).rstrip()

        tagline = Text("ARCLUX CORE INTEGRATION v2.0 | COGNITIVE AGENT ARCHITECTURE", style="bold magenta")
        subline = Text("Operational Status: Secure, Autonomous & Independent", style="dim white")

        self.console.print(Align.center(ascii_art))
        self.console.print(Align.center(tagline))
        self.console.print(Align.center(subline))
        self.console.print(Panel("", border_style="magenta", height=1))

    def main_menu(self):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Index", style="bold magenta", justify="right")
        table.add_column("Action", style="bold white")

        table.add_row("[1]", "Establish Agent Uplink (Interactive Shell Control)")
        table.add_row("[2]", "Inject Core API Credentials")
        table.add_row("[3]", "System Blueprint (About)")
        table.add_row("[4]", "Terminate Core Session (Exit)")

        self.console.print(Panel(
            Align.center(table),
            title="[bold magenta]AGENT MAIN INTERFACE[/bold magenta]",
            border_style="purple",
            padding=(1, 5)
        ))

    def show_msg(self, title: str, content: str, color: str = "white"):
        self.console.print(Panel(content, title=f"[bold]{title}[/]", border_style=color))

    def get_input(self, label: str = "ARCLUX") -> str:
        p_style = Config.Colors.PROMPT
        self.console.print(f"[{p_style}]┌──({label})-[~][/]")
        return self.console.input(f"[{p_style}]└─> [/]")

# --- Intelligent Engine ---
class ArcluxBrain:
    SYSTEM_PROMPT = """
You are ARCLUXGPT, an autonomous security research assistant and system optimization core.
Your role is to guide the user in system analysis, code optimization, and defensive security frameworks.
Keep your technical guidance accurate, precise, and highly modular.
"""

    def __init__(self, api_key: str, ui: UI):
        self.ui = ui
        self.api_key = api_key
        self.history = [{"role": "system", "content": self.SYSTEM_PROMPT}]

    def reset(self):
        self.history = [{"role": "system", "content": self.SYSTEM_PROMPT}]

    def chat(self, user_input: str) -> Generator[str, None, None]:
        self.history.append({"role": "user", "content": user_input})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        success = False
        debug_msg = ""

        for model in Config.MODEL_POOL:
            payload = {
                "model": model,
                "messages": self.history,
                "temperature": 0.5,
                "stream": True
            }
            try:
                response = requests.post(Config.BASE_URL, headers=headers, json=payload, timeout=15, stream=True)
                if response.status_code == 200:
                    success = True
                    full_content = ""
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8').replace('data: ', '')
                            if decoded_line.strip() == '[DONE]':
                                break
                            try:
                                json_data = json.loads(decoded_line)
                                if "choices" in json_data and len(json_data["choices"]) > 0:
                                    delta = json_data["choices"][0].get("delta", {})
                                    chunk = delta.get("content", "")
                                    if chunk:
                                        full_content += chunk
                                        yield chunk
                            except:
                                continue
                    self.history.append({"role": "assistant", "content": full_content})
                    break
                else:
                    debug_msg += f"[{model}: HTTP {response.status_code}] "
            except Exception as e:
                debug_msg += f"[{model}: {str(e)}] "

        if not success:
            yield f"Uplink Failure. Log Eror: {debug_msg}"

# --- Infrastructure & System Controller Orchestrator ---
class App:
    def __init__(self):
        self.ui = UI()
        self.brain = None

    def execute_system_command(self, cmd: str) -> str:
        """Fungsi Agen untuk mengontrol sub-proses terminal Linux asli"""
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if res.stdout:
                return res.stdout
            return res.stderr if res.stderr else "Command executed with no output."
        except Exception as e:
            return f"Agent Execution Error: {str(e)}"

    def authenticate_user(self) -> bool:
        """Gatekeeper Login sebelum masuk ke sistem utama"""
        self.ui.clear()
        self.ui.console.print("\n[bold red][!] ARCLUX AGENT SECURITY GATEKEEPER [!][/bold red]")
        try:
            # Menggunakan pwinput agar ketikan password tersembunyi dengan karakter '*'
            access_key = pwinput(prompt=f"{colorama.Fore.MAGENTA}[Gate Access] Enter Passkey for ghockdyyuru-cmd: {colorama.Style.RESET_ALL}", mask="*")
        except:
            access_key = input("[Gate Access] Enter Passkey: ")

        if access_key == Config.SECURITY_KEY:
            self.ui.console.print("[bold green][+] Access Verified. Synchronizing cognitive core subsystems...[/bold green]")
            time.sleep(1.2)
            return True
        else:
            self.ui.console.print("[bold red][-] AUTHENTICATION FAILED. Access Denied. Intrusion event dropped.[/bold red]")
            time.sleep(1.5)
            sys.exit(1)

    def setup(self) -> bool:
        load_dotenv(dotenv_path=Config.ENV_FILE)
        key = os.getenv(Config.API_KEY_NAME)

        if not key:
            self.ui.banner()
            self.ui.show_msg("Warning", "Core API Encryption Key not found inside environment.", "yellow")
            if self.ui.get_input("Inject key now? (y/n)").lower().startswith('y'):
                return self.configure_key()
            return False

        with self.ui.console.status("[bold magenta]Configuring Secure Agent Subsystems...[/]"):
            self.brain = ArcluxBrain(key, self.ui)
            time.sleep(0.8)
        return True

    def configure_key(self) -> bool:
        self.ui.banner()
        self.ui.console.print("[bold magenta]Input your Groq API Key (gsk_...):[/]")
        try:
            key = pwinput(prompt=f"{colorama.Fore.MAGENTA}Key > {colorama.Style.RESET_ALL}", mask="*")
        except:
            key = input("Key > ")

        if not key.strip():
            return False

        set_key(Config.ENV_FILE, Config.API_KEY_NAME, key.strip())
        self.ui.show_msg("Success", "Key secured in local dataring (.Arclux).", "green")
        time.sleep(1)
        return self.setup()

    def run_chat(self):
        if not self.brain: return
        self.ui.banner()
        self.ui.show_msg("Connected", "Agent Active. Controls: /new (flush), /exit (leave menu).\nType 'cek storage', 'cek jaringan', or 'cek proses' for direct Linux control.", "green")

        while True:
            try:
                prompt = self.ui.get_input("Arclux-Agent")
                if not prompt.strip(): continue

                if prompt.lower() == '/exit': return
                if prompt.lower() == '/new':
                    self.brain.reset()
                    self.ui.clear()
                    self.ui.banner()
                    self.ui.show_msg("Reset", "Local memory buffers flushed.", "magenta")
                    continue

                # 🤖 SYSTEM AGENT ROUTING MATRIX (Kontrol Linux Asli Lewat AI Prompt)
                lowered_prompt = prompt.lower()
                if any(x in lowered_prompt for x in ["cek storage", "info disk", "storage hp"]):
                    with self.ui.console.status("[bold cyan]Agent executing Linux command 'df -h'...[/]"):
                        # Target folder home dari Termux environment
                        output = self.execute_system_command("df -h /data/data/com.termux/files/home")
                    self.ui.show_msg("Agent Action: Linux Storage Status", f"```text\n{output}\n```", "cyan")
                    continue

                elif any(x in lowered_prompt for x in ["cek jaringan", "ip ku", "info ip", "audit network"]):
                    with self.ui.console.status("[bold cyan]Agent executing Linux network routine...[/]"):
                        output = self.execute_system_command("ip r 2>/dev/null || ifconfig")
                    self.ui.show_msg("Agent Action: Network Matrix Audit", f"```text\n{output}\n```", "cyan")
                    continue

                elif any(x in lowered_prompt for x in ["cek proses", "liat ram", "proses linux"]):
                    with self.ui.console.status("[bold cyan]Agent executing Linux process monitoring...[/]"):
                        output = self.execute_system_command("ps")
                    self.ui.show_msg("Agent Action: Active Linux Processes", f"```text\n{output}\n```", "cyan")
                    continue

                # Jalur komunikasi kognitif LLM Normal
                generator = self.brain.chat(prompt)
                self.ui.stream_markdown("ArcluxGPT Engine", generator)

            except KeyboardInterrupt:
                self.ui.console.print("\n[bold yellow][!] Link interrupted. Returning to main cockpit...[/]")
                break

    def blueprint(self):
        self.ui.banner()
        text = """
[bold magenta]ArcluxGPT v2.0[/] is an AI Cognitive Agent capable of real-world Linux environment sub-process manipulation and auditing.

[bold magenta]Engine Advancements:[/bold magenta]
• [bold green]Gatekeeper Core:[/] Secure local password encryption routing.
• [bold green]System Controller Layer:[/] Direct execution mapping via Python `subprocess`.
• [bold green]Cognitive Routing Matrix:[/] Automatically shifts between LLM generation and defensive terminal scripts.
• [bold green]Infrastructure Cleanliness:[/] Full protection of your local repository configuration.
        """
        self.ui.console.print(Panel(text, title="[bold]System Blueprint v2.0[/]", border_style="purple"))
        self.ui.get_input("Press Enter to Return")

    def start(self):
        # Eksekusi Login Terlebih Dahulu Demi Keamanan Eksklusif Kamu
        if not self.authenticate_user():
            return
            
        if not self.setup():
            self.ui.console.print("[bold red]Core Halt: Missing authorization credentials.[/]")
            return

        while True:
            self.ui.banner()
            self.ui.main_menu()
            choice = self.ui.get_input("CORE")

            if choice == '1':
                self.run_chat()
            elif choice == '2':
                self.configure_key()
            elif choice == '3':
                self.blueprint()
            elif choice == '4':
                self.ui.console.print("[bold red]Closing secure nodes... Arclux Agent Offline.[/]")
                time.sleep(0.5)
                self.ui.clear()
                sys.exit(0)
            else:
                self.ui.console.print("[red]Unknown Action Command[/]")
                time.sleep(0.5)

if __name__ == "__main__":
    try:
        app = App()
        app.start()
    except KeyboardInterrupt:
        print("\n\033[31mCore Interface Interrupted. System Shutdown.\033[0m")
        sys.exit(0)

