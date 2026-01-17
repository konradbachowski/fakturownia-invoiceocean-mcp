<div align="center">

# 🧾 Fakturownia / InvoiceOcean MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/framework-FastMCP-green.svg)](https://github.com/jlowin/fastmcp)

**Manage your Fakturownia / InvoiceOcean (BitFactura, VosFactures) account directly from your AI agent.**  
Issue invoices, check payments, and list clients using simple natural language commands. Works with all global versions of the platform.

[Report Bug](https://github.com/konradbachowski/fakturownia-invoiceocean-mcp/issues) • [HeyNeuron Website](https://heyneuron.com)

</div>

---

## 🌍 Supported Platforms
This MCP server works with all white-label versions of the platform:
- **Fakturownia.pl** (Poland)
- **InvoiceOcean.com** (Global / USA)
- **BitFactura.es** (Spain)
- **VosFactures.fr** (France)
- **InvoiceOcean.de** (Germany)

---

## 🛠️ Step 0: Where to find your API credentials?

Before you start, you need two things from your account:

1.  **Domain (Subdomain)**: This is the first part of your URL. If you log in at `https://mycompany.fakturownia.pl` or `https://mycompany.invoiceocean.com`, your domain is `mycompany`.
2.  **API Token**:
    *   Log in to your account.
    *   Go to **Settings** -> **Account Settings**.
    *   Select **Integration / API** from the left menu.
    *   Copy your **Authorization Code (API Token)**.

---

## 🚀 Installation (Step-by-Step)

### 1. Download the Code
Open your terminal and paste:
```bash
git clone https://github.com/konradbachowski/fakturownia-invoiceocean-mcp.git
cd fakturownia-invoiceocean-mcp
```

### 2. Prepare the Environment
Paste these commands one by one:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration
You need to tell the program your keys. Create a copy of the settings file:
```bash
cp .env.example .env
```
Open the `.env` file in any text editor and enter your data:
```env
FAKTUROWNIA_API_TOKEN=your_token_here
FAKTUROWNIA_DOMAIN=your_subdomain_here
```

---

## 🤖 Integration with OpenCode / Claude Desktop

To make your AI agent see Fakturownia, you need to add it to your configuration.

### Where is the config file?
*   **OpenCode**: `/Users/YOUR_USER/.config/opencode/opencode.json`
*   **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### What to paste there?
Add this section inside `"mcpServers"` or `"mcp"`:

```json
"fakturownia": {
  "type": "local",
  "command": [
    "/Users/mac/kodziki/mcp/fakturownia-mcp/venv/bin/python3",
    "/Users/mac/kodziki/mcp/fakturownia-mcp/main.py"
  ],
  "enabled": true
}
```
*(Make sure to provide the full paths to the folder where you installed the server!)*

---

## 🌟 What can you do? (Example Commands)

Once the application is restarted, you can chat with your AI:
*   *"Show me the list of invoices from this month."*
*   *"Issue a VAT invoice for client Pixelbee for 100 PLN for consulting."*
*   *"Register a payment of 500 PLN from client with ID 123."*
*   *"How many clients are in our database?"*

---

## 🛠️ Need a Custom AI Solution?

This project is part of our mission to support the Open Source community. If your company needs:
- **Custom MCP Servers** for internal systems.
- **AI Agents** integrated with your business processes.
- **Full end-to-end AI implementation**.

**Visit [HeyNeuron.com](https://heyneuron.com)** — we build and deploy professional AI solutions that save real time.

## 📄 License

Distributed under the **MIT** License. You are free to modify and use it for commercial purposes.

---
<p align="center">Built with passion by the community & <b>HeyNeuron</b></p>
