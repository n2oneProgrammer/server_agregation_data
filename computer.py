import postgres
import psutil
import threading

def add_computer_data():
    cpu_times = psutil.cpu_times_percent()
    postgres.push_command(
        "INSERT INTO computer_params.cpu_times(\"user\", nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (
            cpu_times.user, cpu_times.nice, cpu_times.system, cpu_times.idle, cpu_times.iowait, cpu_times.irq,
            cpu_times.softirq, cpu_times.steal, cpu_times.guest, cpu_times.guest_nice
        ))

    cpu_usage = psutil.cpu_percent()
    cpu_freq = psutil.cpu_freq().current
    memory_usage = psutil.virtual_memory().percent
    memory_swap_usage = psutil.swap_memory().percent
    cpu_temperature = psutil.sensors_temperatures()['cpu_thermal'][0].current

    postgres.push_command(
        "INSERT INTO computer_params.system_params(cpu_usage, cpu_freq, memory_usage, memory_swap_usage, cpu_temperature) VALUES (%s,%s,%s,%s)",
        (cpu_usage, cpu_freq, memory_usage, memory_swap_usage, cpu_temperature))

    threading.Timer(60, add_computer_data).start()


add_computer_data()
