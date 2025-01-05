import psutil
import time
import shutil
import math
import os
from loguru import logger
from datetime import datetime
from multiprocessing import Process

# Get the process ID of the current Python script
process_name = os.getpid()

# Define the directory for logs and the archive directory
log_dir = os.getcwd() 
archive_dir = os.path.join(log_dir, "archived_logs") 

# Create archive directory if it doesn't exist
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

# Set up logging with log rotation for the current process
logger.add(
    f"{log_dir}\\cpu_monitor_test_{process_name}.log", 
    rotation="1 KB",  # Log rotation based on file size (1KB)
    level="INFO",     # Set log level to INFO
    enqueue=True      # Ensures logs are written asynchronously
)

# Function to categorize CPU utilization levels
def get_cpu_level(cpu_percent):
    if cpu_percent < 20:
        return "Idle"
    elif cpu_percent < 50:
        return "Normal"
    elif cpu_percent < 80:
        return "High"
    elif cpu_percent < 99:
        return "Warning"
    else:
        return "Critical"

# Function to monitor CPU usage continuously
def monitor_cpu():
    while True:
        try:
            # Measure CPU usage percentage at regular intervals
            cpu_percent = psutil.cpu_percent(interval=3)
            level = get_cpu_level(cpu_percent)
            
            # Log and display CPU usage and its level
            logger.info(f"CPU Utilization: {cpu_percent}% - Level: {level}")
            print(f"{datetime.now()} - CPU: {cpu_percent}% - Level: {level}")
            
            # If CPU usage exceeds 99%, log a critical warning
            if cpu_percent > 99:
                logger.critical("CPU Critical Level Sustained!")
                print("WARNING: CPU CRITICAL LEVEL SUSTAINED!")
            
            time.sleep(0.5)  # Wait for half a second before checking again
        except KeyboardInterrupt:
            # Stop monitoring if the user interrupts the process
            print("KeyboardInterrupt caught in monitor_cpu. Stopping the CPU monitor process.")
            break  

# Function to stress the CPU by calculating large factorials (infinite loop)
def stress_cpu():
    while True:
        try:
            # Continuously compute large factorials to stress the CPU
            math.factorial(2147483647)
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt to stop the stress_cpu function
            print("KeyboardInterrupt caught in stress_cpu. Stopping the CPU stress process.")
            logger.info("KeyboardInterrupt caught in stress_cpu. Stopping the CPU stress process.")
            break  # Break the loop and stop the stress process


# Function to clean up the log files
def cleanup_logs():
    """Manages empty log files and moves non-empty ones to an archive folder."""
    for file in os.listdir(log_dir):
        if file.startswith("cpu_monitor_test_") and file.endswith(".log"):
            file_path = os.path.join(log_dir, file)

            # If the log file is empty, delete it
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                print(f"Deleted empty log file: {file}")
            else:
                # Otherwise, move the log file to the archive directory
                shutil.move(file_path, os.path.join(archive_dir, file))
                print(f"Moved log file to archive: {file}")

# Function to clean up old log files in the archive
def cleanup_old_logs():
    # Get the list of log files in the archive
    log_files = [f for f in os.listdir(archive_dir)]
    
    # If there are more than 10 archived logs, delete the oldest ones
    if len(log_files) > 10:
        log_files.sort(key=lambda f: os.path.getmtime(os.path.join(archive_dir, f)))  # Sort by modification time
        files_to_delete = log_files[:-10]  # Identify the files to delete
        
        for file in files_to_delete:
            file_path = os.path.join(archive_dir, file)
            os.remove(file_path)  # Remove the file
            print(f"Deleted old log file: {file}")

# Main block to start the CPU monitoring and stress test
if __name__ == "__main__":
    print("Starting CPU Monitor and Stress Test. Press Ctrl+C to stop.")
    
    # Start the CPU monitor in a separate process
    process_monitor = Process(target=monitor_cpu)
    # Uncomment the next line to start the CPU stress test
    #process_stress = Process(target=stress_cpu)    
    process_monitor.start()
    #process_stress.start()

    try:
        # Wait for the monitoring process to finish (if interrupted)
        process_monitor.join()
        #process_stress.join()
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt and stop processes gracefully
        print("Stopping CPU Monitor and Stress Test.")
        process_monitor.terminate()
        #process_stress.terminate()
        
        # Remove the log handler
        logger.remove()
        print("Cleaning up log files...")
        
        # Clean up log files
        cleanup_logs()
        cleanup_old_logs()
        print("Log cleanup and organization completed.")
