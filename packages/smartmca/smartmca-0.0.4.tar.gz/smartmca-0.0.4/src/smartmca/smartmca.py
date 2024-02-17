import json
import requests


from enum import Enum


# Funzione per convertire le stringhe in enum
def convert_to_enum(value, enum):
    for e in enum:
        if e.value == value:
            return e
    return None

# Classe per deserializzare i dati
class ConfigMCA:

    class MCAMode(Enum):
        HARDWARE = "hardware"
        SOFTWARE = "software"

    # Definizione degli enum come specificato
    class TriggerMode(Enum):
        INTERNAL = "internal"
        EXTERNAL = "external"
        LOGIC_OR = "logic_or"
        LOGIC_AND = "logic_and"

    class TriggerType(Enum):
        FAST_TRAPEZOIDAL = "ft"
        LEADING_EDGE = "le"

    class Polarity(Enum):
        NEGATIVE = "negative"
        POSITIVE = "positive"

    class EnergyMode(Enum):
        TRAPEZOIDAL = "trap"
        QDC = "qdc"
        PEAK_HOLDER = "peak"

    class BaselineMode(Enum):
        BASELINE_SHAPER = "baseline_restorer"
        MOVING_AVERAGE = "moving_average"

    class TrapPurMode(Enum):
        NO_PUR = "no_pur"
        SIMPLE_PUR = "simple_pur"
        ADVANCED_PUR = "advanced_pur"
        
    def __init__(self):
        self.mca_mode = ConfigMCA.MCAMode.SOFTWARE
        self.baseline_hold = 10
        self.baseline_len = 10
        self.baseline_mode =  ConfigMCA.BaselineMode.BASELINE_SHAPER
        self.energy_mode = ConfigMCA.EnergyMode.QDC
        self.ft_flat = 1
        self.ft_offset = 0
        self.ft_polarity = ConfigMCA.Polarity.POSITIVE
        self.ft_shaping = 10
        self.ft_tau = 1
        self.ft_threshold = 10
        self.le_delta = 30
        self.le_inib = 25
        self.le_polarity =  ConfigMCA.Polarity.POSITIVE
        self.le_threshold =1000
        self.peak_pileup = 0
        self.peak_sampling = 0
        self.qdc_post_inibit = 100
        self.qdc_pre = 1
        self.qdc_qlong = 100
        self.qdc_qshort = 20
        self.risetime_pre = 0
        self.risetime_start = 0
        self.risetime_stop = 0
        self.risetime_window = 0
        self.trap_flat = 0
        self.trap_gain = 1
        self.trap_offset = 0
        self.trap_pileupinib = 10
        self.trap_polarity = ConfigMCA.Polarity.POSITIVE
        self.trap_pur_mode = ConfigMCA.TrapPurMode.SIMPLE_PUR
        self.trap_sampling = 0
        self.trap_shaping = 0
        self.trap_tau = 0
        self.trigger_mode = ConfigMCA.TriggerMode.INTERNAL 
        self.trigger_type = ConfigMCA.TriggerType.LEADING_EDGE
        
    def process_config_json(self, config):
        self.mca_mode =  config["baseline_hold"]
        self.baseline_hold = config["baseline_hold"]
        self.baseline_len = config["baseline_len"]
        self.baseline_mode = convert_to_enum(config["baseline_mode"], ConfigMCA.BaselineMode)
        self.energy_mode = convert_to_enum(config["energy_mode"], ConfigMCA.EnergyMode)
        self.ft_flat = config["ft_flat"]
        self.ft_offset = config["ft_offset"]
        self.ft_polarity = convert_to_enum(config["ft_polarity"], ConfigMCA.Polarity)
        self.ft_shaping = config["ft_shaping"]
        self.ft_tau = config["ft_tau"]
        self.ft_threshold = config["ft_threshold"]
        self.le_delta = config["le_delta"]
        self.le_inib = config["le_inib"]
        self.le_polarity = convert_to_enum(config["le_polarity"], ConfigMCA.Polarity)
        self.le_threshold = config["le_threshold"]
        self.peak_pileup = config["peak_pileup"]
        self.peak_sampling = config["peak_sampling"]
        self.qdc_post_inibit = config["qdc_post_inibit"]
        self.qdc_pre = config["qdc_pre"]
        self.qdc_qlong = config["qdc_qlong"]
        self.qdc_qshort = config["qdc_qshort"]
        self.risetime_pre = config["risetime_pre"]
        self.risetime_start = config["risetime_start"]
        self.risetime_stop = config["risetime_stop"]
        self.risetime_window = config["risetime_window"]
        self.trap_flat = config["trap_flat"]
        self.trap_gain = config["trap_gain"]
        self.trap_offset = config["trap_offset"]
        self.trap_pileupinib = config["trap_pileupinib"]
        self.trap_polarity = convert_to_enum(config["trap_polarity"], ConfigMCA.Polarity)
        self.trap_pur_mode = convert_to_enum(config["trap_pur_mode"], ConfigMCA.TrapPurMode)
        self.trap_sampling = config["trap_sampling"]
        self.trap_shaping = config["trap_shaping"]
        self.trap_tau = config["trap_tau"]
        self.trigger_mode = convert_to_enum(config["trigger_mode"], ConfigMCA.TriggerMode)
        self.trigger_type = convert_to_enum(config["trigger_type"], ConfigMCA.TriggerType)

    def to_json(self):
        return {
            "mca_mode" : self.mca_mode,
            "baseline_hold": self.baseline_hold,
            "baseline_len": self.baseline_len,
            "baseline_mode": self.baseline_mode.value,
            "energy_mode": self.energy_mode.value,
            "ft_flat": self.ft_flat,
            "ft_offset": self.ft_offset,
            "ft_polarity": self.ft_polarity.value,
            "ft_shaping": self.ft_shaping,
            "ft_tau": self.ft_tau,
            "ft_threshold": self.ft_threshold,
            "le_delta": self.le_delta,
            "le_inib": self.le_inib,
            "le_polarity": self.le_polarity.value,
            "le_threshold": self.le_threshold,
            "peak_pileup": self.peak_pileup,
            "peak_sampling": self.peak_sampling,
            "qdc_post_inibit": self.qdc_post_inibit,
            "qdc_pre": self.qdc_pre,
            "qdc_qlong": self.qdc_qlong,
            "qdc_qshort": self.qdc_qshort,
            "risetime_pre": self.risetime_pre,
            "risetime_start": self.risetime_start,
            "risetime_stop": self.risetime_stop,
            "risetime_window": self.risetime_window,
            "trap_flat": self.trap_flat,
            "trap_gain": self.trap_gain,
            "trap_offset": self.trap_offset,
            "trap_pileupinib": self.trap_pileupinib,
            "trap_polarity": self.trap_polarity.value,
            "trap_pur_mode": self.trap_pur_mode.value,
            "trap_sampling": self.trap_sampling,
            "trap_shaping": self.trap_shaping,
            "trap_tau": self.trap_tau,
            "trigger_mode": self.trigger_mode.value,
            "trigger_type": self.trigger_type.value
        }
        
    def __str__(self):
        properties = vars(self)
        return '\n'.join([f'{key}: {value}' for key, value in properties.items() if key.startswith('_')])
    
    @property
    def mca_mode(self):
        return self._mca_mode
    @mca_mode.setter
    def mca_mode(self, value):
        self._mca_mode = value

    @property
    def baseline_hold(self):
        return self._baseline_hold
    
    @baseline_hold.setter
    def baseline_hold(self, value):
        self._baseline_hold = value
    
    @property
    def baseline_len(self):
        return self._baseline_len
    
    @baseline_len.setter
    def baseline_len(self, value):
        self._baseline_len = value
    
    @property
    def baseline_mode(self):
        return self._baseline_mode
    
    @baseline_mode.setter
    def baseline_mode(self, value):
        self._baseline_mode = value
    
    @property
    def energy_mode(self):
        return self._energy_mode
    
    @energy_mode.setter
    def energy_mode(self, value):
        self._energy_mode = value
    
    @property
    def ft_flat(self):
        return self._ft_flat
    
    @ft_flat.setter
    def ft_flat(self, value):
        self._ft_flat = value
    
    @property
    def ft_offset(self):
        return self._ft_offset
    
    @ft_offset.setter
    def ft_offset(self, value):
        self._ft_offset = value
    
    @property
    def ft_polarity(self):
        return self._ft_polarity
    
    @ft_polarity.setter
    def ft_polarity(self, value):
        self._ft_polarity = value
    
    @property
    def ft_shaping(self):
        return self._ft_shaping
    
    @ft_shaping.setter
    def ft_shaping(self, value):
        self._ft_shaping = value
    
    @property
    def ft_tau(self):
        return self._ft_tau
    
    @ft_tau.setter
    def ft_tau(self, value):
        self._ft_tau = value
    
    @property
    def ft_threshold(self):
        return self._ft_threshold
    
    @ft_threshold.setter
    def ft_threshold(self, value):
        self._ft_threshold = value
    
    @property
    def le_delta(self):
        return self._le_delta
    
    @le_delta.setter
    def le_delta(self, value):
        self._le_delta = value
    
    @property
    def le_inib(self):
        return self._le_inib
    
    @le_inib.setter
    def le_inib(self, value):
        self._le_inib = value
    
    @property
    def le_polarity(self):
        return self._le_polarity
    
    @le_polarity.setter
    def le_polarity(self, value):
        self._le_polarity = value
    
    @property
    def le_threshold(self):
        return self._le_threshold
    
    @le_threshold.setter
    def le_threshold(self, value):
        self._le_threshold = value
    
    @property
    def peak_pileup(self):
        return self._peak_pileup
    
    @peak_pileup.setter
    def peak_pileup(self, value):
        self._peak_pileup = value
    
    @property
    def peak_sampling(self):
        return self._peak_sampling
    
    @peak_sampling.setter
    def peak_sampling(self, value):
        self._peak_sampling = value
    
    @property
    def qdc_post_inibit(self):
        return self._qdc_post_inibit
    
    @qdc_post_inibit.setter
    def qdc_post_inibit(self, value):
        self._qdc_post_inibit = value
    
    @property
    def qdc_pre(self):
        return self._qdc_pre
    
    @qdc_pre.setter
    def qdc_pre(self, value):
        self._qdc_pre = value
    
    @property
    def qdc_qlong(self):
        return self._qdc_qlong
    
    @qdc_qlong.setter
    def qdc_qlong(self, value):
        self._qdc_qlong = value
    
    @property
    def qdc_qshort(self):
        return self._qdc_qshort
    
    @qdc_qshort.setter
    def qdc_qshort(self, value):
        self._qdc_qshort = value
    
    @property
    def risetime_pre(self):
        return self._risetime_pre
    
    @risetime_pre.setter
    def risetime_pre(self, value):
        self._risetime_pre = value
    
    @property
    def risetime_start(self):
        return self._risetime_start
    
    @risetime_start.setter
    def risetime_start(self, value):
        self._risetime_start = value
    
    @property
    def risetime_stop(self):
        return self._risetime_stop
    
    @risetime_stop.setter
    def risetime_stop(self, value):
        self._risetime_stop = value
    
    @property
    def risetime_window(self):
        return self._risetime_window
    
    @risetime_window.setter
    def risetime_window(self, value):
        self._risetime_window = value
    
    @property
    def trap_flat(self):
        return self._trap_flat
    
    @trap_flat.setter
    def trap_flat(self, value):
        self._trap_flat = value
    
    @property
    def trap_gain(self):
        return self._trap_gain
    
    @trap_gain.setter
    def trap_gain(self, value):
        self._trap_gain = value
    
    @property
    def trap_offset(self):
        return self._trap_offset
    
    @trap_offset.setter
    def trap_offset(self, value):
        self._trap_offset = value
    
    @property
    def trap_pileupinib(self):
        return self._trap_pileupinib
    
    @trap_pileupinib.setter
    def trap_pileupinib(self, value):
        self._trap_pileupinib = value
    
    @property
    def trap_polarity(self):
        return self._trap_polarity
    
    @trap_polarity.setter
    def trap_polarity(self, value):
        self._trap_polarity = value
    
    @property
    def trap_pur_mode(self):
        return self._trap_pur_mode
    
    @trap_pur_mode.setter
    def trap_pur_mode(self, value):
        self._trap_pur_mode = value
    
    @property
    def trap_sampling(self):
        return self._trap_sampling
    
    @trap_sampling.setter
    def trap_sampling(self, value):
        self._trap_sampling = value
    
    @property
    def trap_shaping(self):
        return self._trap_shaping
    
    @trap_shaping.setter
    def trap_shaping(self, value):
        self._trap_shaping = value
    
    @property
    def trap_tau(self):
        return self._trap_tau
    
    @trap_tau.setter
    def trap_tau(self, value):
        self._trap_tau = value
    
    @property
    def trigger_mode(self):
        return self._trigger_mode
    
    @trigger_mode.setter
    def trigger_mode(self, value):
        self._trigger_mode = value
    
    @property
    def trigger_type(self):
        return self._trigger_type
    
    @trigger_type.setter
    def trigger_type(self, value):
        self._trigger_type = value


