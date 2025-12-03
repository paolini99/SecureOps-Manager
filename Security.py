import subprocess  # Module to execute system commands
import random      # Module to generate random values

# New fixed MAC address to apply to interfaces (option 2)
NEW_MAC = "24:ab:6c:34:52:da"


def get_active_interfaces():
    """
    Get the list of active (UP state) network interfaces,
    excluding the loopback interface (lo).
    """
    output = subprocess.check_output(
        ["ip", "-o", "link", "show", "up"], text=True
    )

    interfaces = []

    for line in output.splitlines():
        parts = line.split(":")
        if len(parts) >= 2:
            name = parts[1].strip()

            if name == "lo":
                continue  # Exclude loopback

            interfaces.append(name)

    return interfaces


def system_update():
    """
    Executes a full system update:
    - sudo apt update
    - sudo apt full-upgrade -y
    - sudo apt autoremove
    - sudo apt clean
    """
    commands = [
        ["sudo", "apt", "update"],
        ["sudo", "apt", "full-upgrade", "-y"],
        ["sudo", "apt", "autoremove"],
        ["sudo", "apt", "clean"],
    ]

    print("\n>>> Starting full system update...\n")

    for cmd in commands:
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing: {' '.join(cmd)}")
            print(f"Error details: {e}")
            break

    print("\n>>> Update completed.\n")


def change_mac_all_manual():
    """Ask the user for a MAC address and apply it to all active interfaces."""
    try:
        interfaces = get_active_interfaces()
    except subprocess.CalledProcessError as e:
        print(f"Unable to read interfaces: {e}")
        return

    if not interfaces:
        print("No active interfaces found (excluding lo).")
        return

    print("Active interfaces found:", ", ".join(interfaces))

    new_mac = input("\nEnter the MAC to apply (format xx:xx:xx:xx:xx:xx): ").strip()

    print(f"\nSetting MAC {new_mac} on all interfaces...\n")

    for iface in interfaces:
        try:
            output = subprocess.check_output(
                ["cat", f"/sys/class/net/{iface}/address"], text=True
            ).strip()
            old_mac = output
        except Exception:
            old_mac = "Unknown"

        print(f"\n>>> Interface {iface}:")
        print(f"    Current MAC: {old_mac}")
        print(f"    New MAC:     {new_mac}")
        print(f">>> Changing MAC of {iface} from {old_mac} to {new_mac}")

        commands = [
            ["sudo", "ip", "link", "set", iface, "down"],
            ["sudo", "ip", "link", "set", "dev", iface, "address", new_mac],
            ["sudo", "ip", "link", "set", iface, "up"],
        ]

        for cmd in commands:
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                print(f"Error executing: {' '.join(cmd)} (interface {iface})")
                break

    print("\nOperation completed.")


