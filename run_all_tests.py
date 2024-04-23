import subprocess
import pathlib
import sys
import json
from pathlib import Path
import shutil
import datetime
import zipfile
import tkinter as tk
from tkinter import filedialog
import os

logs_dir = Path('./logs')
logs_dir.mkdir(exist_ok=True)

def run_test_script(script_path, base_url, send_rate):
    command = ['python', str(script_path), base_url, send_rate]
    completed_process = subprocess.run(command, text=True, capture_output=True)
    return completed_process.stdout

def display_welcome_message():
    ascii_art = """
     ____           _____ _______ _____ ____  _   _ 
    |  _ \   /\    / ____|__   __|_   _/ __ \| \ | |
    | |_) | /  \  | (___    | |    | || |  | |  \| |
    |  _ < / /\ \  \___ \   | |    | || |  | | . ` | 
    | |_) / /__\ \ ____) |  | |   _| |_ |__| | |\  |
    |____/_/    \_\_____/   |_|  |_____\____/|_| \_|
    """
    print(ascii_art)
    print("Welcome to Bastion!\n")
    print("1. Explore Mutillidae")
    print("2. Explore DVWA")
    print("3. Exit")
    return input("Choose an option: ")

def ask_test_mode():
    print("Do you want to run all tests automatically or select them manually?")
    print("1. Run all tests automatically")
    print("2. Select tests manually")
    choice = input("Choose an option (1 or 2): ")
    return choice

def aggregate_results():
    total_tests = 0
    tests_passed = 0
    tests_failed = 0

    for result_file in logs_dir.glob('results_*.json'):
        with open(result_file, 'r') as file:
            result = json.load(file)
            total_tests += result['total_tests']
            tests_passed += result['tests_passed']
            tests_failed += result['tests_failed']

    print(f"\nAggregated Results from All Scripts:")
    print(f"Total Tests: {total_tests}")
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")

def clear_or_save_logs():
    choice = input("Do you want to clear the logs or save them to a zip file? (clear/save): ").lower()
    if choice == 'clear':
        shutil.rmtree(logs_dir)
        logs_dir.mkdir()
        print("Logs cleared successfully.")
    elif choice == 'save':
        today = datetime.datetime.now()
        zip_filename = f'logs_{today.strftime("%Y-%m-%d_%H-%M-%S")}.zip'
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(logs_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)
        print(f"Logs saved to {zip_filename}.")
        root = tk.Tk()
        root.withdraw()
        save_path = filedialog.asksaveasfilename(initialfile=zip_filename)
        shutil.move(zip_filename, save_path)
        print(f"Logs saved to {save_path}.")
        shutil.rmtree(logs_dir)
        logs_dir.mkdir()
    else:
        print("Invalid choice. No action taken.")

def main():
    choice = display_welcome_message()
    if choice == '3':
        print("Exiting Bastion. Goodbye!")
        sys.exit(0)

    base_url = input("Please enter the base URL: ")
    send_rate = input("Choose the request send rate (low, medium, high): ")
    test_scripts_dir = pathlib.Path('./payloads_Multilidae') if choice == '1' else pathlib.Path('./payloads_DVWA')
    test_mode = ask_test_mode()

    for test_script in test_scripts_dir.glob('*.py'):
        if test_script.name != 'run_all_tests.py':
            if test_mode == '2':
                execute = input(f"Do you want to execute {test_script.name}? (yes/no): ")
                if execute.lower() != 'yes':
                    continue
            print(f"Executing: {test_script.name}")
            result = run_test_script(test_script, base_url, send_rate)
            print(f"Result of {test_script.name}:\n{result}\n{'-'*60}")

    aggregate_results()
    clear_or_save_logs()

if __name__ == '__main__':
    main()