# Classe per la conversione e gestione dei valori
class ConfigIO:

    class Polarity(Enum):
        POSITIVE = "positive"
        NEGATIVE = "negative"

    class AnalogOut(Enum):
        TRIGGER_OUTPUT = "trigger_output"
        ENERGY_FILTER_OUTPUT = "energy_filter_output"
        BASELINE = "baseline"
        ENERGY_VALUE = "energy_value"
        RISETIME = "risetime"
        ANALOG_INPUT = "analog_input"

        # Assumo altri valori possibili qui, aggiungili secondo necessità

    class DigitalIn(Enum):
        EXTERNAL_TRIGGER = "external_trigger"
        EXTERNAL_RUN = "external_run"
        EXTERNAL_RESET = "external_reset"
        EXTERNAL_CLOCK = "external_clock"

        # Assumo altri valori possibili qui, aggiungili secondo necessità

    class DigitalOut(Enum):
        TRIGGER = "trigger"
        ENERGY_VALID = "energy_valid"
        RISETIME_VALID = "risetime_valid"
        RUN = "run"
        
        # Assumo altri valori possibili qui, aggiungili secondo necessità


    def __init__(self):
        self.analog_in_polarity = ConfigIO.Polarity.POSITIVE
        self.analog_out = ConfigIO.AnalogOut.ENERGY_FILTER_OUTPUT
        self.digital_in = ConfigIO.DigitalIn.EXTERNAL_TRIGGER
        self.digital_out = ConfigIO.DigitalOut.TRIGGER
        
    def __str__(self):
        properties = vars(self)
        return '\n'.join([f'{key}: {value}' for key, value in properties.items() if key.startswith('_')])
    
    def process_config_json(self, config):
        self.analog_in_polarity = convert_to_enum(config["analog_in_polarity"], ConfigIO.Polarity)
        self.analog_out = convert_to_enum(config["analog_out"], ConfigIO.AnalogOut)
        self.digital_in = convert_to_enum(config["digital_in"], ConfigIO.DigitalIn)
        self.digital_out = convert_to_enum(config["digital_out"], ConfigIO.DigitalOut)
    
    def to_json(self):
        return {
            "analog_in_polarity": self.analog_in_polarity,
            "analog_out": self.analog_out,
            "digital_in": self.digital_in,
            "digital_out": self.digital_out
        }
    
    @property
    def analog_in_polarity(self):
        return self._analog_in_polarity

    @analog_in_polarity.setter
    def analog_in_polarity(self, value):
        self._analog_in_polarity = value

    @property
    def analog_out(self):
        return self._analog_out

    @analog_out.setter
    def analog_out(self, value):
        self._analog_out = value

    @property
    def digital_in(self):
        return self._digital_in

    @digital_in.setter
    def digital_in(self, value):
        self._digital_in = value

    @property
    def digital_out(self):
        return self._digital_out

    @digital_out.setter
    def digital_out(self, value):
        self._digital_out = value

