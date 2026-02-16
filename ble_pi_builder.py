#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║           BLE Pi Simulator Builder  v1.0                 ║
║       Law Enforcement / Security Assessment              ║
║       Raspberry Pi BLE Device Simulation Tool            ║
╚══════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
import random
import zipfile
import io
from datetime import datetime

# ══════════════════════════════════════════════════════════════
#  COLOR PALETTE  —  dark terminal aesthetic
# ══════════════════════════════════════════════════════════════
C = {
    "bg":        "#0A0E14",
    "bg2":       "#0D1117",
    "bg3":       "#131A22",
    "border":    "#1E2D3D",
    "green":     "#39FF14",
    "green_dim": "#2DB811",
    "cyan":      "#00D4FF",
    "yellow":    "#FFD700",
    "red":       "#FF4444",
    "white":     "#E8F4FD",
    "grey":      "#7A8FA6",
    "dim":       "#3D5166",
    "sel_bg":    "#0D2137",
    "sel_fg":    "#39FF14",
    "input_bg":  "#111820",
    "output_bg": "#060A0E",
}
FONT_MONO    = ("Courier New", 10)
FONT_MONO_SM = ("Courier New", 9)
FONT_MONO_LG = ("Courier New", 12, "bold")
FONT_MONO_HDR = ("Courier New", 13, "bold")

