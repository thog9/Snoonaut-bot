import os
import sys
import asyncio
import random
from typing import List, Tuple
from colorama import init, Fore, Style
import aiohttp
from aiohttp_socks import ProxyConnector

# Initialize colorama
init(autoreset=True)

# Border width
BORDER_WIDTH = 80

# Constants
API_BASE_URL = "https://earn.snoonaut.xyz"
CALLBACK_URL = "https%3A%2F%2Fearn.snoonaut.xyz%2F%3Fref%3DSNOOTY9V62H"
IP_CHECK_URL = "https://api.ipify.org?format=json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://earn.snoonaut.xyz",
    "Referer": "https://earn.snoonaut.xyz/home",
    "Content-Type": "application/json",
    "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

# Configuration
CONFIG = {
    "DELAY_BETWEEN_ACCOUNTS": 5,
    "RETRY_ATTEMPTS": 3,
    "RETRY_DELAY": 3,
    "BYPASS_SSL": False,
    "THREADS": 2,
}

# Bilingual vocabulary
LANG = {
    'vi': {
        'title': 'TỰ ĐỘNG HOÀN THÀNH NHIỆM VỤ GIỚI THIỆU - SNOONAUT',
        'info': 'Thông tin',
        'found': 'Tìm thấy',
        'tokens': 'token',
        'processing_tokens': '⚙ ĐANG XỬ LÝ {count} TOKEN',
        'performing_task': 'Đang thực hiện nhiệm vụ: {task_title}',
        'success': '✅ Thành công: {message}',
        'failure': '❌ Thất bại: {error}',
        'username': 'Tên người dùng',
        'tasks_completed': 'Nhiệm vụ hoàn thành',
        'pausing': 'Tạm dừng',
        'seconds': 'giây',
        'completed': '🏁 HOÀN THÀNH: {successful}/{total} NHIỆM VỤ THÀNH CÔNG',
        'result_info': 'Kết quả nhiệm vụ',
        'error': 'Lỗi',
        'token_not_found': '❌ Không tìm thấy tệp tokens.txt',
        'token_empty': '❌ Không tìm thấy token hợp lệ',
        'token_error': '❌ Không thể đọc tokens.txt',
        'invalid_token': 'không hợp lệ, đã bỏ qua',
        'warning_line': 'Cảnh báo: Dòng',
        'found_proxies': 'Tìm thấy {count} proxy trong proxies.txt',
        'no_proxies': 'Không tìm thấy proxy trong proxies.txt',
        'using_proxy': '🔄 Sử dụng Proxy - [{proxy}] với IP công khai - [{public_ip}]',
        'no_proxy': 'Không có proxy',
        'unknown': 'Không xác định',
        'invalid_proxy': '⚠ Proxy không hợp lệ hoặc không hoạt động: {proxy}',
        'ip_check_failed': '⚠ Không thể kiểm tra IP công khai: {error}',
        'checking_referrals': 'Đang kiểm tra số lượng bạn bè được mời...',
        'referrals_count': 'Số bạn bè được mời: {count}',
        'insufficient_referrals': 'Không đủ bạn bè được mời: {current}/{required} cho nhiệm vụ {title}',
    },
    'en': {
        'title': 'AUTO REFERRAL TASKS - SNOONAUT',
        'info': 'Info',
        'found': 'Found',
        'tokens': 'tokens',
        'processing_tokens': '⚙ PROCESSING {count} TOKENS',
        'performing_task': 'Performing task: {task_title}',
        'success': '✅ Success: {message}',
        'failure': '❌ Failed: {error}',
        'username': 'Username',
        'tasks_completed': 'Tasks Completed',
        'pausing': 'Pausing',
        'seconds': 'seconds',
        'completed': '🏁 COMPLETED: {successful}/{total} TASKS SUCCESSFUL',
        'result_info': 'Task Results',
        'error': 'Error',
        'token_not_found': '❌ tokens.txt file not found',
        'token_empty': '❌ No valid tokens found',
        'token_error': '❌ Failed to read tokens.txt',
        'invalid_token': 'is invalid, skipped',
        'warning_line': 'Warning: Line',
        'found_proxies': 'Found {count} proxies in proxies.txt',
        'no_proxies': 'No proxies found in proxies.txt',
        'using_proxy': '🔄 Using Proxy - [{proxy}] with Public IP - [{public_ip}]',
        'no_proxy': 'None',
        'unknown': 'Unknown',
        'invalid_proxy': '⚠ Invalid or unresponsive proxy: {proxy}',
        'ip_check_failed': '⚠ Failed to check public IP: {error}',
        'checking_referrals': 'Checking number of referrals...',
        'referrals_count': 'Number of referrals: {count}',
        'insufficient_referrals': 'Insufficient referrals: {current}/{required} for task {title}',
    }
}

# Display functions
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

