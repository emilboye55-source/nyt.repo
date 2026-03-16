import snap7
from snap7.util import get_bool, set_bool
from snap7.type import Area
import sys
import time
import Myfunctions
import csv
from datetime import datetime
tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Program startede kl: {tid}")
# =================== PLC Konfiguration =================
PLC_IP = '192.168.0.1'  # Erstat med din PLC's IP-adresse
RACK = 0
SLOT = 1

AREA_IN = snap7.Area.PE
    trin = 1
    try:
        while True:
            #==================first scan==========================
            if first_scan:
                print("Første scan - initialisering")
                first_scan = False
            # =========== Læser Input =======================
            INPUT_RAW = client.read_area(AREA_IN, 1, 0, 1) # Læs 1 byte fra input (PE)
            OUTPUT_RAW = client.read_area(AREA_OUT, 1, 0, 1) # Læs 1 byte fra output (PA)
            i00 = get_bool(INPUT_RAW, 0, 0) # Læs bit 0 fra input
            i01 = get_bool(INPUT_RAW, 0, 1) # Læs bit 1 fra input
            i02 = get_bool(INPUT_RAW, 0, 2) # Læs bit 2 fra input 
            i03 = get_bool(INPUT_RAW, 0, 3) # Læs bit 3 fra input
            # q00, q01, q02 styres af sekvensen
            q00 = False
            q01 = False
            q02 = False

            match trin:
                case 1:
                    # Vente-position: venter på start (i00)
                    if i00:
                        print("Start registreret, går til trin 2")
                        trin = 2
                    # q00 forbliver False
                case 2:
                    # Aktiver q00 indtil i03 aktiveres
                    q00 = True
                    if i03:
                        print("i03 aktiveret, går til trin 3")
                        trin = 3
                case 3:
                    # Aktiver q01 i 2 sekunder
                    q01 = True
                    print("Trin 3: q01 aktiv i 2 sekunder")
                    set_bool(OUTPUT_RAW, 0, 0, q00)
                    set_bool(OUTPUT_RAW, 0, 1, q01)
                    set_bool(OUTPUT_RAW, 0, 2, q02)
                    client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW)
                    time.sleep(2)
                    q01 = False
                    print("Trin 3 fuldført, går til trin 4")
                    trin = 4
                case 4:
                    # Aktiver q02 i 2 sekunder, vent evt. på i02
                    q02 = True
                    print("Trin 4: q02 aktiv i 2 sekunder")
                    set_bool(OUTPUT_RAW, 0, 0, q00)
                    set_bool(OUTPUT_RAW, 0, 1, q01)
                    set_bool(OUTPUT_RAW, 0, 2, q02)
                    client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW)
                    time.sleep(2)
                    q02 = False
                    print("Trin 4 fuldført, går tilbage til trin 1")
                    trin = 1

            # =========== Skriv Output =====================
            set_bool(OUTPUT_RAW, 0, 0, q00)
            set_bool(OUTPUT_RAW, 0, 1, q01)
            set_bool(OUTPUT_RAW, 0, 2, q02)
            client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW)
            i02_prev = i02
            time.sleep(0.035) # Vent i 35 ms før næste cyklus
    except KeyboardInterrupt:
        print("Program stoppet af bruger.")
    except Exception as e:
        print("Der opstod en fejl:", e)
    finally:
        client.disconnect()
        print("Forbindelse lukket.")
                    if i00:
                        print("Start registreret, går til trin 2")
                        trin = 2
                    # q00 forbliver False
                case 2:
                    # Aktiver q00 indtil i03 aktiveres
                    q00 = True
                    if i03:
                        print("i03 aktiveret, går til trin 3")
                        trin = 3
                case 3:
                    # Aktiver q01 i 2 sekunder
                    q01 = True
                    print("Trin 3: q01 aktiv i 2 sekunder")
                    set_bool(OUTPUT_RAW, 0, 0, q00)
                    set_bool(OUTPUT_RAW, 0, 1, q01)
                    set_bool(OUTPUT_RAW, 0, 2, q02)
                    client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW)
                    time.sleep(2)
                    q01 = False
                    print("Trin 3 fuldført, går til trin 4")
                    trin = 4
                case 4:
                    # Aktiver q02 i 2 sekunder, vent evt. på i02
                    q02 = True
                    print("Trin 4: q02 aktiv i 2 sekunder")
                    set_bool(OUTPUT_RAW, 0, 0, q00)
                    set_bool(OUTPUT_RAW, 0, 1, q01)
                    set_bool(OUTPUT_RAW, 0, 2, q02)
                    client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW)
                    time.sleep(2)
                    if i02:
                            print("i02 aktiveret, går tilbage til trin 1")
                    q02 = False
                    print("Trin 4 fuldført, går tilbage til trin 1")
                    trin = 1

            # =========== Skriv Output =====================
            set_bool(OUTPUT_RAW, 0, 0, q00)
            set_bool(OUTPUT_RAW, 0, 1, q01)
            set_bool(OUTPUT_RAW, 0, 2, q02)
            client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW)
            i02_prev = i02
finally:
            time.sleep(0.035) # Vent i 35 ms før næste cyklus