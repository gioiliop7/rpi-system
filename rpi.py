from flask import Flask, jsonify
import os
import psutil
import time
import subprocess

app = Flask(__name__)


# Endpoint to shut down the Raspberry Pi
@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Get the path to the script in the same directory as the Python script
    script_path = os.path.join(os.path.dirname(__file__), 'shutdown.sh')

    # Make sure the script is executable (optional)
    os.chmod(script_path, 0o755)

    # Run the script
    try:
        result = subprocess.run([script_path], check=True, shell=True)
        print("Script executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")


# Endpoint to fetch Raspberry Pi stats
@app.route("/stats", methods=["GET"])
def get_stats():
    try:
        # Get temperature
        temp_output = os.popen("vcgencmd measure_temp").readline()
        temperature = temp_output.replace("temp=", "").strip()

        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        # Get CPU frequency
        cpu_freq = psutil.cpu_freq().current

        # Get CPU temperature per core
        cpu_temp = [
            os.popen(f"cat /sys/class/thermal/thermal_zone{i}/temp").readline().strip()
            for i in range(psutil.cpu_count())
        ]

        # Get memory stats (RAM)
        memory = psutil.virtual_memory()
        memory_total = memory.total / 1024 / 1024  # Convert to MB
        memory_used = memory.used / 1024 / 1024  # Convert to MB
        memory_free = memory.free / 1024 / 1024  # Convert to MB
        memory_available = memory.available / 1024 / 1024  # Convert to MB
        memory_percent = memory.percent  # Percentage used

        # Get swap memory stats
        swap = psutil.swap_memory()
        swap_total = swap.total / 1024 / 1024  # Convert to MB
        swap_used = swap.used / 1024 / 1024  # Convert to MB
        swap_free = swap.free / 1024 / 1024  # Convert to MB
        swap_percent = swap.percent  # Percentage used

        # Get disk stats
        disk = psutil.disk_usage("/")
        disk_total = disk.total / 1024 / 1024 / 1024  # Convert to GB
        disk_used = disk.used / 1024 / 1024 / 1024  # Convert to GB
        disk_free = disk.free / 1024 / 1024 / 1024  # Convert to GB
        disk_percent = disk.percent  # Percentage used

        # Get disk I/O stats
        disk_io = psutil.disk_io_counters()
        disk_read_bytes = disk_io.read_bytes / 1024 / 1024  # MB
        disk_write_bytes = disk_io.write_bytes / 1024 / 1024  # MB

        # Get network stats
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent / 1024 / 1024  # Convert to MB
        bytes_received = net_io.bytes_recv / 1024 / 1024  # Convert to MB

        # Get GPU memory usage
        gpu_mem_output = os.popen("vcgencmd get_mem gpu").readline()
        gpu_memory = gpu_mem_output.replace("gpu=", "").strip()

        # Get uptime
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_hours = uptime_seconds / 3600

        # Get power supply stats
        voltage_output = os.popen("vcgencmd measure_volts").readline()
        voltage = voltage_output.replace("volt=", "").strip()
        throttled_output = os.popen("vcgencmd get_throttled").readline()
        throttled = throttled_output.strip()

        # Get load average (1, 5, 15 minutes)
        load_avg = os.getloadavg()

        # Get serial number
        serial_number = os.popen("cat /proc/cpuinfo | grep Serial").readline().strip()

        # Get Raspberry Pi model
        pi_model = os.popen('cat /proc/cpuinfo | grep "Model"').readline().strip()

        # Create stats dictionary
        stats = {
            "temperature": temperature,
            "cpu_usage": f"{cpu_usage}%",
            "cpu_frequency": f"{cpu_freq} MHz",
            "cpu_temperature": cpu_temp,
            "memory": {
                "total": f"{memory_total:.2f} MB",
                "used": f"{memory_used:.2f} MB",
                "free": f"{memory_free:.2f} MB",
                "available": f"{memory_available:.2f} MB",
                "percent_used": f"{memory_percent}%",
            },
            "swap_memory": {
                "total": f"{swap_total:.2f} MB",
                "used": f"{swap_used:.2f} MB",
                "free": f"{swap_free:.2f} MB",
                "percent_used": f"{swap_percent}%",
            },
            "disk": {
                "total": f"{disk_total:.2f} GB",
                "used": f"{disk_used:.2f} GB",
                "free": f"{disk_free:.2f} GB",
                "percent_used": f"{disk_percent}%",
                "read_bytes": f"{disk_read_bytes:.2f} MB",
                "write_bytes": f"{disk_write_bytes:.2f} MB",
            },
            "network": {
                "bytes_sent": f"{bytes_sent:.2f} MB",
                "bytes_received": f"{bytes_received:.2f} MB",
            },
            "gpu_memory": gpu_memory,
            "uptime": f"{uptime_hours:.2f} hours",
            "power_supply": {
                "voltage": voltage,
                "throttled": throttled,
            },
            "load_avg": load_avg,
            "serial_number": serial_number,
            "pi_model": pi_model,
        }
        return jsonify(stats)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
