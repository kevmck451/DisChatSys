import subprocess
import time
import atexit


# Start MongoDB and set up cleanup
def start_mongo():
    print("Starting MongoDB...")
    mongo_process = subprocess.Popen(["/opt/homebrew/bin/mongod", "--config", "/opt/homebrew/etc/mongod.conf"])

    # Register cleanup to stop MongoDB when the script exits
    atexit.register(stop_mongo, mongo_process)

    # Wait a moment to ensure it has started, then check if it’s running
    time.sleep(2)
    if mongo_process.poll() is None:
        print("MongoDB is running.")
    else:
        print("Failed to start MongoDB.")


# Stop MongoDB
def stop_mongo(process):
    print("Stopping MongoDB...")
    process.terminate()
    process.wait()
    print("MongoDB stopped.")


if __name__ == "__main__":
    start_mongo()
    try:
        # Keep the script running to keep MongoDB active
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script interrupted by user.")
