import time
import subprocess
import sys
import os

SLEEP_TIME_TASK_1 = 1  # Task to run every second
SLEEP_TIME_TASK_2 = 604800  # Task to run every week (7 days in seconds)

def run_task_1():
    print("Running update_average_ratings.py...")
    
    python_path = sys.executable
    manage_py_path = os.path.join(os.getcwd(), 'manage.py')
    
    subprocess.run([python_path, manage_py_path, 'update_average_ratings'])

def run_task_2():
    print("Running update_average_ratings_parameters_weekly.py...")
    
    python_path = sys.executable
    manage_py_path = os.path.join(os.getcwd(), 'manage.py')
    
    subprocess.run([python_path, manage_py_path,  'update_average_ratings_parameters_weekly'])

def main():
    last_run_task_2 = time.time()

    while True:
        run_task_1()
        print(f'Sleeping for {SLEEP_TIME_TASK_1} seconds...')
        time.sleep(SLEEP_TIME_TASK_1)

        if time.time() - last_run_task_2 >= SLEEP_TIME_TASK_2:
            run_task_2()
            last_run_task_2 = time.time()


if __name__ == "__main__":
    main()
