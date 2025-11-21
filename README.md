# SecureOps-Manager
StealthNet Manager is a CLI tool designed to simplify network security management on Linux systems.
It allows you to:

- Update and clean the entire system
- Enable/disable the UFW firewall
- Set manual or random MAC addresses on all active interfaces
- Authenticate to NordVPN
- Connect, disconnect, and manage NordVPN settings (killswitch, DNS, autoconnect)
- Check the current VPN status
- Manage all features from an interactive terminal menu

------------------------------------------------------------------------

## Requirements and Installation

This program works on Debian and its derivatives (Kali Linux, Ubuntu,
ParrotOS). It requires the installation of UFW (firewall) and NordVPN.

------------------------------------------------------------------------

## UFW Installation

``` bash
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

## Important Notes

To correctly run the main script, use:

``` bash
chmod +x Security.py
sudo python3 Security.py
```

The program requires elevated privileges for:

-   UFW firewall management
-   MAC address modification
-   system updates
-   NordVPN management

------------------------------------------------------------------------

## End