def print_message(message: str, color=Fore.YELLOW):
    print(f"{color}{message}{Style.RESET_ALL}")

def display_results(users: List[dict], language: str = 'en'):
    print_border(LANG[language]['result_info'], Fore.CYAN)
    print(f"{Fore.CYAN}  {'No':<4} | {'Username':<19} | {'Tasks Completed':<50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  {'-' * 4} | {'-' * 19} | {'-' * 50}{Style.RESET_ALL}")
    for i, user in enumerate(users, 1):
        username = user.get('username', 'N/A')
        tasks_completed = ', '.join(user.get('tasks_completed', [])) or 'No referral tasks completed.'
        print(f"{Fore.YELLOW}  {i:<4} | {username:<19} | {tasks_completed:<50}{Style.RESET_ALL}")
    print()

# Utility functions
def is_valid_token(line: str) -> bool:
    line = line.strip()
    if line.startswith('#') or not line:
        return False
    parts = line.split('|')
    if len(parts) != 2:
        return False
    session_token, csrf_token = parts
    return len(session_token.strip()) > 0 and '%7C' in csrf_token.strip()

def load_tokens(file_path: str = "tokens.txt", language: str = 'en') -> List[Tuple[int, str, str]]:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}  ✗ {LANG[language]['token_not_found']}{Style.RESET_ALL}")
            with open(file_path, 'w') as f:
                f.write("# Add session_token|csrf_token here, one per line\n# Example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...|1a49867f7dd5dd6ed8ef843fba657ff9%7Cd614918aea27c394...\n")
            sys.exit(1)
        
        valid_tokens = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if is_valid_token(line):
                        session_token, csrf_token = line.split('|')
                        valid_tokens.append((i, session_token.strip(), csrf_token.strip()))
                    else:
                        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['warning_line']} {i} {LANG[language]['invalid_token']}: {line}{Style.RESET_ALL}")
        
        if not valid_tokens:
            print(f"{Fore.RED}  ✗ {LANG[language]['token_empty']}{Style.RESET_ALL}")
            sys.exit(1)
        
        return valid_tokens
    except Exception as e:
        print(f"{Fore.RED}  ✗ {LANG[language]['token_error']}: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def load_proxies(file_path: str = "proxies.txt", language: str = 'en') -> List[str]:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['no_proxies']}. Using no proxy.{Style.RESET_ALL}")
            with open(file_path, 'w') as f:
                f.write("# Add proxies here, one per line\n# Example: socks5://user:pass@host:port or http://host:port\n")
            return []
        
        proxies = []
        with open(file_path, 'r') as f:
            for line in f:
                proxy = line.strip()
                if proxy and not line.startswith('#'):
                    proxies.append(proxy)
        
        if not proxies:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['no_proxies']}. Using no proxy.{Style.RESET_ALL}")
            return []
        
        print(f"{Fore.YELLOW}  ℹ {LANG[language]['found_proxies'].format(count=len(proxies))}{Style.RESET_ALL}")
        return proxies
    except Exception as e:
        print(f"{Fore.RED}  ✗ {LANG[language]['error']}: {str(e)}{Style.RESET_ALL}")
        return []

async def get_proxy_ip(proxy: str = None, language: str = 'en') -> str:
    try:
        if proxy:
            if proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')):
                connector = ProxyConnector.from_url(proxy)
            else:
                parts = proxy.split(':')
                if len(parts) == 4:  # host:port:user:pass
                    proxy_url = f"socks5://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
                    connector = ProxyConnector.from_url(proxy_url)
                elif len(parts) == 3 and '@' in proxy:  # user:pass@host:port
                    connector = ProxyConnector.from_url(f"socks5://{proxy}")
                else:
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['invalid_proxy'].format(proxy=proxy)}{Style.RESET_ALL}")
                    return LANG[language]['unknown']
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(IP_CHECK_URL, headers=HEADERS) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('ip', LANG[language]['unknown'])
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=f'HTTP {response.status}')}{Style.RESET_ALL}")
                    return LANG[language]['unknown']
        else:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(IP_CHECK_URL, headers=HEADERS) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('ip', LANG[language]['unknown'])
                    print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=f'HTTP {response.status}')}{Style.RESET_ALL}")
                    return LANG[language]['unknown']
    except Exception as e:
        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['ip_check_failed'].format(error=str(e))}{Style.RESET_ALL}")
        return LANG[language]['unknown']