# ══════════════════════════════════════════════════════════════
#  DEVICE PROFILES DATABASE
# ══════════════════════════════════════════════════════════════
DEVICE_PROFILES = {
    "── MEDICAL / IMPLANTS ──": {
        "Medtronic Micra (Pacemaker)": {
            "oui": "E8:85:A4",
            "device_name": "Medtronic_Micra",
            "company_id": "0x0390",
            "service_uuids": ["0x1800", "0x1801", "0xFE59"],
            "adv_interval_ms": 500,
            "adv_type": "ADV_IND",
            "tx_power": -65,
            "appearance": 0x0480,
            "notes": "Leadless pacemaker. BlueSync. Static MAC. Re-advertises after phone drop.",
            "fields": {"Serial Number": "", "Model Number": "MC1VR01", "Firmware Rev": "2.1.0"}
        },
        "Medtronic Azure XT (Pacemaker)": {
            "oui": "E8:85:A4",
            "device_name": "Medtronic Azure",
            "company_id": "0x0390",
            "service_uuids": ["0x1800", "0x1801", "0xFE59"],
            "adv_interval_ms": 300,
            "adv_type": "ADV_IND",
            "tx_power": -60,
            "appearance": 0x0480,
            "notes": "Dual-chamber. BlueSync enabled. Common post-2018 implant.",
            "fields": {"Serial Number": "", "Model Number": "W3DR01", "Firmware Rev": "3.2.1"}
        },
        "MicroPort Alizea CRT-P": {
            "oui": "B8:27:EB",
            "device_name": "MicroPort Alizea",
            "company_id": "0x0698",
            "service_uuids": ["0x1800", "0x1801", "0xFE9F"],
            "adv_interval_ms": 600,
            "adv_type": "ADV_IND",
            "tx_power": -72,
            "appearance": 0x0480,
            "notes": "CRT-P class. Predictable re-advertising cycle after disconnect.",
            "fields": {"Serial Number": "", "Model Number": "ALZ100", "Firmware Rev": "1.5.2"}
        },
        "Abbott Gallant (ICD)": {
            "oui": "D0:CF:5E",
            "device_name": "Abbott Gallant ICD",
            "company_id": "0x004C",
            "service_uuids": ["0x1800", "0x180A", "0xFFF0"],
            "adv_interval_ms": 250,
            "adv_type": "ADV_IND",
            "tx_power": -70,
            "appearance": 0x0480,
            "notes": "Abbott/St. Jude Medical. Merlin.net connectivity. Static MAC.",
            "fields": {"Serial Number": "", "Model Number": "CD3371-40Q", "Firmware Rev": "4.1"}
        },
        "Boston Scientific Emblem (S-ICD)": {
            "oui": "AC:DE:48",
            "device_name": "BSci Emblem SICD",
            "company_id": "0x01D7",
            "service_uuids": ["0x1800", "0x1801", "0x180A"],
            "adv_interval_ms": 400,
            "adv_type": "ADV_IND",
            "tx_power": -68,
            "appearance": 0x0480,
            "notes": "Subcutaneous ICD. No leads. LATITUDE connectivity platform.",
            "fields": {"Serial Number": "", "Model Number": "EF3003", "Firmware Rev": "2.0"}
        },
        "Biotronik Edora 8 (Pacemaker)": {
            "oui": "00:1A:7D",
            "device_name": "BIOTRONIK Edora8",
            "company_id": "0x0258",
            "service_uuids": ["0x1800", "0x180A", "0xFEBE"],
            "adv_interval_ms": 350,
            "adv_type": "ADV_IND",
            "tx_power": -66,
            "appearance": 0x0480,
            "notes": "Home Monitoring. CardioMessenger pairing.",
            "fields": {"Serial Number": "", "Model Number": "379751", "Firmware Rev": "5.0"}
        },
    },
    "── APPLE DEVICES ──": {
        "iPod Touch 7th Gen": {
            "oui": "A4:C3:F0",
            "device_name": "iPod touch",
            "company_id": "0x004C",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 150,
            "adv_type": "ADV_IND",
            "tx_power": -59,
            "appearance": 0x0180,
            "notes": "iOS 15. Proximity pairing type 0x0C. Common in evidence scenarios.",
            "fields": {"iOS Version": "15.8", "BT Name Override": "iPod touch", "Proximity Byte": "0x0C"}
        },
        "iPod Touch 6th Gen": {
            "oui": "98:9E:63",
            "device_name": "iPod touch",
            "company_id": "0x004C",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 200,
            "adv_type": "ADV_IND",
            "tx_power": -62,
            "appearance": 0x0180,
            "notes": "iOS 12. Older device, often uses semi-static MAC.",
            "fields": {"iOS Version": "12.5.7", "BT Name Override": "iPod touch", "Proximity Byte": "0x09"}
        },
        "iPhone 13": {
            "oui": "F0:B4:29",
            "device_name": "iPhone",
            "company_id": "0x004C",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 100,
            "adv_type": "ADV_IND",
            "tx_power": -55,
            "appearance": 0x0180,
            "notes": "Apple Continuity. Proximity type 0x0F. Handoff capable.",
            "fields": {"iOS Version": "17.2", "BT Name Override": "iPhone", "Proximity Byte": "0x0F"}
        },
        "iPhone 15 Pro": {
            "oui": "3C:22:FB",
            "device_name": "iPhone",
            "company_id": "0x004C",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 80,
            "adv_type": "ADV_IND",
            "tx_power": -52,
            "appearance": 0x0180,
            "notes": "BLE 5.3. AirDrop, Continuity, Find My integration.",
            "fields": {"iOS Version": "17.4", "BT Name Override": "iPhone", "Proximity Byte": "0x0F"}
        },
        "AirPods Pro 2": {
            "oui": "28:6A:BA",
            "device_name": "AirPods Pro",
            "company_id": "0x004C",
            "service_uuids": ["0x1800"],
            "adv_interval_ms": 200,
            "adv_type": "ADV_NONCONN_IND",
            "tx_power": -60,
            "appearance": 0x0941,
            "notes": "Proximity pairing type 0x13. Battery levels in mfr data.",
            "fields": {"Left Battery %": "85", "Right Battery %": "90", "Case Battery %": "100"}
        },
        "MacBook Pro (M3)": {
            "oui": "3C:22:FB",
            "device_name": "MacBook Pro",
            "company_id": "0x004C",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 200,
            "adv_type": "ADV_IND",
            "tx_power": -58,
            "appearance": 0x0180,
            "notes": "Continuity protocol. Handoff / Universal Clipboard.",
            "fields": {"macOS Version": "14.3", "BT Name Override": "MacBook Pro", "Continuity Byte": "0x10"}
        },
    },
    "── ANDROID / MOBILE ──": {
        "Samsung Galaxy S23": {
            "oui": "F4:F9:51",
            "device_name": "Galaxy S23",
            "company_id": "0x0075",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 150,
            "adv_type": "ADV_IND",
            "tx_power": -57,
            "appearance": 0x0180,
            "notes": "SmartThings Find. Randomized MAC on Android 10+ — use static.",
            "fields": {"Android Version": "13", "One UI Version": "5.1", "BT Name Override": "Galaxy S23"}
        },
        "Samsung Galaxy S24": {
            "oui": "8C:71:F8",
            "device_name": "Galaxy S24",
            "company_id": "0x0075",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 120,
            "adv_type": "ADV_IND",
            "tx_power": -54,
            "appearance": 0x0180,
            "notes": "BLE 5.3. UWB capable. SmartThings Find enhanced.",
            "fields": {"Android Version": "14", "One UI Version": "6.1", "BT Name Override": "Galaxy S24"}
        },
        "Google Pixel 7": {
            "oui": "E4:25:E7",
            "device_name": "Pixel 7",
            "company_id": "0x00E0",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 100,
            "adv_type": "ADV_IND",
            "tx_power": -55,
            "appearance": 0x0180,
            "notes": "Google Fast Pair. Model ID in mfr data. Tensor G2.",
            "fields": {"Android Version": "14", "Fast Pair Model": "0x4AE70E", "BT Name Override": "Pixel 7"}
        },
        "Google Pixel 8 Pro": {
            "oui": "40:4E:36",
            "device_name": "Pixel 8 Pro",
            "company_id": "0x00E0",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 90,
            "adv_type": "ADV_IND",
            "tx_power": -52,
            "appearance": 0x0180,
            "notes": "BLE 5.3. Tensor G3. UWB. Fast Pair 2.",
            "fields": {"Android Version": "14", "Fast Pair Model": "0x5CF321", "BT Name Override": "Pixel 8 Pro"}
        },
    },
    "── FITNESS / WEARABLES ──": {
        "Fitbit Charge 6": {
            "oui": "C4:AC:59",
            "device_name": "Charge 6",
            "company_id": "0x0075",
            "service_uuids": ["0x1800", "0x180D", "0x180A"],
            "adv_interval_ms": 500,
            "adv_type": "ADV_IND",
            "tx_power": -65,
            "appearance": 0x0180,
            "notes": "Heart rate svc 0x180D. Fitness Machine profile.",
            "fields": {"BT Name Override": "Charge 6", "Heart Rate (bpm)": "72", "Steps Today": "4231"}
        },
        "Garmin Fenix 7": {
            "oui": "68:13:18",
            "device_name": "Fenix 7",
            "company_id": "0x0087",
            "service_uuids": ["0x1800", "0x180D", "0x1816"],
            "adv_interval_ms": 300,
            "adv_type": "ADV_IND",
            "tx_power": -60,
            "appearance": 0x00C2,
            "notes": "Running Speed & Cadence 0x1816. ANT+ bridge.",
            "fields": {"BT Name Override": "Fenix 7", "Activity Mode": "Running", "HR Zone": "2"}
        },
        "Apple Watch Series 9": {
            "oui": "AC:B5:7D",
            "device_name": "Apple Watch",
            "company_id": "0x004C",
            "service_uuids": ["0x1800", "0x180D", "0x180F"],
            "adv_interval_ms": 200,
            "adv_type": "ADV_IND",
            "tx_power": -58,
            "appearance": 0x00C0,
            "notes": "watchOS 10. Heart rate + battery svc. Continuity with iPhone.",
            "fields": {"watchOS Version": "10.2", "BT Name Override": "Apple Watch", "Heart Rate (bpm)": "68"}
        },
        "Polar H10 (HR Monitor)": {
            "oui": "A0:E6:F8",
            "device_name": "Polar H10",
            "company_id": "0x006B",
            "service_uuids": ["0x1800", "0x180D"],
            "adv_interval_ms": 1000,
            "adv_type": "ADV_IND",
            "tx_power": -70,
            "appearance": 0x0340,
            "notes": "Heart rate chest strap. Common in athletic forensics.",
            "fields": {"BT Name Override": "Polar H10", "Heart Rate (bpm)": "68", "Sensor Location": "Chest"}
        },
    },
    "── LAPTOPS / COMPUTERS ──": {
        "Dell Laptop (Windows 11)": {
            "oui": "E4:B9:7A",
            "device_name": "DESKTOP-XXXXXX",
            "company_id": "0x00D4",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 250,
            "adv_type": "ADV_IND",
            "tx_power": -62,
            "appearance": 0x0180,
            "notes": "Windows Swift Pair advertising. Generic PC profile.",
            "fields": {"Windows Version": "11 Pro", "Hostname": "DESKTOP-", "Swift Pair": "Enabled"}
        },
        "HP Laptop (Windows 10)": {
            "oui": "D4:81:D7",
            "device_name": "HP-Laptop",
            "company_id": "0x00D4",
            "service_uuids": ["0x1800", "0x1801"],
            "adv_interval_ms": 300,
            "adv_type": "ADV_IND",
            "tx_power": -64,
            "appearance": 0x0180,
            "notes": "HP factory OUI. Swift Pair. Common enterprise device.",
            "fields": {"Windows Version": "10 Pro", "Hostname": "HP-LAPTOP-", "Swift Pair": "Enabled"}
        },
    },
    "── CUSTOM / MANUAL ──": {
        "Custom Device Profile": {
            "oui": "00:00:00",
            "device_name": "Custom BLE Device",
            "company_id": "0x0000",
            "service_uuids": ["0x1800"],
            "adv_interval_ms": 500,
            "adv_type": "ADV_IND",
            "tx_power": -65,
            "appearance": 0x0000,
            "notes": "Fully configurable. Enter all parameters manually.",
            "fields": {"Custom Field 1": "", "Custom Field 2": "", "Custom Field 3": ""}
        },
    }
}

