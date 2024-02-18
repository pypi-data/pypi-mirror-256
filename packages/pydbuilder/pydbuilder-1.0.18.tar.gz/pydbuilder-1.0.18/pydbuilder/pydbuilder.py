import subprocess
import random
import string
import shutil
import json
import sys
import os


# LOAD SETTINGS
curr_dir = os.path.abspath(__file__)
curr_dir = os.path.dirname(curr_dir)
fdir = lambda filename: os.path.join(curr_dir, filename)

with open(fdir('settings.json'), 'r', encoding='UTF-8') as file:
    settings = json.load(file)
    language = settings.get('lang', 'en')

with open(fdir('language.json'), 'r', encoding='UTF-8') as file:
    lsettings = json.load(file)
    language = lsettings[language.lower()]
    org_lang_list = lsettings.keys()
    lang_list = '\n'.join([f'- {name}' for name in lsettings.keys()])
del lsettings


# COLORS
if settings['color']:
    magenta = '\033[38;2;133;116;244m'
    orange = '\033[38;2;255;202;117m'
    yellow = '\033[38;2;255;255;128m'
    sgreen = '\033[38;2;46;211;152m'
    green = '\033[38;2;138;255;124m'
    pink = '\033[38;2;255;128;191m'
    gray = '\033[38;2;114;140;167m'
    blue = '\033[38;2;128;255;234m'
    red = '\033[38;2;235;64;52m'
    white = '\33[97m'
    end = '\033[0m'
else:
    magenta = ''
    orange = ''
    yellow = ''
    sgreen = ''
    green = ''
    pink = ''
    gray = ''
    blue = ''
    red = ''
    white = ''
    end = ''


# FUNCTIONS
def apply_setting(key, value):
    try:
        with open(fdir('settings.json'), 'r', encoding='UTF-8') as file:
            settings = json.load(file)

        settings[key] = value

        with open(fdir('settings.json'), 'w', encoding='UTF-8') as file:
            json.dump(settings, file, indent=4)
    except Exception as er:
        return f'{red}Error: {white}{er}'
    else:
        return f'{green}Successfully changed!{end}'

def change_settings():
    print(orange+f'Program settings'+end)

    settings_list = ('lang', 'color')
    settings_help = '\n'.join([f'• {name}' for name in (
        f'lang {white}- {gray}Change language for the library{blue}',
        f'color {white}- {gray}Enable/Disable colorized text'
    )])

    print(blue+f'\n{settings_help}\n'+end)

    try:
        while True:
            command = input(white+'> '+pink).strip().lower()

            if command not in settings_list:
                print(f'{red}Error: {white}Setting not found'+end)
                continue

            if command == 'lang':
                print(orange+f'Select the language {gray}(Available "help")'+end)
                while True:
                    lang = input(white+'> '+pink)

                    if lang.lower().strip() == 'help':
                        print(blue+f'\n{lang_list}\n'+end)
                        continue

                    if lang not in org_lang_list:
                        print(f'{red}Error: {white}Language not found'+end)
                        continue

                    print(apply_setting('lang', lang))
                    raise SystemExit(0)
            elif command == 'color':
                print(orange+f'Select the language {gray}(True/False)'+end)
                
                color = input(white+'> '+pink).strip().lower()

                if color.strip().lower() == 'false':
                    color = False
                else:
                    color = True

                print(apply_setting('color', color))
                raise SystemExit(0)
    except KeyboardInterrupt:
        print(end=end)
        raise SystemExit(0)

def load_ext(string=None):
    default_ext = ('py', 'pyw', 'pyx')
    if not string:
        return default_ext
    extensions = [ext.strip() for ext in string.split(',')]
    return [ext for ext in default_ext if ext in extensions]

def get_folder_path(path):
    if os.path.exists(path):
        path = os.path.abspath(path)

        if os.path.isfile(path):
            return os.path.dirname(path)
        return path
    else:
        return os.getcwd()

