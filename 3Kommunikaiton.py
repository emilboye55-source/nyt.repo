from time import sleep
import snap7
from snap7.util import get_bool, set_bool
from snap7.type import Area, Areas

# =============================== PLC varibaler ===========================

PLC_ip = "192.168.0.1"
RACK = 0
SLOT = 1

# =============================== Variabler for Læsning ============================

AREA_INPUT = Area.PE
AREA_OUTPUT = Area.PA
AREA_MEMORY = Area.MK
BOOL_RAW_INPUT = None
BOOL_RAW_OUTPUT = None
BOOL_RAW_MEMORY = None
BOOL_INPUT_OFFSET = 0
BOOL_OUTPUT_OFFSET = 0
BOOL_MEMORY_OFFSET = 0
SIZE = 1
HEJ = True
# =============================== Connection ============================

client = snap7.client.Client()
client.connect(PLC_ip, RACK, SLOT)

# =============================== Main ============================
while True:

    # =============================== Reading variables ============================
    print("Læser input, output og memory variabler...")

    BOOL_RAW_INPUT = client.read_area(AREA_INPUT, 1, BOOL_INPUT_OFFSET, SIZE)
    i00 = get_bool(BOOL_RAW_INPUT, 0, 0)
    print(f"i00 = {i00}")

    BOOL_RAW_OUTPUT = client.read_area(AREA_OUTPUT, 1, BOOL_OUTPUT_OFFSET, SIZE)
    q00 = get_bool(BOOL_RAW_OUTPUT, 0, 0)
    print(f"q00 = {q00}")

    BOOL_RAW_MEMORY = client.read_area(AREA_MEMORY, 1, BOOL_MEMORY_OFFSET, SIZE)
    m00 = get_bool(BOOL_RAW_MEMORY, 0, 0)
    print(f"m00 = {m00}")


    if i00 == True:
        BOOL_RAW_OUTPUT = set_bool(BOOL_RAW_OUTPUT, 0, 0, HEJ)
        client.write_area(AREA_OUTPUT, 0, 0, BOOL_RAW_OUTPUT)
    else:

        BOOL_RAW_INPUT = set_bool(BOOL_RAW_INPUT, 0, 0, HEJ)
        client.write_area(AREA_INPUT, 0, 0, BOOL_RAW_INPUT)
        
        BOOL_RAW_MEMORY = set_bool(BOOL_RAW_MEMORY, 0, 0, HEJ)
        client.write_area(AREA_MEMORY, 0, 0, BOOL_RAW_MEMORY)

    # =============================== Reading variables again============================
    print("Læser input, output og memory variabler efter opdatering...")

    BOOL_RAW_INPUT = client.read_area(AREA_INPUT, 1, BOOL_INPUT_OFFSET, SIZE)
    i00 = get_bool(BOOL_RAW_INPUT, 0, 0)
    print(f"i00 = {i00}")

    BOOL_RAW_OUTPUT = client.read_area(AREA_OUTPUT, 1, BOOL_OUTPUT_OFFSET, SIZE)
    q00 = get_bool(BOOL_RAW_OUTPUT, 0, 0)
    print(f"q00 = {q00}")

    BOOL_RAW_MEMORY = client.read_area(AREA_MEMORY, 1, BOOL_MEMORY_OFFSET, SIZE)
    m00 = get_bool(BOOL_RAW_MEMORY, 0, 0)
    print(f"m00 = {m00}")

    sleep(0.5)

# ===============================Disconnect ============================
client.disconnect()
client.destroy()