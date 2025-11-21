import subprocess  # Module to execute system commands
import random      # Module to generate random values

# New fixed MAC address to apply to interfaces (option 2)
NEW_MAC = "24:ab:6c:34:52:da"


def get_active_interfaces():
    """
    Gets the list of active network interfaces (state UP),
    excluding loopback (lo).
    """
    # Executes "ip -o link show up" and takes the output as text
    output = subprocess.check_output(
        ["ip", "-o", "link", "show", "up"], text=True
    )

    interfaces = []

    # Parses each line of the output
    for line in output.splitlines():
        # Typical format: "2: eth0: <...>"
        parts = line.split(":")
        if len(parts) >= 2:
            name = parts[1].strip()  # The interface name is in the second part

            if name == "lo":
                continue  # Excludes loopback

            interfaces.append(name)

    return interfaces


def update_system():
    """
    Performs complete system update:
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

    print("\n>>> Starting full system update procedure...\n")

    for cmd in commands:
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing: {' '.join(cmd)}")
            print(f"Error details: {e}")
            break

    print("\n>>> Update completed.\n")


def change_mac_all():
    """Asks the user for a MAC and applies it to all active interfaces."""
    try:
        interfaces = get_active_interfaces()
    except subprocess.CalledProcessError as e:
        print(f"Unable to read interfaces: {e}")
        return

    if not interfaces:
        print("No active interfaces found (excluding lo).")
        return

    print("Active interfaces found:", ", ".join(interfaces))

    # Request MAC from user
    new_mac = input("\nEnter the MAC to apply (format xx:xx:xx:xx:xx:xx): ").strip()

    print(f"\nSetting MAC {new_mac} on all interfaces...\n")

    for iface in interfaces:
        # Reads current MAC
        try:
            output = subprocess.check_output(
                ["cat", f"/sys/class/net/{iface}/address"], text=True
            ).strip()
            current_mac = output
        except Exception:
            current_mac = "Unknown"

        print(f"\n>>> Interface {iface}:")
        print(f"    Current MAC: {current_mac}")
        print(f"    New MAC:     {new_mac}")
        print(f">>> Changing MAC of {iface} from {current_mac} to {new_mac}")

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
    Generates a random MAC address in the format xx:xx:xx:xx:xx:xx
    Sets the first byte as a local unicast address (e.g. 0x02).
    """
    first_byte = 0x02  # "local admin" bit active, "multicast" bit off
    other_bytes = [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join([f"{first_byte:02x}"] + [f"{b:02x}" for b in other_bytes])


def change_mac_random_all():
    """
    Changes MAC address on all active interfaces using
    a different random MAC for each interface.
    """
    try:
        interfaces = get_active_interfaces()
    except subprocess.CalledProcessError as e:
        print(f"Unable to read interfaces: {e}")
        return

    if not interfaces:
        print("No active interfaces found (excluding lo).")
        return

    print("Active interfaces found:", ", ".join(interfaces))
    print("Applying a RANDOM MAC to each interface...\n")

    for iface in interfaces:
        new_mac = generate_random_mac()

        try:
            output = subprocess.check_output(
                ["cat", f"/sys/class/net/{iface}/address"], text=True
            ).strip()
            current_mac = output
        except Exception:
            current_mac = "Unknown"

        print(f"\n>>> Interface {iface}:")
        print(f"    Current MAC: {current_mac}")
        print(f"    New MAC:     {new_mac}")
        print(f">>> Changing MAC of {iface} from {current_mac} to {new_mac}")

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

    print("\nOperation completed with random MACs.")


def enable_firewall():
    """Enables UFW firewall and shows status."""
    print("\n>>> Enabling UFW firewall...\n")

    try:
        subprocess.run(["sudo", "ufw", "enable"], check=True)
    except subprocess.CalledProcessError:
        print("Error during firewall activation.")
        return

    try:
        subprocess.run(["sudo", "ufw", "status", "verbose"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing firewall status.")

    print("\n>>> Firewall enabled.\n")


def disable_firewall():
    """Disables UFW firewall and shows status."""
    print("\n>>> Disabling UFW firewall...\n")

    try:
        subprocess.run(["sudo", "ufw", "disable"], check=True)
    except subprocess.CalledProcessError:
        print("Error during firewall deactivation.")
        return

    print("\n>>> Firewall status after deactivation:\n")

    try:
        subprocess.run(["sudo", "ufw", "status"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing firewall status.")

    print("\n>>> Firewall disabled.\n")


def nordvpn_auth():
    """Starts NordVPN login procedure."""
    print("\n>>> Starting NordVPN authentication...\n")

    try:
        subprocess.run(["nordvpn", "login"], check=True)
    except subprocess.CalledProcessError:
        print("Error during login procedure.")
        return

    print("\n>>> Authentication completed (if no errors occurred).\n")


def activate_vpn():
    """Starts VPN connection through NordVPN."""
    try:
        subprocess.run(["nordvpn", "connect"])
    except Exception as e:
        print(f"Error during connection: {e}")


def connect_vpn_country():
    """Connects NordVPN to a country chosen by the user."""
    print("\n>>> NordVPN connection with country selection...\n")

    country = input("Enter the country (e.g. Italy, France, Germany): ").strip()

    if not country:
        print("No country entered. Operation canceled.")
        return

    try:
        subprocess.run(["nordvpn", "connect", country], check=True)
    except subprocess.CalledProcessError:
        print("Error during connection to selected country.")
        return

    print(f"\n>>> Connection started to {country}.\n")


def disconnect_vpn():
    """Disconnects NordVPN and shows current status."""
    print("\n>>> Disconnecting NordVPN...\n")

    try:
        subprocess.run(["nordvpn", "disconnect"], check=True)
    except subprocess.CalledProcessError:
        print("Error during disconnection.")
        return

    print("\n>>> Current VPN status:\n")

    try:
        subprocess.run(["nordvpn", "status"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing VPN status.")

    print("\n>>> VPN disconnected.\n")


def enable_nordvpn_settings():
    """Enables killswitch, DNS, autoconnect + shows status."""
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

    print("\n>>> Current VPN status:\n")
    try:
        subprocess.run(["nordvpn", "status"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing VPN status.")

    print("\n>>> Advanced settings enabled.\n")


def disable_nordvpn_settings():
    """Disables killswitch, resets DNS, disables autoconnect + shows status."""
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

    print("\n>>> Current VPN status:\n")
    try:
        subprocess.run(["nordvpn", "settings"], check=True)
    except subprocess.CalledProcessError:
        print("Error showing VPN status.")

    print("\n>>> Advanced settings disabled.\n")


def menu():
    """Shows a simple terminal menu."""
    while True:
        print("\n===== KALI LINUX MENU =====")
        print("1) System Update")

        print("\n--- Firewall ---")
        print("2) Enable Firewall (UFW)")
        print("3) Disable Firewall (UFW)")

        print("\n--- MAC Address ---")
        print("4) Change MAC address MANUALLY on all active interfaces")
        print("5) Change MAC address RANDOMLY on all active interfaces")

        print("\n--- NordVPN - Authentication and Settings ---")
        print("6) NordVPN Authentication (login)")
        print("7) Enable advanced NordVPN settings (killswitch / DNS / autoconnect)")
        print("8) Disable advanced NordVPN settings (killswitch / DNS / autoconnect)")
        print("9) NordVPN Status")

        print("\n--- NordVPN - Connections ---")
        print("10) Connect VPN (Auto - nordvpn connect)")
        print("11) Connect VPN choosing Country")
        print("12) Disconnect NordVPN")

        print("\n--- EXIT ---")
        print("13) Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            update_system()
        elif choice == "2":
            enable_firewall()
        elif choice == "3":
            disable_firewall()
        elif choice == "4":
            change_mac_all()
        elif choice == "5":
            change_mac_random_all()
        elif choice == "6":
            nordvpn_auth()
        elif choice == "7":
            enable_nordvpn_settings()
        elif choice == "8":
            disable_nordvpn_settings()
        elif choice == "9":
            subprocess.run(["nordvpn", "status"])
        elif choice == "10":
            activate_vpn()
        elif choice == "11":
            connect_vpn_country()
        elif choice == "12":
            disconnect_vpn()
        elif choice == "13":
            print("Exiting...")
            break
        else:
            print("Invalid option!")


# Program entry point
if __name__ == "__main__":
    menu()
