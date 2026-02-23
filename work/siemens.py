import snap7
from snap7.util import get_bool, get_int, get_real


ip_adress = "192.168.0.1"
Slot = 1
Rack = 0
DB_number = 1
Start_offset = 0
Bool_size = 1

client = snap7.client.Client()
client.connect(ip_adress, Rack, Slot)

print("Alt det gik fint")
mybool = client.db_read(DB_number, Start_offset, Bool_size)
DBX00 = get_bool(mybool, 0, 2)
print(DBX00)

myint = client.db_read(DB_number, 2, 2)
DBX20 = get_int(myint, 0)  # Read 2 bytes starting from offset 2
print(DBX20)

myreal = client.db_read(DB_number, 8, 4)
DBX80 = get_real(myreal, 0)
print(DBX80)

client.disconnect()
client.destroy()