def generate_random_mac():
    """
    Generate a random MAC address in xx:xx:xx:xx:xx:xx format.
    First byte is set as locally administered (0x02).
    """
    first_byte = 0x02
    other_bytes = [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join([f"{first_byte:02x}"] + [f"{b:02x}" for b in other_bytes])


def change_mac_all_random():
    """Set a different random MAC on each active interface."""
    try:
        interfaces = get_active_interfaces()
    except subprocess.CalledProcessError as e:
        print(f"Unable to read interfaces: {e}")
        return

    if not interfaces:
        print("No active interfaces found (excluding lo).")
        return

    print("Active interfaces found:", ", ".join(interfaces))
    print("Applying RANDOM MAC to each interface...\n")

    for iface in interfaces:
        new_mac = generate_random_mac()

        try:
            output = subprocess.check_output(
                ["cat", f"/sys/class/net/{iface}/address"], text=True
            ).strip()
            old_mac = output
        except Exception:
            old_mac = "Unknown"

        print(f"\n>>> Interface {iface}:")
        print(f"    Current MAC: {old_mac}")
        print(f"    New MAC:     {new_mac}")
        print(f">>> Changing MAC of {iface} from {old_mac} to {new_mac}")

        commands = [
            ["sudo", "ip", "link", "set", iface, "down"],
            ["sudo", "ip", "link", "set", "dev", iface, "address", new_mac],
            ["sudo", "ip", "link", "set", iface, "up"],
        ]

        for cmd in commands:
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                print(f"Error executing: {' '.join(cmd)} (interface {iface})")
                break

    print("\nRandom MAC operation completed.")


def enable_firewall():
    """Enable UFW firewall and show status."""
    print("\n>>> Enabling UFW firewall...\n")
    try:
        subprocess.run(["sudo", "ufw", "enable"], check=True)
    except subprocess.CalledProcessError:
        print("Error enabling firewall.")
        return

    try:
        subprocess.run(["sudo", "ufw", "status", "verbose"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing firewall status.")

    print("\n>>> Firewall enabled.\n")


def disable_firewall():
    """Disable UFW firewall and show status."""
    print("\n>>> Disabling UFW firewall...\n")
    try:
        subprocess.run(["sudo", "ufw", "disable"], check=True)
    except subprocess.CalledProcessError:
        print("Error disabling firewall.")
        return

    print("\n>>> Firewall status after disable:\n")

    try:
        subprocess.run(["sudo", "ufw", "status"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing firewall status.")

    print("\n>>> Firewall disabled.\n")


def firewall_status():
    """Show UFW firewall status."""
    print("\n>>> UFW firewall status...\n")
    try:
        subprocess.run(["sudo", "ufw", "status"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing firewall status.")
    print("\n>>> End firewall status.\n")


def set_firewall_rules():
    """
    Apply UFW rules:
    - default deny incoming
    - default allow outgoing
    - enable logging
    - allow lo
    - allow DNS only on nordlynx interface
    - block all other DNS requests
    """
    print("\n>>> Setting UFW firewall rules...\n")

    commands = [
        ["sudo", "ufw", "default", "deny", "incoming"],
        ["sudo", "ufw", "default", "allow", "outgoing"],
        ["sudo", "ufw", "logging", "on"],
        ["sudo", "ufw", "allow", "in", "on", "lo"],
        ["sudo", "ufw", "allow", "out", "on", "nordlynx"],
        ["sudo", "ufw", "allow", "out", "on", "nordlynx", "to", "103.86.96.100", "port", "53", "proto", "udp"],
        ["sudo", "ufw", "allow", "out", "on", "nordlynx", "to", "103.86.99.100", "port", "53", "proto", "udp"],
        ["sudo", "ufw", "allow", "out", "on", "nordlynx", "to", "103.86.96.100", "port", "53", "proto", "tcp"],
        ["sudo", "ufw", "allow", "out", "on", "nordlynx", "to", "103.86.99.100", "port", "53", "proto", "tcp"],
        ["sudo", "ufw", "deny", "out", "to", "any", "port", "53", "proto", "udp"],
        ["sudo", "ufw", "deny", "out", "to", "any", "port", "53", "proto", "tcp"],
    ]

    for cmd in commands:
        try:
            print("Executing:", " ".join(cmd))
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("Error executing:", " ".join(cmd))
            break

    print("\n>>> Firewall rules applied.\n")


def is_firewall_active():
    """Return True if UFW firewall is active, otherwise False."""
    try:
        output = subprocess.check_output(["sudo", "ufw", "status"], text=True)
        return "Status: active" in output or "Status: Active" in output
    except subprocess.CalledProcessError:
        print("Unable to determine firewall status.")
        return False


def run_vpn_with_firewall_handling(vpn_action):
    """
    If firewall is active:
      - disable it manually
      - run VPN action
      - if successful, re-enable firewall
    """
    active_before = is_firewall_active()

    if active_before:
        print("\n[VPN] Firewall active → disabling temporarily...\n")
        try:
            subprocess.run(["sudo", "ufw", "disable"], check=False)
            print("[VPN] Firewall disabled.\n")
        except Exception as e:
            print(f"[VPN] Error disabling firewall: {e}")
            return False

    success = vpn_action()

    if active_before:
        if success:
            print("[VPN] Operation successful → re-enabling firewall...\n")
            try:
                subprocess.run(["sudo", "ufw", "enable"], check=False)
                print("[VPN] Firewall re-enabled.\n")
            except Exception as e:
                print(f"[VPN] Error re-enabling firewall: {e}")
        else:
            print("[VPN] Operation failed → firewall NOT re-enabled automatically.\n")

    return success


def nordvpn_login():
    """Start NordVPN login procedure."""
    print("\n>>> Starting NordVPN login...\n")

    try:
        subprocess.run(["nordvpn", "login"], check=True)
    except subprocess.CalledProcessError:
        print("Error during login.")
        return False

    print("\n>>> Login completed (if no errors occurred).\n")
    return True


def vpn_connect():
    """Connect NordVPN."""
    try:
        result = subprocess.run(["nordvpn", "connect"])
        if result.returncode != 0:
            print("Error connecting.")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

    print("\n>>> VPN connection started.\n")
    return True


def connect_vpn_country():
    """Connect NordVPN to a selected country."""
    print("\n>>> NordVPN connection with country selection...\n")

    country = input("Enter country (e.g., Italy, France, Germany): ").strip()

    if not country:
        print("No country entered. Operation cancelled.")
        return False

    try:
        subprocess.run(["nordvpn", "connect", country], check=True)
    except subprocess.CalledProcessError:
        print("Error connecting to selected country.")
        return False

    print(f"\n>>> Connecting to {country}.\n")
    return True


def vpn_disconnect():
    """Disconnect NordVPN and show status."""
    print("\n>>> Disconnecting NordVPN...\n")

    try:
        subprocess.run(["nordvpn", "disconnect"], check=True)
    except subprocess.CalledProcessError:
        print("Error disconnecting.")
        return False

    print("\n>>> Current VPN status:\n")

    try:
        subprocess.run(["nordvpn", "status"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing status.")

    print("\n>>> VPN disconnected.\n")
    return True


def enable_nordvpn_settings():
    """Enable killswitch, DNS, autoconnect."""
    print("\n>>> Enabling advanced NordVPN settings...\n")

    commands = [
        ["nordvpn", "set", "killswitch", "on"],
        ["nordvpn", "set", "dns", "103.86.96.100", "103.86.99.100"],
        ["nordvpn", "set", "autoconnect", "on"],
    ]

    for cmd in commands:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"Error executing: {' '.join(cmd)}")
            return False

    print("\n>>> Current VPN settings:\n")
    try:
        subprocess.run(["nordvpn", "status"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing status.")

    print("\n>>> Advanced settings enabled.\n")
    return True


def disable_nordvpn_settings():
    """Disable killswitch, reset DNS, disable autoconnect."""
    print("\n>>> Disabling advanced NordVPN settings...\n")

    commands = [
        ["nordvpn", "set", "killswitch", "off"],
        ["nordvpn", "set", "dns", "0"],
        ["nordvpn", "set", "autoconnect", "off"],
    ]

    for cmd in commands:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"Error executing: {' '.join(cmd)}")
            return False

    print("\n>>> Current VPN settings:\n")
    try:
        subprocess.run(["nordvpn", "settings"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing settings.")

    print("\n>>> Advanced settings disabled.\n")
    return True


def enable_apparmor():
    """Enable and start AppArmor."""
    print("\n>>> Enabling and starting AppArmor...\n")
    try:
        subprocess.run(["sudo", "systemctl", "enable", "--now", "apparmor"], check=True)
        print("\n>>> AppArmor enabled and started.\n")
    except subprocess.CalledProcessError:
        print("Error enabling/starting AppArmor.")


def disable_apparmor():
    """Disable and stop AppArmor."""
    print("\n>>> Disabling and stopping AppArmor...\n")
    try:
        subprocess.run(["sudo", "systemctl", "disable", "--now", "apparmor"], check=True)
        print("\n>>> AppArmor disabled and stopped.\n")
    except subprocess.CalledProcessError:
        print("Error disabling/stopping AppArmor.")


def apply_additional_security():
    """Disable IPv6 temporarily using sysctl (until reboot)."""
    print("\n>>> Applying additional security settings (disabling IPv6)...\n")

    commands = [
        ["sudo", "sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=1"],
        ["sudo", "sysctl", "-w", "net.ipv6.conf.default.disable_ipv6=1"],
        ["sudo", "sysctl", "-w", "net.ipv6.conf.lo.disable_ipv6=1"],
    ]

    for cmd in commands:
        try:
            print("Executing:", " ".join(cmd))
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("Error executing:", " ".join(cmd))
            print("Stopped: IPv6 may not be fully disabled.")
            return

    print("\n>>> IPv6 disabled (until reboot).")


def restore_security_settings():
    """Re-enable IPv6 by restoring sysctl settings."""
    print("\n>>> Restoring security settings (re-enabling IPv6)...\n")

    commands = [
        ["sudo", "sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=0"],
        ["sudo", "sysctl", "-w", "net.ipv6.conf.default.disable_ipv6=0"],
        ["sudo", "sysctl", "-w", "net.ipv6.conf.lo.disable_ipv6=0"],
    ]

    for cmd in commands:
        try:
            print("Executing:", " ".join(cmd))
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("Error executing:", " ".join(cmd))
            print("Stopped: IPv6 may not have been fully restored.")
            return

    print("\n>>> IPv6 restored.\n")


def menu():
    """Show a simple terminal menu."""
    while True:
        print("\n===== KALI LINUX MENU =====")
        print("1) System Update")

        print("\n--- Firewall ---")
        print("2) Enable Firewall (UFW)")
        print("3) Disable Firewall (UFW)")
        print("4) Firewall Status (UFW)")
        print("5) Apply Firewall Rules (UFW)")

        print("\n--- MAC Address ---")
        print("6) Change MAC Address MANUALLY on all active interfaces")
        print("7) Change MAC Address RANDOMLY on all active interfaces")

        print("\n--- NordVPN - Authentication & Settings ---")
        print("8) NordVPN Login")
        print("9) Enable Advanced NordVPN Settings (killswitch / DNS / autoconnect)")
        print("10) Disable Advanced NordVPN Settings")
        print("11) NordVPN Status")

        print("\n--- NordVPN - Connections ---")
        print("12) Connect VPN (Auto)")
        print("13) Connect VPN by Country")
        print("14) Disconnect VPN")

        print("\n--- AppArmor ---")
        print("15) Enable AppArmor")
        print("16) Disable AppArmor")

        print("\n--- Additional Security Options ---")
        print("17) Apply Additional Security (disable IPv6)")
        print("18) Restore Security Settings (enable IPv6)")

        print("\n--- EXIT ---")
        print("19) Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            system_update()
        elif choice == "2":
            enable_firewall()
        elif choice == "3":
            disable_firewall()
        elif choice == "4":
            firewall_status()
        elif choice == "5":
            set_firewall_rules()
        elif choice == "6":
            change_mac_all_manual()
        elif choice == "7":
            change_mac_all_random()
        elif choice == "8":
            run_vpn_with_firewall_handling(nordvpn_login)
        elif choice == "9":
            run_vpn_with_firewall_handling(enable_nordvpn_settings)
        elif choice == "10":
            run_vpn_with_firewall_handling(disable_nordvpn_settings)
        elif choice == "11":
            run_vpn_with_firewall_handling(
                lambda: (subprocess.run(["nordvpn", "status"]).returncode == 0)
            )
        elif choice == "12":
            run_vpn_with_firewall_handling(vpn_connect)
        elif choice == "13":
            run_vpn_with_firewall_handling(connect_vpn_country)
        elif choice == "14":
            run_vpn_with_firewall_handling(vpn_disconnect)
        elif choice == "15":
            enable_apparmor()
        elif choice == "16":
            disable_apparmor()
        elif choice == "17":
            apply_additional_security()
        elif choice == "18":
            restore_security_settings()
        elif choice == "19":
            print("Exiting...")
            break


if __name__ == "__main__":
    menu()


