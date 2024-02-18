"""
Infiltra - Open-Source CLI Penetration Testing Tool To Automate Various Processes

This script is designed for automating various network and security tasks.
It integrates multiple tools and utilities to facilitate domain analysis, network scanning, vulnerability
assessment, and more. Key features include:

- WHOIS lookups and parsing: Automates the process of gathering and interpreting WHOIS data.
- ICMP Echo: Implements ping requests to identify live hosts in a network.
- OSINT and Black Box OSINT: Integrates tools like AORT and DNS Recon for open-source intelligence gathering.
- BBOT: Utilizes the black-box testing tool for detailed domain and network analysis.
- NMAP Scans: Offers functionalities to perform comprehensive port and service scanning.
- SSLScan and Parsing: Facilitates scanning for SSL vulnerabilities and interpreting the results.
- Nikto Web Scans: Implements Nikto for scanning web servers for potential security issues.
- Additional Utilities: Includes features for update checking, vulnerability scanning, and more.

The script provides a user-friendly command-line interface for easy navigation and execution of various tasks.

Author: @jivy26
GitHub: https://github.com/jivy26/infiltra
"""

import os
import re
import subprocess
import sys

from colorama import init, Fore, Style

from infiltra.bbot.bbot_parse import bbot_main
from infiltra.bbot.check_bbot import is_bbot_installed, install_bbot
from infiltra.icmpecho import run_fping
from infiltra.nuclei import nuclei_main
from infiltra.project_handler import project_submenu, last_project_file_path
from infiltra.updater import check_and_update
from infiltra.utils import is_valid_ip, is_valid_hostname, get_version, get_ascii_art
from infiltra.website_enum.feroxbuster import main as run_feroxbuster

# Moved from ANSI to Colorama
# Initialize Colorama
init(autoreset=True)


# Define colors using Colorama
DEFAULT_COLOR = Fore.WHITE
IT_MAG = Fore.MAGENTA + Style.BRIGHT
BOLD_BLUE = Fore.BLUE + Style.BRIGHT
BOLD_CYAN = Fore.CYAN + Style.BRIGHT
BOLD_GREEN = Fore.GREEN + Style.BRIGHT
BOLD_RED = Fore.RED + Style.BRIGHT
BOLD_MAG = Fore.MAGENTA + Style.BRIGHT
BOLD_YELLOW = Fore.YELLOW + Style.BRIGHT
BOLD_WHITE = Fore.WHITE + Style.BRIGHT

# Utility Functions, Need to integrate into utils.py

def list_txt_files(directory):
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not txt_files:
        print(f"{BOLD_RED}No .txt files found in the current directory.")
        return None
    return txt_files

def read_file_lines(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"{BOLD_RED}File not found: {filepath}")
        return None

def write_to_file(filepath, content, mode='w'):
    try:
        with open(filepath, mode) as file:
            file.write(content)
    except IOError as e:
        print(f"{BOLD_RED}IO error occurred: {e}")

