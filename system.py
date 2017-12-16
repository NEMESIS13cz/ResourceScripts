import psutil
import time
import cpuinfo

data = ""

cpui = cpuinfo.get_cpu_info()
data += "\t\"cpu\": {\n"
data += "\t\t\"threads\": \"" + str(psutil.cpu_count(logical=True)) + "\",\n"
data += "\t\t\"cores\": \"" + str(psutil.cpu_count(logical=False)) + "\",\n"
stats = psutil.cpu_stats()
data += "\t\t\"context_switches\": \"" + str(stats.ctx_switches) + "\",\n"
data += "\t\t\"interrupts\": \"" + str(stats.interrupts) + "\",\n"
data += "\t\t\"soft_interrupts\": \"" + str(stats.soft_interrupts) + "\",\n"
data += "\t\t\"architecture\": \"" + cpui["arch"] + "\",\n"
data += "\t\t\"vendor\": \"" + cpui["brand"] + "\",\n"
data += "\t\t\"frequency\": \"" + str(cpui["hz_actual_raw"][0]) + "\",\n"
data += "\t\t\"base_frequency\": \"" + str(cpui["hz_advertised_raw"][0]) + "\",\n"
data += "\t\t\"vendor_id\": \"" + cpui["vendor_id"] + "\",\n"
data += "\t\t\"bits\": \"" + str(cpui["bits"]) + "\",\n"
data += "\t\t\"cache\": \"" + str(cpui["l2_cache_size"]) + "\",\n"
data += "\t\t\"cores\": {\n"
counter = 0
cores = psutil.cpu_times_percent(interval=1, percpu=True)
for times in cores:
    data += "\t\t\t\"" + str(counter) + "\": {\n"
    data += "\t\t\t\t\"nice\": \"" + str(times.nice) + "\",\n"
    data += "\t\t\t\t\"iowait\": \"" + str(times.iowait) + "\",\n"
    data += "\t\t\t\t\"irq\": \"" + str(times.irq) + "\",\n"
    data += "\t\t\t\t\"softirq\": \"" + str(times.softirq) + "\",\n"
    data += "\t\t\t\t\"steal\": \"" + str(times.steal) + "\",\n"
    data += "\t\t\t\t\"guest\": \"" + str(times.guest) + "\",\n"
    data += "\t\t\t\t\"guest_nice\": \"" + str(times.guest_nice) + "\",\n"
    data += "\t\t\t\t\"idle\": \"" + str(times.idle) + "\",\n"
    data += "\t\t\t\t\"system\": \"" + str(times.system) + "\",\n"
    data += "\t\t\t\t\"user\": \"" + str(times.user) + "\"\n"
    counter += 1
    if counter == len(cores):
        data += "\t\t\t}\n"
    else:
        data += "\t\t\t},\n"
data += "\t\t}\n"
data += "\t},\n"
data += "\t\"memory\": {\n"
mem = psutil.virtual_memory()
data += "\t\t\"total\": \"" + str(mem.total) + "\",\n"
data += "\t\t\"available\": \"" + str(mem.available) + "\",\n"
data += "\t\t\"used\": \"" + str(mem.used) + "\",\n"
data += "\t\t\"free\": \"" + str(mem.free) + "\",\n"
data += "\t\t\"active\": \"" + str(mem.active) + "\",\n"
data += "\t\t\"inactive\": \"" + str(mem.inactive) + "\",\n"
data += "\t\t\"buffers\": \"" + str(mem.buffers) + "\",\n"
data += "\t\t\"cached\": \"" + str(mem.cached) + "\",\n"
data += "\t\t\"percentage\": \"" + str(mem.percent) + "\"\n"
data += "\t},\n"

data += "\t\"swap\": {\n"
swap = psutil.swap_memory()
data += "\t\t\"total\": \"" + str(swap.total) + "\",\n"
data += "\t\t\"used\": \"" + str(swap.used) + "\",\n"
data += "\t\t\"free\": \"" + str(swap.free) + "\",\n"
data += "\t\t\"in\": \"" + str(swap.sin) + "\",\n"
data += "\t\t\"out\": \"" + str(swap.sout) + "\",\n"
data += "\t\t\"percentage\": \"" + str(swap.percent) + "\"\n"
data += "\t},\n"

data += "\t\"network\": {\n"
netlist = psutil.net_io_counters(pernic=True)
counter = 0
for nic in netlist:
    net = netlist[nic]
    data += "\t\t\"" + nic + "\": {\n"
    data += "\t\t\t\"bytes_sent\": \"" + str(net.bytes_sent) + "\",\n"
    data += "\t\t\t\"bytes_recv\": \"" + str(net.bytes_recv) + "\",\n"
    data += "\t\t\t\"packets_sent\": \"" + str(net.packets_sent) + "\",\n"
    data += "\t\t\t\"packets_recv\": \"" + str(net.packets_recv) + "\"\n"
    counter += 1
    if counter == len(netlist):
        data += "\t\t}\n"
    else:
        data += "\t\t},\n"
data += "\t},\n"

data += "\t\"other\": {\n"
boot = psutil.boot_time();
data += "\t\t\"uptime\": \"" + str(int(time.time() - boot)) + "\"\n"
data += "\t},\n"

temps = psutil.sensors_temperatures()
for sensor in temps:
    if sensor == "coretemp":
        data += "\t\"temperatures\": {\n"
        temps2 = temps[sensor];
        counter = 0
        for temp in temps2:
            data += "\t\t\"" + temp.label + "\": {\n"
            data += "\t\t\t\"current\": \"" + str(temp.current) + "\",\n"
            data += "\t\t\t\"high\": \"" + str(temp.high) + "\",\n"
            data += "\t\t\t\"critical\": \"" + str(temp.critical) + "\"\n"
            counter += 1
            if counter == len(temps2):
                data += "\t\t}\n"
            else:
                data += "\t\t},\n"
        data += "\t}"

print(data)
