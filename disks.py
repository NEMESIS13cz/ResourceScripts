import psutil
import subprocess
import sys

partitions = {}

def translate_filesystem_type(fs):
    if fs == "fuseblk":
        return "ntfs"
    elif fs == "hfsplus":
        return "hfs+"
    return fs

data = ""

for partition in psutil.disk_partitions(all=True):
    if (partition.device.startswith("/dev")):
        partitions[partition.device[5:]] = partition

data += "\t\"disks\": {\n"
counters = psutil.disk_io_counters(perdisk=True)
c = 0
for counter in counters:
    io = counters[counter]
    data += "\t\t\"" + counter + "\": {\n"
    data += "\t\t\t\"read_bytes\": \"" + str(io.read_bytes) + "\",\n"
    data += "\t\t\t\"write_bytes\": \"" + str(io.write_bytes) + "\",\n"
    if counter in partitions:
        data += "\t\t\t\"partition\": \"true\",\n"
        disk = partitions[counter]
        usage = psutil.disk_usage(disk.mountpoint)
        data += "\t\t\t\"mount\": \"" + disk.mountpoint + "\",\n"
        data += "\t\t\t\"filesystem\": \"" + translate_filesystem_type(disk.fstype) + "\",\n"
        data += "\t\t\t\"space_total\": \"" + str(usage.total) + "\",\n"
        data += "\t\t\t\"space_used\": \"" + str(usage.used) + "\",\n"
        data += "\t\t\t\"space_free\": \"" + str(usage.free) + "\",\n"
        data += "\t\t\t\"space_percentage\": \"" + str(usage.percent) + "\"\n"
    else:
        data += "\t\t\t\"partition\": \"false\"\n"
    c += 1
    if c == len(counters):
        data += "\t\t}\n"
    else:
        data += "\t\t},\n"
data += "\t}\n"

print(data)
