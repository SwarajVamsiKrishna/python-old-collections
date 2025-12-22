import subprocess

def get_wifi_name_windows():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interface'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if "SSID" in line:
                return line.split(":")[1].strip()
    except subprocess.CalledProcessError:
        return "Unable to retrieve Wi-Fi information"

print(get_wifi_name_windows())

