# Snoonaut Bot 🚀

Snoonaut Bot is a powerful Python-based tool designed to automate interactions with the Snoonaut platform. From daily check-ins to Solana wallet submissions, it streamlines your workflow with proxy support, multi-threading, and a vibrant bilingual CLI (English/Vietnamese). Perfect for maximizing rewards with minimal effort!

🔗 Snoonaut Bot: [Snoonaut Bot](https://earn.snoonaut.xyz/?ref=SNOOTGHSLFG)

## ✨ Features Overview

### General Features

- **Multi-Account Support**: Processes multiple accounts using tokens from `tokens.txt`.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text and borders.
- **Proxy Support**: Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies via `proxies.txt`.
- **Asynchronous Execution**: Built with `asyncio` for efficient blockchain interactions.
- **Error Handling**: Comprehensive error catching for blockchain transactions and RPC issues.
- **Bilingual Support**: Supports both English and Vietnamese output based on user selection.

### Included Scripts

1. **Daily Check-in**: Automates daily check-ins for Snoonaut rewards.
2. **Auto Tasks**: Completes social media tasks [ Twitter, Discord, Telegram, etc. ] with generated proof URLs.
3. **Auto Referral Tasks 🔒**: Automates referral invites [ 2, 5, 10 users, etc. ].
4. **Solana Wallet Submission**: Submits validated Solana addresses from `address.txt` using solders.

## 🛠️ Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- **Dependencies**: Install via `pip install -r requirements.txt` (ensure `web3.py`, `colorama`, `asyncio`, `eth-account`, `aiohttp_socks` and `inquirer` are included).
- **tokens.txt**: Add private keys (one per line) for wallet automation.
- **address.txt**: (optional): Solana wallet addresses.
- **proxies.txt** (optional): Add proxy addresses for network requests, if needed.

## 📦 Installation

1. **Clone this repository:**
- Open cmd or Shell, then run the command:
```sh
git clone https://github.com/thog9/Snoonaut-bot.git
```
```sh
cd Snoonaut-bot
```
2. **Install Dependencies:**
- Open cmd or Shell, then run the command:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Open the `tokens.txt`: Add your Session-token|Csrf-token (one per line) in the root directory.
```sh
nano tokens.txt 
```
- Create `address.txt`, `proxies.txt` for specific operations:
```sh
nano address.txt
nano proxies.txt
```
4. **Run:**
- Open cmd or Shell, then run command:
```sh
python main.py
```
- Choose a language (Vietnamese/English).

## 📬 Contact
Connect with us for support or updates:

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 

----

## ☕ Support Us
Love these scripts? Fuel our work with a coffee!

🔗 BUYMECAFE: [BUY ME CAFE](https://buymecafe.vercel.app/)

