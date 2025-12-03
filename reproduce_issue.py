import subprocess
import sys
import json
import time

def run_reproduction():
    # Command to run the server as a module
    cmd = [sys.executable, "-m", "code_trajectory.server"]
    
    # Start the server process
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,  # Binary mode
        bufsize=0   # Unbuffered
    )
    
    # JSON-RPC initialization message
    init_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"}
        }
    }
    
    # Serialize to JSON and append CRLF explicitly
    json_str = json.dumps(init_msg)
    # Windows style line ending encoded to utf-8
    input_bytes = (json_str + "\r\n").encode('utf-8')
    
    print(f"Sending bytes: {input_bytes}")
    
    try:
        process.stdin.write(input_bytes)
        process.stdin.flush()
        
        # Read response with timeout
        start_time = time.time()
        while time.time() - start_time < 5:
            if process.poll() is not None:
                print(f"Process exited prematurely with code {process.returncode}")
                stdout, stderr = process.communicate()
                print("STDOUT:", stdout.decode('utf-8', errors='replace'))
                print("STDERR:", stderr.decode('utf-8', errors='replace'))
                return

            line = process.stdout.readline()
            if line:
                print(f"Received bytes: {line}")
                print(f"Received: {line.decode('utf-8', errors='replace').strip()}")
                if b"jsonrpc" in line:
                    if b'\r\n' in line:
                        print("WARNING: Response contains CRLF (\\r\\n) - FIX NOT WORKING")
                    else:
                        print("INFO: Response contains LF (\\n) only - FIX WORKING")
                    
                    print("SUCCESS: Received JSON-RPC response.")
                    process.terminate()
                    return
            time.sleep(0.1)
            
        print("TIMEOUT: No response received within 5 seconds.")
        process.terminate()
        stdout, stderr = process.communicate()
        print("STDOUT:", stdout.decode('utf-8', errors='replace'))
        print("STDERR:", stderr.decode('utf-8', errors='replace'))

    except Exception as e:
        print(f"Exception: {e}")
        process.kill()

if __name__ == "__main__":
    run_reproduction()
