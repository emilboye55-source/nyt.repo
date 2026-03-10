import snap7
from snap7.util import get_bool, set_bool
from snap7.type import Area
import sys
import time

# =================== PLC Konfiguration =================
PLC_IP = '192.168.0.1'  # Erstat med din PLC's IP-adresse
RACK = 0
SLOT = 1

AREA_IN = snap7.Area.PE
AREA_OUT = snap7.Area.PA

i00 = False
i01 = False
i02 = False
q00 = False


# =================== Opret forbindelse =================

try:
    client = snap7.client.Client()
    client.connect(PLC_IP, RACK, SLOT) # husk tcp_port hvis i bruger server.py
    print("Forbindelse oprettet.")
except Exception as e:
    print("Fejl ved oprettelse af forbindelse:", e)
    sys.exit(1) # Afslut programmet hvis forbindelsen ikke kunne oprettes

try:
    while True:
        # =========== Læser Input =======================

        INPUT_RAW = client.read_area(AREA_IN, 1, 0, 1) # Læs 1 byte fra input (PE)
        OUTPUT_RAW = client.read_area(AREA_OUT, 1, 0, 1) # Læs 1 byte fra output (PA)
        # i00 = get_bool(INPUT_RAW, 0, 0) # Læs bit 0 fra input
        # q00 = get_bool(OUTPUT_RAW, 0, 0) # Læs bit 0 fra output

        # =========== Logik ============================
        i00 = get_bool(INPUT_RAW, 0, 0) # Læs bit 0 fra input
        i01 = get_bool(INPUT_RAW, 0, 1) # Læs bit 1 fra input
        i02 = get_bool(INPUT_RAW, 0, 2) # Læs bit 2 fra input 
        q00 = get_bool(OUTPUT_RAW, 0, 0) # Læs bit 0 fra output

        if i00 and not i01:
            q00 = True
        elif i01:
            q00 = False
        # =========== Skriv Output =====================
        set_bool(OUTPUT_RAW, 0, 0, q00) # Sæt bit 0 i output til q00
        client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW) # Skriv det muterede bytearray tilbage til output (PA)
        time.sleep(0.035) # Vent i 35 ms før næste cyklus
except KeyboardInterrupt:
    print("Program stoppet af bruger.")
except Exception as e:
    print("Der opstod en fejl:", e)

finally:
    client.disconnect()
    print("Forbindelse lukket.")
    client.destroy()