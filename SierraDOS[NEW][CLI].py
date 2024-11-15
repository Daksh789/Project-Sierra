import os
import shutil
import time
import re
import datetime
import platform
import psutil 
print('''Starting SierraDOS....''')
time.sleep(5)
print("System started successfully")

def show_help():
    print("""
    SierraDOS Commands:
    --------------------
    dir                   - List directory contents
    cd [folder]           - Change directory
    mkdir [name]          - Create a directory
    rmdir [name]          - Remove a directory
    copy [src] [dest]     - Copy a file
    move [src] [dest]     - Move a file
    edit [file]           - Create/Edit a text file
    type [file]           - Display the contents of a text file
    spreadsheet           - Simple spreadsheet functionality
    save_spreadsheet      - Save current spreadsheet to a file
    load_spreadsheet      - Load spreadsheet from a file
    search [name]         - Search for files by name
    calc                  - Simple calculator
    color [color]         - Change text color
    time                  - Show current time
    date                  - Show current date
    system_details        - Display hardware and software information
    volume                - Calculate the volume of a regular 3D object
    tablecalc             - Get the multiplication tables of large numbers
    reboot                - Restart the DOS
    exit                  - Exit the program
    help                  - Show this help message
    """)

def list_directory():
    for item in os.listdir('.'):
        print(item)

def change_directory(folder):
    try:
        os.chdir(folder)
    except FileNotFoundError:
        print(f"Directory '{folder}' not found.")

def create_directory(name):
    try:
        os.mkdir(name)
    except FileExistsError:
        print(f"Directory '{name}' already exists.")

def remove_directory(name):
    try:
        os.rmdir(name)
    except OSError:
        print(f"Directory '{name}' is not empty or cannot be removed.")

def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
        print(f"File '{src}' copied to '{dest}'.")
    except FileNotFoundError:
        print(f"File '{src}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def move_file(src, dest):
    try:
        shutil.move(src, dest)
        print(f"File '{src}' moved to '{dest}'.")
    except FileNotFoundError:
        print(f"File '{src}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def edit_file(filename):
    print("Enter text (type 'SAVE' to save and exit):")
    lines = []
    while True:
        line = input()
        if line.upper() == 'SAVE':
            break
        lines.append(line)
    
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))
    print(f"File '{filename}' saved.")

def view_file(filename):
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

def search_files(name):
    found_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if re.search(name, file):
                found_files.append(os.path.join(root, file))
    if found_files:
        for file in found_files:
            print(file)
    else:
        print(f"No files found matching '{name}'.")

spreadsheet_data = []

def spreadsheet():
    global spreadsheet_data
    print("Simple Spreadsheet - Enter 'exit' to quit")
    while True:
        command = input("Enter data (row, col, value) or math expression or command: ")
        if command.lower() == 'exit':
            break
        elif command.startswith(('save_spreadsheet', 'load_spreadsheet')):
            break
        try:
            if any(op in command for op in ['+', '-', '*', '/']):
                print(f"Result: {eval(command)}")
            else:
                row, col, value = command.split(',')
                row, col = int(row), int(col)
                if len(spreadsheet_data) <= row:
                    spreadsheet_data.extend([[] for _ in range(row - len(spreadsheet_data) + 1)])
                if len(spreadsheet_data[row]) <= col:
                    spreadsheet_data[row].extend(['' for _ in range(col - len(spreadsheet_data[row]) + 1)])
                spreadsheet_data[row][col] = value
        except ValueError:
            print("Invalid input. Use 'row,col,value' format.")
        except Exception as e:
            print(f"Error: {e}")
    
    print("Spreadsheet Content:")
    for row in spreadsheet_data:
        print('\t'.join(row))

def save_spreadsheet(filename):
    global spreadsheet_data
    with open(filename, 'w') as file:
        for row in spreadsheet_data:
            file.write(','.join(row) + '\n')
    print(f"Spreadsheet saved to '{filename}'.")

