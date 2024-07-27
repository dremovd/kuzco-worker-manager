import argparse
import subprocess
import time
import threading
import re
from datetime import datetime, timedelta

def run_worker(command, worker_id, silent):
    if not silent:
        print(f"Starting Worker {worker_id}")
    else:
        print(f"Worker {worker_id}: Started")

    process = None
    last_inference_time = datetime.now()
    
    while True:
        if process is None or process.poll() is not None:
            if process is not None:
                print(f"Worker {worker_id}: Restarting")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            last_inference_time = datetime.now()

        try:
            line = process.stdout.readline()
            if not line:
                time.sleep(1)
                continue

            if not silent:
                print(f"Worker {worker_id}: {line.strip()}")
            
            if re.search(r'\[.*\]: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z \d+ Inference finished from subscription instance\..*\.inference\.', line):
                last_inference_time = datetime.now()
            
            if datetime.now() - last_inference_time > timedelta(minutes=5):
                print(f"Worker {worker_id}: No inference finished for 5 minutes. Restarting...")
                process.terminate()
                process = None
                last_inference_time = datetime.now()

        except Exception as e:
            print(f"Worker {worker_id}: Error - {str(e)}. Restarting...")
            if process:
                process.terminate()
            process = None
            time.sleep(5)  # Wait a bit before restarting to avoid rapid restarts in case of persistent errors

def main():
    parser = argparse.ArgumentParser(description="Run Kuzco workers in parallel")
    parser.add_argument("command", help="Kuzco worker command to run")
    parser.add_argument("instances", type=int, help="Number of instances to run in parallel")
    parser.add_argument("--silent", action="store_true", help="Enable silent mode (only output logs about starting/restarting workers)")
    args = parser.parse_args()

    if not args.silent:
        print(f"Starting {args.instances} workers")

    threads = []
    for i in range(args.instances):
        thread = threading.Thread(target=run_worker, args=(args.command, i, args.silent))
        thread.start()
        threads.append(thread)
        time.sleep(1)  # 1-second pause between starting each worker

    for thread in threads:
        thread.join()

    if not args.silent:
        print("All workers have finished")

if __name__ == "__main__":
    main()