async def get_user_info(session_token: str, csrf_token: str, language: str = 'en', proxy: str = None) -> dict:
    try:
        headers = {
            **HEADERS,
            "Cookie": f"__Secure-next-auth.session-token={session_token}; __Host-next-auth.csrf-token={csrf_token}; __Secure-next-auth.callback-url={CALLBACK_URL}"
        }
        connector = ProxyConnector.from_url(proxy) if proxy and proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')) else None
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(f"{API_BASE_URL}/api/auth/session", headers=headers, ssl=not CONFIG['BYPASS_SSL']) as response:
                response_text = await response.text()
                if response.status == 200:
                    try:
                        data = await response.json()
                        user = data.get('user', {})
                        if user.get('id'):
                            return {'username': user.get('username', 'N/A')}
                        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error='No user ID in session response')}{Style.RESET_ALL}")
                    except aiohttp.ContentTypeError:
                        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'Invalid JSON: {response_text}')}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'HTTP {response.status}: {response_text}')}{Style.RESET_ALL}")
                return {}
    except Exception as e:
        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=str(e))}{Style.RESET_ALL}")
        return {}

async def get_user_stats(session_token: str, csrf_token: str, language: str = 'en', proxy: str = None) -> int:
    try:
        headers = {
            **HEADERS,
            "Cookie": f"__Secure-next-auth.session-token={session_token}; __Host-next-auth.csrf-token={csrf_token}; __Secure-next-auth.callback-url={CALLBACK_URL}"
        }
        connector = ProxyConnector.from_url(proxy) if proxy and proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')) else None
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(f"{API_BASE_URL}/api/user/stats", headers=headers, ssl=not CONFIG['BYPASS_SSL']) as response:
                response_text = await response.text()
                if response.status == 200:
                    try:
                        data = await response.json()
                        referrals = data.get('referrals', [])
                        num_referrals = len(referrals)
                        print(f"{Fore.YELLOW}  ℹ {LANG[language]['referrals_count'].format(count=num_referrals)}{Style.RESET_ALL}")
                        return num_referrals
                    except aiohttp.ContentTypeError:
                        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'Invalid JSON: {response_text}')}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'HTTP {response.status}: {response_text}')}{Style.RESET_ALL}")
                return 0
    except Exception as e:
        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=str(e))}{Style.RESET_ALL}")
        return 0

async def get_tasks(session_token: str, csrf_token: str, language: str = 'en', proxy: str = None) -> List[dict]:
    try:
        headers = {
            **HEADERS,
            "Cookie": f"__Secure-next-auth.session-token={session_token}; __Host-next-auth.csrf-token={csrf_token}; __Secure-next-auth.callback-url={CALLBACK_URL}"
        }
        connector = ProxyConnector.from_url(proxy) if proxy and proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')) else None
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(f"{API_BASE_URL}/api/tasks?type=referral", headers=headers, ssl=not CONFIG['BYPASS_SSL']) as response:
                response_text = await response.text()
                if response.status == 200:
                    try:
                        data = await response.json()
                        return data.get('tasks', [])
                    except aiohttp.ContentTypeError:
                        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'Invalid JSON: {response_text}')}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'HTTP {response.status}: {response_text}')}{Style.RESET_ALL}")
                return []
    except Exception as e:
        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=str(e))}{Style.RESET_ALL}")
        return []

async def complete_task(session_token: str, csrf_token: str, task_id: str, task_title: str, task_type: str, min_referrals: int, num_referrals: int, profile_num: int, language: str = 'en', proxy: str = None) -> bool:
    if num_referrals < min_referrals:
        print(f"{Fore.YELLOW}  ℹ {LANG[language]['insufficient_referrals'].format(current=num_referrals, required=min_referrals, title=task_title)}{Style.RESET_ALL}")
        return False

    print(f"{Fore.CYAN}  > {LANG[language]['performing_task'].format(task_title=task_title)}{Style.RESET_ALL}")
    headers = {
        **HEADERS,
        "Cookie": f"__Secure-next-auth.session-token={session_token}; __Host-next-auth.csrf-token={csrf_token}; __Secure-next-auth.callback-url={CALLBACK_URL}"
    }
    payload = {"taskId": task_id, "action": "complete"}

    for attempt in range(CONFIG['RETRY_ATTEMPTS']):
        try:
            connector = ProxyConnector.from_url(proxy) if proxy and proxy.startswith(('socks5://', 'socks4://', 'http://', 'https://')) else None
            async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.post(f"{API_BASE_URL}/api/tasks/complete", headers=headers, json=payload, ssl=not CONFIG['BYPASS_SSL']) as response:
                    response_text = await response.text()
                    if response.status == 200:
                        try:
                            data = await response.json()
                            if data.get("success"):
                                print(f"{Fore.GREEN}  ✓ {LANG[language]['success'].format(message=f'Task {task_title} completed, Reward: {data.get("reward", 0)}')}{Style.RESET_ALL}")
                                return True
                            print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=data.get('message', 'Unknown error'))}{Style.RESET_ALL}")
                        except aiohttp.ContentTypeError:
                            print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'Invalid JSON: {response_text}')}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'HTTP {response.status}: {response_text}')}{Style.RESET_ALL}")
                    if attempt < CONFIG['RETRY_ATTEMPTS'] - 1:
                        delay = CONFIG['RETRY_DELAY']
                        print(f"{Fore.YELLOW}    {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
                        await asyncio.sleep(delay)
        except Exception as e:
            if attempt < CONFIG['RETRY_ATTEMPTS'] - 1:
                delay = CONFIG['RETRY_DELAY']
                print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=str(e))}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
                await asyncio.sleep(delay)
            else:
                print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=str(e))}{Style.RESET_ALL}")
                return False
    return False

