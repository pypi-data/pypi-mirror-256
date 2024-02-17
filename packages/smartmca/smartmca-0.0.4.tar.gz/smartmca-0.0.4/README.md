# SmartMCA for Caen DT5771

This library allows to interface user code with the Caen DT5771 MCA Firmware.

With the library it is possible to:
- Connect to the MCA
- Configure high-level MCA/PSD processing parameters
- Start, stop reset 1D and 2D spectra
- Dump waveforms

## Code Example

```Python
from smartmca import SmartMCA
from smartmca import ConfigMCA, ConfigIO


mca = SmartMCA()

mca.connect("http://192.168.102.120", "user", "password")
# or mca.connect("http://localhost", "user", "password") if used on
# integrated jupiterlab

mca.get_server_status()

config = mca.get_mca_configuration()

config.trigger_mode = ConfigMCA.TriggerMode.INTERNAL
config.le_threshold = 5000
config.trigger_type = ConfigMCA.TriggerType.LEADING_EDGE

mca.set_mca_configuration(config)


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

```