from smartmca import SmartMCA
from smartmca import ConfigMCA, ConfigIO

from matplotlib import pyplot as plt

import time

mca = SmartMCA()

mca.connect("http://192.168.102.120", "user", "password")
mca.get_server_status()
config = mca.get_mca_configuration()

print(config)

config.baseline_hold=3000
config.trigger_mode = ConfigMCA.TriggerMode.INTERNAL
mca.set_mca_configuration(config)

config = mca.get_mca_configuration()

print(config)

config_io = mca.get_io_configuration()
print(config_io)

mca.reset_statistics()

y= mca.oscilloscope_get_data(enable_trace_processing=False)
plt.plot(y.channels[0].analog)
plt.show()

mca.histogram_start()

time.sleep(5)

stats = mca.get_mca_statistics()
print(stats)

x, counts = mca.histogram_get(rebin=16)
#plot x
plt.plot(x)
plt.show()

print(counts)