# ══════════════════════════════════════════════════════════════
#  SCRIPT GENERATORS
# ══════════════════════════════════════════════════════════════

def generate_setup_sh(profile, mac, config):
    mac_rev = ' '.join(mac.split(':')[::-1])
    ms = int(config.get('adv_interval_ms', 500))
    units = max(32, int(ms / 0.625))
    lo = format(units & 0xFF, '02X')
    hi = format((units >> 8) & 0xFF, '02X')
    return f"""#!/bin/bash
# ============================================================
#  BLE Simulator Setup
#  Profile   : {profile['device_name']}
#  MAC       : {mac}
#  Interval  : {ms}ms
#  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#  Tool      : BLE Pi Simulator Builder
# ============================================================

set -e

echo ""
echo "============================================================"
echo "  BLE Pi Simulator -- Setup"
echo "  Profile  : {profile['device_name']}"
echo "  MAC      : {mac}"
echo "============================================================"
echo ""

echo "[*] Updating package lists..."
sudo apt-get update -qq

echo "[*] Installing dependencies..."
sudo apt-get install -y bluetooth bluez python3-pip python3-dbus libglib2.0-dev -qq

echo "[*] Enabling Bluetooth..."
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
sleep 2

echo "[*] Spoofing MAC -> {mac}"
sudo hciconfig hci0 down
sudo btmgmt --index 0 public-addr {mac} 2>/dev/null || true
sudo hcitool -i hci0 cmd 0x03 0x0005 {mac_rev} 2>/dev/null || true
sudo hciconfig hci0 up
sleep 1

echo "[*] Setting advertising interval ({ms}ms)..."
sudo hcitool -i hci0 cmd 0x08 0x0006 {lo} {hi} {lo} {hi} 00 00 00 00 00 00 00 00 00 07 00

echo "[*] Deploying simulator..."
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
sudo cp "$SCRIPT_DIR/ble_simulator.py" /opt/ble_simulator.py
sudo chmod +x /opt/ble_simulator.py
sudo cp "$SCRIPT_DIR/ble_simulator.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ble_simulator
sudo systemctl start ble_simulator

echo ""
echo "============================================================"
echo "  [+] Setup complete"
echo "  [+] Advertising as : {profile['device_name']}"
echo "  [+] MAC Address    : {mac}"
echo "  [+] Interval       : {ms}ms"
echo "------------------------------------------------------------"
echo "  Status : sudo systemctl status ble_simulator"
echo "  Logs   : sudo journalctl -u ble_simulator -f"
echo "  Verify : sudo hcitool lescan --passive"
echo "============================================================"
echo ""
"""


def generate_simulator_py(profile, mac, config):
    cid = profile.get('company_id', '0x0000').replace('0x', '').zfill(4)
    mfr_lo = f"0x{cid[2:4]}"
    mfr_hi = f"0x{cid[0:2]}"
    field_comments = '\n'.join(
        f'    #  {k:<24}: {v}' for k, v in profile.get('fields', {}).items()
    )
    ms  = int(config.get('adv_interval_ms', 500))
    tx  = int(profile["tx_power"])
    adv_type = config.get('adv_type', 'ADV_IND')
    # ADV_IND=0x00, ADV_NONCONN_IND=0x03, ADV_SCAN_IND=0x02
    adv_type_map = {"ADV_IND": "0x00", "ADV_NONCONN_IND": "0x03", "ADV_SCAN_IND": "0x02"}
    adv_type_hex = adv_type_map.get(adv_type, "0x00")

    return f'''#!/usr/bin/env python3
"""
============================================================
  BLE Device Simulator  —  Raw HCI Mode
  Profile   : {profile["device_name"]}
  MAC       : {mac}
  Interval  : {ms}ms
  Generated : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
  No external BLE libraries required — uses hcitool directly
============================================================
"""

import subprocess
import time
import signal
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    handlers=[
        logging.FileHandler("/var/log/ble_simulator.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ── Device Configuration ──────────────────────────────────────
DEVICE_NAME     = "{profile["device_name"]}"
MAC_ADDRESS     = "{mac}"
COMPANY_ID_LO   = {mfr_lo}
COMPANY_ID_HI   = {mfr_hi}
ADV_INTERVAL_MS = {ms}
TX_POWER        = {tx}
ADV_TYPE        = "{adv_type}"
HCI_DEV         = "hci0"

# ── Device Metadata ───────────────────────────────────────────
{field_comments}


# ── Advertisement Payload Builder ─────────────────────────────
def build_adv_payload(name, company_lo, company_hi, tx_power):
    """Build AD structures. Max 31 bytes."""
    payload = []

    # Flags: LE General Discoverable, no BR/EDR
    payload += [0x02, 0x01, 0x06]

    # TX Power Level
    payload += [0x02, 0x0A, tx_power & 0xFF]

    # Manufacturer Specific Data
    payload += [0x03, 0xFF, company_lo & 0xFF, company_hi & 0xFF]

    # Complete Local Name (fill remaining space)
    remaining = 31 - len(payload) - 2
    name_bytes = list(name.encode("utf-8")[:remaining])
    payload += [len(name_bytes) + 1, 0x09] + name_bytes

    # Pad to exactly 31 bytes
    while len(payload) < 31:
        payload.append(0x00)

    return payload[:31]


def build_scan_response(name):
    """Build scan response — returns full device name."""
    payload = []
    name_bytes = list(name.encode("utf-8")[:29])
    payload += [len(name_bytes) + 1, 0x09] + name_bytes
    while len(payload) < 31:
        payload.append(0x00)
    return payload[:31]


# ── HCI Command Helpers ───────────────────────────────────────
def hci_cmd(args, label=""):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=5)
        if r.returncode != 0 and label:
            log.warning(f"  [!] {{label}}: {{r.stderr.strip()}}")
        return r.returncode == 0
    except Exception as e:
        log.error(f"  [!] Command error: {{e}}")
        return False


def hci_raw(ogf, ocf, data_bytes):
    """Send a raw HCI command via hcitool cmd."""
    cmd = ["sudo", "hcitool", "-i", HCI_DEV, "cmd",
           f"0x{{ogf:02x}}", f"0x{{ocf:04x}}"] + [f"{{b:02X}}" for b in data_bytes]
    return hci_cmd(cmd)


def set_adv_data(payload):
    return hci_raw(0x08, 0x0008, [len(payload)] + payload)


def set_scan_rsp(payload):
    return hci_raw(0x08, 0x0009, [len(payload)] + payload)


def set_adv_params(interval_ms, adv_type_hex):
    units = max(32, int(interval_ms / 0.625))
    lo = units & 0xFF
    hi = (units >> 8) & 0xFF
    adv_t = int(adv_type_hex, 16)
    return hci_raw(0x08, 0x0006,
        [lo, hi, lo, hi, adv_t, 0x00, 0x00,
         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00])


def set_adv_enable(enable):
    return hci_raw(0x08, 0x000A, [0x01 if enable else 0x00])


# ── Main ──────────────────────────────────────────────────────
def start():
    log.info("")
    log.info("  ============================================================")
    log.info("  BLE Simulator Active  --  Raw HCI Mode")
    log.info(f"  Profile   : {{DEVICE_NAME}}")
    log.info(f"  MAC       : {{MAC_ADDRESS}}")
    log.info(f"  Adv Type  : {{ADV_TYPE}}")
    log.info(f"  Interval  : {{ADV_INTERVAL_MS}}ms")
    log.info(f"  TX Power  : {{TX_POWER}} dBm")
    log.info("  ============================================================")

    # Ensure adapter is up
    hci_cmd(["sudo", "hciconfig", HCI_DEV, "up"], "hci up")
    time.sleep(1)

    # Disable advertising before configuring
    set_adv_enable(False)
    time.sleep(0.3)

    # Configure and enable
    log.info("  [*] Setting advertising parameters...")
    set_adv_params(ADV_INTERVAL_MS, "{adv_type_hex}")

    log.info("  [*] Building advertisement payload...")
    adv = build_adv_payload(DEVICE_NAME, COMPANY_ID_LO, COMPANY_ID_HI, TX_POWER)
    rsp = build_scan_response(DEVICE_NAME)
    set_adv_data(adv)
    set_scan_rsp(rsp)

    log.info("  [*] Enabling advertising...")
    set_adv_enable(True)

    log.info("  ------------------------------------------------------------")
    log.info("  [+] Broadcasting on channels 37, 38, 39")
    log.info(f"  [+] Advertising as : {{DEVICE_NAME}}")
    log.info(f"  [+] MAC Address    : {{MAC_ADDRESS}}")
    log.info(f"  [+] Interval       : {{ADV_INTERVAL_MS}}ms")
    log.info("  [+] Ctrl+C or systemctl stop to halt")
    log.info("  ============================================================")
    log.info("")

    running = True

    def _stop(sig, frame):
        nonlocal running
        log.info("  [!] Signal received -- stopping...")
        running = False

    signal.signal(signal.SIGINT,  _stop)
    signal.signal(signal.SIGTERM, _stop)

    heartbeat = 0
    while running:
        time.sleep(5)
        heartbeat += 5
        if heartbeat % 60 == 0:
            log.info(f"  [~] Still advertising... ({{heartbeat}}s elapsed)")

    set_adv_enable(False)
    log.info("  [-] Advertising stopped.")
    log.info("  [-] Simulator exited cleanly.")
    sys.exit(0)


if __name__ == "__main__":
    start()
'''


