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

AREA_IN = snap7.Area.PE
AREA_OUT = snap7.Area.PA

first_scan = True

I00 = False #Start
I01 = False #Reset
I02 = False #Kapacativ_Føler
I03 = False #Fotocelle
Q00 = False #Bånd
Q01 = False #Chain_Transfer_Løft
Q02 = False #Chain_Transfer_Go
Fotocelle_old = False 
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
        INPUT_RAW = client.read_area(AREA_IN, 1, 0, 1) # Læs 1 byte fra input (PE)
        OUTPUT_RAW = client.read_area(AREA_OUT, 1, 0, 1) # Læs 1 byte fra output (PA)
        # i00 = get_bool(INPUT_RAW, 0, 0) # Læs bit 0 fra input
        # q00 = get_bool(OUTPUT_RAW, 0, 0) # Læs bit 0 fra output

        # =========== Logik ============================
        global Step, Counter

        if I01: #Reset funktion som sætter til step 0 og nulstiller counteren
            step = 0
            Counter = 0
            print("Reset aktiveret, counter nulstilles.")


        match step:
            case 0: #Standby
                if I00 and Counter <5: #Hvis start knappen er trykket og counteren er under 5 så start step 1
                    step = 1

            case 1: #Bånd kører
                Q00 = True
                if I02: #Hvis den kapacitive føler bliver aktiveret så gå til step 2
                    step = 2
            
            case 2: #Chain transfer løft aktiveres og Chain transfer go aktiveres
                Q00 = False
                Q01 = True
                Q02 = True
                if Myfunctions.falling_edge(I03, Fotocelle_old): #Falling edge som tæller counter op når kasse er forbi fotocellen
                    Counter += 1
                    step = 3
            case 3: #Chain transfer løft og go deaktiveres
                Q01 = False
                Q02 = False
                if Counter < 5: #Hvis counteren er 5 eller over så gå tilbage til step 0
                    step = 1
                else:
                    print("Processen er fuldført 5 gange, tryk på reset.")
                    step = 0
                
        Fotocelle_old = I03 #Opdaterer fotocelle_old til den nuværende værdi af I03

        # =========== Skriv Output =====================
        # set_bool(OUTPUT_RAW, 0, 0, True) # Sæt bit 0 i output til True
        # client.write_area(AREA_OUT, 1, 0, OUTPUT_RAW) # Skriv det muterede bytearray tilbage til output (PA)
        time.sleep(0.035) # Vent i 35 ms før næste cyklus
except KeyboardInterrupt:
    print("Program stoppet af bruger.")
except Exception as e:
    print("Der opstod en fejl:", e)

finally:
    client.disconnect()
    print("Forbindelse lukket.")
    client.destroy()