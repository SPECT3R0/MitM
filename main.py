#!/usr/bin/env python3

"""
Darkside - Offensive Network Security Framework
Developed by SPECT3R for network penetration testing and MITM attacks.
This script provides an interactive menu and command-line interface for executing
network security operations like ARP spoofing, DNS spoofing, SSL stripping, etc.
"""

import sys
import argparse
from interface.cli import run_cli
import pyfiglet
from termcolor import colored

# Define global commands for the menu and command-line
COMMANDS = {
    "arp_spoof": "Perform ARP spoofing to intercept network traffic",
    "dns_spoof": "Spoof DNS responses to redirect traffic",
    "ssl_strip": "Strip SSL/TLS to downgrade HTTPS to HTTP",
    "http_inject": "Inject content (e.g., JavaScript) into HTTP responses",
    "analyze": "Analyze network traffic and log activities",
    "stop": "Stop all active operations and restore network state"
}

def display_banner():
    """
    Display the Darkside ASCII art banner and title in colored text.
    """
    ascii_art = """
████████▄     ▄████████    ▄████████    ▄█   ▄█▄    ▄████████  ▄█  ████████▄     ▄████████ 
███   ▀███   ███    ███   ███    ███   ███ ▄███▀   ███    ███ ███  ███   ▀███   ███    ███ 
███    ███   ███    ███   ███    ███   ███▐██▀     ███    █▀  ███▌ ███    ███   ███    █▀  
███    ███   ███    ███  ▄███▄▄▄▄██▀  ▄█████▀      ███        ███▌ ███    ███  ▄███▄▄▄     
███    ███ ▀███████████ ▀▀███▀▀▀▀▀   ▀▀█████▄    ▀███████████ ███▌ ███    ███ ▀▀███▀▀▀     
███    ███   ███    ███ ▀███████████   ███▐██▄            ███ ███  ███    ███   ███    █▄  
███   ▄███   ███    ███   ███    ███   ███ ▀███▄    ▄█    ███ ███  ███   ▄███   ███    ███ 
████████▀    ███    █▀    ███    ███   ███   ▀█▀  ▄████████▀  █▀   ████████▀    ██████████ 
                          ███    ███   ▀                                                   
    """
    print(colored(ascii_art, 'red', attrs=['bold']))
    title = "[ Darkside | Offensive Network Security Framework ] [ Developed by SPECT3R ]"
    print(colored(title, 'red'))

def display_menu():
    """
    Display the interactive menu with numbered options and descriptions.
    """
    print(colored("\n=== Darkside Interactive Menu ===", 'cyan'))
    for i, (cmd, desc) in enumerate(COMMANDS.items(), 1):
        print(colored(f"  {i}. {cmd}: {desc}", 'white'))
    print(colored(f"  {len(COMMANDS) + 1}. exit: Exit the menu", 'white'))

    # Show command-line usage examples
    print(colored("\n=== Or Use Command-Line Examples ===", 'yellow'))
    print(colored("1. Show help: python3 main.py --help", 'yellow'))
    print(colored("2. Start ARP spoofing: python3 main.py arp_spoof", 'yellow'))
    print(colored("3. Inject JavaScript alert: python3 main.py http_inject -c \"alert('Hacked by Darkside');\"", 'yellow'))
    print(colored("4. Stop all operations: python3 main.py stop", 'yellow'))

def get_user_choice():
    """
    Get and validate user input for the interactive menu.
    Returns the chosen command or 'exit'.
    """
    while True:
        choice = input(colored("\nEnter your choice (1-7) or command name: ", 'cyan')).lower().strip()
        try:
            # Check if input is a number
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(COMMANDS):
                    return list(COMMANDS.keys())[num - 1]
                elif num == len(COMMANDS) + 1:
                    return "exit"
            # Check if input is a command name
            elif choice in COMMANDS or choice == "exit":
                return choice
            print(colored("Invalid choice. Please enter a number (1-7) or command name.", 'red'))
        except ValueError:
            print(colored("Invalid input. Please enter a number or command name.", 'red'))

def parse_command_line():
    """
    Parse command-line arguments using argparse.
    Returns parsed arguments or raises an error if invalid.
    """
    parser = argparse.ArgumentParser(description='Darkside - Offensive Network Security Framework')
    parser.add_argument('command', choices=list(COMMANDS.keys()), help='Command to execute')
    parser.add_argument('-c', '--content', help='Content to inject for http_inject (e.g., JavaScript)')
    args = parser.parse_args()

    if args.command == 'http_inject' and not args.content:
        parser.error("the following arguments are required: --content")
    
    return args

def run_interactive_mode():
    """
    Run the interactive menu loop, handling user input and executing commands.
    """
    while True:
        choice = get_user_choice()
        if choice == "exit":
            print(colored("Exiting Darkside. Goodbye!", 'green'))
            break

        if choice == "http_inject":
            content = input(colored("Enter content to inject (e.g., JavaScript): ", 'cyan'))
            if not content:
                print(colored("Content is required for http_inject. Try again.", 'red'))
                continue
            args = argparse.Namespace(command=choice, content=content)
        else:
            args = argparse.Namespace(command=choice, content=None)

        try:
            run_cli(args)
        except Exception as e:
            print(colored(f"Error executing {choice}: {e}", 'red'))

def main():
    """
    Main entry point for Darkside, handling both command-line and interactive modes.
    """
    display_banner()
    display_menu()

    # Check if command-line arguments are provided
    if len(sys.argv) > 1:
        try:
            args = parse_command_line()
            run_cli(args)
        except SystemExit as e:
            sys.exit(1)
    else:
        run_interactive_mode()

if __name__ == '__main__':
    main()
