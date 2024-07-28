import argparse
import subprocess
import time
import threading
import re
import signal
import select
import os
import psutil
from datetime import datetime, timedelta

stop_flag = threading.Event()

def terminate_process(process, worker_id):
    if process is None:
        return

    print(f"Worker {worker_id}: Forcefully terminating process...")
    try:
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        
        for child in children:
            child.terminate()
        parent.terminate()

        gone, alive = psutil.wait_procs(children + [parent], timeout=3)
        
        for p in alive:
            print(f"Worker {worker_id}: Force killing process {p.pid}")
            p.kill()

    except psutil.NoSuchProcess:
        print(f"Worker {worker_id}: Process already terminated")
    except Exception as e:
        print(f"Worker {worker_id}: Error while terminating process - {str(e)}")
    
    # Final check to ensure the process is no longer running
    try:
        os.kill(process.pid, 0)
        print(f"Worker {worker_id}: Process still exists. Force killing...")
        os.kill(process.pid, signal.SIGKILL)
    except OSError:
        pass
    
    print(f"Worker {worker_id}: Process termination completed")

def run_worker(command, worker_id, silent):
    if not silent:
        print(f"Starting Worker {worker_id}")
    else:
        print(f"Worker {worker_id}: Started")

    process = None
    last_inference_time = datetime.now()
    
    while not stop_flag.is_set():
        if process is None or process.poll() is not None:
            if process is not None:
                print(f"Worker {worker_id}: Restarting")
                terminate_process(process, worker_id)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
            last_inference_time = datetime.now()

        try:
            # Use select for non-blocking read with a timeout
            ready, _, _ = select.select([process.stdout], [], [], 60.0)  # 60-second timeout
            if ready:
                line = process.stdout.readline()
                if not line:
                    continue

                if not silent:
                    print(f"Worker {worker_id}: {line.strip()}")
                
                if re.search(r'\[.*\]: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z \d+ Inference finished from subscription instance\..*\.inference\.', line):
                    last_inference_time = datetime.now()
            else:
                # No output for 60 seconds, check if process is still responsive
                if process.poll() is None:
                    print(f"Worker {worker_id}: No output for 60 seconds. Checking process...")
                    # Send a signal to the process to check if it's responsive
                    process.send_signal(signal.SIGURG)
                    time.sleep(1)
                    if process.poll() is None:
                        print(f"Worker {worker_id}: Process is still running but unresponsive. Restarting...")
                        terminate_process(process, worker_id)
                        process = None
                        last_inference_time = datetime.now()
                
            if datetime.now() - last_inference_time > timedelta(minutes=5):
                print(f"Worker {worker_id}: No inference finished for 5 minutes. Restarting...")
                terminate_process(process, worker_id)
                process = None
                last_inference_time = datetime.now()

        except Exception as e:
            print(f"Worker {worker_id}: Error - {str(e)}. Restarting...")
            terminate_process(process, worker_id)
            process = None
            time.sleep(5)  # Wait a bit before restarting to avoid rapid restarts in case of persistent errors

    if process:
        print(f"Worker {worker_id}: Stopping")
        terminate_process(process, worker_id)

def signal_handler(signum, frame):
    print("\nCtrl+C pressed. Stopping all workers...")
    stop_flag.set()

def main():
    parser = argparse.ArgumentParser(description="Run Kuzco workers in parallel")
    parser.add_argument("command", help="Kuzco worker command to run")
    parser.add_argument("instances", type=int, help="Number of instances to run in parallel")
    parser.add_argument("--silent", action="store_true", help="Enable silent mode (only output logs about starting/restarting workers)")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

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