async def process_tasks(session_token: str, csrf_token: str, profile_num: int, language: str = 'en', proxy: str = None) -> List[str]:
    completed_tasks = []
    
    # Get number of referrals
    print(f"{Fore.CYAN}  > {LANG[language]['checking_referrals']}{Style.RESET_ALL}")
    num_referrals = await get_user_stats(session_token, csrf_token, language, proxy)
    
    # Get referral tasks
    tasks = await get_tasks(session_token, csrf_token, language, proxy)
    for task in tasks:
        if task.get('status') == 'completed' or task.get('task_type') != 'referral':
            continue
        if await complete_task(session_token, csrf_token, task['id'], task['title'], task['task_type'], task.get('min_referrals', 0), num_referrals, profile_num, language, proxy):
            completed_tasks.append(task['title'])
    
    return completed_tasks

async def run_autotaskref(language: str = 'en'):
    try:
        print()
        print_border(LANG[language]['title'], Fore.CYAN)
        print()

        proxies = load_proxies('proxies.txt', language)
        tokens = load_tokens('tokens.txt', language)
        print(f"{Fore.YELLOW}  ℹ {LANG[language]['info']}: {LANG[language]['found']} {len(tokens)} {LANG[language]['tokens']}{Style.RESET_ALL}")
        print()

        if not tokens:
            print(f"{Fore.RED}  ✗ {LANG[language]['token_empty']}{Style.RESET_ALL}")
            return

        print_separator()
        random.shuffle(tokens)
        print_border(LANG[language]['processing_tokens'].format(count=len(tokens)), Fore.MAGENTA)
        print()

        users = []
        total_tasks = 0
        successful_tasks = 0

        async def process_token(index, profile_num, session_token, csrf_token):
            nonlocal total_tasks, successful_tasks
            proxy = proxies[index % len(proxies)] if proxies else None
            public_ip = await get_proxy_ip(proxy, language)
            proxy_display = proxy if proxy else LANG[language]['no_proxy']
            print(f"{Fore.CYAN}  🔄 {LANG[language]['using_proxy'].format(proxy=proxy_display, public_ip=public_ip)}{Style.RESET_ALL}")

            async with semaphore:
                try:
                    print_border(f"Processing Token {profile_num}", Fore.YELLOW)
                    
                    user_info = await get_user_info(session_token, csrf_token, language, proxy)
                    if not user_info:
                        print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error='Failed to get user info')}{Style.RESET_ALL}")
                        total_tasks += 1
                        return

                    completed_tasks = await process_tasks(session_token, csrf_token, profile_num, language, proxy)
                    user_info['tasks_completed'] = completed_tasks
                    if completed_tasks:
                        successful_tasks += 1
                        print(f"{Fore.GREEN}  ✓ {LANG[language]['success'].format(message=f'Completed tasks: {", ".join(completed_tasks)}')}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}  ℹ No referral tasks completed for profile {profile_num}{Style.RESET_ALL}")
                    
                    total_tasks += 1
                    users.append(user_info)

                    if index < len(tokens) - 1:
                        delay = CONFIG['DELAY_BETWEEN_ACCOUNTS']
                        print_message(f"  ℹ {LANG[language]['pausing']}: {delay:.2f} {LANG[language]['seconds']}", Fore.YELLOW)
                        await asyncio.sleep(delay)
                except Exception as e:
                    total_tasks += 1
                    print(f"{Fore.RED}  ✗ {LANG[language]['failure'].format(error=f'Token error: {str(e)}')}{Style.RESET_ALL}")

        semaphore = asyncio.Semaphore(CONFIG['THREADS'])
        tasks = [process_token(i, profile_num, session_token, csrf_token) for i, (profile_num, session_token, csrf_token) in enumerate(tokens)]
        await asyncio.gather(*tasks, return_exceptions=True)

        print()
        display_results(users, language)
        print_border(f"{LANG[language]['completed'].format(successful=successful_tasks, total=total_tasks)}", Fore.GREEN)
        print()

    except Exception as e:
        print(f"{Fore.RED}  ✗ {LANG[language]['error']}: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(run_autotaskref())
    except Exception as e:
        print(f"{Fore.RED}  ✗ {LANG['en']['error']}: {str(e)}{Style.RESET_ALL}")
