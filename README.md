# ResourceScripts
Simple Resource Monitoring Scripts in Python with JSON output

Dependencies:
```
psutil
py-cpuinfo
PySensors
```

Disk and System scripts are separate because the disk script can take quite a while to process if there is intensive disk I/O and should **not** be run as often as the system script (that being every second)
