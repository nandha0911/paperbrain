"""
share.py
========
One-command WFH sharing script.
Starts the FastAPI backend, Streamlit frontend, and opens 2 ngrok tunnels.
Then prints the shareable public URLs.

Usage:
    venv\Scripts\python share.py

Requirements:
    - Ollama running: ollama serve
    - ngrok auth token set: ngrok config add-authtoken <YOUR_TOKEN>
"""

import subprocess
import sys
import time
import threading
import os
import json
import re

import requests


# ─── Config ───────────────────────────────────────────────────────────────────
API_PORT      = 8000
STREAMLIT_PORT = 8501
NGROK_API_PORT = 4040   # ngrok local dashboard port

# Colors for terminal output
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def banner():
    print(f"""
{BOLD}{CYAN}
╔══════════════════════════════════════════════════════╗
║         PDF RAG Chatbot — WFH Share Mode             ║
║         Powered by Ollama + ChromaDB + ngrok         ║
╚══════════════════════════════════════════════════════╝
{RESET}""")


def check_ollama():
    """Check if Ollama is running."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        if r.status_code == 200:
            print(f"  {GREEN}✓{RESET} Ollama is running")
            return True
    except Exception:
        pass
    print(f"  {RED}✗{RESET} Ollama not running!")
    print(f"    → Open a new terminal and run: {YELLOW}ollama serve{RESET}")
    return False


def start_process(cmd, name, cwd=None):
    """Start a subprocess and return it."""
    proc = subprocess.Popen(
        cmd,
        cwd=cwd or os.getcwd(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
    )
    print(f"  {GREEN}✓{RESET} {name} started (pid={proc.pid})")
    return proc


def wait_for_port(port, name, timeout=30):
    """Wait until a local port is accepting connections."""
    import socket
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                print(f"  {GREEN}✓{RESET} {name} ready on port {port}")
                return True
        except OSError:
            time.sleep(1)
    print(f"  {RED}✗{RESET} {name} not ready after {timeout}s")
    return False


def get_ngrok_urls():
    """Fetch tunnel URLs from the ngrok local API."""
    try:
        r = requests.get(f"http://127.0.0.1:{NGROK_API_PORT}/api/tunnels", timeout=5)
        tunnels = r.json().get("tunnels", [])
        urls = {}
        for t in tunnels:
            port = t["config"]["addr"].split(":")[-1]
            url  = t["public_url"]
            if url.startswith("https://"):
                urls[port] = url
        return urls
    except Exception as e:
        return {}


def update_api_url_in_env(ngrok_api_url):
    """Write the ngrok API URL into the .env file so Streamlit uses it."""
    env_path = ".env"
    with open(env_path, "r") as f:
        content = f.read()

    # Replace or add API_BASE_URL
    if "API_BASE_URL=" in content:
        content = re.sub(r"API_BASE_URL=.*", f"API_BASE_URL={ngrok_api_url}", content)
    else:
        content += f"\nAPI_BASE_URL={ngrok_api_url}\n"

    with open(env_path, "w") as f:
        f.write(content)
    print(f"  {GREEN}✓{RESET} .env updated with ngrok API URL")


def main():
    banner()

    print(f"{BOLD}[1/5] Checking prerequisites…{RESET}")
    if not check_ollama():
        print(f"\n{RED}Please start Ollama first, then re-run this script.{RESET}")
        sys.exit(1)

    print(f"\n{BOLD}[2/5] Starting FastAPI backend on port {API_PORT}…{RESET}")
    api_proc = start_process(
        f"venv\\Scripts\\uvicorn api:app --host 0.0.0.0 --port {API_PORT}",
        "FastAPI backend",
    )
    wait_for_port(API_PORT, "FastAPI")

    print(f"\n{BOLD}[3/5] Starting Streamlit frontend on port {STREAMLIT_PORT}…{RESET}")
    ui_proc = start_process(
        f"venv\\Scripts\\streamlit run app.py --server.address 0.0.0.0 --server.port {STREAMLIT_PORT} --server.headless true",
        "Streamlit UI",
    )
    wait_for_port(STREAMLIT_PORT, "Streamlit")

    print(f"\n{BOLD}[4/5] Opening ngrok tunnels…{RESET}")
    print(f"  {YELLOW}Note: Free ngrok allows 1 tunnel. Sign up free at ngrok.com for 2 tunnels.{RESET}")

    # Start ngrok for API
    ngrok_api_proc = start_process(
        f"ngrok http {API_PORT} --log=stdout",
        "ngrok API tunnel",
    )
    time.sleep(3)

    # Get the API tunnel URL
    urls = get_ngrok_urls()
    api_url = urls.get(str(API_PORT), "")

    if api_url:
        update_api_url_in_env(api_url)
        print(f"  {GREEN}✓{RESET} ngrok API tunnel: {CYAN}{api_url}{RESET}")
    else:
        print(f"  {YELLOW}⚠{RESET}  Could not get ngrok URL. Check your auth token.")
        print(f"    → Get free token: https://dashboard.ngrok.com/get-started/your-authtoken")
        print(f"    → Then run: ngrok config add-authtoken <YOUR_TOKEN>")

    # Start ngrok for Streamlit
    ngrok_ui_proc = start_process(
        f"ngrok http {STREAMLIT_PORT} --log=stdout",
        "ngrok UI tunnel",
    )
    time.sleep(3)
    urls = get_ngrok_urls()
    ui_url = urls.get(str(STREAMLIT_PORT), f"http://localhost:{STREAMLIT_PORT}")

    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}{GREEN}[5/5] ✅ All systems running! Share this with your coworker:{RESET}")
    print(f"{BOLD}{'═'*60}{RESET}\n")
    print(f"  🌐 {BOLD}Chatbot URL:  {CYAN}{ui_url}{RESET}")
    print(f"  🔧 {BOLD}API URL:      {CYAN}{api_url or f'http://localhost:{API_PORT}'}{RESET}")
    print(f"  📖 {BOLD}API Docs:     {CYAN}{api_url or f'http://localhost:{API_PORT}'}/docs{RESET}")
    print(f"\n{YELLOW}  Your coworker just opens the Chatbot URL — no install needed!{RESET}")
    print(f"\n{BOLD}{'═'*60}{RESET}")
    print(f"\n  Press {BOLD}Ctrl+C{RESET} to stop all servers.\n")

    # Keep running until interrupted
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Shutting down all servers…{RESET}")
        for proc in [api_proc, ui_proc, ngrok_api_proc, ngrok_ui_proc]:
            try:
                proc.terminate()
            except Exception:
                pass
        print(f"{GREEN}All stopped. Goodbye!{RESET}\n")


if __name__ == "__main__":
    main()