from enum import Enum

class ConfigOscilloscope:
    class ScopeAnalog(Enum):
        TRAPEZOIDAL_BASELINE = "trapezoidal_baseline"
        SIGNAL_BASELINE = "signal_baseline"
        PEAK_STRETCHER_BASELINE = "peak_stretcher_baseline"
        DELTA_TRIGGER = "delta_trigger"
        TRAPEZOIDAL_TRIGGER = "trapezoidal_trigger"
        TRAPEZOIDAL = "trapezoidal"
        Q_LONG_VALUE = "q_long_value"
        Q_SHORT_VALUE = "q_short_value"
        PEAK_VALUE = "peak_value"
        BASELINE = "baseline"
        RISETIME = "risetime"

    class TriggerSource(Enum):
        FREE_RUNNING = "free_running"
        ANALOG_CHANNEL_1 = "analog_channel_1"
        ANALOG_CHANNEL_2 = "analog_channel_2"
        EXTERNAL_TRIGGER = "external_trigger"
        INTERNAL_TRIGGER = "internal_trigger"
        ENERGY_VALID = "energy_valid"
        EXTERNAL_RUN = "external_run"

    # class HISTROGRAM_SOURCE(Enum):
    #     ENERGY = "energy",
    #     RISETIME = "risetime",
    #     TIME = "risetime"
    
    # class PSD_SOURCE(Enum):
    #     ENERGY = "energy_",
    #     PSD = "psd",
    #     RISETIME = "risetime"


    def __init__(self):
        self.decimator = None
        self.pre_trigger = None
        self.scope_analog = None
        self.trigger_edge = None
        self.trigger_level = None
        self.trigger_source = None
        
    def __str__(self):
        properties = vars(self)
        return '\n'.join([f'{key}: {value}' for key, value in properties.items()])

    def process_config_json(self, config):
        self.decimator = config["decimator"]
        self.pre_trigger = config["pre_trigger"]
        self.scope_analog = convert_to_enum(config["scope_analog"], ConfigOscilloscope.ScopeAnalog)
        self.trigger_edge = convert_to_enum(config["trigger_edge"], ConfigIO.Polarity)
        self.trigger_level = config["trigger_level"]
        self.trigger_source = convert_to_enum(config["trigger_source"], ConfigOscilloscope.TriggerSource)

    def to_json(self):
        return {
            "decimator": self.decimator,
            "pre_trigger": self.pre_trigger,
            "scope_analog": self.scope_analog.value,
            "trigger_edge": self.trigger_edge.value,
            "trigger_level": self.trigger_level,
            "trigger_source": self.trigger_source.value
        }
    
    @property
    def decimator(self):
        return self._decimator
    
    @decimator.setter
    def decimator(self, value):
        self._decimator = value
    
    @property
    def pre_trigger(self):
        return self._pre_trigger
    
    @pre_trigger.setter
    def pre_trigger(self, value):
        self._pre_trigger = value
    
    @property
    def scope_analog(self):
        return self._scope_analog
    
    @scope_analog.setter
    def scope_analog(self, value):
        self._scope_analog = value
    
    @property
    def trigger_edge(self):
        return self._trigger_edge
    
    @trigger_edge.setter
    def trigger_edge(self, value):
        self._trigger_edge = value
    
    @property
    def trigger_level(self):
        return self._trigger_level
    
    @trigger_level.setter
    def trigger_level(self, value):
        self._trigger_level = value
    
    @property
    def trigger_source(self):
        return self._trigger_source
    
    @trigger_source.setter
    def trigger_source(self, value):
        self._trigger_source = value

