# SecureOps-Manager

SecureOps-Manager is a CLI tool designed to simplify network security and privacy management on Linux systems.  
It allows you to:

- Update and clean the entire system  
- Enable, disable, or check the status of the UFW firewall  
- Apply a full hardened UFW ruleset (including DNS leak protection for NordVPN)  
- Set manual or random MAC addresses on all active interfaces  
- Authenticate to NordVPN  
- Connect, disconnect, and choose a specific country for VPN connections  
- Enable or disable NordVPN advanced settings (killswitch, DNS, autoconnect)  
- Automatically manage UFW during VPN operations to prevent conflicts  
- Check NordVPN current status  
- Enable or disable AppArmor  
- Temporarily disable IPv6 for privacy and restore it when needed  
- Manage all features through an interactive terminal menu  

---

## Requirements and Installation

This program works on Debian-based systems (tested on Kali Linux).  
It requires:

- UFW (firewall)  
- NordVPN Linux client  
- Python 3  
- AppArmor (optional but supported)  

---

## UFW Installation

```bash
sudo apt update
sudo apt install ufw -y
```

------------------------------------------------------------------------

## NordVPN Installation

Download the official script:

``` bash
sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)
```

------------------------------------------------------------------------

## AppArmor Installation

To install AppArmor and its user-space tools, run:

``` bash
sudo apt update
sudo apt install apparmor apparmor-utils -y
```

------------------------------------------------------------------------

## Important Notes

To correctly run the main script, use:

``` bash
chmod +x Security.py
sudo python3 Security.py
```

The program requires elevated privileges for:

- UFW firewall management
-MAC address modification
-System updates
-NordVPN configuration and connection management
-IPv6 hardening
-AppArmor management

------------------------------------------------------------------------

## End
