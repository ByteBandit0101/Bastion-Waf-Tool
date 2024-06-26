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
import webbrowser

logs_dir = Path('./logs')
logs_dir.mkdir(exist_ok=True)

def run_test_script(script_path, base_url, send_rate):
    command = ['python', str(script_path), base_url, send_rate]
    completed_process = subprocess.run(command, text=True, capture_output=True)
    return completed_process.stdout

def generate_html_report():
    logs_dir = Path('logs')
    report_template_path = Path('templates/report_template.html')
    report_output_path = logs_dir / 'test_results.html'
    
    test_data_rows = ''
    total_tests = 0
    tests_passed = 0
    tests_failed = 0
    test_data = {
        'labels': [],
        'passed_data': [],
        'failed_data': []
    }
    
    for log_file in logs_dir.glob('results_*.json'):
        with open(log_file, 'r') as file:
            log_data = json.load(file)
            total_tests += log_data['total_tests']
            tests_passed += log_data['tests_passed']
            tests_failed += log_data['tests_failed']
            test_data_rows += f"<tr><td>{log_file.stem}</td><td>{log_data['tests_passed']}</td><td>{log_data['tests_failed']}</td></tr>"
            test_data['labels'].append(log_file.stem)
            test_data['passed_data'].append(log_data['tests_passed'])
            test_data['failed_data'].append(log_data['tests_failed'])
    
    with open(report_template_path, 'r') as file:
        report_html = file.read()
    
    report_html = report_html.replace('{{test_data_rows}}', test_data_rows)
    report_html = report_html.replace('{{total_tests}}', str(total_tests))
    report_html = report_html.replace('{{tests_passed}}', str(tests_passed))
    report_html = report_html.replace('{{tests_failed}}', str(tests_failed))
    report_html = report_html.replace('{{test_data}}', json.dumps(test_data))
    
    with open(report_output_path, 'w') as file:
        file.write(report_html)
    
    report_output_path = report_output_path.absolute()
    webbrowser.open_new_tab(report_output_path.as_uri())

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
    print("1. Use Tor")
    print("2. Do not use Tor")
    print("3. Exit")
    
    while True:
        choice = input("Choose an option (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")

def ask_test_mode():
    print("Do you want to run all tests automatically or select them manually?")
    print("1. Run all tests automatically")
    print("2. Select tests manually")
    
    while True:
        choice = input("Choose an option (1 or 2): ")
        if choice in ['1', '2']:
            return choice
        print("Invalid input. Please enter 1 or 2.")

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
    while choice not in ['clear', 'save']:
        print("Invalid choice. Please enter 'clear' or 'save'.")
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

    use_tor = choice == '1'
    
    if use_tor:
        print("1. Explore Mutillidae with Tor")
        print("2. Explore DVWA with Tor")
    else:
        print("1. Explore Mutillidae without Tor")
        print("2. Explore DVWA without Tor")
        
    while True:
        test_choice = input("Choose an option (1 or 2): ")
        if test_choice in ['1', '2']:
            break
        print("Invalid input. Please enter 1 or 2.")
    
    base_url = input("Please enter the base URL: ")
    send_rate = input("Choose the request send rate (low, medium, high): ")
    
    if test_choice == '1':
        test_scripts_dir = pathlib.Path('./Payloads/payloads_Mutilidae/With_Tor') if use_tor else pathlib.Path('./Payloads/payloads_Mutilidae/Whitout_Tor')
    else:
        test_scripts_dir = pathlib.Path('./Payloads/payloads_DVWA/With_Tor') if use_tor else pathlib.Path('./Payloads/payloads_DVWA/Without_Tor')
        
    test_mode = ask_test_mode()

    for test_script in test_scripts_dir.glob('*.py'):
        if test_script.name != 'run_all_tests.py':
            if test_mode == '2':
                execute = input(f"Do you want to execute {test_script.name}? (yes/no): ")
                while execute.lower() not in ['yes', 'no']:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    execute = input(f"Do you want to execute {test_script.name}? (yes/no): ")
                if execute.lower() != 'yes':
                    continue
            print(f"Executing: {test_script.name}")
            print("")
            result = run_test_script(test_script, base_url, send_rate)
            print(f"Result of {test_script.name}:\n{result}\n{'-'*60}")

    aggregate_results()
    generate_html_report()
    clear_or_save_logs()

if __name__ == '__main__':
    main()