class StatisticsMCA:
    class DataItem:
        def __init__(self, name, value, min_value=None, max_value=None):
            self._name = name
            self._value = value
            self._min_value = min_value
            self._max_value = max_value
        
        @property
        def name(self):
            return self._name
        
        @property
        def value(self):
            return self._value
        
        @property
        def min_value(self):
            return self._min_value
        
        @property
        def max_value(self):
            return self._max_value

    def __init__(self):
        self._data = []
        self._result = None
        
        # Definizione manuale delle proprietà per gli elementi dei dati
        self.icr = self._get_data_item_by_name("ICR (Hz)")
        self.ocr = self._get_data_item_by_name("OCR (Hz)")
        self.input_count = self._get_data_item_by_name("INPUT COUNT")
        self.output_count = self._get_data_item_by_name("OUTPUT COUNT")
        self.dead_percent = self._get_data_item_by_name("DEAD (%)")
        self.lost_count = self._get_data_item_by_name("LOST COUNT")
        self.live_time_s = self._get_data_item_by_name("LIVE TIME (s)")

    def _get_data_item_by_name(self, name):
        for item in self._data:
            if item.name == name:
                return item
        return None

    def __str__(self):
        data_str = '\n'.join([f'{item.name}: {item.value}' for item in self._data])
        return f"Data:\n{data_str}\n"

    def process_json(self, json_data):
        for item in json_data["data"]:
            if "min_value" in item and "max_value" in item:
                data_item = self.DataItem(item["name"], item["value"], item["min_value"], item["max_value"])
            else:
                data_item = self.DataItem(item["name"], item["value"])
            self._data.append(data_item)
        self._result = json_data["result"]

        self.icr = self._get_data_item_by_name("ICR (Hz)")
        self.ocr = self._get_data_item_by_name("OCR (Hz)")
        self.input_count = self._get_data_item_by_name("INPUT COUNT")
        self.output_count = self._get_data_item_by_name("OUTPUT COUNT")
        self.dead_percent = self._get_data_item_by_name("DEAD (%)")
        self.lost_count = self._get_data_item_by_name("LOST COUNT")
        self.live_time_s = self._get_data_item_by_name("LIVE TIME (s)")        

    @property
    def result(self):
        return self._result
    


