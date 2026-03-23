import snap7
from snap7.util import get_bool, set_bool, get_real
import sys
import time
from datetime import datetime


# PLC Opsætning
PLC_IP = "192.168.0.1"  # Husk at rette denne til din PLC's IP
RACK = 0
SLOT = 1

INPUT_AREA = snap7.type.Area.PE
OUTPUT_AREA = snap7.type.Area.PA
Q00 = True
# Forbindelse til PLC
try:
    client = snap7.client.Client()
    client.connect(PLC_IP, RACK, SLOT)
except Exception as e:
    print("Fejl: ", e)
    sys.exit(1)

# Logik og filhåndtering
try:
    # Opretter filnavn baseret på nuværende tidspunkt
    fileName = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".csv"
    
    with open(fileName, "a", encoding="utf-8") as file:
        file.write("Time, Tank Level, flow\n") # Tilføjede \n for linjeskift i CSV-filen
        try:
            while True:
                input_raw = client.read_area(INPUT_AREA, 1, 0, 8) # Læs 8 bytes (REAL) fra inputområdet
                ID0 = get_real(input_raw, 0) # Læs REAL-værdien fra inputområdet
                ID4 = get_real(input_raw, 4) # Læs REAL-værdien fra inputområdet
                print(f"Tank Level: {ID0} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Flow: {ID4}")

                Output = set_bool(bytearray(8), 0, 0, Q00)
                client.write_area(OUTPUT_AREA, 0, 0, Output) # Skriv output til PLC

                file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {ID0}, {ID4}\n") # Skriv tid og tankniveau til CSV-filen
                file.flush() # Sørg for at data bliver skrevet til filen med det samme
                time.sleep(0.3) # Vent i 0.3 sekunder før næste læsning

        except Exception as e:
            print("Fejl i programmet", e)

        finally:
         client.disconnect()
         client.destroy()
   
except Exception as e:
    print("Fejl i programmet: ", e)