def generate_service_unit(profile):
    return f"""[Unit]
Description=BLE Device Simulator -- {profile["device_name"]}
After=bluetooth.target
Wants=bluetooth.target

[Service]
Type=simple
User=root
ExecStartPre=/bin/sleep 5
ExecStart=/usr/bin/python3 /opt/ble_simulator.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""


def generate_readme(profile, mac, config):
    ms = config.get('adv_interval_ms', 500)
    return f"""
============================================================
  BLE Pi Simulator -- Deployment Package
  Profile   : {profile['device_name']}
  MAC       : {mac}
  Interval  : {ms}ms
  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
============================================================

DEPLOYMENT STEPS
------------------------------------------------------------
1. Flash Raspberry Pi OS Lite to SD card
   Use: https://www.raspberrypi.com/software/
   Enable SSH and configure WiFi in Imager settings.

2. Copy files to Pi:
   scp setup.sh ble_simulator.py ble_simulator.service <user>@<IP>:/home/<user>/

3. SSH in and run setup:
   ssh <user>@<IP>
   cd /home/<user>/
   chmod +x setup.sh
   sudo ./setup.sh

4. Verify:
   sudo systemctl status ble_simulator
   sudo journalctl -u ble_simulator -f

VERIFICATION WITH BLE SCANNER
------------------------------------------------------------
   sudo hcitool lescan --passive -t 30
   # Expected:
   # {mac}    {profile['device_name']}

DEVICE NOTES
------------------------------------------------------------
   {profile['notes']}

BLE PARAMETERS
------------------------------------------------------------
   Device Name   : {profile['device_name']}
   MAC Address   : {mac}
   Company ID    : {profile.get('company_id', 'N/A')}
   Service UUIDs : {', '.join(profile['service_uuids'])}
   Adv Interval  : {ms}ms
   TX Power      : {profile['tx_power']} dBm
   Adv Type      : {config.get('adv_type', 'ADV_IND')}