def random_name():
    upper_letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase
    numbers = string.digits
    
    password = ''
    password += random.choice(upper_letters)
    password += random.choice(lower_letters)
    password += random.choice(upper_letters)
    password += random.choice(lower_letters)
    password += random.choice(numbers)
    password += random.choice(upper_letters)
    password += random.choice(lower_letters)
    
    return password

def find_and_move_pyd(directory, target_dir, source_name):
    for filename in os.listdir(directory):
        if filename.startswith(f'{source_name}.') and filename.endswith('.pyd'):
            source_path = os.path.join(directory, filename)
            current_path = os.path.join(target_dir, f'{source_name}.pyd')
            
            try:
                os.rename(source_path, current_path)
            except FileExistsError:
                os.remove(current_path)
                os.rename(source_path, current_path)

def compile_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
                main_code = file.read()
        except Exception as er:
            print(f'{red}{language["read_err"]}: {white}{er}'+end)
            raise SystemExit(0)

        os.system(f'title Cythonizing "{os.path.basename(file_path)}"...')
        source_name = os.path.basename(file_path.split('.')[0])
        source_path = os.path.dirname(file_path)
        dir_path = os.path.join('C:\\Windows\\Temp', random_name())
        os.mkdir(dir_path)

        with open(os.path.join(dir_path, f'{source_name}.pyx'), 'w', encoding='UTF-8') as file:
            file.write(main_code)

        setup_code = f'from setuptools import setup\nfrom Cython.Build import cythonize\n\nsetup(\n    ext_modules=cythonize(\'{source_name}.pyx\', compiler_directives={{\'language_level\': \'3\'}})\n)'

        with open(os.path.join(dir_path, 'setup.py'), 'w', encoding='UTF-8') as file:
            file.write(setup_code)

        try:
            subprocess.run('python setup.py build_ext --inplace', cwd=dir_path, check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f'{red}{language["cmd_err"]}: {white}{e}'+end)
            raise SystemExit(0)

        try:
            find_and_move_pyd(dir_path, source_path, source_name)
            print(f'{green}{language["success1"]} {orange}"{source_name}.pyd" {green}{language["success2"]}!'+end)
        except Exception as er:
            print(f'{red}{language["repl_err"]}: {white}{er}'+end)
            raise SystemExit(0)

        shutil.rmtree(dir_path)
    else:
        print(f'{red}Error: {white}{language["path_err"]}'+end)

def find_arg(*arguments, next_arg=True):
    arguments = [arg.lower() for arg in arguments]

    for index, arg in enumerate(sys.argv):
        if arg.lower() in arguments:
            if next_arg:
                try:
                    return sys.argv[index + 1]
                except:
                    pass
            return True
    return None


# MAIN CODE
def main():
    if os.name == 'nt':
        os.system('color')

    if find_arg('--help', '-h', next_arg=False):
        arguments = [
            f'{magenta}--settings {gray}— {yellow}{language["help"]["1"]}',
            f'{magenta}--help {gray}— {yellow}{language["help"]["2"]}',
            f'{magenta}-all {gray}— {yellow}{language["help"]["3"]}',
            f'{magenta}-ext {gray}— {yellow}{language["help"]["4"]}'
        ]

        formatted_help = '\n\n'.join([f'  {arg}' for arg in arguments])

        print(f'{gray}{language["help"]["0"]}:\n{formatted_help}'+end)
        raise SystemExit(0)

    if find_arg('--settings', next_arg=False):
        change_settings()

    if len(sys.argv) < 2:
        print(f'{red}{language["usage_msg"]}: {white}<{language["usage_msg2"]}>'+end)
    else:
        try:
            file_path = sys.argv[-1]
            if find_arg('-all', next_arg=False):
                file_path = get_folder_path(file_path)
                uexts = None

                if exts := find_arg('-ext'):
                    uexts = exts
                extensions = load_ext(uexts)
                file_list = [os.path.join(file_path, file) for file in os.listdir(file_path) if file.split('.')[-1] in extensions]

                for file in file_list:
                    compile_file(file)
                raise SystemExit(0)
            compile_file(file_path)
        except KeyboardInterrupt:
            raise SystemExit(0)

if __name__ == '__main__':
    main()