class OscilloscopeChannel:
    def __init__(self, analog, digital):
        self.analog = analog
        self.digital = digital

class OscilloscopeData:
    def __init__(self, wave):  
        self._channels = [] 

        for w in wave:
            analog = w["analog"][0]
            digitals = w["digital"]
            digital = [[int(value) for value in sub_array] for sub_array in digitals]

            channel = OscilloscopeChannel(analog, digital)
            self.channels.append(channel)
    
    @property
    def channels(self):
        return self._channels
    


class SmartMCA:
    url = ""  
    connected = False  
    cookie = None
    _API_PATH_ = "/mca/api"

    class Status(Enum):
        IDLE = "idle"
        RUNNING = "running"

    class ScaleMode (Enum):
        LINEAR = "linear"
        LOG = "log"

    def __init__(self) -> None:
        url = ""
        
        
    def connect(self, url, username, password):
        self.url = url
        #post username and passowrd in a form format to the url /login
        #if the response is 200, then set connected to True
        #else set connected to False
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(self.url + "/api/login", json=data)
        
        if json.loads(response.text)["success"] == True:
            self.connected = True
            #store the cookie in a variable
            self.cookie = response.cookies
        else:
            self.connected = False

        
    
    def disconnect(self):
        self.connected = False
        self.cookie = None
        return self.connected
    
    def http_get(self, url):
        if not self.connected:
            raise Exception("Not connected to the server", 1)
        response = requests.get(self.url + url, cookies=self.cookie)
        if response.status_code != 200:
            raise Exception("Error in getting server status", 2)        
        j = response.json()
        
        return j
        
    
    def http_post(self, url, data):
        if not self.connected:
            raise Exception("Not connected to the server", 1)
        response = requests.post(self.url + url, cookies=self.cookie, json=data)
        if response.status_code != 200:
            raise Exception("Error in getting server status", 2)    
        return response.json()
    
    def get_server_status(self):
        j = self.http_get(self._API_PATH_ + "/get_server_status")
        return j["status"]
        
    def get_mca_configuration(self):
        j = self.http_get(self._API_PATH_ + "/HLL/hl_get_processing_param")
        config = ConfigMCA()
        config.process_config_json(j)
        return config
    
    def set_mca_configuration(self, config : ConfigMCA):
        j = config.to_json()
        r = self.http_post(self._API_PATH_ + "/HLL/hl_set_processing_param", j)
        if r["result"] != "ok":
            raise Exception(r["error"], 3)
    
    def get_io_configuration(self):
        j = self.http_get(self._API_PATH_ + "/HLL/hl_get_signal_param")
        config = ConfigIO()
        config.process_config_json(j)
        return config
    
    def set_io_configuration(self, config : ConfigIO):
        j = config.to_json()
        r = self.http_post(self._API_PATH_ + "/HLL/hl_set_signal_param", j)
        if r["result"] != "ok":
            raise Exception(r["error"], 3)
        
    def get_oscilloscope_configuration(self):
        j = self.http_get(self._API_PATH_ + "/HLL/hl_get_scope_param")
        config = ConfigOscilloscope()
        config.process_config_json(j)
        return config
    
    def set_oscilloscope_configuration(self, config : ConfigOscilloscope):
        j = config.to_json()
        r = self.http_post(self._API_PATH_ + "/HLL/hl_set_scope_param", j)
        if r["result"] != "ok":
            raise Exception(r["error"], 3)

    def get_mca_statistics(self):
        j = self.http_get(self._API_PATH_ + "/HLL/hl_get_statistics")
        stats = StatisticsMCA()
        stats.process_json(j)
        return stats

    def reset_statistics(self):
        r = self.http_get(self._API_PATH_ + "/HLL/hl_reset_statistics")
        if r["result"] != "ok":
            raise Exception(r["error"], 3)
        
    def histogram_get_status(self):
        param = {
            "histo_type" : "energy"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_get_status_histo", param)
        if j["result"] == "running":
            return SmartMCA.Status.RUNNING
        else:
            return SmartMCA.Status.IDLE
        
    def multiparametric_get_status(self):
        param = {
            "histo_type" : "energy_psd"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_get_status_histo", param)
        if j["result"] == "running":
            return SmartMCA.Status.RUNNING
        else:
            return SmartMCA.Status.IDLE        
        
    def histogram_start(self):
        param = {
            "histo_type" : "energy"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_start_histo", param)

        
    def multiparametric_start(self):
        param = {
            "histo_type" : "energy_psd"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_start_histo", param)
             
        
    def histogram_stop(self):
        param = {
            "histo_type" : "energy"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_stop_histo", param)

        
    def multiparametric_stop(self):
        param = {
            "histo_type" : "energy_psd"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_stop_histo", param)
       
        
    def histogram_reset(self):
        param = {
            "histo_type" : "energy"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_reset_histo", param)
        
        
    def multiparametric_reset(self):
        param = {
            "histo_type" : "energy_psd"
        }
        j = self.http_post(self._API_PATH_ + "/HLL/hl_reset_histo", param)

    def histogram_get(self, yscale:ScaleMode = ScaleMode.LINEAR, fit_data:bool=False, rebin:int=None):
        if yscale.value == "log":
            islog = True
        else:
            islog = False
            
        param = {
            "histo_type": "energy",
            "log": islog,
            "fit": fit_data
        }
        
        if rebin is not None:
            param["histo_rebin"] = rebin
        
        j = self.http_post(self._API_PATH_ + "/HLL/hl_get_histo", param)
        return j["data"], j["events"]
    
    def multiparametric_get(self, yscale:ScaleMode = ScaleMode.LINEAR, fit_data:bool=False, rebin:int=None):
        if yscale.value == "log":
            islog = True
        else:
            islog = False
            
        param = {
            "histo_type": "energy_psd",
            "log": islog,
            "fit": fit_data
        }
        
        if rebin is not None:
            param["histo_rebin"] = rebin
        
        j = self.http_post(self._API_PATH_ + "/HLL/hl_get_histo", param)
        return j["data"], j["events"]
    

    def oscilloscope_get_data(self, enable_trace_signal : bool = True, enable_trace_processing : bool = True ):
        waves = []
        if enable_trace_signal:
            waves.append(0)
        if enable_trace_processing:
            waves.append(1)
        param = {
            "waves": waves,
        }
        j = self.http_post(self._API_PATH_ + "/MMCComponents/Oscilloscope_0/get_waves_data",param)
     
        return OscilloscopeData(j["wave"])
