import network
import time
import gc

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
#sta_if.scan()                             # Scan for available access points
sta_if.connect("fablab-wue", "cwurzdfi") # Connect to an AP
while not sta_if.isconnected():                      # Check for successful connection
    time.sleep(0.5)
    print ('Waiting for connection...')

print ('Connected!')

gc.collect()
print (gc.mem_free())
