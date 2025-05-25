# System Health Monitor

A lightweight Python tool for monitoring system health metrics including CPU usage, memory consumption, disk usage, and disk I/O statistics.

## Features

- **CPU Monitoring**: Real-time CPU usage percentage
- **Memory Monitoring**: Total, available, used memory and usage percentage
- **Disk Monitoring**: Total, used, free disk space and usage percentage
- **Disk I/O Monitoring**: Read and write bytes statistics
- **JSON Output**: Clean, structured output format for easy integration

## Requirements

- Python 3.12 or higher
- psutil library

## Installation

This tool uses PEP 723 inline script metadata, which means dependencies are automatically managed when run with compatible Python package managers.

### Option 1: Using uv (Recommended)

```bash
uv run monitor.py
```

### Option 2: Manual Installation

```bash
pip install psutil
python monitor.py
```

### Option 3: Using pipx

```bash
pipx run monitor.py
```

## Usage

Simply run the script to get current system health metrics:

```bash
python monitor.py
```

## Output Format

The tool outputs a JSON object with the following structure:

```json
{
    "status": "healthy",
    "cpu_usage": 15.2,
    "memory_total": 17179869184,
    "memory_available": 8589934592,
    "memory_used": 8589934592,
    "memory_percent": 50.0,
    "disk_total": 1000204886016,
    "disk_used": 500102443008,
    "disk_free": 500102443008,
    "disk_percent": 50.0,
    "disk_read_bytes": 1234567890,
    "disk_write_bytes": 987654321
}
```

### Field Descriptions

| Field | Description | Unit |
|-------|-------------|------|
| `status` | Overall system health status | String |
| `cpu_usage` | Current CPU usage percentage | Percentage (0-100) |
| `memory_total` | Total system memory | Bytes |
| `memory_available` | Available memory for new processes | Bytes |
| `memory_used` | Currently used memory | Bytes |
| `memory_percent` | Memory usage percentage | Percentage (0-100) |
| `disk_total` | Total disk space (root partition) | Bytes |
| `disk_used` | Used disk space | Bytes |
| `disk_free` | Free disk space | Bytes |
| `disk_percent` | Disk usage percentage | Percentage (0-100) |
| `disk_read_bytes` | Total bytes read from disk since boot | Bytes |
| `disk_write_bytes` | Total bytes written to disk since boot | Bytes |

## Examples

### Basic Usage

```bash
$ python monitor.py
{
    "status": "healthy",
    "cpu_usage": 12.5,
    "memory_total": 17179869184,
    "memory_available": 10737418240,
    "memory_used": 6442450944,
    "memory_percent": 37.5,
    "disk_total": 1000204886016,
    "disk_used": 250051221504,
    "disk_free": 750153664512,
    "disk_percent": 25.0,
    "disk_read_bytes": 5678901234,
    "disk_write_bytes": 1234567890
}
```

### Saving Output to File

```bash
python monitor.py > system_health.json
```

### Using with jq for Formatted Output

```bash
python monitor.py | jq '.'
```

### Extracting Specific Metrics

```bash
# Get only CPU usage
python monitor.py | jq '.cpu_usage'

# Get memory usage percentage
python monitor.py | jq '.memory_percent'

# Get disk usage
python monitor.py | jq '{disk_used, disk_free, disk_percent}'
```

## Integration Examples

### Shell Script Monitoring

```bash
#!/bin/bash
# Simple monitoring script
while true; do
    echo "$(date): $(python monitor.py | jq '.cpu_usage')% CPU"
    sleep 60
done
```

### Python Integration

```python
import subprocess
import json

def get_system_metrics():
    result = subprocess.run(['python', 'monitor.py'], 
                          capture_output=True, text=True)
    return json.loads(result.stdout)

metrics = get_system_metrics()
print(f"CPU Usage: {metrics['cpu_usage']}%")
print(f"Memory Usage: {metrics['memory_percent']}%")
```

### Remote Monitoring via SSH

Monitor system health on remote servers using SSH:

```bash
# Basic remote monitoring
ssh user@remote-server 'python /path/to/monitor.py'

# Monitor multiple servers
for server in server1 server2 server3; do
    echo "=== $server ==="
    ssh user@$server 'python /path/to/monitor.py' | jq '{cpu_usage, memory_percent, disk_percent}'
done

# Continuous remote monitoring with timestamps
ssh user@remote-server 'while true; do echo "$(date): $(python /path/to/monitor.py | jq -c .)"; sleep 300; done'

# Save remote metrics to local file
ssh user@remote-server 'python /path/to/monitor.py' > remote_metrics_$(date +%Y%m%d_%H%M%S).json

# Monitor and alert on high usage
ssh user@remote-server 'python /path/to/monitor.py' | jq -r '
  if .cpu_usage > 80 then "HIGH CPU: " + (.cpu_usage | tostring) + "%" 
  elif .memory_percent > 90 then "HIGH MEMORY: " + (.memory_percent | tostring) + "%" 
  elif .disk_percent > 95 then "HIGH DISK: " + (.disk_percent | tostring) + "%" 
  else "System OK" end'
```

### Automated Remote Monitoring Script

```bash
#!/bin/bash
# remote_monitor.sh - Monitor multiple servers

SERVERS=("server1.example.com" "server2.example.com" "server3.example.com")
USER="monitoring"
SCRIPT_PATH="/opt/monitor.py"

for server in "${SERVERS[@]}"; do
    echo "Checking $server..."
    
    # Get metrics via SSH
    metrics=$(ssh "$USER@$server" "python $SCRIPT_PATH" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        cpu=$(echo "$metrics" | jq -r '.cpu_usage')
        memory=$(echo "$metrics" | jq -r '.memory_percent')
        disk=$(echo "$metrics" | jq -r '.disk_percent')
        
        printf "%-20s CPU: %5.1f%% | Memory: %5.1f%% | Disk: %5.1f%%\n" \
               "$server" "$cpu" "$memory" "$disk"
        
        # Alert if any metric is high
        if (( $(echo "$cpu > 80" | bc -l) )) || \
           (( $(echo "$memory > 90" | bc -l) )) || \
           (( $(echo "$disk > 95" | bc -l) )); then
            echo "  ⚠️  WARNING: High resource usage detected!"
        fi
    else
        echo "  ❌ Failed to connect to $server"
    fi
    echo
done
```

## Notes

- CPU usage is measured over a 1-second interval for accuracy
- Disk metrics are measured for the root partition (`/`)
- Disk I/O counters represent cumulative values since system boot
- Memory values are in bytes; divide by 1024³ for GB conversion
- The tool requires read access to system information (usually available to all users)

## Troubleshooting

### Permission Issues
If you encounter permission errors, ensure the script has read access to system information. This is typically available to all users on most systems.

### Missing psutil
If psutil is not installed:
```bash
pip install psutil
```

### Python Version
Ensure you're using Python 3.12 or higher:
```bash
python --version
```

## License

This tool is provided as-is for system monitoring purposes.
