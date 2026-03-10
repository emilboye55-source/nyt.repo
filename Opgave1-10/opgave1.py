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
        try:
            # =========== Læser Input =======================
            INPUT_RAW = client.read_area(AREA_IN, 1, 0, 1) # Læs 1 byte fra input (PE)
            OUTPUT_RAW = client.read_area(AREA_OUT, 1, 0, 1) # Læs 1 byte fra output (PA)
        except Exception as e:
            print(f"Fejl ved læsning af input/output: {e}")
            time.sleep(1)
            continue

        # =========== Logik ============================
        S1 = get_bool(INPUT_RAW, 0, 0)  # i00 (NO)
        S2 = get_bool(INPUT_RAW, 0, 1)  # i01 (NO)
        S3 = get_bool(INPUT_RAW, 0, 2)  # i02 (NC)
        Q1 = S1 and S2 and not S3

        # =========== Skriv Output =====================
        set_bool(OUTPUT_RAW, 0, 0, Q1) # Sæt Q1 (q00) efter logik
        try:
            client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW) # Skriv output tilbage
        except Exception as e:
            print(f"Fejl ved skrivning af output: {e}")

        # Print kun når Q1 ændrer sig
        if 'last_Q1' not in locals() or Q1 != last_Q1:
            print(f"S1: {S1} | S2: {S2} | S3: {S3} | Q1: {Q1}")
        last_Q1 = Q1
        time.sleep(0.035) # Vent i 35 ms før næste cyklus
except KeyboardInterrupt:
    print("Program stoppet af bruger.")
except Exception as e:
    print("Der opstod en fejl:", e)

finally:
    client.disconnect()
    print("Forbindelse lukket.")
    client.destroy()