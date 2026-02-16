# ble_simulator
# BLE Pi Simulator
### Raspberry Pi Zero W — Bluetooth Device Simulation
**Law Enforcement / Authorized Security Assessment Tool**

> Simulate BLE device advertisements from medical implants, consumer electronics, and IoT devices using a Raspberry Pi Zero W. From a blank SD card to active BLE advertisement in under 15 minutes.

---

##  Legal Notice

This tool is designed for **authorized law enforcement investigations and cybersecurity security assessments only**. Unauthorized simulation of Bluetooth devices may violate federal and state laws. Always operate within the scope of your authorized engagement.

---

## Table of Contents

- [What You Need](#what-you-need)
- [Step 1 — Flash the OS](#step-1--flash-the-os)
- [Step 2 — First Boot & SSH](#step-2--first-boot--ssh)
- [Step 3 — Update the OS](#step-3--update-the-os)
- [Step 4 — Transfer & Run Setup Package](#step-4--transfer--run-setup-package)
- [Step 5 — Verify Bluetooth is Advertising](#step-5--verify-bluetooth-is-advertising)
- [Step 6 — Deploy a Device Profile](#step-6--deploy-a-device-profile)
- [Troubleshooting](#troubleshooting)
- [Command Reference](#command-reference)
- [Device Profile Reference](#device-profile-reference)
- [Technical Architecture](#technical-architecture)
- [File Reference](#file-reference)

---

## Deployment Workflow

```
┌──────┬────────────────────────────────────────────────────┬──────────┐
│ Step │ Action                                             │ Time     │
├──────┼────────────────────────────────────────────────────┼──────────┤
│  1   │ Flash Raspberry Pi OS Lite via Pi Imager           │ ~5 min   │
│  2   │ Boot Pi, find IP, connect via SSH                  │ ~2 min   │
│  3   │ Update the operating system                        │ ~5 min   │
│  4   │ Transfer setup package via SCP and run firstrun.sh │ ~5 min   │
│  5   │ Verify Bluetooth adapter is active and advertising │ ~1 min   │
│  6   │ Deploy device profile from Builder app             │ ~2 min   │
└──────┴────────────────────────────────────────────────────┴──────────┘
```

---

## What You Need

### Hardware

| Item | Specification | Notes |
|------|--------------|-------|
| Raspberry Pi Zero W | Pi Zero **W** — not Pi Zero (no W) | Built-in BLE 4.1 + WiFi. ~$15 |
| MicroSD Card | 8GB min, 16GB recommended | Class 10 or A1 speed rating |
| Micro USB Power Supply | 5V / 2A | Use **PWR IN** port — not the USB port |
| MicroSD Card Reader | USB-A or USB-C | To flash OS from your laptop |
| Windows Laptop | Windows 10 or 11 | Runs Pi Imager, PowerShell SCP, SSH |

### Software (all free)

- **Raspberry Pi Imager** — [raspberrypi.com/software](https://www.raspberrypi.com/software/)
- **Python 3 for Windows** — [python.org/downloads](https://www.python.org/downloads/)
- `ble_pi_builder.py` — The Builder GUI app (in this repo)
- `ble_pi_setup_package.zip` — The Pi setup package (in this repo)

> **Pi Zero W Power Ports**
> The Pi Zero W has two identical-looking Micro USB ports on the bottom edge.
> - **PWR IN** — Power input. Always use this one.
> - **USB** — OTG data port only. Do not power through this port.

---

## Step 1 — Flash the OS

Download and install **Raspberry Pi Imager** from [raspberrypi.com/software](https://www.raspberrypi.com/software/).

Insert your MicroSD card, open Pi Imager, and follow these steps:

**1.** Click **Choose Device** → select **Raspberry Pi Zero**

**2.** Click **Choose OS** → **Raspberry Pi OS (other)** → **Raspberry Pi OS Lite (32-bit)**

> **Why Lite?** No desktop environment — smaller footprint, faster boot, no unnecessary services. The simulator runs headless so a desktop is not needed.

**3.** Click **Choose Storage** → select your MicroSD card

**4.** Click the **gear icon (Edit Settings)** before writing — configure the following:

| Setting | What to Enter |
|---------|--------------|
| Hostname | `ble-sim` |
| Enable SSH |  Checked — Use password authentication |
| Username | your chosen username (e.g. `hansgar`) |
| Password | a strong password — remember this |
| WiFi SSID | your network name |
| WiFi Password | your WiFi password |
| Locale / Timezone | set to your region |

>  **Do not skip the gear icon step.** WiFi credentials are baked into the card during flashing. If you skip this, the Pi won't join your network and SSH won't work.

**5.** Click **Write** — wait approximately 5 minutes

**6.** Eject the MicroSD card when complete

---

## Step 2 — First Boot & SSH

### Power On

1. Insert the MicroSD card into the Pi Zero W
2. Connect power to the **PWR IN** Micro USB port
3. Green LED will flash during boot — wait **60–90 seconds**

### Find the Pi's IP Address

**Option A — Ping by hostname (easiest)**

Open PowerShell on your Windows laptop:

```powershell
ping -4 ble-sim.local
```

The IP address appears in the reply output.

**Option B — Check your router**

Log into your router admin page (usually `192.168.1.1` in a browser). Look for `ble-sim` or `raspberrypi` in the DHCP client list.

**Option C — Network scan**

```powershell
nmap -sn 192.168.1.0/24
```

Look for the Raspberry Pi entry — the IP is listed next to it.

### Connect via SSH

```powershell
ssh hansgar@192.168.1.56
```

Replace `hansgar` with your username and the IP with your Pi's actual IP.

- First time: type `yes` when asked about the fingerprint
- Enter your password when prompted — no characters will appear as you type

A successful login looks like:

```
hansgar@ble-sim:~ $
```

> 📝 Write down your Pi's IP address — you'll need it for every SCP and SSH session.

---

## Step 3 — Update the OS

From your SSH session:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

This takes **3–8 minutes** on a Pi Zero W. Wait for the prompt to return.

>  **Do not skip this step.** Running setup on an outdated Pi OS can cause package conflicts and Bluetooth initialization failures.

When the upgrade finishes, reboot:

```bash
sudo reboot
```

The SSH session will disconnect — this is normal. Wait 45 seconds then SSH back in:

```powershell
ssh hansgar@192.168.1.56
```

---

## Step 4 — Transfer & Run Setup Package

### Transfer the Package

Open a **new PowerShell window** on your Windows laptop and run:

```powershell
scp C:\Users\YourUser\Downloads\ble_pi_setup_package.zip hansgar@192.168.1.56:/home/hansgar/
```

Successful transfer:

```
ble_pi_setup_package.zip          100%   12KB   3.7MB/s   00:00
```

### Run the Setup

Switch back to your SSH session:

```bash
cd /home/hansgar
unzip ble_pi_setup_package.zip
sudo bash firstrun.sh
```

That's it. The script handles everything automatically.

### What the Setup Script Does

| Check | Action | Auto-Fixed? |
|-------|--------|:-----------:|
| System packages | Installs bluetooth, bluez, python3, libglib2.0-dev |  |
| Boot config | Adds UART overlay and krnbt to `/boot/firmware/config.txt` |  |
| BlueZ experimental | Enables `--experimental` flag in `bluetooth.service` |  |
| main.conf | Sets `Experimental = true` in `/etc/bluetooth/main.conf` |  |
| Bluetooth service | Enables and starts `bluetooth.service` |  |
| BLE adapter (hci0) | Brings up `hci0` and verifies `UP RUNNING` |  |
| Python environment | Verifies Python 3 and required modules |  |
| Simulator script | Deploys `ble_simulator.py` to `/opt/` |  |
| systemd service | Installs and enables `ble_simulator.service` |  |
| Reboot | Prompts for reboot if `config.txt` was modified | Prompts |

### If a Reboot Is Required

The script will ask:

```
  Reboot now?  (y/n)
```

Type `y` and press Enter. SSH back in after 45 seconds, then verify:

```bash
sudo bash ble_pi_setup.sh
```

### Expected Output (All Passing)

```
============================================================
  BLE Pi Simulator — Master Setup
============================================================

STEP 1 — SYSTEM PACKAGES
────────────────────────────────────────────────────────────
  [✓]  Package list updated
  [✓]  Package installed: bluetooth
  [✓]  Package installed: bluez
  [✓]  Package installed: python3
  ...

STEP 5 — BLE ADAPTER
────────────────────────────────────────────────────────────
  [✓]  hci0 is UP RUNNING
  [✓]  BD Address : B8:27:EB:83:92:85
  [✓]  HCI Version: 4.2 (0x8)

STEP 8 — SYSTEMD SERVICE
────────────────────────────────────────────────────────────
  [✓]  ble_simulator.service installed and enabled
  [✓]  ble_simulator.service is ACTIVE

============================================================
  [+] ALL CHECKS PASSED — Pi is ready
============================================================
```

---

## Step 5 — Verify Bluetooth is Advertising

### Check Service Status

```bash
# Service status
sudo systemctl status ble_simulator

# Watch live logs
sudo journalctl -u ble_simulator -f
```

Expected log output:

```
  ============================================================
  BLE Simulator Active  --  Raw HCI Mode
  Profile   : BLE-Device
  MAC       : (hardware default)
  Interval  : 500ms
  ============================================================
  [+] Broadcasting on channels 37, 38, 39
  [+] Advertising as : BLE-Device
  ============================================================
```

Press `Ctrl+C` to stop watching logs. The simulator keeps running in the background.

### Run the Health Check

```bash
sudo bash /home/hansgar/health_check.sh
```

Expected output:

```
── Bluetooth Service
  [✓]  bluetooth.service is active
  [✓]  bluetooth.service is enabled (starts on boot)
── BLE Adapter (hci0)
  [✓]  hci0 is UP RUNNING
── Simulator Service
  [✓]  ble_simulator.service is ACTIVE
── Results:  8 passed   0 warnings   0 failed
  All checks passed — Pi is healthy and advertising
```

### Verify with Your Phone

The Pi will **not** appear in your phone's standard Bluetooth settings — that only shows pairable devices like headphones. Use a BLE scanner app:

| App | Platform | Notes |
|-----|----------|-------|
| **LightBlue** | iOS + Android | Best for general use — shows all raw BLE advertisements |
| **nRF Connect** | iOS + Android | Most detail — shows full GATT service tree |
| **BLE Scanner** | iOS + Android | Simple, clean interface |

Open the app, pull to refresh, and look for `BLE-Device`. Once you see it the Pi is confirmed advertising.

---

## Step 6 — Deploy a Device Profile

### Run the Builder App

On your Windows laptop:

```powershell
python C:\Users\YourUser\Downloads\ble_pi_builder.py
```

> If `python` is not recognized, install Python from [python.org](https://www.python.org/downloads/) and check **Add Python to PATH** during install.

### Select and Configure a Profile

1. Select a category from the left panel (e.g. `── MEDICAL / IMPLANTS ──`)
2. Select a device profile (e.g. `Medtronic Azure XT (Pacemaker)`)
3. Click the **MAC / Identity** tab
4. Click **OUI from Profile** to generate the correct vendor MAC
5. Review parameters in the **Configure** tab
6. Click **Preview** tab to verify the advertisement payload

### Export the ZIP Package

1. Click **Generate & Export** tab
2. Click **>> EXPORT ZIP PACKAGE**
3. Save to your Downloads folder

The ZIP contains:

| File | Purpose |
|------|---------|
| `setup.sh` | Spoofs MAC, sets interval, deploys service |
| `ble_simulator.py` | Configured simulator for this device profile |
| `ble_simulator.service` | systemd unit file |
| `README.md` | Profile-specific deployment notes |
| `profile.json` | Configuration record |

### Transfer and Deploy

From PowerShell:

```powershell
scp C:\Users\YourUser\Downloads\ble_sim_Medtronic_Azure.zip hansgar@192.168.1.56:/home/hansgar/
```

From SSH on the Pi:

```bash
cd /home/hansgar
unzip ble_sim_Medtronic_Azure.zip
chmod +x setup.sh
sudo ./setup.sh
```

Within seconds the Pi is advertising as the target device. Verify in your BLE scanner app — look for the device name from the profile (e.g. `Medtronic Azure`).

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Can't ping `ble-sim.local` | Re-flash card with correct WiFi credentials in Imager settings |
| SSH connection refused | Re-flash and enable SSH in Imager settings before writing |
| `hci0: Can't init device` | Run `sudo bash ble_pi_setup.sh` — fixes `config.txt` automatically |
| `service is failed` in status | Run `sudo journalctl -u ble_simulator -f` to see error, then `sudo bash ble_pi_setup.sh` |
| `setup.sh: No such file` | You ran the command from Windows PowerShell — SSH into the Pi first |
| `scp: No such file` | ZIP filename doesn't match — check exact filename in Downloads |
| Device not in BLE scanner app | Use LightBlue or nRF Connect — not the phone's built-in Bluetooth settings |
| Wrong device name showing | Deploy a profile ZIP from the Builder app to replace the default |
| `hci0` shows DOWN after reboot | Run `sudo hciconfig hci0 up` or `sudo bash ble_pi_setup.sh` |

---

## Command Reference

### Day-to-Day Commands (run on Pi via SSH)

```bash
# Check simulator status
sudo systemctl status ble_simulator

# Watch live logs
sudo journalctl -u ble_simulator -f

# Run health check
sudo bash /home/hansgar/health_check.sh

# Restart simulator
sudo systemctl restart ble_simulator

# Stop simulator
sudo systemctl stop ble_simulator

# Check BLE adapter
hciconfig -a

# Bring adapter up manually
sudo hciconfig hci0 up

# Test simulator script directly
sudo python3 /opt/ble_simulator.py

# Re-run full setup (safe to run multiple times)
sudo bash /home/hansgar/ble_pi_setup.sh

# Reboot
sudo reboot
```

### Setup Checklist

- [ ] MicroSD flashed with Raspberry Pi OS Lite via Pi Imager
- [ ] Hostname, SSH, WiFi, password configured in Imager before writing
- [ ] Pi powered via PWR IN port
- [ ] Pi found on network — IP confirmed with `ping -4 ble-sim.local`
- [ ] SSH connection working
- [ ] `sudo apt update && sudo apt upgrade -y` completed
- [ ] `ble_pi_setup_package.zip` transferred via SCP
- [ ] `sudo bash firstrun.sh` completed with no errors
- [ ] Rebooted if prompted by setup script
- [ ] `sudo bash ble_pi_setup.sh` shows ALL CHECKS PASSED
- [ ] `sudo bash health_check.sh` shows 0 failed
- [ ] Device visible in LightBlue / nRF Connect on phone
- [ ] Profile ZIP exported from Builder app
- [ ] Profile ZIP transferred and `setup.sh` run
- [ ] Device visible in BLE scanner app with correct name and MAC

---

## Device Profile Reference

### Medical / Implants

| Device | OUI | Company ID | Interval | Adv Type | Notes |
|--------|-----|-----------|----------|----------|-------|
| Medtronic Micra (Pacemaker) | `E8:85:A4` | 0x0390 | 500ms | ADV_IND | BlueSync, static MAC |
| Medtronic Azure XT (Pacemaker) | `E8:85:A4` | 0x0390 | 300ms | ADV_IND | Dual-chamber, common post-2018 |
| MicroPort Alizea CRT-P | `B8:27:EB` | 0x0698 | 600ms | ADV_IND | Predictable re-advertising cycle |
| Abbott Gallant ICD | `D0:CF:5E` | 0x004C | 250ms | ADV_IND | Merlin.net, static MAC |
| Boston Scientific Emblem S-ICD | `AC:DE:48` | 0x01D7 | 400ms | ADV_IND | LATITUDE platform, no leads |
| Biotronik Edora 8 (Pacemaker) | `00:1A:7D` | 0x0258 | 350ms | ADV_IND | CardioMessenger pairing |

### Consumer Devices

| Device | OUI | Company ID | Interval | Notes |
|--------|-----|-----------|----------|-------|
| iPod Touch 7th Gen | `A4:C3:F0` | 0x004C | 150ms | iOS 15, common in evidence |
| iPod Touch 6th Gen | `98:9E:63` | 0x004C | 200ms | iOS 12, semi-static MAC |
| iPhone 13 | `F0:B4:29` | 0x004C | 100ms | Continuity, Handoff |
| iPhone 15 Pro | `3C:22:FB` | 0x004C | 80ms | BLE 5.3, AirDrop |
| AirPods Pro 2 | `28:6A:BA` | 0x004C | 200ms | ADV_NONCONN_IND |
| Samsung Galaxy S23 | `F4:F9:51` | 0x0075 | 200ms | SmartThings Find |
| Google Pixel 7 | `E4:25:E7` | 0x00E0 | 150ms | Fast Pair, Tensor G2 |
| Fitbit Charge 6 | `C4:AC:59` | 0x0006 | 1000ms | Health/fitness BLE |
| Garmin Fenix 7 | `68:13:18` | 0x01D7 | 1000ms | ANT+ bridge |
| Apple Watch Series 9 | `A4:C3:F0` | 0x004C | 300ms | ADV_NONCONN_IND |

---

## Technical Architecture

### How the Simulator Works

The simulator bypasses high-level BLE libraries entirely and communicates directly with the BlueZ HCI layer using `hcitool` commands. This approach is compatible with all Python versions and BlueZ releases — no `bless`, `bleak`, or `dbus` dependencies.

```
Builder App (Windows)          Pi Zero W
──────────────────────         ─────────────────────────────
ble_pi_builder.py              /opt/ble_simulator.py
  │                              │
  │  Select profile               │  set_adv_params()
  │  Configure MAC                │    hcitool cmd 0x08 0x0006
  │  Export ZIP        ──SCP──>   │  build_adv_payload()
  │                               │    Flags + TX Power + Mfr + Name
  └── setup.sh                    │  set_adv_data()
        │                         │    hcitool cmd 0x08 0x0008
        │  btmgmt MAC spoof        │  set_adv_enable()
        │  HCI interval            │    hcitool cmd 0x08 0x000A
        └─> systemd service ──>   └─> Broadcasting channels 37/38/39
```

### Advertisement Payload Structure

Each BLE advertisement is a 31-byte AD structure payload:

```
Byte  Type    Description
────  ──────  ────────────────────────────────────────
02    01      Flags
      06        LE General Discoverable, no BR/EDR
02    0A      TX Power Level
      C4        -60 dBm (0xC4 = -60 signed)
03    FF      Manufacturer Specific Data
      90 03     Company ID 0x0390 (Medtronic)
0F    09      Complete Local Name
      4D...     'Medtronic Azure' in UTF-8
00    ...     Padding to 31 bytes
```

### MAC Spoofing

```bash
# Primary method
sudo btmgmt --index 0 public-addr E8:85:A4:9A:93:B5

# Fallback — raw HCI (bytes reversed)
sudo hcitool -i hci0 cmd 0x03 0x0005 B5 93 9A A4 85 E8
```

### Boot Config Changes Made by Setup Script

The setup script adds these lines to `/boot/firmware/config.txt`:

```ini
enable_uart=1         # required for Pi Zero W serial
dtoverlay=miniuart-bt # moves BT off main UART — prevents conflict
dtparam=krnbt=on      # kernel BT initialization
```

---

## File Reference

### Setup Package (`ble_pi_setup_package.zip`)

| File | Description |
|------|-------------|
| `firstrun.sh` | Entry point — sets permissions then calls setup |
| `ble_pi_setup.sh` | Main setup — 10 automated checks and fixes |
| `ble_simulator.py` | Default BLE simulator — no external dependencies |
| `ble_simulator.service` | systemd unit — auto-starts on boot |
| `health_check.sh` | Run anytime to verify full Pi status |
| `README.txt` | Quick start instructions |

### Builder App Output ZIP

| File | Description |
|------|-------------|
| `setup.sh` | Device-specific setup — MAC spoof, interval, service install |
| `ble_simulator.py` | Configured simulator for the chosen device profile |
| `ble_simulator.service` | systemd unit with device name in description |
| `README.md` | Profile-specific deployment notes |
| `profile.json` | Full configuration record with timestamp |

---

## Contributing

Pull requests welcome. Please keep additions focused on:
- New device profiles with accurate OUI, company ID, and advertising parameters
- Verified compatibility notes for different Pi OS versions
- Additional BLE scanner tool documentation

---

*Law Enforcement / Authorized Security Assessment Use Only*
