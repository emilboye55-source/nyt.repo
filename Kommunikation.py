import snap7
from snap7.util import get_bool

# =============================== PLC konfig ============================

PLC_ip = "192.168.0.1"
RACK = 0
SLOT = 1

# =============================== Variabler for DB ============================

DB_number = 1
BOOL_OFFSET = 0
BOOL_SIZE = 1

# =============================== Connection ============================

client = snap7.client.Client()
client.connect(PLC_ip, RACK, SLOT)

# =============================== Reading variables ============================

BOOL_RAW = None
DBX00 = None

BOOL_RAW = client.db_read(DB_number, BOOL_OFFSET, BOOL_SIZE)
DBX00 = get_bool(BOOL_RAW, 0, 0)
print(f"DBX00: {DBX00}")

# ===============================Disconnect ============================

client.disconnect()
client.destroy()