def run_subprocess(command, working_directory=None, shell=False):
    try:
        result = subprocess.run(command, cwd=working_directory, shell=shell,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{BOLD_RED}Subprocess error: {e.stderr}")
        return None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# End utils

# AORT Integration
def run_aort(domain):
    clear_screen()

    # Module Info Box
    message_lines = [
        "This module will look use AORT and DNSRecon",
        "to enumerate DNS information"
    ]

    # Determine the width of the box based on the longest message line
    width = max(len(line) for line in message_lines) + 4  # padding for the sides of the box

    # Print the top border of the box
    print("+" + "-" * (width - 2) + "+")

    # Print each line of the message, centered within the box
    for line in message_lines:
        print("| " + line.center(width - 4) + " |")

    # Print the bottom border of the box
    print("+" + "-" * (width - 2) + "+")
    # End Module Info Box

    print(f"{BOLD_CYAN}Running AORT for domain: {BOLD_GREEN}{domain}\n")

    script_directory = os.path.dirname(os.path.realpath(__file__))
    aort_script_path = os.path.join(script_directory, 'aort/AORT.py')
    aort_command = f"python3 {aort_script_path} -d {domain} -a -w -n --output aort_dns.txt"

    print(f"{BOLD_BLUE}AORT is starting, subdomains will be saved to aort_dns.txt.\n")

    try:
        # Call AORT and let it handle the output directly
        os.system(aort_command)
    except Exception as e:
        print(f"{BOLD_RED}An error occurred while running AORT: {e}")

    input(f"\n{BOLD_GREEN}Press Enter to return to proceed with DNSRecon...")


def run_bbot(domain, display_menu, project_path):
    # Make sure the domain is valid before proceeding
    if not is_valid_domain(domain):
        print(f"{BOLD_RED}Invalid domain provided: {domain}")
        return

    # Check if bbot is installed
    if not is_bbot_installed():
        print(f"{BOLD_YELLOW}bbot is not installed, installing now...")
        install_bbot()

    # Clear the screen and display sample commands
    clear_screen()
    print(f"{BOLD_CYAN}Select the bbot command to run:")
    print(f"{BOLD_YELLOW}All output is saved to the bbot/ folder\n")
    print(f"1. Enumerate Subdomains")
    print(f"2. Subdomains, Port Scans, and Web Screenshots")
    print(f"3. Subdomains and Basic Web Scan")
    print(f"4. Full Enumeration {BOLD_YELLOW}--- Enumerates subdomains, emails, cloud buckets, port scan with nmap, basic web scan, nuclei scan, and web screenshots")

    # Define bbot commands
    commands = {
        '1': "-f subdomain-enum",
        '2': "-f subdomain-enum -m nmap gowitness",
        '3': "-f subdomain-enum web-basic",
        '4': "-f subdomain-enum email-enum cloud-enum web-basic -m nmap gowitness nuclei --allow-deadly",
    }

    choice = input(f"{BOLD_GREEN}Enter your choice (1-4): ").strip()

    if choice in commands:
        command = commands[choice]
        bbot_command = f"echo -ne \"\\033]0;BBOT\\007\"; exec bbot -t {domain} {command} -o . --name bbot"
        full_command = ['gnome-terminal', '--', 'bash', '-c', bbot_command]

        # Change directory to the project path
        os.chdir(project_path)

        # Print the command being executed for the user's reference
        print(f"{BOLD_YELLOW}Executing: {full_command}")

        # Run the bbot command
        subprocess.Popen(full_command)
        # exit_status = os.system(full_command)
        #
        # # Check exit status
        # if exit_status != 0:
        #     print(f"{BOLD_RED}bbot command failed with exit status {exit_status}")
    else:
        print(f"{BOLD_RED}Invalid choice, please enter a number from 1 to 4.")

    # Wait for the user to acknowledge before returning to the menu
    input(f"{BOLD_GREEN}Press Enter to return to the menu...")
    display_menu(get_version(), project_path, ascii_art=None)


# DNSRecon Integration
def run_dnsrecon(domain):
    clear_screen()
    print(f"{BOLD_CYAN}Running DNSRecon for domain: {BOLD_GREEN}{domain}\n")

    dnsrecon_command = f"dnsrecon -d {domain} -t std"

    print(f"{BOLD_BLUE}DNSRecon is starting, results will be saved to dnsrecon_results.json.\n")

    try:
        # Call DNSRecon and let it handle the output directly
        os.system(dnsrecon_command)
    except Exception as e:
        print(f"{BOLD_RED}An error occurred while running DNSRecon: {e}")

    input(f"\n{BOLD_GREEN}Press Enter to return to the menu...")


# Function to check if dnsrecon is installed
def is_dnsrecon_installed():
    try:
        subprocess.run(["dnsrecon", "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Nikto Integration

def run_nikto(targets):
    clear_screen()
    nikto_dir = 'nikto'
    os.makedirs(nikto_dir, exist_ok=True)  # Create the nikto directory if it doesn't exist
    hosts = targets
    # Check if the input is a file or a single host
    if os.path.isfile(targets):
        hosts = read_file_lines(targets)
    elif is_valid_ip(targets) or is_valid_hostname(targets):
        hosts = [targets]  # If it's a single host, put it in a list
    else:
        print(f"{BOLD_RED}Invalid target: {targets} is not a valid IP, hostname, or file.")
        return

    for host in hosts:
        output_filename = f"nikto_{host.replace(':', '_').replace('/', '_')}.txt"  # Replace special characters
        output_path = os.path.join(nikto_dir, output_filename)

        print(f"{BOLD_CYAN}Running Nikto for {host} in a new window.")
        nikto_command = f"nikto -h {host} -C all -Tuning 13 -o {output_path} -Format txt"

        # Open a new terminal window to run Nikto
        terminal_command = ['x-terminal-emulator', '-e', f'sudo {nikto_command}']
        subprocess.Popen(terminal_command)

    print(f"{BOLD_GREEN}Nikto scans launched in separate windows.")
    input(f"\n{BOLD_GREEN}Press Enter to return to the menu...")


# Handle FPING
def check_alive_hosts():
    clear_screen()

    # List .txt files in the current directory
    txt_files = list_txt_files(os.getcwd())
    if txt_files:
        print(f"{BOLD_GREEN}ICMP Echo and Parser\n")
        print(f"{BOLD_CYAN}Available .txt Files In This Project's Folder\n")
        for idx, file in enumerate(txt_files, start=1):
            print(f"{BOLD_GREEN}{idx}. {BOLD_WHITE}{file}")

    # Prompt the user for an IP address or a file number
    selection = input(f"\n{BOLD_GREEN}Enter a number to select a file, or input a single IP address: {BOLD_WHITE}").strip()

    # If user enters a digit within the range of listed files, select the file
    if selection.isdigit() and 1 <= int(selection) <= len(txt_files):
        file_selected = txt_files[int(selection) - 1]
        hosts_input = os.path.join(os.getcwd(), file_selected)
    elif is_valid_ip(selection):
        hosts_input = selection
    else:
        print(f"{BOLD_RED}Invalid input. Please enter a valid IP address or selection number.")
        return

    # If it's a file, read IPs from it; if it's a single IP, create a list with it
    if os.path.isfile(hosts_input):
        hosts = read_file_lines(hosts_input)
    else:
        hosts = [hosts_input]

    # Run fping with the list of IPs
    clear_screen()
    print(f"\n{BOLD_CYAN}Running FPING\n")
    alive_hosts = run_fping(hosts)
    print(f"\n{BOLD_GREEN}Alive Hosts:")
    for host in alive_hosts:
        print(f"{BOLD_YELLOW}{host}")

    input(f"\n{BOLD_GREEN}Press Enter to return to the menu...")


# Function to run EyeWitness
def run_eyewitness(domain):
    clear_screen()
    script_directory = os.path.dirname(os.path.realpath(__file__))
    eyewitness_script_path = os.path.join(script_directory, 'eyewitness.py')

    # Set default file path
    default_file = 'aort_dns.txt'

    # Prompt user for input
    print(
        f"\n{BOLD_CYAN}If you provide a domain, it will enumerate subdomains and attempt to screenshot them after enumeration.")
    user_input = input(
        f"\n{BOLD_GREEN}Enter a single IP, domain, or path to a file with domains (leave blank to use default aort_dns.txt from nmap_grep): ").strip()

    # Determine which file or IP to use
    if user_input:
        input_file = user_input  # Use the user-provided file or IP
    else:
        input_file = default_file

    # Inform the user which input will be used
    if os.path.isfile(input_file):
        print(f"Using file: {input_file}")
    else:
        print(f"Using IP/domain: {input_file}")

    # Run the EyeWitness Python script
    subprocess.run(['python3', eyewitness_script_path, input_file])

    input(
        f"{BOLD_GREEN}Press Enter to return to the menu...")  # Allow users to see the message before returning to the menu


# Function to run sslscan and parse results
# Function to run sslscan and parse results
def run_sslscanparse():
    clear_screen()
    sslscan_script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sslscanparse.py')

    # List the available .txt files
    txt_files = list_txt_files(os.getcwd())
    if txt_files:
        print(f"{BOLD_GREEN}SSLScanner and Parser\n")
        print(f"{BOLD_CYAN}Available .txt Files In This Project's Folder\n")
        for idx, file in enumerate(txt_files, start=1):
            print(f"{BOLD_GREEN}{idx}. {BOLD_WHITE}{file}")

    # Prompt for input: either a file number or a custom file path
    selection = input(f"{BOLD_GREEN}\nEnter a number to select a file, or input a custom file path: {BOLD_WHITE}").strip()

    # Check if the input is a digit and within the range of listed files
    if selection.isdigit() and 1 <= int(selection) <= len(txt_files):
        input_file = os.path.join(os.getcwd(), txt_files[int(selection) - 1])  # Use the selected file
    else:
        input_file = selection  # Assume the entered string is a custom file path

    # Validate that the file exists
    if not os.path.isfile(input_file):
        print(f"{BOLD_RED}File does not exist: {input_file}")
        return

    # Run the sslscanparse script
    clear_screen()
    print(f"\n{BOLD_GREEN}Running sslscanparse.py on {input_file}")
    with subprocess.Popen(['python3', sslscan_script_path, input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        try:
            # Output each line as it's generated
            for line in process.stdout:
                print(line, end='')  # stdout is already newline-terminated
            process.wait()
            # After the process ends, check for any remaining stderr output
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"{BOLD_RED}Error:\n{stderr_output}")
        except Exception as e:
            print(f"{BOLD_RED}An error occurred: {e}")

    input(f"\n\n{BOLD_BLUE}Press Enter to return to the menu....")


# Function to run whois script
def run_whois():
    clear_screen()
    whois_script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'whois_script.sh')

    txt_files = list_txt_files(os.getcwd())
    if txt_files:
        print(f"{BOLD_GREEN}WHOIS Scan and Parse\n")
        print(f"\n{BOLD_CYAN}Available .txt Files In This Project's Folder\n")
        for idx, file in enumerate(txt_files, start=1):
            print(f"{BOLD_GREEN}{idx}. {BOLD_WHITE}{file}")

    ip_input = input(f"\n{BOLD_GREEN}Enter a number to select a file, or input a single IP address: {BOLD_WHITE}").strip()

    if ip_input.isdigit() and 1 <= int(ip_input) <= len(txt_files):
        ip_input = txt_files[int(ip_input) - 1]  # If user selects a file, use its name as input
    elif not (is_valid_ip(ip_input) or ip_input.isdigit()):
        print(f"{BOLD_RED}Invalid input. Please enter a valid IP address or selection number.")
        return

    # Proceed with running the script using ip_input as either a filename or a single IP
    clear_screen()
    print(f"\n{BOLD_GREEN}Running WHOIS and Parsing results on {ip_input}\n")
    stdout = run_subprocess(['bash', whois_script_path, ip_input])
    print(stdout)
    input(f"{BOLD_GREEN}Press any key to return to the menu...")


def run_ngrep(scan_type):
    clear_screen()
    script_directory = os.path.dirname(os.path.realpath(__file__))
    ngrep_script_path = os.path.join(script_directory, 'nmap-grep.sh')
    output_file = f"{scan_type.lower()}.txt"  # Assume the output file is named tcp.txt or udp.txt based on the scan_type
    output_path = f"{scan_type.lower()}_parsed/"  # Assume the output folder is named tcp_parsed/ or udp_parsed/ based on the scan_type

    # Check if the output directory already exists
    if os.path.isdir(output_path):
        overwrite = input(f"The directory {output_path} already exists. Overwrite it? (y/n): ").strip().lower()
        if overwrite == 'y':
            subprocess.run(['rm', '-rf', output_path])  # Removes the directory recursively
        else:
            print(f"Not overwriting the existing directory {output_path}.")
            return  # Exit the function if the user does not want to overwrite

    # Continue with running the nmap-grep.sh script
    print(f"{BOLD_GREEN}Running nmap-grep.sh on {output_file} for {scan_type.upper()} scans")
    subprocess.run(['bash', ngrep_script_path, output_file, scan_type.upper()])
    input(
        f"{BOLD_GREEN}Press Enter to return to the menu...")  # Allow users to see the message before returning to the menu

### Start Menu
# Function to run nmap scan
def run_nmap():
    clear_screen()

    # List the available .txt files
    txt_files = list_txt_files(os.getcwd())
    if txt_files:
        print(f"{BOLD_GREEN}NMAP Scanner\n")
        print(f"{BOLD_CYAN}Available .txt Files In This Project's Folder\n")
        for idx, file in enumerate(txt_files, start=1):
            print(f"{BOLD_GREEN}{idx}. {BOLD_WHITE}{file}")

    # Prompt for input: either a file number, a single IP, or 'x' to cancel
    selection = input(
        f"{BOLD_GREEN}\nEnter a number to select a file, input a single IP address: {BOLD_WHITE}").strip()

    # Check if the input is a digit and within the range of listed files
    if selection.isdigit() and 1 <= int(selection) <= len(txt_files):
        ip_input = txt_files[int(selection) - 1]  # Use the selected file
    elif is_valid_ip(selection) or is_valid_domain(selection):
        ip_input = selection  # Use the entered IP or domain
    else:
        print(f"{BOLD_RED}Invalid input. Please enter a valid IP address, domain, or selection number.")
        return

    # Ask for the type of scan
    clear_screen()
    print(f"{BOLD_GREEN}NMAP Scanner\n")
    print(f"{BOLD_MAG}NMAP Scans will launch in a separate terminal")
    print(f"{BOLD_CYAN}TCP: {BOLD_WHITE}nmap -sSV --top-ports 4000 -Pn ")
    print(f"{BOLD_CYAN}UDP: {BOLD_WHITE}nmap -sU --top-ports 400 -Pn ")
    scan_type = input(f"\n{BOLD_GREEN}Enter scan type (tcp/udp/both): ").lower()

    # Validate scan_type
    if scan_type not in ['tcp', 'udp', 'both']:
        print(f"{BOLD_RED}Invalid scan type: {scan_type}. Please enter 'tcp', 'udp', or 'both'.")
        return

    # Run the nmap scan using the selected file or entered IP/domain
    nmap_script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nmap_scan.py')
    if scan_type in ['tcp', 'both']:
        tcp_command_string = f"echo -ne \"\\033]0;NMAP TCP\\007\"; exec sudo python3 {nmap_script_path} {ip_input} tcp"
        tcp_command = ['gnome-terminal', '--', 'bash', '-c', tcp_command_string]
        subprocess.Popen(tcp_command)
    if scan_type in ['udp', 'both']:
        udp_command_string = f"echo -ne \"\\033]0;NMAP UDP\\007\"; exec sudo python3 {nmap_script_path} {ip_input} udp"
        udp_command = ['gnome-terminal', '--', 'bash', '-c', udp_command_string]
        subprocess.Popen(udp_command)

    print(f"\n{BOLD_GREEN}Nmap {scan_type} scans launched.")
    input(f"{BOLD_GREEN}Press Enter to return to the menu...")


# OSINT Sub menu
def is_valid_domain(domain):
    # Basic pattern for validating a standard domain name
    pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"
    return re.match(pattern, domain) is not None

def osint_submenu(project_path):
    clear_screen()
    domain = ''
    osint_domain_file = 'osint_domain.txt'  # File to store the domain

    # Check if osint_domain.txt exists and read the domain from it
    domain_lines = read_file_lines(osint_domain_file)
    if domain_lines:
        domain = domain_lines[0].strip()

    while True:
        clear_screen()
        print(f"{BOLD_CYAN}OSINT Menu: {domain}:\n")
        menu_options = [
            ("1. Set Domain", f"{DEFAULT_COLOR}Define the domain to be used for OSINT."),
            ("2. Run AORT and DNSRecon", f"{DEFAULT_COLOR}Enumerate DNS information."),
            ("3. Run BBOT", f"{DEFAULT_COLOR}Black-box testing for domain and network analysis."),
            ("4. Parse BBOT Results", f"{DEFAULT_COLOR}Interpret the output from BBOT."),
            ("5. Run EyeWitness", f"{DEFAULT_COLOR}Visual inspection tool for web domains.")
        ]

        for option, description in menu_options:
            print(f"{BOLD_GREEN}{option.ljust(50)}{description}")

        print(f"\n{BOLD_CYAN}Utilities:")
        print(f"{BOLD_RED}X. Return to Main Menu".ljust(50) + f"\n")

        choice = input(f"\n{BOLD_GREEN}Enter your choice: ").lower()

        if choice == '1':
            domain_input = input(f"{BOLD_CYAN}Please Input the Domain (i.e. google.com): ").strip()
            if is_valid_domain(domain_input):
                domain = domain_input
                print(f"{BOLD_GREEN}Domain set to: {domain}")
                write_to_file(osint_domain_file, domain)
            else:
                print(f"{BOLD_RED}Invalid domain name. Please enter a valid domain.")
            input(f"{BOLD_CYAN}Press Enter to continue...")
        elif choice == '2':
            if domain:
                run_aort(domain)
                if is_dnsrecon_installed():
                    run_dnsrecon(domain)
                else:
                    print(f"{BOLD_RED}DNSRecon is not installed. Please install it to use this feature.")
            else:
                print(f"{BOLD_RED}Please set a domain first using option 1.")
            input(f"{BOLD_GREEN}Press Enter to return to the submenu...")
        elif choice == '3':
            if domain:
                run_bbot(domain, display_menu, project_path)
            else:
                print(f"{BOLD_RED}Please set a domain first using option 1.")
        elif choice == '4':
            bbot_main()
        elif choice == '5':
            if domain:
                run_eyewitness(domain)
            else:
                print(f"{BOLD_RED}Please set a domain first using option 1.")
        elif choice == 'x':
            return
        else:
            print(f"{BOLD_YELLOW}Invalid choice, please try again.")
            input(f"{BOLD_GREEN}Press Enter to continue...")


def website_enumeration_submenu():
    clear_screen()
    domain = ''
    osint_domain_file = 'osint_domain.txt'
    website_enum_domain_file = 'website_enum_domain.txt'

    # Check if osint_domain.txt exists and read the domain from it
    if os.path.exists(osint_domain_file):
        with open(osint_domain_file, 'r') as file:
            domain = file.read().strip()
        use_osint_domain = input(f"{BOLD_CYAN}Use OSINT domain '{domain}' for website enumeration? (Y/n): ").strip().lower()
        if use_osint_domain not in ['y', 'yes', '']:
            domain = input(f"{BOLD_CYAN}Please input the domain for website enumeration: ").strip()
            with open(website_enum_domain_file, 'w') as file:
                file.write(domain)
    else:
        print(f"{BOLD_YELLOW}No OSINT domain has been set. Please set the domain.")
        domain_input = input(f"{BOLD_CYAN}Please input the domain for website enumeration: ").strip()
        if is_valid_domain(domain_input):
            domain = domain_input
            with open(website_enum_domain_file, 'w') as file:
                file.write(domain)
        else:
            print(f"{BOLD_RED}Invalid domain name. Please enter a valid domain.")
            return

    while True:
        clear_screen()
        domain_set_status = f"{BOLD_GREEN}Domain is set to: {domain}" if domain else f"{BOLD_YELLOW}Domain is not set."
        domain_status_menu = f"{BOLD_CYAN}1. Domain Is Set" if domain else f"{BOLD_RED}1. Set Domain"
        print(f"{BOLD_CYAN}Website Enumeration Menu: {domain_set_status}\n")
        menu_options = [
            (f"{domain_status_menu}", f"         {DEFAULT_COLOR}Checks if domain is set or not. Yellow means a domain needs to be set."),
            ("2. Run Feroxbuster for Directory Brute Forcing", f"{DEFAULT_COLOR}Discover hidden directories and files."),
            ("2. Identify Technologies with Wappalyzer", f"{BOLD_YELLOW}Not working {DEFAULT_COLOR}Uncover technologies used on websites."),
            ("3. Perform OWASP ZAP Scan", f"{BOLD_YELLOW}Not working {DEFAULT_COLOR}Find vulnerabilities in web applications."),
            ("4. Run WPScan for WordPress Sites", f"{BOLD_YELLOW}Not working {DEFAULT_COLOR}Check for vulnerabilities in WordPress sites.")
        ]

        for option, description in menu_options:
            print(f"{BOLD_GREEN}{option.ljust(50)}{description}")

        print(f"\n{BOLD_CYAN}Utilities:")
        print(f"{BOLD_RED}X. Return to Main Menu".ljust(30) + f"\n")

        choice = input(f"\n{BOLD_GREEN}Enter your choice: ").lower()

        if choice == '1':
            domain_input = input(f"{BOLD_CYAN}Please input the domain for website enumeration: ").strip()
            if is_valid_domain(domain_input):
                domain = domain_input
                with open(website_enum_domain_file, 'w') as file:
                    file.write(domain)
                print(f"{BOLD_GREEN}Domain set to: {domain}")
            else:
                print(f"{BOLD_RED}Invalid domain name. Please enter a valid domain.")
            input(f"{BOLD_CYAN}Press Enter to continue...")
        elif choice == '2':
            run_feroxbuster(domain)
        elif choice == '3':
            # Placeholder for Wappalyzer integration
            print(f"{BOLD_YELLOW}Wappalyzer integration is in progress...")
            # run_wappalyzer()
        elif choice == '4':
            # Placeholder for OWASP ZAP integration
            print(f"{BOLD_YELLOW}OWASP ZAP integration is in progress...")
            # run_owasp_zap()
        elif choice == '5':
            # Placeholder for WPScan integration
            print(f"{BOLD_YELLOW}WPScan integration is in progress...")
            # run_wpscan()
        elif choice == 'x':
            # Return to the main menu
            return
        else:
            print(f"{BOLD_RED}Invalid choice, please try again.")
            input(f"{BOLD_GREEN}Press Enter to continue...")
            website_enumeration_submenu()


def display_menu(version, project_path, ascii_art):
    clear_screen()
    update_available = check_and_update()
    print(ascii_art)
    print(f"{BOLD_CYAN}========================================================")
    update_msg = "\n                  Update Available!\n  Please exit and run pip install --upgrade infiltra\n" if update_available else ""
    print(f"{BOLD_CYAN}                Current Version: v{version}")
    print(f"{BOLD_MAG}{update_msg}")
    print(f"{BOLD_YELLOW}            https://github.com/jivy26/infiltra")
    print(f"{BOLD_YELLOW}            Author: @jivy26")
    print(f"{BOLD_CYAN}========================================================\n")

    current_directory = project_path if project_path else os.getcwd()
    print(f"{BOLD_GREEN}Current Directory: {current_directory}\n")

    print(f"\n{BOLD_GREEN}Main Menu")
    print(f"{BOLD_GREEN}========================================================\n")
    menu_options = [
        ("1. Projects", f"{DEFAULT_COLOR}Create, Load, or Delete Projects"),
        ("2. Whois", f"{DEFAULT_COLOR}Perform WHOIS lookups and parse results."),
        ("3. ICMP Echo ", f"{DEFAULT_COLOR}Ping requests and parse live hosts."),
        ("4. OSINT and Black Box OSINT", f"{DEFAULT_COLOR}AORT, DNS Recon, BBOT, and EyeWitness available."),
        ("5. NMAP Scans", f"{DEFAULT_COLOR}Discover open ports and services on the network."),
        ("6. Parse NMAP Scans", f"{DEFAULT_COLOR}Parse NMAP TCP/UDP Scans."),
        ("7. SSLScan and Parse", f"{DEFAULT_COLOR}Run SSLScan for Single IP or Range and Parse Findings."),
        ("8. Nikto Web Scans", f"{DEFAULT_COLOR}Scan web servers to identify potential security issues."),
        ("9. Website Enumeration", f"{DEFAULT_COLOR}Directory brute-forcing, technology identification, and more."),
        ("10. Vulnerability Scanner", f"{BOLD_YELLOW}(In-Progress)")
    ]

    for option, description in menu_options:
        print(f"{BOLD_GREEN}{option.ljust(30)}{description}")

    print(f"\n{BOLD_CYAN}Utilities:")
    print(f"{BOLD_RED}X. Exit".ljust(30) + f"{DEFAULT_COLOR} Exit the application.\n")

    choice = input(f"\n{BOLD_GREEN}Enter your choice: ").lower()
    return choice


# Main function
def main():
    projects_base_path = os.path.expanduser('~/projects')  # Define the base projects directory path
    project_path = projects_base_path  # Initialize project_path
    version = get_version()

    # Inside your main function or wherever you need to print the ASCII art
    ascii_art = get_ascii_art('logo.png', columns=80)

    # Check for last used project
    clear_screen()
    if last_project_file_path.exists():
        with last_project_file_path.open() as file:
            last_project = file.read().strip()
        if last_project:
            use_last_project = input(
                f"{BOLD_GREEN}Do you want to load the last project used '{last_project}'? (Y/n): ").strip().lower()
            if use_last_project in ['', 'y']:
                project_path = os.path.join(projects_base_path, last_project)
                os.chdir(project_path)
                print(f"{BOLD_GREEN}Loaded the recent project: {last_project}")

    while True:
        try:
            choice = display_menu(version, project_path, ascii_art)
            if choice == '1':
                new_project_path = project_submenu()
                if new_project_path is not None:  # Check if a new project path was returned or if it's a deletion
                    project_path = new_project_path
                    os.chdir(project_path)  # Change the working directory
                    print(f"Changed directory to {project_path}")
                else:
                    # If None is returned, reset to the base projects directory (e.g. after deletion)
                    project_path = os.path.expanduser('~/projects')
                    os.chdir(project_path)
                    print(f"Changed directory to the base projects directory {project_path}")
            elif choice == '2':
                run_whois()
            elif choice == '3':
                check_alive_hosts()
            elif choice == '4':
                osint_submenu(project_path)
            elif choice == '5':
                run_nmap()
            elif choice == '6':
                clear_screen()
                print(f"{BOLD_CYAN}NMAP Results Parser\n")
                scan_type = input(f"{BOLD_GREEN}Enter the scan type that you want to parse (TCP/UDP): ").upper()
                run_ngrep(scan_type)
            elif choice == '7':
                run_sslscanparse()
            elif choice == '8':
                target_input = input(
                    f"{BOLD_GREEN}Enter a single IP/domain or path to a file with IPs/domains: ")
                run_nikto(target_input)
            elif choice == '9':
                website_enumeration_submenu()
            elif choice == '10':
                nuclei_main()
            elif choice == 'u':
                print("Checking for updates...")
                updated = check_and_update()
            elif choice == 'x':
                break
            else:
                print(f"{BOLD_YELLOW}Invalid choice, please try again.")
        except EOFError:
            print(f"{BOLD_RED}EOFError encountered. Exiting...")
            sys.exit(1)
        except KeyboardInterrupt:
            print(f"{BOLD_RED}Operation cancelled by user. Exiting...")
            sys.exit(1)


# Ensure the `packaging` library is installed
try:
    from packaging import version
except ImportError:
    print(
        f"{BOLD_RED}The 'packaging' library is required for version comparison. Please install it using 'pip install packaging'.")
    exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        sys.exit()
