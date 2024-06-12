import yaml
import os
import random
import subprocess
from colorama import Fore, Style
from main import AbuseOS

class ScriptEngine:
    @staticmethod
    def load_script(file_path):
        with open(file_path, 'r') as file:
            script_content = yaml.safe_load(file)
        return script_content

    @staticmethod
    def run_script(file_path):
        script_content = ScriptEngine.load_script(file_path)
        
        info = script_content.get('info', {})
        author = info.get('author', 'Unknown')
        name = info.get('name', 'Unknown Script')
        version = info.get('version', 'Unknown Version')
        
        print(f"{Style.BRIGHT}{Fore.GREEN}Running \"{file_path}\". Info: {name} v{version} by {author}!{Style.RESET_ALL}")
        
        variables = script_content.get('variables', {})
        script_lines = script_content.get('script', [])
        
        ScriptEngine.execute_script(script_lines, variables)

    @staticmethod
    def execute_script(script_lines, variables):
        i = 0
        while i < len(script_lines):
            line = script_lines[i]
            if line.startswith("for"):
                parts = line.split(' ')
                var_name = parts[1].strip()
                start = int(parts[3])
                end = int(parts[5])
                j = start
                while j <= end:
                    variables[var_name] = str(j)
                    i += 1
                    ScriptEngine.execute_script(script_lines[i:], variables)
                    i -= 1
                    j += 1
            elif line.startswith("while true"):
                while True:
                    i = ScriptEngine.execute_script(script_lines[i + 1:], variables)
                    if i == -1:
                        break
            elif line.startswith("break"):
                return -1
            elif line.startswith("input"):
                parts = line.split(' ', 1)
                var_name = parts[1].strip()
                user_input = input(f"Enter value for {var_name}: ")
                variables[var_name] = user_input
            elif line.startswith("random"):
                parts = line.split(' ')
                var_name = parts[1].strip()
                start = int(parts[2])
                end = int(parts[3])
                variables[var_name] = str(random.randint(start, end))
            elif line.startswith("if"):
                condition = line[3:].strip()
                if ScriptEngine.evaluate_condition(condition, variables):
                    i += 1
                    i = ScriptEngine.execute_script(script_lines[i:], variables)
                else:
                    i = ScriptEngine.find_else_or_end(script_lines, i)
                    continue
            elif line.startswith("else"):
                i = ScriptEngine.find_end(script_lines, i)
                continue
            elif line.startswith("echo"):
                line = line[5:]  # Удаляем "echo "
                for key, value in variables.items():
                    variable_placeholder = f"${key}"
                    if variable_placeholder in line:
                        line = line.replace(variable_placeholder, value)
                ScriptEngine.print_colored(line)
            else:
                for key, value in variables.items():
                    variable_placeholder = f"${key}"
                    if variable_placeholder in line:
                        line = line.replace(variable_placeholder, value)
                AbuseOS.execute_command(line)
            i += 1

    @staticmethod
    def evaluate_condition(condition, variables):
        for key, value in variables.items():
            variable_placeholder = f"${key}"
            if variable_placeholder in condition:
                condition = condition.replace(variable_placeholder, value)
        try:
            return eval(condition)
        except:
            return False

    @staticmethod
    def find_end(script_lines, start_index):
        depth = 1
        for i in range(start_index + 1, len(script_lines)):
            line = script_lines[i]
            if line.startswith("for") or line.startswith("while true") or line.startswith("if"):
                depth += 1
            elif line.startswith("end"):
                depth -= 1
                if depth == 0:
                    return i
        return len(script_lines)

    @staticmethod
    def find_else_or_end(script_lines, start_index):
        depth = 1
        for i in range(start_index + 1, len(script_lines)):
            line = script_lines[i]
            if line.startswith("for") or line.startswith("while true") or line.startswith("if"):
                depth += 1
            elif line.startswith("end"):
                depth -= 1
                if depth == 0:
                    return i
            elif line.startswith("else") and depth == 1:
                return i
        return len(script_lines)

    @staticmethod
    def print_colored(text):
        colored_text = text.replace("$purple", Fore.MAGENTA).replace("$cyan", Fore.CYAN).replace("$darkcyan", Fore.LIGHTCYAN_EX).replace("$blue", Fore.BLUE).replace("$green", Fore.GREEN).replace("$yellow", Fore.YELLOW).replace("$end", Style.RESET_ALL).replace("$red", Fore.RED).replace("$bold", Style.BRIGHT)
        print(colored_text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: scriptengine <script.aos>")
        exit(1)
    
    script_path = sys.argv[1]
    if not os.path.exists(script_path):
        print(f"Script file {script_path} does not exist.")
        exit(1)
    
    ScriptEngine.run_script(script_path)