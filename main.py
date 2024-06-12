import os
import json
import shutil
from datetime import datetime
from colorama import Fore, Style

class Config:
    def __init__(self, RAM, DISK, CPU, CPUCores):
        self.RAM = RAM
        self.DISK = DISK
        self.CPU = CPU
        self.CPUCores = CPUCores

class AbuseOS:
    RAM = 0
    DISK = 0
    CPU = ""
    CPUCores = 0

    @staticmethod
    def main():
        AbuseOS.load_specs()
        host = input("Enter host: ")
        password = input("Enter password: ")

        if AbuseOS.validate_user(host, password):
            print(f"{Style.BRIGHT}{Fore.GREEN}Welcome to aOs 1.3.1, {host}!{Style.RESET_ALL}")
            AbuseOS.run_shell(host)
        else:
            print(f"{Fore.RED}Unknown password&host.{Style.RESET_ALL}")

    @staticmethod
    def load_specs():
        try:
            config_path = "config.json"
            if os.path.exists(config_path):
                with open(config_path, "r") as file:
                    config_data = json.load(file)
                    config = Config(**config_data)
                    AbuseOS.RAM = config.RAM
                    AbuseOS.DISK = config.DISK
                    AbuseOS.CPU = config.CPU
                    AbuseOS.CPUCores = config.CPUCores
            else:
                print("ERROR While loading server.")
        except Exception as ex:
            print(f"ERROR While loading server: {ex}")

    @staticmethod
    def validate_user(host, password):
        with open("users.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(':')
                if parts[0] == host and parts[1] == password:
                    return True
        return False

    @staticmethod
    def run_shell(host):
        while True:
            input_str = input(f"{Style.BRIGHT}{Fore.MAGENTA}aos {Fore.GREEN}| {Fore.RED}{host} {Fore.GREEN}# {Style.RESET_ALL}")
            AbuseOS.execute_command(input_str)

    @staticmethod
    def execute_command(input_str):
        parts = input_str.split(' ', 2)
        command = parts[0]
        argument1 = parts[1] if len(parts) > 1 else ""
        argument2 = parts[2] if len(parts) > 2 else ""

        commands = {
            "free": AbuseOS.command_free,
            "info": AbuseOS.command_info,
            "ram": AbuseOS.command_ram,
            "disk": AbuseOS.command_disk,
            "cpu": AbuseOS.command_cpu,
            "echo": AbuseOS.command_echo,
            "help": AbuseOS.command_help,
            "clear": AbuseOS.command_clear,
            "exit": AbuseOS.command_exit,
            "date": AbuseOS.command_date,
            "time": AbuseOS.command_time,
            "dir": AbuseOS.command_dir,
            "mkdir": AbuseOS.command_mkdir,
            "rmdir": AbuseOS.command_rmdir,
            "touch": AbuseOS.command_touch,
            "rm": AbuseOS.command_rm,
            "adduser": AbuseOS.command_adduser,
            "copydir": AbuseOS.command_copydir,
            "copy": AbuseOS.command_copy,
            "pterodactyl": AbuseOS.command_pterodactyl,
            "scriptengine": AbuseOS.command_scriptengine,
        }
        if command == 'echo':
            if os.path.exists("core.db"):
                ggg = input_str.split(' ')[1:]
                outp = ""
                for g in ggg:
                    outp += f" {g}"
                AbuseOS.command_echo(outp, None)
            else:
                for _ in range(0, 150):
                    print(f"{Style.BRIGHT}{Fore.RED}SYSTEM CORE REMOVED!")
        elif command in commands:
            if os.path.exists("core.db"):
                commands[command](argument1, argument2)
            else:
                for _ in range(0, 150):
                    print(f"{Style.BRIGHT}{Fore.RED}SYSTEM CORE REMOVED!")
        else:
            if os.path.exists("core.db"):
                print(f"Unknown command: {command}")
            else:
                for _ in range(0, 150):
                    print(f"{Style.BRIGHT}{Fore.RED}SYSTEM CORE REMOVED!")

    @staticmethod
    def command_free(argument1, _):
        if argument1 == "-h":
            print(f"Free RAM: {AbuseOS.RAM} MB")
        else:
            print("Unknown argument for free command.")
    @staticmethod
    def command_scriptengine(argument1, _):
        if argument1:
            from scriptengine import ScriptEngine
            ScriptEngine.run_script(argument1)
        else:
            print("No script file provided.")
    @staticmethod
    def command_info(_, __):
        print(f"RAM: {AbuseOS.RAM} MB")
        print(f"DISK: {AbuseOS.DISK} MB")
        print(f"CPU: {AbuseOS.CPU}")
        print(f"CPU Cores: {AbuseOS.CPUCores}")

    @staticmethod
    def command_ram(_, __):
        print(f"RAM: {AbuseOS.RAM} MB")

    @staticmethod
    def command_disk(_, __):
        print(f"DISK: {AbuseOS.DISK} MB")

    @staticmethod
    def command_cpu(_, __):
        print(f"CPU: {AbuseOS.CPU}")
        print(f"CPU Cores: {AbuseOS.CPUCores}")

    @staticmethod
    def command_echo(argument1, _):
        print(argument1)

    @staticmethod
    def command_help(_, __):
        AbuseOS.show_help()

    @staticmethod
    def command_clear(_, __):
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def command_exit(_, __):
        exit(0)

    @staticmethod
    def command_date(_, __):
        print(datetime.now())

    @staticmethod
    def command_time(_, __):
        print(datetime.now().strftime('%H:%M:%S'))

    @staticmethod
    def command_dir(_, __):
        AbuseOS.show_directory()

    @staticmethod
    def command_mkdir(argument1, _):
        if argument1:
            os.makedirs(argument1, exist_ok=True)
            print(f"Directory created: {argument1}")
        else:
            print("No directory name provided.")

    @staticmethod
    def command_rmdir(argument1, _):
        if argument1:
            os.rmdir(argument1)
            print(f"Directory removed: {argument1}")
        else:
            print("No directory name provided.")

    @staticmethod
    def command_touch(argument1, _):
        if argument1:
            open(argument1, 'a').close()
            print(f"File created: {argument1}")
        else:
            print("No file name provided.")

    @staticmethod
    def command_rm(argument1, _):
        if argument1:
            os.remove(argument1)
            print(f"File removed: {argument1}")
        else:
            print("No file name provided.")

    @staticmethod
    def command_adduser(argument1, argument2):
        if argument1 and argument2:
            AbuseOS.add_user(argument1, argument2)
        else:
            print("Usage: adduser <host> <password>")

    @staticmethod
    def command_copydir(argument1, argument2):
        if argument1 and argument2:
            AbuseOS.copy_directory(argument1, argument2)
        else:
            print("Usage: copydir <dir to copy> <copied dir name>")

    @staticmethod
    def command_copy(argument1, argument2):
        if argument1 and argument2:
            AbuseOS.copy_file(argument1, argument2)
        else:
            print("Usage: copy <file to copy> <copied file name>")

    @staticmethod
    def command_pterodactyl(argument1, argument2):
        if argument1 == "install" and argument2:
            args = argument2.split(' ')
            if len(args) == 2:
                AbuseOS.pterodactyl_install(args[0], args[1])
            else:
                print("Usage: pterodactyl install <user> <password>")
        elif argument1 == "adduser" and argument2:
            args = argument2.split(' ')
            if len(args) == 2:
                AbuseOS.pterodactyl_add_user(args[0], args[1])
            else:
                print("Usage: pterodactyl adduser <user> <password>")
        elif argument1 == "start":
            AbuseOS.pterodactyl_start()
        else:
            print("Unknown pterodactyl command.")

    @staticmethod
    def show_help():
        help_text = """
        Available commands:
        free -h    - Display free memory in human-readable format
        info       - Display system info
        ram        - Display RAM info
        disk       - Display disk info
        cpu        - Display CPU info
        echo       - Echo input text
        help       - Show this help message
        clear      - Clear the screen
        exit       - Exit the shell
        date       - Display the current date and time
        time       - Display the current time
        dir        - List the current directory contents
        mkdir      - Create a new directory
        rmdir      - Remove a directory
        touch      - Create a new file
        rm         - Remove a file
        adduser    - Add a new user (usage: adduser <host> <password>)
        pterodactyl install <user> <password> - Install Pterodactyl panel
        pterodactyl adduser <user> <password> - Add user to Pterodactyl panel
        pterodactyl start                     - Start Pterodactyl panel
        copydir <dir to copy> <copied dir name> - Copy a directory
        copy <file to copy> <copied file name>  - Copy a file
        scriptengine <script file> - Run script by aOs ScriptEngine
        """
        print(help_text)

    @staticmethod
    def show_directory():
        files = os.listdir('.')
        for f in files:
            print(f"<DIR> {f}" if os.path.isdir(f) else f"      {f}")

    @staticmethod
    def add_user(host, password):
        with open("users.txt", "a") as file:
            file.write(f"{host}:{password}\n")
        print(f"User added: {host}")

    @staticmethod
    def copy_directory(source_dir, dest_dir):
        shutil.copytree(source_dir, dest_dir)
        print(f"Directory copied from {source_dir} to {dest_dir}")

    @staticmethod
    def copy_file(source_file, dest_file):
        shutil.copy2(source_file, dest_file)
        print("Executed script successfuly!")

if __name__ == "__main__":
    AbuseOS.main()