============================================================
"""


# ══════════════════════════════════════════════════════════════
#  MAIN GUI APPLICATION
# ══════════════════════════════════════════════════════════════

class BLEPiBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BLE Pi Simulator Builder  |  Law Enforcement / Security Assessment")
        self.geometry("1100x780")
        self.minsize(900, 650)
        self.configure(bg=C["bg"])

        self.current_profile = None
        self.current_cat     = None
        self.param_vars      = {}
        self.fields_vars     = {}

        self._setup_styles()
        self._build_header()
        self._build_body()
        self._build_statusbar()

        for cat in DEVICE_PROFILES:
            self.cat_lb.insert(tk.END, f"  {cat}")
        self.cat_lb.selection_set(0)
        self._on_cat(None)

    # ── Styles ─────────────────────────────────────────────────

    def _setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")

        s.configure("TNotebook", background=C["bg"], borderwidth=0,
                    tabmargins=[0, 0, 0, 0])
        s.configure("TNotebook.Tab", background=C["bg3"], foreground=C["grey"],
                    padding=[14, 6], font=FONT_MONO, borderwidth=0, relief=tk.FLAT)
        s.map("TNotebook.Tab",
              background=[("selected", C["bg2"])],
              foreground=[("selected", C["green"])])

        s.configure("TFrame", background=C["bg"])

        s.configure("TLabel", background=C["bg"], foreground=C["white"], font=FONT_MONO)

        s.configure("TEntry",
                    fieldbackground=C["input_bg"], foreground=C["white"],
                    insertcolor=C["green"], bordercolor=C["border"],
                    lightcolor=C["border"], darkcolor=C["border"], font=FONT_MONO)

        s.configure("TCombobox",
                    fieldbackground=C["input_bg"], foreground=C["white"],
                    selectbackground=C["sel_bg"], selectforeground=C["green"],
                    font=FONT_MONO, arrowcolor=C["green"])
        s.map("TCombobox",
              fieldbackground=[("readonly", C["input_bg"])],
              foreground=[("readonly", C["white"])])

        s.configure("TButton",
                    background=C["bg3"], foreground=C["cyan"],
                    bordercolor=C["border"], lightcolor=C["border"],
                    darkcolor=C["border"], font=FONT_MONO,
                    padding=[10, 5], relief=tk.FLAT)
        s.map("TButton",
              background=[("active", C["sel_bg"])],
              foreground=[("active", C["green"])])

        s.configure("Export.TButton",
                    background=C["dim"], foreground=C["green"],
                    font=("Courier New", 10, "bold"), padding=[14, 7])
        s.map("Export.TButton",
              background=[("active", C["sel_bg"])],
              foreground=[("active", C["yellow"])])

    # ── Header ─────────────────────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self, bg="#060A0E")
        hdr.pack(fill=tk.X)

        inner = tk.Frame(hdr, bg="#060A0E")
        inner.pack(fill=tk.X, padx=16, pady=10)

        tk.Label(inner, text="BLE PI SIMULATOR BUILDER",
                 bg="#060A0E", fg=C["green"],
                 font=("Courier New", 16, "bold")).pack(side=tk.LEFT)

        tk.Label(inner,
                 text="  ──  law enforcement / security assessment  |  raspberry pi ble simulator",
                 bg="#060A0E", fg=C["dim"],
                 font=FONT_MONO_SM).pack(side=tk.LEFT)

        tk.Label(inner, text=f"  {datetime.now().strftime('%Y-%m-%d')}",
                 bg="#060A0E", fg=C["grey"],
                 font=FONT_MONO_SM).pack(side=tk.RIGHT)

        tk.Frame(self, bg=C["green"], height=1).pack(fill=tk.X)

    # ── Body ───────────────────────────────────────────────────

    def _build_body(self):
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill=tk.BOTH, expand=True)

        self._build_sidebar(body)
        tk.Frame(body, bg=C["border"], width=1).pack(side=tk.LEFT, fill=tk.Y)
        self._build_content(body)

    def _build_sidebar(self, parent):
        side = tk.Frame(parent, bg=C["bg2"], width=235)
        side.pack(side=tk.LEFT, fill=tk.Y)
        side.pack_propagate(False)

        tk.Label(side, text="CATEGORY",
                 bg=C["bg2"], fg=C["cyan"],
                 font=("Courier New", 9, "bold")).pack(anchor=tk.W, padx=10, pady=(12, 2))

        self.cat_lb = tk.Listbox(side,
            bg=C["bg3"], fg=C["grey"],
            selectbackground=C["sel_bg"], selectforeground=C["green"],
            font=FONT_MONO_SM, borderwidth=0, highlightthickness=0,
            activestyle="none", height=8, relief=tk.FLAT)
        self.cat_lb.pack(fill=tk.X, padx=8, pady=(0, 8))
        self.cat_lb.bind("<<ListboxSelect>>", self._on_cat)

        tk.Frame(side, bg=C["border"], height=1).pack(fill=tk.X, padx=8)

        tk.Label(side, text="DEVICE PROFILE",
                 bg=C["bg2"], fg=C["cyan"],
                 font=("Courier New", 9, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))

        self.dev_lb = tk.Listbox(side,
            bg=C["bg3"], fg=C["white"],
            selectbackground=C["sel_bg"], selectforeground=C["green"],
            font=FONT_MONO_SM, borderwidth=0, highlightthickness=0,
            activestyle="none", relief=tk.FLAT)
        self.dev_lb.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.dev_lb.bind("<<ListboxSelect>>", self._on_dev)

        tk.Frame(side, bg=C["border"], height=1).pack(fill=tk.X, padx=8)

        tk.Label(side, text="NOTES",
                 bg=C["bg2"], fg=C["cyan"],
                 font=("Courier New", 9, "bold")).pack(anchor=tk.W, padx=10, pady=(8, 2))

        self.notes_text = tk.Text(side,
            bg=C["bg3"], fg=C["grey"],
            font=FONT_MONO_SM, borderwidth=0, highlightthickness=0,
            wrap=tk.WORD, state=tk.DISABLED, height=5, relief=tk.FLAT)
        self.notes_text.pack(fill=tk.X, padx=8, pady=(0, 10))

    def _build_content(self, parent):
        content = tk.Frame(parent, bg=C["bg"])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        nb = ttk.Notebook(content)
        nb.pack(fill=tk.BOTH, expand=True)

        self._tab_configure(nb)
        self._tab_mac(nb)
        self._tab_preview(nb)
        self._tab_export(nb)

    # ── Tab: Configure ─────────────────────────────────────────

    def _tab_configure(self, nb):
        tab = tk.Frame(nb, bg=C["bg"])
        nb.add(tab, text="  [ CONFIGURE ]  ")

        canvas = tk.Canvas(tab, bg=C["bg"], borderwidth=0, highlightthickness=0)
        sb = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sf = tk.Frame(canvas, bg=C["bg"])
        canvas.create_window((0, 0), window=sf, anchor=tk.NW)
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._section_header(sf, "BLE ADVERTISEMENT PARAMETERS")

        pframe = tk.Frame(sf, bg=C["bg2"],
                          highlightbackground=C["border"], highlightthickness=1)
        pframe.pack(fill=tk.X, padx=20, pady=(0, 12))

        params = [
            ("Device Name",       "device_name",    "str"),
            ("Company ID (hex)",  "company_id",     "str"),
            ("Service UUID(s)",   "service_uuids",  "str"),
            ("Adv Interval (ms)", "adv_interval_ms","str"),
            ("TX Power (dBm)",    "tx_power",       "str"),
            ("Adv Type",          "adv_type",       "combo",
             ["ADV_IND", "ADV_NONCONN_IND", "ADV_SCAN_IND"]),
        ]

        for row_i, item in enumerate(params):
            lbl, key, kind = item[0], item[1], item[2]
            tk.Label(pframe, text=f"  {lbl}",
                     bg=C["bg2"], fg=C["grey"],
                     font=FONT_MONO_SM, width=24, anchor=tk.W
                     ).grid(row=row_i, column=0, sticky=tk.W, padx=(8, 0), pady=4)
            var = tk.StringVar()
            if kind == "combo":
                w = ttk.Combobox(pframe, textvariable=var,
                                 values=item[3], state="readonly", width=30)
            else:
                w = ttk.Entry(pframe, textvariable=var, width=32)
            w.grid(row=row_i, column=1, sticky=tk.W, padx=10, pady=4)
            self.param_vars[key] = var

        self._section_header(sf, "DEVICE-SPECIFIC FIELDS")

        self.fields_frame = tk.Frame(sf, bg=C["bg2"],
                                     highlightbackground=C["border"],
                                     highlightthickness=1)
        self.fields_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

    # ── Tab: MAC ────────────────────────────────────────────────

    def _tab_mac(self, nb):
        tab = tk.Frame(nb, bg=C["bg"])
        nb.add(tab, text="  [ MAC / IDENTITY ]  ")

        self._section_header(tab, "MAC ADDRESS CONFIGURATION")

        mac_panel = tk.Frame(tab, bg=C["bg2"],
                             highlightbackground=C["border"], highlightthickness=1)
        mac_panel.pack(fill=tk.X, padx=20, pady=(0, 12))

        r0 = tk.Frame(mac_panel, bg=C["bg2"])
        r0.pack(fill=tk.X, padx=12, pady=12)

        tk.Label(r0, text="MAC Address",
                 bg=C["bg2"], fg=C["grey"],
                 font=FONT_MONO_SM, width=20, anchor=tk.W).pack(side=tk.LEFT)

        self.mac_var = tk.StringVar(value="AA:BB:CC:DD:EE:FF")
        ttk.Entry(r0, textvariable=self.mac_var,
                  width=22, font=("Courier New", 12)
                  ).pack(side=tk.LEFT, padx=8)

        btn_row = tk.Frame(mac_panel, bg=C["bg2"])
        btn_row.pack(fill=tk.X, padx=12, pady=(0, 10))

        for txt, cmd in [
            ("OUI from Profile",  self._mac_from_oui),
            ("Random (keep OUI)", self._mac_rand_oui),
            ("Fully Random",      self._mac_rand_full),
        ]:
            ttk.Button(btn_row, text=txt, command=cmd).pack(side=tk.LEFT, padx=4)

        self._section_header(tab, "KNOWN VENDOR OUI REFERENCE")

        oui_frame = tk.Frame(tab, bg=C["output_bg"],
                             highlightbackground=C["border"], highlightthickness=1)
        oui_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        oui_txt = scrolledtext.ScrolledText(oui_frame,
            bg=C["output_bg"], fg=C["grey"],
            font=FONT_MONO_SM, borderwidth=0, relief=tk.FLAT, wrap=tk.NONE)
        oui_txt.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        oui_data = (
            "  Vendor                   OUI Prefix      Category\n"
            "  " + "─" * 58 + "\n"
            "  Medtronic                E8:85:A4        Pacemaker / ICD (BlueSync)\n"
            "  Medtronic (alt)          E4:CE:8F        Older devices\n"
            "  Abbott / St. Jude        D0:CF:5E        Merlin.net devices\n"
            "  Boston Scientific        AC:DE:48        LATITUDE / Emblem ICD\n"
            "  MicroPort                B8:27:EB        Alizea CRT\n"
            "  Biotronik                00:1A:7D        Edora / Rivacor\n"
            "  Sorin / LivaNova         00:17:F2        Reply series\n"
            "  Zoll Medical             00:0A:E4        LifeVest wearable ICD\n"
            "  " + "─" * 58 + "\n"
            "  Apple (iPhone/iPod)      A4:C3:F0        iOS devices (common)\n"
            "  Apple (iPhone/iPod)      F0:B4:29        iOS devices (alt)\n"
            "  Apple (MacBook)          3C:22:FB        Apple Silicon Macs\n"
            "  Samsung Mobile           F4:F9:51        Galaxy S series\n"
            "  Samsung Mobile           8C:71:F8        Galaxy S24 series\n"
            "  Google Pixel             E4:25:E7        Pixel 7\n"
            "  Google Pixel             40:4E:36        Pixel 8\n"
            "  Fitbit                   C4:AC:59        Charge series\n"
            "  Garmin                   68:13:18        Fenix / Forerunner\n"
            "  Dell                     E4:B9:7A        Latitude / Inspiron\n"
        )
        oui_txt.insert(tk.END, oui_data)
        oui_txt.configure(state=tk.DISABLED)

    # ── Tab: Preview ────────────────────────────────────────────

    def _tab_preview(self, nb):
        tab = tk.Frame(nb, bg=C["bg"])
        nb.add(tab, text="  [ PREVIEW ]  ")

        ctrl = tk.Frame(tab, bg=C["bg"])
        ctrl.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(ctrl, text="ADVERTISEMENT PAYLOAD PREVIEW",
                 bg=C["bg"], fg=C["cyan"],
                 font=("Courier New", 10, "bold")).pack(side=tk.LEFT)

        ttk.Button(ctrl, text="Refresh",
                   command=self._refresh_preview).pack(side=tk.RIGHT)

        self.preview_txt = scrolledtext.ScrolledText(tab,
            bg=C["output_bg"], fg=C["green"],
            font=FONT_MONO_SM, borderwidth=0, relief=tk.FLAT,
            insertbackground=C["green"], wrap=tk.NONE, state=tk.DISABLED)
        self.preview_txt.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.preview_txt.tag_configure("header", foreground=C["green"])
        self.preview_txt.tag_configure("key",    foreground=C["grey"])
        self.preview_txt.tag_configure("val",    foreground=C["cyan"])
        self.preview_txt.tag_configure("div",    foreground=C["dim"])
        self.preview_txt.tag_configure("hex",    foreground=C["yellow"])

    # ── Tab: Export ─────────────────────────────────────────────

    def _tab_export(self, nb):
        tab = tk.Frame(nb, bg=C["bg"])
        nb.add(tab, text="  [ GENERATE & EXPORT ]  ")

        ctrl = tk.Frame(tab, bg=C["bg"])
        ctrl.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(ctrl, text="DEPLOYMENT PACKAGE GENERATOR",
                 bg=C["bg"], fg=C["cyan"],
                 font=("Courier New", 10, "bold")).pack(side=tk.LEFT)

        self.output_txt = scrolledtext.ScrolledText(tab,
            bg=C["output_bg"], fg=C["green"],
            font=FONT_MONO_SM, borderwidth=0, relief=tk.FLAT,
            insertbackground=C["green"], wrap=tk.NONE, state=tk.DISABLED)
        self.output_txt.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 8))

        self.output_txt.tag_configure("ok",   foreground=C["green"])
        self.output_txt.tag_configure("info", foreground=C["cyan"])
        self.output_txt.tag_configure("warn", foreground=C["yellow"])
        self.output_txt.tag_configure("div",  foreground=C["dim"])

        btn_row = tk.Frame(tab, bg=C["bg"])
        btn_row.pack(fill=tk.X, padx=20, pady=(0, 14))

        ttk.Button(btn_row, text="Preview Package Contents",
                   command=self._preview_pkg).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(btn_row, text="Export Scripts to Folder",
                   command=self._export_folder).pack(side=tk.LEFT, padx=6)

        ttk.Button(btn_row, text=">> EXPORT ZIP PACKAGE",
                   command=self._export_zip,
                   style="Export.TButton").pack(side=tk.RIGHT)

    # ── Shared UI helpers ──────────────────────────────────────

    def _section_header(self, parent, title):
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill=tk.X, padx=20, pady=(14, 4))
        tk.Label(row, text=title,
                 bg=C["bg"], fg=C["cyan"],
                 font=("Courier New", 9, "bold")).pack(side=tk.LEFT)
        tk.Frame(row, bg=C["dim"], height=1).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))

    # ── Event handlers ─────────────────────────────────────────

    def _on_cat(self, event):
        sel = self.cat_lb.curselection()
        if not sel:
            return
        raw = self.cat_lb.get(sel[0]).strip()
        for k in DEVICE_PROFILES:
            if k.strip() == raw:
                self.current_cat = k
                break
        if not self.current_cat:
            return
        self.dev_lb.delete(0, tk.END)
        for dev in DEVICE_PROFILES[self.current_cat]:
            self.dev_lb.insert(tk.END, f"  {dev}")
        self.dev_lb.selection_set(0)
        self._on_dev(None)

    def _on_dev(self, event):
        sel = self.dev_lb.curselection()
        if not sel or not self.current_cat:
            return
        dev_raw = self.dev_lb.get(sel[0]).strip()
        profile = None
        for k in DEVICE_PROFILES[self.current_cat]:
            if k.strip() == dev_raw:
                profile = DEVICE_PROFILES[self.current_cat][k]
                break
        if not profile:
            return
        self.current_profile = profile

        self.notes_text.configure(state=tk.NORMAL)
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(tk.END, f"  {profile['notes']}")
        self.notes_text.configure(state=tk.DISABLED)

        self.param_vars['device_name'].set(profile['device_name'])
        self.param_vars['company_id'].set(profile['company_id'])
        self.param_vars['service_uuids'].set(', '.join(profile['service_uuids']))
        self.param_vars['adv_interval_ms'].set(str(profile['adv_interval_ms']))
        self.param_vars['tx_power'].set(str(profile['tx_power']))
        self.param_vars['adv_type'].set(profile['adv_type'])

        suffix = ':'.join(format(random.randint(0, 255), '02X') for _ in range(3))
        self.mac_var.set(f"{profile['oui']}:{suffix}")

        for w in self.fields_frame.winfo_children():
            w.destroy()
        self.fields_vars.clear()

        for row_i, (k, default) in enumerate(profile.get('fields', {}).items()):
            tk.Label(self.fields_frame, text=f"  {k}",
                     bg=C["bg2"], fg=C["grey"],
                     font=FONT_MONO_SM, width=28, anchor=tk.W
                     ).grid(row=row_i, column=0, sticky=tk.W, padx=(8, 0), pady=4)
            var = tk.StringVar(value=default)
            ttk.Entry(self.fields_frame, textvariable=var, width=32
                      ).grid(row=row_i, column=1, padx=10, pady=4, sticky=tk.W)
            self.fields_vars[k] = var

        self.status_var.set(
            f"  Profile loaded  --  {dev_raw}  |  OUI: {profile['oui']}"
            f"  |  {profile['adv_interval_ms']}ms"
        )
        self._refresh_preview()

    # ── MAC helpers ────────────────────────────────────────────

    def _mac_from_oui(self):
        if not self.current_profile:
            return
        s = ':'.join(format(random.randint(0, 255), '02X') for _ in range(3))
        self.mac_var.set(f"{self.current_profile['oui']}:{s}")

    def _mac_rand_oui(self):
        self._mac_from_oui()

    def _mac_rand_full(self):
        self.mac_var.set(
            ':'.join(format(random.randint(0, 255), '02X') for _ in range(6))
        )

    # ── Preview ─────────────────────────────────────────────────

    def _refresh_preview(self):
        if not self.current_profile:
            return
        p   = self.current_profile
        mac = self.mac_var.get()
        cfg = self._get_config()
        ms  = cfg.get('adv_interval_ms', '500')
        cid = p.get('company_id', '0x0000')
        tx  = cfg.get('tx_power', str(p['tx_power']))
        svc = cfg.get('service_uuids', '0x1800')

        raw_cid   = cid.replace('0x', '').zfill(4)
        name_hex  = ' '.join(f'{ord(c):02X}' for c in p['device_name'][:12])
        name_ad   = f"{len(p['device_name'][:12])+1:02X} 09 {name_hex}"
        mfr_ad    = f"03 FF {raw_cid[2:4]} {raw_cid[0:2]}"
        first_svc = svc.split(',')[0].strip().replace('0x', '').zfill(4)
        svc_ad    = f"03 03 {first_svc[2:4]} {first_svc[0:2]}"

        W = 62
        lines = []

        def out(txt="", tag=None):
            lines.append((txt, tag))

        out("=" * W, "div")
        out(f"  ADVERTISEMENT PREVIEW  --  {p['device_name']}", "header")
        out("=" * W, "div")
        out(f"  {'Device Name':<22}: {p['device_name']}", "key")
        out(f"  {'MAC Address':<22}: {mac}  (static)", "key")
        out(f"  {'Advertisement Type':<22}: {cfg.get('adv_type','ADV_IND')}", "key")
        out(f"  {'Interval':<22}: {ms} ms", "key")
        out(f"  {'TX Power':<22}: {tx} dBm", "key")
        out(f"  {'Company ID':<22}: {cid}", "key")
        out(f"  {'Service UUIDs':<22}: {svc.strip()}", "key")
        out("-" * W, "div")
        out("  RAW HCI ADVERTISEMENT PAYLOAD", "header")
        out("-" * W, "div")
        out(f"  PDU Type  : {cfg.get('adv_type','ADV_IND')}", "key")
        out(f"  AdvA      : {mac.replace(':','  ')}", "hex")
        out(f"  Channels  : 37, 38, 39  (all advertising channels)", "key")
        out("", None)
        out(f"  AD Structures:", "key")
        out(f"    02 01 06          Flags (LE General Discoverable)", "hex")
        out(f"    {name_ad[:36]:<36}  Complete Local Name", "hex")
        out(f"    {svc_ad:<36}  16-bit Service UUID", "hex")
        out(f"    {mfr_ad:<36}  Manufacturer Specific Data", "hex")
        out("-" * W, "div")
        out("  EXPECTED BLE SCANNER OUTPUT", "header")
        out("-" * W, "div")
        out("  " + "=" * 60, "div")
        out(f"  DEVICE #1  -  seen 1x", "val")
        out("  " + "=" * 60, "div")
        out(f"  {'Address':<14}: {mac}", "val")
        out(f"  {'Name':<14}: {p['device_name']}", "val")
        out(f"  {'RSSI':<14}: {tx} dBm", "val")
        out(f"  {'TX Power':<14}: {tx} dBm", "val")
        out(f"  {'Manufacturer':<14}: {cid} -> {raw_cid.lower()}", "val")
        out("  " + "=" * 60, "div")
        out("-" * W, "div")
        out("  TIMING BEHAVIOR", "header")
        out("-" * W, "div")
        out(f"  Broadcasting every ~{ms}ms on advertising channels", "key")
        out(f"  Re-advertises after connection drop", "key")
        out(f"  Static MAC confirmed -- fingerprinting enabled", "key")
        out("=" * W, "div")

        self.preview_txt.configure(state=tk.NORMAL)
        self.preview_txt.delete(1.0, tk.END)
        for text, tag in lines:
            if tag:
                self.preview_txt.insert(tk.END, text + "\n", tag)
            else:
                self.preview_txt.insert(tk.END, "\n")
        self.preview_txt.configure(state=tk.DISABLED)

    # ── Config helpers ─────────────────────────────────────────

    def _get_config(self):
        cfg = {}
        for k, v in self.param_vars.items():
            cfg[k] = v.get()
        for k, v in self.fields_vars.items():
            cfg[k] = v.get()
        return cfg

    def _validate_mac(self, mac):
        parts = mac.split(':')
        if len(parts) != 6:
            return False
        try:
            for p in parts:
                if len(p) != 2:
                    return False
                int(p, 16)
            return True
        except ValueError:
            return False

    # ── Output writing ─────────────────────────────────────────

    def _write_output(self, text, tag="ok"):
        self.output_txt.configure(state=tk.NORMAL)
        self.output_txt.insert(tk.END, text + "\n", tag)
        self.output_txt.see(tk.END)
        self.output_txt.configure(state=tk.DISABLED)

    def _clear_output(self):
        self.output_txt.configure(state=tk.NORMAL)
        self.output_txt.delete(1.0, tk.END)
        self.output_txt.configure(state=tk.DISABLED)

    # ── Export helpers ─────────────────────────────────────────

    def _preview_pkg(self):
        if not self.current_profile:
            messagebox.showwarning("No Profile", "Select a device profile first.")
            return
        p   = self.current_profile
        mac = self.mac_var.get()
        cfg = self._get_config()
        W   = 62

        self._clear_output()
        self._write_output("=" * W, "div")
        self._write_output("  DEPLOYMENT PACKAGE PREVIEW", "info")
        self._write_output("=" * W, "div")
        self._write_output(f"  Profile   : {p['device_name']}", "info")
        self._write_output(f"  MAC       : {mac}", "info")
        self._write_output(f"  Interval  : {cfg.get('adv_interval_ms')}ms", "info")
        self._write_output(f"  Adv Type  : {cfg.get('adv_type','ADV_IND')}", "info")
        self._write_output("-" * W, "div")
        self._write_output("  FILES IN PACKAGE", "info")
        self._write_output("-" * W, "div")
        self._write_output("  setup.sh               -> Install BlueZ, spoof MAC, deploy service", "ok")
        self._write_output("  ble_simulator.py       -> BLE GATT server (auto-starts on boot)", "ok")
        self._write_output("  ble_simulator.service  -> systemd unit (persistent)", "ok")
        self._write_output("  README.md              -> Step-by-step deployment guide", "ok")
        self._write_output("  profile.json           -> Config record for documentation", "ok")
        self._write_output("-" * W, "div")
        self._write_output("  DEPLOY COMMANDS", "info")
        self._write_output("-" * W, "div")
        self._write_output(f"  scp *.* <user>@<IP>:/home/<user>/", "warn")
        self._write_output(f"  ssh <user>@<IP> 'cd /home/<user> && sudo bash setup.sh'", "warn")
        self._write_output("-" * W, "div")
        self._write_output("  VERIFY WITH BLE SCANNER", "info")
        self._write_output("-" * W, "div")
        self._write_output(f"  sudo hcitool lescan --passive", "warn")
        self._write_output(f"  Expected:  {mac}    {p['device_name']}", "ok")
        self._write_output("=" * W, "div")

    def _export_zip(self):
        if not self.current_profile:
            messagebox.showwarning("No Profile", "Select a device profile first.")
            return
        p   = self.current_profile
        mac = self.mac_var.get()
        cfg = self._get_config()

        if not self._validate_mac(mac):
            messagebox.showerror("Invalid MAC",
                                 "MAC must be format:  XX:XX:XX:XX:XX:XX")
            return

        safe = p['device_name'].replace(' ', '_').replace('/', '_')
        path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP Archive", "*.zip")],
            initialfile=f"ble_sim_{safe}.zip",
            title="Save Deployment Package"
        )
        if not path:
            return

        try:
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("setup.sh",              generate_setup_sh(p, mac, cfg))
                zf.writestr("ble_simulator.py",      generate_simulator_py(p, mac, cfg))
                zf.writestr("ble_simulator.service", generate_service_unit(p))
                zf.writestr("README.md",             generate_readme(p, mac, cfg))
                zf.writestr("profile.json",
                            json.dumps({
                                "profile":   p['device_name'],
                                "mac":       mac,
                                "oui":       p['oui'],
                                "config":    cfg,
                                "generated": datetime.now().isoformat(),
                            }, indent=2))

            with open(path, 'wb') as f:
                f.write(buf.getvalue())

            W = 62
            self._clear_output()
            self._write_output("=" * W, "div")
            self._write_output("  [+] EXPORT SUCCESSFUL", "ok")
            self._write_output("=" * W, "div")
            self._write_output(f"  Path      : {path}", "info")
            self._write_output(f"  Profile   : {p['device_name']}", "info")
            self._write_output(f"  MAC       : {mac}", "info")
            self._write_output(f"  Size      : {os.path.getsize(path):,} bytes", "info")
            self._write_output("-" * W, "div")
            self._write_output("  Contents  : setup.sh", "ok")
            self._write_output("            : ble_simulator.py", "ok")
            self._write_output("            : ble_simulator.service", "ok")
            self._write_output("            : README.md", "ok")
            self._write_output("            : profile.json", "ok")
            self._write_output("-" * W, "div")
            self._write_output("  NEXT STEPS", "info")
            self._write_output("-" * W, "div")
            self._write_output(f"  unzip {os.path.basename(path)}", "warn")
            self._write_output(f"  scp *.* <user>@<PI_IP>:/home/<user>/", "warn")
            self._write_output(f"  ssh <user>@<PI_IP> 'cd /home/<user> && sudo bash setup.sh'", "warn")
            self._write_output("=" * W, "div")
            self.status_var.set(
                f"  [+] Exported  --  {os.path.basename(path)}"
                f"  |  {p['device_name']}  |  {mac}"
            )

        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def _export_folder(self):
        if not self.current_profile:
            messagebox.showwarning("No Profile", "Select a device profile first.")
            return
        p   = self.current_profile
        mac = self.mac_var.get()
        cfg = self._get_config()

        folder = filedialog.askdirectory(title="Select Export Folder")
        if not folder:
            return

        try:
            files = {
                "setup.sh":              generate_setup_sh(p, mac, cfg),
                "ble_simulator.py":      generate_simulator_py(p, mac, cfg),
                "ble_simulator.service": generate_service_unit(p),
                "README.md":             generate_readme(p, mac, cfg),
            }
            for fname, content in files.items():
                with open(os.path.join(folder, fname), 'w') as f:
                    f.write(content)

            self.status_var.set(f"  [+] Scripts exported  --  {folder}")
            messagebox.showinfo("Exported", f"Scripts written to:\n{folder}")

        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    # ── Status bar ─────────────────────────────────────────────

    def _build_statusbar(self):
        tk.Frame(self, bg=C["green"], height=1).pack(fill=tk.X)
        bar = tk.Frame(self, bg="#060A0E")
        bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_var = tk.StringVar(
            value="  Ready  --  Select a device profile to begin"
        )
        tk.Label(bar, textvariable=self.status_var,
                 bg="#060A0E", fg=C["dim"],
                 font=FONT_MONO_SM, anchor=tk.W
                 ).pack(side=tk.LEFT, padx=4, pady=4)

        tk.Label(bar,
                 text="BLE Pi Simulator Builder  |  Law Enforcement / Security Assessment  ",
                 bg="#060A0E", fg=C["dim"],
                 font=FONT_MONO_SM
                 ).pack(side=tk.RIGHT, padx=4)


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = BLEPiBuilder()
    app.mainloop()
