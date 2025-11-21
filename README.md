# README – Requirements and Installation

StealthNet Manager is a CLI tool designed to simplify network security management on Linux systems.
It allows you to:

- Update and clean the entire system
- Enable/disable the UFW firewall
- Set manual or random MAC addresses on all active interfaces
- Authenticate to NordVPN
- Connect, disconnect, and manage NordVPN settings (killswitch, DNS, autoconnect)
- Check the current VPN status
- Manage all features from an interactive terminal menu

This program works on Debian (Kali Linux).
It requires the installation of UFW (firewall) and NordVPN.

------------------------------------------------------------
UFW INSTALLATION
------------------------------------------------------------

sudo apt update
sudo apt install ufw -y

------------------------------------------------------------
NORDVPN INSTALLATION
------------------------------------------------------------

sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)

------------------------------------------------------------
IMPORTANT NOTES
------------------------------------------------------------

To correctly run the main script, use:

chmod +x Security.py
sudo python3 Security.py

------------------------------------------------------------
END
---------------------------------
