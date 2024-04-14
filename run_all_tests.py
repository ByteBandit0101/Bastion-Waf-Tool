import subprocess
import pathlib
import sys
import json
from pathlib import Path
import shutil  # Necessary import for removing directories
import datetime
import zipfile
import tkinter as tk
from tkinter import filedialog
import os

logs_dir = Path('./logs')  # Directory for merging logs
logs_dir.mkdir(exist_ok=True)  # Script to create the log folder if it does not exist

def run_test_script(script_path, base_url, send_rate):
    # Command to execute the external Python script with the send rate as an argument
    command = ['python', str(script_path), base_url, send_rate]
    # Execute the script and capture the output
    completed_process = subprocess.run(command, text=True, capture_output=True)
    # Return the standard output of the script
    return completed_process.stdout

def display_welcome_message():
    ascii_art = """
     ____           _____ _______ _____ ____  _   _ 
    |  _ \   /\    / ____|__   __|_   _/ __ \| \ | |
    | |_) | /  \  | (___    | |    | || |  | |  \| |
    |  _ < / /\ \  \___ \   | |    | || |  | | . ` | 
    | |_) / /__\ \ ____) |  | |   _| |_ |__| | |\  |
    |____/_/    \_\_____/   |_|  |_____\____/|_| \_|
                               Made by ByteBandit               

    """  
    print(ascii_art)
    print("Welcome to Bastion!\n")
    print("1. Explore Mutillidae")
    print("2. Explore DVWA")
    print("3. Exit")
    choice = input("Choose an option: ")
    return choice

# Function to clear the 'logs' folder if desired
def clear_logs_folder():
    try:
        # User confirmation to clear the 'logs' folder
        clear_choice = input("\nDo you want to clear the logs folder or save? (clear/save): ").lower()
        if clear_choice == 'clear':
            shutil.rmtree(logs_dir)
            print("Logs folder successfully cleared.")
            logs_dir.mkdir()  # Recreate the 'logs' folder after clearing
        elif clear_choice == 'save':
            today = datetime.date.today()  # Get today's date
            zip_name = f"log_{today.strftime('%d-%m-%Y_%H-%M-%S')}.zip"  # Name the zip file with today's date

            # Create a zip file and add the logs directory
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(logs_dir):
                    for file in files:
                        zipf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file),
                                                   os.path.join(logs_dir, '..')))

            print(f"Logs folder was not cleared. Contents zipped to: {zip_name}")

            # Ask user where to save the zip file
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            save_path = filedialog.asksaveasfilename(defaultextension=".zip", initialfile=zip_name)
            if save_path:  # If a save path was chosen
                shutil.move(zip_name, save_path)
                print(f"Zip file saved to: {save_path}")
                
                # Clear the logs folder after zipping
                shutil.rmtree(logs_dir)  # Remove the logs folder and its contents
                logs_dir.mkdir()  # Recreate the logs folder, now empty
            else:
                print("Zip file save cancelled. File is located in the current directory.")

        else:
            print("Invalid option. Logs folder was not cleared.")
    except Exception as e:
        print(f"Error handling logs folder: {e}")
        
def main():
    choice = display_welcome_message()
    if choice == '1':
        # Request the base URL from the user
        base_url = input("Please enter the base URL: ")
        # Request the send rate from the user
        send_rate = input("Choose the request send rate (low, medium, high): ")
        # Path to the directory containing the test scripts
        test_scripts_dir = pathlib.Path('./payloads_Multilidae')  # Update this path as needed

        # List to store the test results
        test_results = []
        
        # Variables to store aggregated totals
        total_aggregated_tests = 0
        aggregated_passed_tests = 0
        aggregated_failed_tests = 0

        # Iterating over each test script and executing it
        for test_script in test_scripts_dir.glob('*.py'):
            if test_script.name != 'run_all_tests.py':  # Ignore the main script
                print(f'Executing: {test_script.name}')
                # Pass the send rate as an argument to each test script
                result = run_test_script(script_path=test_script, base_url=base_url, send_rate=send_rate)
                test_results.append((test_script.name, result))

        # Displaying the unique results
        for script_name, result in test_results:
            print(f'Result of {script_name}:\n{result}\n{"-"*60}\n')
            
        
        # Use a more general pattern to find all result files
        filename_pattern = 'results_*.json'

        # Read and summarize the results from all generated JSON files
        for result_file in logs_dir.glob(filename_pattern):
            with open(result_file, 'r') as file:
                result = json.load(file)
                total_aggregated_tests += result['total_tests']
                aggregated_passed_tests += result['tests_passed']
                aggregated_failed_tests += result['tests_failed']

        # Print aggregated totals
        print(f'\nAggregated Results from All Scripts:')
        print(f'Total Tests: {total_aggregated_tests}')
        print(f'Tests Passed: {aggregated_passed_tests}')
        print(f'Tests Failed: {aggregated_failed_tests}')
        
    elif choice == '2':
         # Request the base URL from the user
        base_url = input("Please enter the base URL: ")
        # Request the send rate from the user
        send_rate = input("Choose the request send rate (low, medium, high): ")
        # Path to the directory containing the test scripts
        test_scripts_dir = pathlib.Path('./payloads_DVWA')  # Update this path as needed

        # List to store the test results
        test_results = []
        
        # Variables to store aggregated totals
        total_aggregated_tests = 0
        aggregated_passed_tests = 0
        aggregated_failed_tests = 0

        # Iterating over each test script and executing it
        for test_script in test_scripts_dir.glob('*.py'):
            if test_script.name != 'run_all_tests.py':  # Ignore the main script
                print(f'Executing: {test_script.name}')
                # Pass the send rate as an argument to each test script
                result = run_test_script(script_path=test_script, base_url=base_url, send_rate=send_rate)
                test_results.append((test_script.name, result))

        # Displaying the unique results
        for script_name, result in test_results:
            print(f'Result of {script_name}:\n{result}\n{"-"*60}\n')
        
        # Use a more general pattern to find all result files
        filename_pattern = 'results_*.json'

        # Read and summarize the results from all generated JSON files
        for result_file in logs_dir.glob(filename_pattern):
            with open(result_file, 'r') as file:
                result = json.load(file)
                total_aggregated_tests += result['total_tests']
                aggregated_passed_tests += result['tests_passed']
                aggregated_failed_tests += result['tests_failed']

        # Print aggregated totals
        print(f'\nAggregated Results from All Scripts:')
        print(f'Total Tests: {total_aggregated_tests}')
        print(f'Tests Passed: {aggregated_passed_tests}')
        print(f'Tests Failed: {aggregated_failed_tests}')
    
    elif choice == '3':
        print("Exiting Bastion. Goodbye!")
        sys.exit(0)
    else:
        print("Invalid option. Exiting...")
        sys.exit(1)

if __name__ == '__main__':
    main()
    # Function to ask the user about cleaning the 'logs' folder
    clear_logs_folder()