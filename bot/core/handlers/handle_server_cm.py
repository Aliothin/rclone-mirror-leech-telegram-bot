import shutil
import psutil
from bot.core.get_vars import get_val
from telethon.tl.types import KeyboardButtonCallback
from telethon import events
import time
from ... import uptime
from bot.utils import human_format


async def handle_server_command(message):
    print(type(message))
    if isinstance(message, events.CallbackQuery.Event):
        callbk = True
    else:
        callbk = False

    try:
        # Memory
        mem = psutil.virtual_memory()
        memavailable = human_format.human_readable_bytes(mem.available)
        memtotal = human_format.human_readable_bytes(mem.total)
        mempercent = mem.percent
        memfree = human_format.human_readable_bytes(mem.free)
    except:
        memavailable = "N/A"
        memtotal = "N/A"
        mempercent = "N/A"
        memfree = "N/A"

    try:
        # Frequencies
        cpufreq = psutil.cpu_freq()
        freqcurrent = cpufreq.current
        freqmax = cpufreq.max
    except:
        freqcurrent = "N/A"
        freqmax = "N/A"

    try:
        # Cores
        cores = psutil.cpu_count(logical=False)
        lcores = psutil.cpu_count()
    except:
        cores = "N/A"
        lcores = "N/A"

    try:
        cpupercent = psutil.cpu_percent()
    except:
        cpupercent = "N/A"

    try:
        # Storage
        usage = shutil.disk_usage("/")
        totaldsk = human_format.human_readable_bytes(usage.total)
        useddsk = human_format.human_readable_bytes(usage.used)
        freedsk = human_format.human_readable_bytes(usage.free)
    except:
        totaldsk = "N/A"
        useddsk = "N/A"
        freedsk = "N/A"

    try:
        upb, dlb = 0, 0
        dlb = human_format.human_readable_bytes(dlb)
        upb = human_format.human_readable_bytes(upb)
    except:
        dlb = "N/A"
        upb = "N/A"

    diff = time.time() - uptime
    diff = human_format.human_readable_timedelta(diff)

    if callbk:
        msg = (
            f"<b>BOT UPTIME:-</b> {diff}\n\n"
            "<b>CPU STATS:-</b>\n"
            f"Cores: {cores} Logical: {lcores}\n"
            f"CPU Frequency: {freqcurrent}  Mhz Max: {freqmax}\n"
            f"CPU Utilization: {cpupercent}%\n"
            "\n"
            "<b>STORAGE STATS:-</b>\n"
            f"Total: {totaldsk}\n"
            f"Used: {useddsk}\n"
            f"Free: {freedsk}\n"
            "\n"
            "<b>MEMORY STATS:-</b>\n"
            f"Available: {memavailable}\n"
            f"Total: {memtotal}\n"
            f"Usage: {mempercent}%\n"
            f"Free: {memfree}\n"
            "\n"
            "<b>TRANSFER INFO:</b>\n"
            f"Download: {dlb}\n"
            f"Upload: {upb}\n"
        )
        await message.edit(msg, parse_mode="html", buttons=None)
    else:
        try:
            storage_percent = round((usage.used / usage.total) * 100, 2)
        except:
            storage_percent = 0

        msg = (
            f"<b>BOT UPTIME:-</b> {diff}\n\n"
            f"CPU Utilization: {progress_bar(cpupercent)} - {cpupercent}%\n\n"
            f"Storage used:- {progress_bar(storage_percent)} - {storage_percent}%\n"
            f"Total: {totaldsk} Free: {freedsk}\n\n"
            f"Memory used:- {progress_bar(mempercent)} - {mempercent}%\n"
            f"Total: {memtotal} Free: {memfree}\n\n"
            f"Transfer Download:- {dlb}\n"
            f"Transfer Upload:- {upb}\n"
        )
        await message.reply(msg, parse_mode="html",
                            buttons=[[KeyboardButtonCallback("Get detailed stats.", "fullserver")]])

def progress_bar(percentage):
    # percentage is on the scale of 0-1
    comp = get_val("COMPLETED_STR")
    ncomp = get_val("REMAINING_STR")
    pr = ""

    if isinstance(percentage, str):
        return "NaN"

    try:
        percentage = int(percentage)
    except:
        percentage = 0

    for i in range(1, 11):
        if i <= int(percentage / 10):
            pr += comp
        else:
            pr += ncomp
    return pr                            