def load_spreadsheet(filename):
    global spreadsheet_data
    try:
        with open(filename, 'r') as file:
            spreadsheet_data = [line.strip().split(',') for line in file]
        print(f"Spreadsheet loaded from '{filename}'.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def calculator():
    print("Simple Calculator - Enter 'exit' to quit")
    while True:
        expression = input("Enter expression: ")
        if expression.lower() == 'exit':
            break
        try:
            result = eval(expression)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

def change_color(color):
    colors = {
        'black': '0',
        'blue': '1',
        'green': '2',
        'aqua': '3',
        'red': '4',
        'purple': '5',
        'yellow': '6',
        'white': '7',
        'gray': '8',
        'light_blue': '9'
    }
    color_code = colors.get(color.lower(), None)
    if color_code:
        os.system(f'color {color_code}')
        print(f"Color changed to {color}.")
    else:
        print(f"Color '{color}' not recognized. Available colors: {', '.join(colors.keys())}")

def show_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current Time: {current_time}")

def show_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"Current Date: {current_date}")

def get_weather(city):
    print("Weather functionality requires API integration. This is a placeholder.")
    # Placeholder for actual weather data retrieval
    # You can integrate with an API like OpenWeatherMap or similar
    print(f"Fetching weather for {city}...")

def system_details():
    print("System Details:")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"RAM: {round(psutil.virtual_memory().total / (1024**3))} GB")
    print(f"Available Disk Space: {round(psutil.disk_usage('/').free / (1024**3))} GB")

def main():
    print("SierraDOS")
    show_help()
    
    while True:
        command = input("SierraDOS@Py3-$  ").strip().split()
        if not command:
            continue
        
        cmd = command[0].lower()
        
        if cmd == 'dir':
            list_directory()
        elif cmd == 'cd' and len(command) > 1:
            change_directory(command[1])
        elif cmd == 'mkdir' and len(command) > 1:
            create_directory(command[1])
        elif cmd == 'rmdir' and len(command) > 1:
            remove_directory(command[1])
        elif cmd == 'copy' and len(command) > 2:
            copy_file(command[1], command[2])
        elif cmd == 'move' and len(command) > 2:
            move_file(command[1], command[2])
        elif cmd == 'edit' and len(command) > 1:
            edit_file(command[1])
        elif cmd == 'type' and len(command) > 1:
            view_file(command[1])
        elif cmd == 'search' and len(command) > 1:
            search_files(command[1])
        elif cmd == 'spreadsheet':
            spreadsheet()
        elif cmd == 'save_spreadsheet' and len(command) > 1:
            save_spreadsheet(command[1])
        elif cmd == 'load_spreadsheet' and len(command) > 1:
            load_spreadsheet(command[1])
        elif cmd == 'calc':
            calculator()
        elif cmd == 'color' and len(command) > 1:
            change_color(command[1])
        elif cmd == 'time':
            show_time()
        elif cmd == 'date':
            show_date()
        elif cmd == 'weather' and len(command) > 1:
            get_weather(command[1])
        elif cmd == 'system_details':
            system_details()
        elif cmd == 'exit':
            print("Exiting SierraDOS...")
            break
        elif cmd == 'help':
            show_help()
        elif cmd == 'volume':
            h = input('Please enter the name of the shape: ')
            if h == "cuboid":
                length = float(input("What is the length of the cuboid? "))
                width = float(input("What is the width of the cuboid? "))
                height = float(input("What is the height of the cuboid?: "))
                Volume = length * width * height
                print("The Volume of the Cuboid = %.2f" % Volume)
            elif h == "sphere":
                PI = 3.14
                radius = float(input('Please Enter the Radius of the Sphere: '))
                Volume = (4 / 3) * PI * radius * radius * radius
                print(" The Volume of the Sphere = %.2f" % Volume)
            elif h == "cylinder":
                pi = 3.14
                radius = int(input('Enter the radius of the cylinder: '))
                height = int(input('Enter the height of the cylinder: '))
                volume = pi * radius * radius * height
                print(" Volume of the cylinder = ", volume)
            elif h == "cube":
                length = float(input("What is the length of the cube? "))
                width = float(input("What is the width of the cube? "))
                height = float(input("What is the height of the cube? "))
                Volume = length * width * height
                print("The Volume of the Cube = %.2f" % Volume)
        elif cmd == "reboot":
         print("Restarting...")
         time.sleep(2.0)
         # restart the loop
        elif cmd == "tablecalc":
            num1 = int(input('what is the table?'))
            num2 = int(input('what is the multiple?'))
            num2 = num2 + 1
            num3 = 1
            while num3 < num2:
                print(num1, 'x', num3, "=", num1 * num3)
                num3 = num3 + 1  
        else:
            print(f"Unknown command: {cmd}")
    
if __name__ == "__main__":
    main()
