# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "psutil",
# ]
# ///

import psutil
import json

def get_system_health():
    """
    Get the system health metrics including CPU, memory, and disk usage.
    Returns:
        dict: A dictionary containing system health metrics.
    """
    
    disk_io_counters = psutil.disk_io_counters()
    disk_read_bytes = disk_io_counters.read_bytes
    disk_write_bytes = disk_io_counters.write_bytes

    return {
        "status": "healthy",
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_total": psutil.virtual_memory().total,
        "memory_available": psutil.virtual_memory().available,
        "memory_used": psutil.virtual_memory().used,
        "memory_percent": psutil.virtual_memory().percent,
        "disk_total": psutil.disk_usage('/').total,
        "disk_used": psutil.disk_usage('/').used,
        "disk_free": psutil.disk_usage('/').free,
        "disk_percent": psutil.disk_usage('/').percent,
        "disk_read_bytes": disk_read_bytes,
        "disk_write_bytes": disk_write_bytes,
    }

print(json.dumps(get_system_health(), indent=4))
