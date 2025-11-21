# Requirements and Installation

This program works on Debian and its derivatives (Kali Linux, Ubuntu,
ParrotOS). It requires the installation of UFW (firewall) and NordVPN.

------------------------------------------------------------------------

## UFW Installation

``` bash
sudo apt update
sudo apt install ufw -y
```

Enable the firewall (optional):

``` bash
sudo ufw enable
sudo ufw status
```

------------------------------------------------------------------------

## NordVPN Installation

Download the official script:

``` bash
wget https://downloads.nordcdn.com/apps/linux/install.sh
```

Make the script executable:

``` bash
chmod +x install.sh
```

Install NordVPN:

``` bash
sudo ./install.sh
```

Enable and start the service:

``` bash
sudo systemctl enable nordvpnd
sudo systemctl start nordvpnd
```

Log in to your account:

``` bash
nordvpn login
```

------------------------------------------------------------------------

## Important Notes

To correctly run the main script, use:

``` bash
sudo python3 script_name.py
```

The program requires elevated privileges for:

-   UFW firewall management
-   MAC address modification
-   system updates
-   NordVPN management

------------------------------------------------------------------------

## End
