# cpu_monitor
# Overview

This script continuously monitors the CPU utilization on your system and logs the data into a file. It also offers an option to stress the CPU by running an intensive computation (calculating large factorials). The script provides logs to track CPU utilization levels and can help in performance monitoring, load testing, or troubleshooting. Additionally, the script manages log files, keeping only the most recent ones and archiving or deleting old logs as needed.

## Key Features

- **CPU Monitoring**: Continuously tracks CPU usage using `psutil.cpu_percent()`.
- **CPU Usage Levels**: Categorizes CPU usage into:
  - **Idle**: CPU usage is below 20%.
  - **Normal**: CPU usage is between 20% and 50%.
  - **High**: CPU usage is between 50% and 80%.
  - **Warning**: CPU usage is between 80% and 99%.
  - **Critical**: CPU usage is above 99%.
- **Logging**: Logs every CPU usage measurement, including its category.
- **Log Rotation**: Log files are rotated when they exceed 5 KB in size.
- **Log Cleanup**: 
  - Empty log files are automatically deleted.
  - Non-empty log files are moved to an archive folder (`archived_logs`).
  - If there are more than 10 archived logs, older logs are deleted to keep the archive organized.
  
- **Stress Testing**: Optionally, the script can stress the CPU by performing intensive computations (calculating large factorials).

## Graceful Shutdown

- The script can be interrupted using **Ctrl + C**.
- Upon interruption, the script gracefully terminates the monitoring and stress processes, cleans up the log files, and manages the archived logs.


### Discussion and Answers

#### 1. How to test the solution without overloading the CPU of the actual system?

To test the solution without overloading the CPU, we can use a **virtual machine** to simulate the load in an isolated environment. Tools like Docker or VirtualBox allow for testing without affecting the host system. 

#### 2. How to add a critical event warning if the CPU stays in a critical state for a long period?

The script currently shows a warning in the command line if the CPU remains in a critical state (above 99%) for a prolonged time. To improve, a **custom notification** (e.g., email, desktop alert) could be added to notify the user more effectively if the CPU stays critical for too long.
