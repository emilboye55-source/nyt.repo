import snap7
from snap7.util import get_bool, set_bool
from snap7.type import Area
import time
import sys
import Myfunctions

# =================== PLC Konfiguration =================
PLC_IP = '192.168.0.1'  # Erstat med din PLC's IP-adresse
RACK = 0
SLOT = 1

#AREA_IN = snap7.Area.PE
#AREA_OUT = snap7.Area.PA
DB_AREA = snap7.Area.DB

first_scan = True
I00 = False
I01 = False
I02 = False
I03 = False
Q00 = False
Q01 = False
Q02 = False

Fotocelle_old = False 
step = 0
Counter = 0
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
        # =========== First Scan Bit ====================
        if first_scan:
            # Initialiseringskode her
            first_scan = False
        # =========== Læser Input =======================
        #INPUT_RAW = client.read_area(AREA_IN, 1, 0, 1) # Læs 1 byte fra input (PE)
        #OUTPUT_RAW = client.read_area(AREA_OUT, 1, 0, 1) # Læs 1 byte fra output (PA)
        DB_RAW = client.read_area(DB_AREA, 1, 0, 1) # Læs 1 byte fra DB1
        I00 = get_bool(DB_RAW, 0, 0) # Læs bit 0 fra DB1
        I01 = get_bool(DB_RAW, 0, 1) # Læs bit 1 fra DB1
        I02 = get_bool(DB_RAW, 0, 2) # Læs bit 2 fra DB1
        I03 = get_bool(DB_RAW, 0, 3) # Læs bit 3 fra DB1
        Q00 = get_bool(DB_RAW, 0, 4) # Læs bit 4 fra DB1
        Q01 = get_bool(DB_RAW, 0, 5) # Læs bit 5 fra DB1
        Q02 = get_bool(DB_RAW, 0, 6) # Læs bit 6 fra DB1

        # =========== Logik ============================

        if I01: #Reset funktion som sætter til step 0 og nulstiller counteren
            step = 0
            Counter = 0
            print("Reset aktiveret, counter nulstilles.")

        if step == 0: #Standby

            if I00 and Counter < 5: #Hvis start knappen er trykket og counteren er under 5 så start step 1
                step = 1

        if step == 1:

            Q00 = True
        else:
            Q00 = False

        if I02: #Hvis den kapacitive føler bliver aktiveret så gå til step 2
            step = 2

        if step == 2: #Chain transfer løft aktiveres og Chain transfer go aktiveres
            Q01 = True
            Q02 = True
        else:
            Q01 = False
            Q02 = False
        
        if Myfunctions.falling_edge(I03, Fotocelle_old): #Falling edge som deaktiverer chain transfer når den kapacitive føler ikke længere er aktiveret
            Counter += 1
            print(f"Kasse {Counter}/5 passeret fotocelle.")
            step = 3

        if step == 3: #Chain transfer løft og go deaktiveres
            if Counter < 5: #Hvis counteren er 5 eller over så gå tilbage til step 0
                step = 1
            else:
                print("Processen er fuldført 5 gange, tryk på reset.")
                step = 0
                
        set_bool(DB_RAW, 0, 4, Q00)
                
        set_bool(DB_RAW, 0, 5, Q01)
               
        set_bool(DB_RAW, 0, 6, Q02)
        client.write_area(DB_AREA, 1, 0, DB_RAW) # Skriv det muterede bytearray tilbage til output (PA)
                
        Fotocelle_old = I03 #Opdaterer fotocelle_old til den nuværende værdi af I03

        # =========== Skriv Output =====================
        # set_bool(OUTPUT_RAW, 0, 0, True) # Sæt bit 0 i output til True
        # client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW) # Skriv det muterede bytearray tilbage til output (PA)
        time.sleep(0.1) # Vent i 100 ms før næste cyklus
except KeyboardInterrupt:
    print("Program stoppet af bruger.")
except Exception as e:
    print("Der opstod en fejl:", e)

finally:
    client.disconnect()
    print("Forbindelse lukket.")
    client.destroy()