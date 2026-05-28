import pyvisa
import time

class Fluke8588A:
    """Class that controls Fluke8588A.
    """
    
    def __init__(self, dev_info, read_termination = '\r\n', write_termination = '\r\n', delay = 0.05, timeout = 10_000) -> None:
        """Constructor

        Args:
            dev_info (str): TCPIP connection e.g. ['TCPIP::169.254.163.80::3490::SOCKET'])
            read_termination (str, optional): Read termination. Defaults to '\\r\\n'.
            write_termination (str, optional): Write termination. Defaults to '\\r\\n'.
            delay (float, optional): Delay between two commands. Defaults to 0.05.
            timeout (int, optional): VISA timeout. Defaults to 10_000.
        """
        self.__instrument_connected = False
        
        rm = pyvisa.ResourceManager()
        try:
            self.__inst = rm.open_resource(dev_info, write_termination=write_termination, read_termination=read_termination)
            self.__instrument_connected = True
            self.__inst.timeout = timeout
            self.__delay = delay
        except Exception as e:
            print(e)
            print('Check connection with Fluke8588A')
    
    def __get_data(self,query) -> str:
        if self.__instrument_connected:
            try:
                recv = self.__inst.query(query)
                time.sleep(self.__delay)
                return recv
            except:
                print('Can not query data from the instrument')
            
        else:
            print('Fluke8588A is not connected')
        return None
    
    def __get_binary_data(self,query, datatype, is_big_endian) -> list:
        if self.__instrument_connected:
            try:
                recv = self.__inst.query_binary_values(query, datatype=datatype, is_big_endian=is_big_endian)
                time.sleep(self.__delay)
                return recv
            except:
                print('Can not query data from the instrument')
            
        else:
            print('Fluke8588A is not connected')
        return None
    
    def __write_data(self, data) -> bool:
        if self.__instrument_connected:
            try:
                self.__inst.write(data)
                time.sleep(self.__delay)
                return True
            except Exception as e: 
                print('Can not send data to the Fluke8588A')
                print('Reason:', e)
            
        else:
            print('Fluke8588A is not connected')
        return False

    def close_connection(self) -> None:
        """Close connection
        """
        if self.__instrument_connected:
            self.__inst.close()
            self.__instrument_connected = False

    def get_info(self) -> str:
        """Get calibrator info

        Returns:
            str: info
        """
        return self.__get_data('*IDN?')
    
    def clear_error(self) -> bool:
        """Clear status byte summary, and all event registers.

        Returns:
            bool: status
        """
        return self.__write_data('*CLS')
    
    def reset(self) -> bool:
        """Reset to power-on state

        Returns:
            bool: status
        """

        return self.__write_data('*RST')

    def get_error(self) -> str:
        """Get next error from error buffer

        Returns:
            str: error
        """
        return self.__get_data('SYST:ERR?')
    
    def set_current_dc_function(self)-> bool:
        """Sets function to DCI

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "CURR:DC"')
    
    def set_current_dc_aperture(self, apper = 'DEF') -> bool:
        """Sets the ADC aperture value in seconds or to the MIN, MAX, or Default setting.

        Args:
            apper (str, optional): ADC aperture value in seconds or MIN|MAX|DEF. The smallest time aperture is 0 seconds with
            200 ns increments and has an upper time limit of 10 seconds. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            apper = float(apper)
            if apper<=10 and apper>=0:
                return self.__write_data(f'CURR:DC:APER {apper}')
            else:
                return False
        except ValueError:
            if (apper in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'CURR:DC:APER {apper}')
            else:
                return False

    def get_current_dc_aperture(self) -> str:
        """Gets the ADC aperture value in seconds or to the MIN, MAX, or Default setting.

        Returns:
            str: ADC aperture value in seconds.
        """
        return self.__get_data(f'CURR:DC:APER?')

    def set_current_dc_aperture_mode(self, mode='AUTO') -> bool:
        """Sets the aperture mode.

        Args:
            mode (str, optional): Mode can be AUTO, FAST or MAN (manual). Defaults to "AUTO".

        Returns:
            bool: status
        """

        if mode in ['AUTO','FAST','MAN']:
            return self.__write_data(f'CURR:DC:APER:MODE {mode}')
        else:
            return False
        
    def get_current_dc_aperture_mode(self) -> str:
        """Gets the aperture mode and it can be AUTO, FAST or MAN (manual).

        Returns:
            str: aperture mode.
        """
        return self.__get_data(f'CURR:DC:APER:MODE?')

    def set_current_dc_nplc(self, nplc = 'DEF') -> bool:
        """Sets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Args:
            nplc (str, optional): Can be MIN, MAX, DEF or can be in range [0.01, 500]. Defaults to 'DEF'. 
            The smallest aperture that can be set by PLC is 0.01.

        Returns:
            bool: status
        """
        try:
            nplc = float(nplc)
            if nplc<=500 and nplc>=0.01:
                return self.__write_data(f'CURR:DC:NPLC {nplc}')
            else:
                return False
        except ValueError:
            if (nplc in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'CURR:DC:NPLC {nplc}')
            else:
                return False

    def get_current_dc_nplc(self) -> str:
        """Gets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Returns:
            str: number of power line cycles
        """
        return self.__get_data(f'CURR:DC:NPLC?')

    def set_current_dc_autorange(self, autorange='ON') -> bool:
        """Turns Auto range ON or OFF.

        Args:
            autorange (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if autorange in ['ON', 'OFF']:
            return self.__write_data(f'CURR:DC:RANG:AUTO {autorange}')
        else:
            return False
        
    def get_current_dc_autorange(self) -> str:
        """Gets autorange status.

        Returns:
            str: Returns 1 for Auto range ON, 0 for auto range OFF.
        """
        return self.__get_data(f'CURR:DC:RANG:AUTO?')

    def set_current_dc_range(self, range='DEF') -> bool:
        """Set maximum expected value or min, max or default range.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or can be [10E-6, 100E-6, 1E-3, 10E-3, 100E-3, 1, 10, 30]. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range<=30 and range>=10E-6:
                return self.__write_data(f'CURR:DC:RANG {range}')
            else:
                return False
        except ValueError:
            if (range in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'CURR:DC:RANG {range}')
            else:
                return False

    def get_current_dc_range(self) -> str:
        """Returns the selected range, or if specified, the MIN, MAX, or Default range

        Returns:
            str: DC current range
        """
        return self.__get_data(f'CURR:DC:RANG?')
    
    def set_current_dc_resolution(self, res='DEF') -> bool:
        """Set maximum expected value or min, max or default resolution;
            for example, range is 1 A, Resolution <nrf>. = 0.0001 (100 µA),
            the measurement is returned with a resolution of +1.000E-4.

        Args:
            resolution (str, optional): Can be 'MIN', 'MAX', 'DEF' or user defined number. Defaults to 'DEF'.

        Returns:
            bool: _description_
        """ 

        try:
            res = float(res)
            if res<=1 and res>=0:
                return self.__write_data(f'CURR:DC:RES {res}')
            else:
                return False
        except ValueError:
            if (res in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'CURR:DC:RES {res}')
            else:
                return False
            
    def get_current_dc_resolution(self) -> str:
        """Returns the selected resolution, or if specified, the minimum, maximum or default range.

        Returns:
            str: resolution
        """

        return self.__get_data(f'CURR:DC:RES?')
    
    def set_memory_format(self, format='ASCII') -> bool:
        """Set packed format.

        Args:
            format (str, optional): Packed format is 2 ("PACK,2") or 4 bytes ("PACK,4") (integer) Default ASCII. Defaults to 'ASCII'.

        Returns:
            bool: status
        """
        if format in ['ASC', 'PACK,2', 'PACK,4']:
            return self.__write_data(f'FORMAT {format}')
        else:
            return False

    def set_voltage_dc_function(self)-> bool:
        """Sets function to DCV

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "VOLT:DC"')
    
    def set_voltage_dc_aperture(self, apper = 'DEF') -> bool:
        """Sets the ADC aperture value in seconds or to the MIN, MAX, or Default setting.

        Args:
            apper (str, optional): ADC aperture value in seconds or MIN|MAX|DEF. The smallest time aperture is 0 seconds with
            200 ns increments and has an upper time limit of 10 seconds. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            apper = float(apper)
            if apper<=10 and apper>=0:
                return self.__write_data(f'VOLT:DC:APER {apper}')
            else:
                return False
        except ValueError:
            if (apper in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:DC:APER {apper}')
            else:
                return False

    def get_voltage_dc_aperture(self) -> str:
        """Gets the ADC aperture value in seconds or to the MIN, MAX, or Default setting.

        Returns:
            str: ADC aperture value in seconds.
        """
        return self.__get_data(f'VOLT:DC:APER?')

    def set_voltage_dc_aperture_mode(self, mode='AUTO') -> bool:
        """Sets the aperture mode.

        Args:
            mode (str, optional): Mode can be AUTO, FAST or MAN (manual). Defaults to "AUTO".

        Returns:
            bool: status
        """

        if mode in ['AUTO','FAST','MAN']:
            return self.__write_data(f'VOLT:DC:APER:MODE {mode}')
        else:
            return False
        
    def get_voltage_dc_aperture_mode(self) -> str:
        """Gets the aperture mode and it can be AUTO, FAST or MAN (manual).

        Returns:
            str: aperture mode.
        """
        return self.__get_data(f'VOLT:DC:APER:MODE?')

    def set_voltage_dc_nplc(self, nplc = 'DEF') -> bool:
        """Sets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Args:
            nplc (str, optional): Can be MIN, MAX, DEF or can be in range [0.01, 500]. Defaults to 'DEF'. 
            The smallest aperture that can be set by PLC is 0.01.

        Returns:
            bool: status
        """
        try:
            nplc = float(nplc)
            if nplc<=500 and nplc>=0.01:
                return self.__write_data(f'VOLT:DC:NPLC {nplc}')
            else:
                return False
        except ValueError:
            if (nplc in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:DC:NPLC {nplc}')
            else:
                return False

    def get_voltage_dc_nplc(self) -> str:
        """Gets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Returns:
            str: number of power line cycles
        """
        return self.__get_data(f'VOLT:DC:NPLC?')
    
    def set_voltage_dc_impedance(self, imp='AUTO') -> bool:
        """Sets the input impedance.

        Args:
            imp (str, optional): Auto is >1TΩ if range is <100 V, otherwise 10 MΩ. User can optionaly set 1 MΩ. Defaults to 'AUTO'.

        Returns:
            bool: status
        """
        if imp in ['AUTO', '1M', '10M']:
            return self.__write_data(f'VOLT:DC:IMP {imp}')
        else:
            return False

    def get_voltage_dc_impedance(self) -> str:
        """Gets the input impedance.

        Returns:
            str: Input impedance.
        """
        return self.__get_data(f'VOLT:DC:IMP?')

    def set_voltage_dc_autorange(self, autorange='ON') -> bool:
        """Turns Auto range ON or OFF.

        Args:
            autorange (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if autorange in ['ON', 'OFF']:
            return self.__write_data(f'VOLT:DC:RANG:AUTO {autorange}')
        else:
            return False
        
    def get_voltage_dc_autorange(self) -> str:
        """Gets autorange status.

        Returns:
            str: Returns 1 for Auto range ON, 0 for auto range OFF.
        """
        return self.__get_data(f'VOLT:DC:RANG:AUTO?')

    def set_voltage_dc_range(self, range='DEF') -> bool:
        """Set maximum expected value or min, max or default range.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or can be [0.1, 1, 10, 100, 1000]. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range<=1000 and range>=0.1:
                return self.__write_data(f'VOLT:DC:RANG {range}')
            else:
                return False
        except ValueError:
            if (range in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:DC:RANG {range}')
            else:
                return False

    def get_voltage_dc_range(self) -> str:
        """Returns the selected range, or if specified, the MIN, MAX, or Default range

        Returns:
            str: DC voltage range
        """
        return self.__get_data(f'VOLT:DC:RANG?')
    
    def set_voltage_dc_resolution(self, res='DEF') -> bool:
        """Set maximum expected value or min, max or default resolution; for example, range is 1V, Resolution res=0.0001 (100 μV), 
        the measurement is returned with a resolution of +1.000E-4.

        Args:
            resolution (str, optional): Can be 'MIN', 'MAX', 'DEF' or user defined number. Defaults to 'DEF'.

        Returns:
            bool: _description_
        """ 

        try:
            res = float(res)
            if res<=100 and res>=0:
                return self.__write_data(f'VOLT:DC:RES {res}')
            else:
                return False
        except ValueError:
            if (res in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:DC:RES {res}')
            else:
                return False
            
    def get_voltage_dc_resolution(self) -> str:
        """Returns the selected resolution, or if specified, the minimum, maximum or default range.

        Returns:
            str: resolution
        """

        return self.__get_data(f'VOLT:DC:RES?')

    def get_memory_format(self) -> str:
        """Get packed format.

        Returns:
            str: Retrieve last set data format. "PACK" if 2 byte set, "PACK,4" if 4 byte set.
        """

        return self.__get_data('FORM?')
    

    def get_memory_data_scale(self) -> str:
        """Retrieve scaling factor associated with binary data mode (always returns 1.0 when ASCII selected).

        Returns:
            str: scaling factor
        """
        return self.__get_data('FORM:SCALE?')
    

    def set_endianness(self, endianness='NORM') -> bool:
        """Change the byte order.

        Args:
            endianness (str, optional): Can be NORM (big-endian) or SWAP (little-endian). Defaults to 'NORM'.

        Returns:
            bool: status
        """

        if endianness in ['NORM', 'SWAP']:
            return self.__write_data(f'FORM:BORD {endianness}')
        else:
            return False
    
    def get_endianness(self) -> str:
        """Return the byte order

        Returns:
            str: NORM (big-endian) or SWAP (little-endian)
        """

        return self.__get_data('FORM:BORD?')

    def set_memory_buffer_location(self, location='BUFF') -> bool:
        """Selects memory buffer location.

        Args:
            location (str, optional): BUFF or no parameter = Volatile Buffer (Default) or BINT = Non-Volatile memory. Defaults to 'BUFF'.

        Returns:
            bool: status
        """

        if location in ['BUFF', 'BINT']:
            return self.__write_data(f'MEM:LOC {location}')
        else:
            return False
        
    def get_memory_buffer_location(self) -> str:
        """Gets memory buffer location.

        Returns:
            str: BUFF or no parameter = Volatile Buffer (Default) or BINT = Non-Volatile memory.
        """

        return self.__get_data('MEM:LOC?')
    
    def read_data(self) -> str:
        """ Puts the Product into the wait-for-trigger state. The trigger system arm and trigger layer conditions must be 
        satisfied before a measurement is taken and returned. Read is the same as sending the TRIGger commands:
        ABORt; INITiate:IMMediate;FETCh? command.

        Returns:
            str: Get samples.
        """
        try:
            format = self.get_memory_format().strip()

            if format == 'PACK,4':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('READ?', datatype='i', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('READ?', datatype='i', is_big_endian=False)
            elif format == 'PACK':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('READ?', datatype='h', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('READ?', datatype='h', is_big_endian=False)
            elif format == 'ASC':
                return [float(x) for x in self.__get_data('READ?').split(',')]
            else:
                return None
        except Exception as e:
            print(e)
            return False
        

    def set_remote(self) -> bool:
        """Puts the instrument in remote mode

        Returns:
            bool: status
        """

        return self.__write_data('SYST:REM')
    
    def set_local(self) -> bool:
        """Puts the instrument in local mode

        Returns:
            bool: status
        """

        return self.__write_data('SYST:LOC')

    def set_date(self, year, month, day) -> bool:
        """Set date

        Args:
            year (int): rounded to 4 digit integer number
            month (int): rounded to Integer in range 1 to 12
            day (int): rounded to Integer in range 1 to max days in month for year and day

        Returns:
            bool: status
        """
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            if (year >=2020 and year <= 2100) and (month >= 1 and month <= 12) and (day >= 1 and day <= 31):
                return self.__write_data(f'SYST:DATE {year},{month},{day}')
            else:
                return False
        except:
            return False

    def get_date(self) -> str:
        """Retrieves the date in same format as set

        Returns:
            str: date in format yyyy,mm,dd
        """

        return self.__get_data('SYST:DATE?')
    
    def set_time(self, hour, minute, second) -> bool:
        """Set time

        Args:
            hour (int): rounded to Integer from 0 to 23
            minut (int): rounded to Integer from 0 to 59
            second (int): rounded to number with resolution of the RTC from 0 to 60

        Returns:
            bool: status
        """
        try:
            hour = int(hour)
            minute = int(minute)
            second = int(second)
            if (hour >=0 and hour <= 23) and (minute >= 0 and minute <= 59) and (second >= 0 and second <= 60):
                return self.__write_data(f'SYST:TIME {hour},{minute},{second}')
            else: 
                return False
        except:
            return False

    def get_time(self) -> str:
        """Returns the current RTC time

        Returns:
            str: date in format hh,mm,ss
        """

        return self.__get_data('SYST:TIME?')

    def set_line_frequency_auto(self,auto = 1) -> bool:
        """Enable or disable auto setup of line frequency.

        Args:
            auto (int, str, optional): Auto detect 1 (ON) or 0 (OFF). ONCE measures and sets line
            frequency then turns AUTO off. Defaults to 1.

        Returns:
            bool: status
        """
        if auto in [0,1,'0','1','ONCE']:
            return self.__write_data(f'SYST:LFR:AUTO {auto}')
        else:
            return False

    def set_line_frequency(self, freq=50) -> bool:
        """Sets line frequency.

        Args:
            freq (int, optional): Can be 50 or 60. Defaults to 50.

        Returns:
            bool: status
        """
        try:
            freq = int(freq)
            if freq == 50 or freq == 60:
                return self.__write_data(f'SYST:LFR {freq}')
            else:
                return False
        except:
            return False

    def get_line_frequency(self) -> str:
        """Return the line frequency setting.

        Returns:
            str: 50 Hz or 60 Hz.
        """

        return self.__get_data(f'SYST:LFR?')
    
    def get_hardware_modification_level(self) -> str:
        """Returns the hardware Modification level.

        Returns:
            str: hardware modification level.
        """

        return self.__get_data(f'SYST:MLEV?')
    
    def set_preset(self, preset = 'NORM') -> bool:
        """Preset instrument in fast or normal mode.

        Args:
            preset (str, optional): FAST sets all conditions for special high-speed mode.
            NORM sets the normal operating conditions (as after reset). Defaults to 'NORM'.

        Returns:
            bool: status
        """

        if preset == 'NORM' or preset == 'FAST':
            return self.__write_data(f'SYST:PRES {preset}')
        else:
            return False
        

    def set_timestamp_state(self, state='OFF') -> bool:
        """Turn reading time stamps ON or OFF

        Args:
            state (str, optional): Can be 'ON' or 'OFF'. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if state in ['ON','OFF']:
            return self.__write_data(f'SYST:TIME:TIM {state}')
        else:
            return False
        
    def get_timestamp_state(self) -> str:
        """Return the state of reading time stamps

        Returns:
            str: timestamp 0 = OFF, 1 = ON
        """

        return self.__get_data('SYST:TIME:TIM?')
    
    def get_internal_temperature(self) -> str:
        """Returns internal temperatures.

        Returns: 
            str: Returns temperature in form x,y
            x = temperature in degrees Celsius measured on the analogue assembly
            y = temperature in degrees Celsius measured on the Digital assembly
        """

        return self.__get_data('SYST:TEMP?')
    
    def trigger_abort(self):
        """The abort command is at the root level in the command hierachy but included with the Trigger
            subsystem commands because of their close functional relationships. The abort command resets the
            trigger system and places it in the IDLE state. Actions related to the trigger system that are in progress,
            such as acquiring a measurement, will be aborted as quickly as possible.
        """

        return self.__write_data('ABOR')

    def set_trigger_init_continuous(self, state='ON') -> bool:
        """Determines what happens when the triggering process enters the Initiate layer.

        Args:
            state (str, optional): CONTinuous ON causes the trigger system to exit the Initiate
            layer on the downward path without entering the Idle state.
            CONTinuous OFF causes the trigger system to enter the Idle
            state.. Defaults to 'ON'.

        Returns:
            bool: status
        """
        
        if state in ['ON', 'OFF']:
            return self.__write_data(f'INIT:CONT {state}')
        else:
            return False
        
    def get_trigger_init_continuous(self) -> str:
        """Returns the state of INITiate:CONTinuous.

        Returns:
            str: 1 = ON, 0 = OFF
        """

        return self.__get_data(f'INIT:CONT?')
    
    def set_init_epoch_start_time(self, year, month, day, hour, minute, second) -> bool:
        """Sets Epoch start time. If Continuous is OFF at Epoch start time, CONTinuous is set to ON.

        Args:
            year (int): rounded to 4 digit integer number
            month (int): rounded to Integer in range 1 to 12
            day (int): rounded to Integer in range 1 to max days in month for year and day
            hour (int): rounded to Integer from 0 to 23
            minut (int): rounded to Integer from 0 to 59
            second (int): rounded to number with resolution of the RTC from 0 to 60

        Returns:
            bool: state
        """

        try:
            hour = int(hour)
            minute = int(minute)
            second = int(second)
            year = int(year)
            month = int(month)
            day = int(day)
            if (year >=2020 and year <= 2100) and (month >= 1 and month <= 12) and (day >= 1 and day <= 31)\
                and (hour >=0 and hour <= 23) and (minute >= 0 and minute <= 59) and (second >= 0 and second <= 60):
                return self.__write_data(f'INIT:EPOC:STAR {year},{month},{day},{hour},{minute},{second}')
            else:
                return False
        except:
            return False
    
    def get_init_epoch_start_time(self) -> str:
        """Gets Epoch start time.

        Returns:
            str: format is yyyy,mm,dd,hh,mm,ss, NONE if it is not set before.
        """

        return self.__get_data(f'INIT:EPOC:STAR?')
    
    def set_init_epoch_stop_time(self, year, month, day, hour, minute, second) -> bool:
        """Sets Epoch stop time. If Continuous is OFF at Epoch stop time, CONTinuous is set to ON.

        Args:
            year (int): rounded to 4 digit integer number
            month (int): rounded to Integer in range 1 to 12
            day (int): rounded to Integer in range 1 to max days in month for year and day
            hour (int): rounded to Integer from 0 to 23
            minut (int): rounded to Integer from 0 to 59
            second (int): rounded to number with resolution of the RTC from 0 to 60

        Returns:
            bool: state
        """

        try:
            hour = int(hour)
            minute = int(minute)
            second = int(second)
            year = int(year)
            month = int(month)
            day = int(day)
            if (year >=2020 and year <= 2100) and (month >= 1 and month <= 12) and (day >= 1 and day <= 31)\
                and (hour >=0 and hour <= 23) and (minute >= 0 and minute <= 59) and (second >= 0 and second <= 60):
                return self.__write_data(f'INIT:EPOC:STOP {year},{month},{day},{hour},{minute},{second}')
            else:
                return False
        except:
            return False
    
    def get_init_epoch_stop_time(self) -> str:
        """Gets Epoch stop time.

        Returns:
            str: format is yyyy,mm,dd,hh,mm,ss, NONE if it is not set before.
        """

        return self.__get_data(f'INIT:EPOC:STOP?')

    def set_trigger_init_immediate(self) -> bool:
        """INITiate:IMMediate causes exit from the idle state. CONTinuous
            state is not affected.

        Returns:
            bool: status
        """ 

        return self.__write_data(f'INIT')
    
    def set_arm1_count(self, number_of_passes = 1) -> bool:
        """Specifies the number of passes through layer and subordinate
            layers before control flows up to the superior layer.

        Args:
            number_of_passes (int, str, optional): Min = 1,Max = 10_000_000. Defaults to 1.

        Returns:
            bool: status
        """
        try:
            number_of_passes = int(number_of_passes)
            if number_of_passes >= 1 and number_of_passes<=10_000_000:
                return self.__write_data(f'ARM:LAY1:COUN {number_of_passes}')
            else:
                return False
        except:
            return False
        
    def get_arm1_count(self) -> str:
        """Returns the Count setting.

        Returns:
            str: count
        """
        return self.__get_data(f'ARM:LAY1:COUN?')
    

    def set_arm1_coupling(self, coupling = 'AC') -> bool:
        """Sets the coupling used with INTernal bus source. Coupling can 
        be set in any layer but will always be the same for all layers.
        Note that The Signal level parameters can be set in any layer
        but will always be the same for all layers.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """

        return self.__write_data(f'ARM:LAY1:COUP {coupling}')
    
    def get_arm1_coupling(self) -> str:
        """Returns the coupling settings. 

        Returns:
            str: coupling settings.
        """
    
        return self.__get_data('ARM:LAY1:COUP?')


    def set_arm1_delay_auto(self, delay = 'ON') -> bool:
        """Sets the auto delay setting.

        Args:
            delay (str, optional): When ON, the time delay between source event detection and
            flow passing to the subordinate layer is determined
            automatically (the DMM sets an appropriate delay needed for
            settling after a configuration change). Default = ON. Defaults to 'ON'.

        Returns:
            bool: status
        """

        if delay in ['ON', 'OFF']:
            return self.__write_data(f'ARM:LAY1:DEL:AUTO {delay}')
        else:
            return False
        
    def get_arm1_delay_auto(self) -> str:
        """Returns the auto delay setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """

        return self.__get_data('ARM:LAY1:DEL:AUTO?')

    def set_arm1_delay(self, delay = 0) -> bool:
        """Set the time delay between source event detection and flow
            passing to the subordinate layer.

        Args:
            delay (str, optional): Delay can be manually set for a fixed time of 30 ns to
            4,000,000 seconds. Resolution is 10 ns for delays up to 40 seconds. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            delay = float(delay)
            if delay>=0 and delay<=4_000_000:
                return self.__write_data(f'ARM:LAY1:DEL {delay}')
            else:
                return False
        except:
            return False
        
    def get_arm1_delay(self) -> str:
        """Returns the delay setting in seconds.

        Returns:
            str: delay
        """

        return self.__get_data('ARM:LAY1:DEL?')

    def set_arm1_event_count(self, event_count=1) -> bool:
        """Event count is an integer value to specify how many ARM events
            must be recognised before DELay is started on the downwards
            transit through the layer. ECOunt provides ARM event division.

        Args:
            event_count (int, str, optional): Can be integer value in range [1,10_000_000]. Defaults to 1.

        Returns:
            bool: status
        """

        try:
            event_count = int(event_count)
            if event_count>=0 and event_count<=10_000_000:
                return self.__write_data(f'ARM:LAY1:ECO {event_count}')
            else:
                return False
        except:
            return False

    def get_arm1_event_count(self) -> str:
        """Returns the event counter setting

        Returns:
            str: event counter
        """

        return self.__get_data('ARM:LAY1:ECO?')
    

    def set_arm1_external_trigger_polarity(self, trigger_edge = 'NEG', signal_type  = 'TTL') -> bool:
        """Sets the polarity of the External trigger edge and signal type. Note that The
        Ext Trig parameters can be set in any layer but will always be the same for all layers.

        Args:
            trigger_edge (str, optional): Can be "NEG" for negative edge or "POS" for positive edge. Defaults to "NEG".
            signal_type (str, optional): Can be "TTL" for TTL or "BIP" for bipolar signal type. Defaults to "TTL".

        Returns:
            bool: status
        """

        if (signal_type in ['TTL', 'BIP']) and (trigger_edge in ['POS', 'NEG']):
            return self.__write_data(f'ARM:LAY1:EXT {trigger_edge},{signal_type}')
        else:
            return False
        
    def get_arm1_external_trigger_polarity(self) -> str:
        """Returns the external edge polarity and edge type settings.

        Returns:
            str: external edge polarity and edge type settings.
        """

        return self.__get_data('ARM:LAY1:EXT?')
    
    def set_arm1_filter(self, filter = 'OFF') -> bool:
        """Turns the filter in the event detector path ON or OFF. The filter
            affects both the signal and event detector paths.

        Args:
            filter (str, optional): Can be 'ON' or 'OFF'. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if filter in ['ON', 'OFF']:
            return self.__write_data(f'ARM:LAY1:FILT {filter}')
        else:
            return False
        
    def get_arm1_filter(self) -> str:
        """Returns the filter state.

        Returns:
            str: filter state 0 for OFF or 1 for ON 
        """
        return self.__get_data('ARM:LAY1:FILT?')

    def set_arm1_immediate_special_event(self) -> bool:
        """Modifies event detection behaviour. If the system is waiting for
            an event in this layer, this one-time command bypasses event
            detection ECOUNT and DELay causing immediate exit from the
            layer on the downward path. If not waiting at the event detector
            the command is ignored and error -221 issued.

        Returns:
            bool: status
        """
        return self.__write_data('ARM:LAY1:IMM')
    
    def set_arm1_signal_level(self, percentage=0) -> bool:
        """Sets the percentage of range at which arming occurs when Source is INTernal.
           Note that The Signal level parameters can be set in any layer but will always 
           be the same for all layers.

        Args:
            percentage (int, optional): Can be integer in range Min -200 % or Max = 200 %. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            percentage = int(percentage)
            if percentage>=-200 and percentage<=200:
                return self.__write_data(f'ARM:LAY1:LEV {percentage}')
            else:
                return False
        except:
            return False

    def get_arm1_signal_level(self) -> str:
        """Returns the level setting as a percentage of range.

        Returns:
            str: percentage
        """

        return self.__get_data('ARM:LAY1:LEV?')

    def set_arm1_signal_special_event(self) -> bool:
        """Modifies event detection behaviour. If the system is waiting for
            an event in this layer this one-time command bypasses event
            detection. Otherwise, the command is ignored and error -221
            issued.

        Returns:
            bool: status
        """
        return self.__write_data('ARM:LAY1:SIGN')

    def set_arm1_internal_slope(self, slope='POS') -> bool:
        """Sets the signal slope that causes the event detector to be
           satisfied if Soure is Internal. See also set_signal_level
            and set_coupling. Note that The Signal level parameters can be 
            set in any layer but will always be the same for all layers.

        Args:
            slope (str, optional): Can be 'POS' for positive edge or 'NEG'. Defaults to 'POS'.

        Returns:
            bool: _description_
        """
        if slope in ['POS', 'NEG']:
            #NOTE: Ovo je bug. POS je setovalo negativnu ivicu pa je ovako sredjeno
            if slope == 'POS':
                return self.__write_data(f'ARM:LAY1:SLOP NEG')
            if slope == 'NEG':
                return self.__write_data(f'ARM:LAY1:SLOP POS')
        else:
            return False

    def set_arm1_source(self, source) -> bool:
        """Source of ARM signal

        Args:
            source (_type_): BUS = Receipt of *TRG or GET \n
            EXT = Conforming rear panel trigger edge\n
            HOLD = Arming cannot occur unless a immediate or signal command is received\n
            IMM = The process does not stop at the event detector in this layer\n
            INT = Trigger from the signal being measured at the Level
            on the Slope set by the set_level, set_slope and set_coupling commands. \n
            LINE = trigger derived from the mains input. Triggers occur at
            the line frequency rate or multiples of that rate if the trigger
            system cycle time exceeds the line frequency.\n
            MAN = when the TRIG key is pushed\n
            SYNC = Arms when the multimeter's output buffer is
            empty, and the controller requests data.\n
            TIM = at the interval set by set_timer. On the first of
            set_count passes, arming is immediate, subsequent arms occur at TIMer intervals

        Returns:
            bool: status
        """
        if source in ['BUS', 'EXT', 'HOLD', 'IMM', 'INT', 'LINE', 'MAN', 'SYNC', 'TIM']:
            return self.__write_data(f'ARM:LAY1:SOUR {source}')
        else:
            return False
        
    def get_arm1_source(self) -> str:
        """Returns the source setting.

        Returns:
            str: source
        """
        return self.__get_data('ARM:LAY1:SOUR?')

    def set_arm1_timer(self, timer=2E-7) -> bool:
        """Sets the interval between TIMer events. Only active if Source = timer.

        Args:
            timer (float, optional): Can be from 20 ns up to 4_000_000 s. Defaults to 2E-7(200 ns).

        Returns:
            bool: status
        """
        try:
            timer = float(timer)
            if timer>=0 and timer<=4_000_000:
                return self.__write_data(f'ARM:LAY1:TIM {timer}')
            else:
                return False
        except:
            return False
    
    def get_arm1_timer(self) -> str:
        """Returns the timer setting

        Returns:
            str: timer interval
        """
        return self.__get_data('ARM:LAY1:TIM?')

    def set_arm2_count(self, number_of_passes = 1) -> bool:
        """Specifies the number of passes through layer and subordinate
            layers before control flows up to the superior layer.

        Args:
            number_of_passes (int, str, optional): Min = 1,Max = 10_000_000. Defaults to 1.

        Returns:
            bool: status
        """
        try:
            number_of_passes = int(number_of_passes)
            if number_of_passes >= 1 and number_of_passes<=10_000_000:
                return self.__write_data(f'ARM:LAY2:COUN {number_of_passes}')
            else:
                return False
        except:
            return False
        
    def get_arm2_count(self) -> str:
        """Returns the Count setting.

        Returns:
            str: count
        """
        return self.__get_data(f'ARM:LAY2:COUN?')
    

    def set_arm2_coupling(self, coupling = 'AC') -> bool:
        """Sets the coupling used with INTernal bus source. Coupling can 
        be set in any layer but will always be the same for all layers.
        Note that The Signal level parameters can be set in any layer
        but will always be the same for all layers.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """

        return self.__write_data(f'ARM:LAY2:COUP {coupling}')
    
    def get_arm2_coupling(self) -> str:
        """Returns the coupling settings. 

        Returns:
            str: coupling settings.
        """
    
        return self.__get_data('ARM:LAY2:COUP?')


    def set_arm2_delay_auto(self, delay = 'ON') -> bool:
        """Sets the auto delay setting.

        Args:
            delay (str, optional): When ON, the time delay between source event detection and
            flow passing to the subordinate layer is determined
            automatically (the DMM sets an appropriate delay needed for
            settling after a configuration change). Default = ON. Defaults to 'ON'.

        Returns:
            bool: status
        """

        if delay in ['ON', 'OFF']:
            return self.__write_data(f'ARM:LAY2:DEL:AUTO {delay}')
        else:
            return False
        
    def get_arm2_delay_auto(self) -> str:
        """Returns the auto delay setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """

        return self.__get_data('ARM:LAY2:DEL:AUTO?')

    def set_arm2_delay(self, delay = 0) -> bool:
        """Set the time delay between source event detection and flow
            passing to the subordinate layer.

        Args:
            delay (str, optional): Delay can be manually set for a fixed time of 30 ns to
            4,000,000 seconds. Resolution is 10 ns for delays up to 40 seconds. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            delay = float(delay)
            if delay>=0 and delay<=4_000_000:
                return self.__write_data(f'ARM:LAY2:DEL {delay}')
            else:
                return False
        except:
            return False
        
    def get_arm2_delay(self) -> str:
        """Returns the delay setting in seconds.

        Returns:
            str: delay
        """

        return self.__get_data('ARM:LAY2:DEL?')

    def set_arm2_event_count(self, event_count=1) -> bool:
        """Event count is an integer value to specify how many ARM events
            must be recognised before DELay is started on the downwards
            transit through the layer. ECOunt provides ARM event division.

        Args:
            event_count (int, str, optional): Can be integer value in range [1,10_000_000]. Defaults to 1.

        Returns:
            bool: status
        """

        try:
            event_count = int(event_count)
            if event_count>=0 and event_count<=10_000_000:
                return self.__write_data(f'ARM:LAY2:ECO {event_count}')
            else:
                return False
        except:
            return False

    def get_arm2_event_count(self) -> str:
        """Returns the event counter setting

        Returns:
            str: event counter
        """

        return self.__get_data('ARM:LAY2:ECO?')
    

    def set_arm2_external_trigger_polarity(self, trigger_edge = 'NEG', signal_type  = 'TTL') -> bool:
        """Sets the polarity of the External trigger edge and signal type. Note that The
        Ext Trig parameters can be set in any layer but will always be the same for all layers.

        Args:
            trigger_edge (str, optional): Can be "NEG" for negative edge or "POS" for positive edge. Defaults to "NEG".
            signal_type (str, optional): Can be "TTL" for TTL or "BIP" for bipolar signal type. Defaults to "TTL".

        Returns:
            bool: status
        """

        if (signal_type in ['TTL', 'BIP']) and (trigger_edge in ['POS', 'NEG']):
            return self.__write_data(f'ARM:LAY2:EXT {trigger_edge},{signal_type}')
        else:
            return False
        
    def get_arm2_external_trigger_polarity(self) -> str:
        """Returns the external edge polarity and edge type settings.

        Returns:
            str: external edge polarity and edge type settings.
        """

        return self.__get_data('ARM:LAY2:EXT?')
    
    def set_arm2_filter(self, filter = 'OFF') -> bool:
        """Turns the filter in the event detector path ON or OFF. The filter
            affects both the signal and event detector paths.

        Args:
            filter (str, optional): Can be 'ON' or 'OFF'. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if filter in ['ON', 'OFF']:
            return self.__write_data(f'ARM:LAY2:FILT {filter}')
        else:
            return False
        
    def get_arm2_filter(self) -> str:
        """Returns the filter state.

        Returns:
            str: filter state 0 for OFF or 1 for ON 
        """
        return self.__get_data('ARM:LAY2:FILT?')

    def set_arm2_immediate_special_event(self) -> bool:
        """Modifies event detection behaviour. If the system is waiting for
            an event in this layer, this one-time command bypasses event
            detection ECOUNT and DELay causing immediate exit from the
            layer on the downward path. If not waiting at the event detector
            the command is ignored and error -221 issued.

        Returns:
            bool: status
        """
        return self.__write_data('ARM:LAY2:IMM')
    
    def set_arm2_signal_level(self, percentage=0) -> bool:
        """Sets the percentage of range at which arming occurs when Source is INTernal.
           Note that The Signal level parameters can be set in any layer but will always 
           be the same for all layers.

        Args:
            percentage (int, optional): Can be integer in range Min -200 % or Max = 200 %. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            percentage = int(percentage)
            if percentage>=-200 and percentage<=200:
                return self.__write_data(f'ARM:LAY2:LEV {percentage}')
            else:
                return False
        except:
            return False

    def get_arm2_signal_level(self) -> str:
        """Returns the level setting as a percentage of range.

        Returns:
            str: percentage
        """

        return self.__get_data('ARM:LAY2:LEV?')

    def set_arm2_signal_special_event(self) -> bool:
        """Modifies event detection behaviour. If the system is waiting for
            an event in this layer this one-time command bypasses event
            detection. Otherwise, the command is ignored and error -221
            issued.

        Returns:
            bool: status
        """
        return self.__write_data('ARM:LAY2:SIGN')

    def set_arm2_internal_slope(self, slope='POS') -> bool:
        """Sets the signal slope that causes the event detector to be
           satisfied if Soure is Internal. See also set_signal_level
            and set_coupling. Note that The Signal level parameters can be 
            set in any layer but will always be the same for all layers.

        Args:
            slope (str, optional): Can be 'POS' for positive edge or 'NEG'. Defaults to 'POS'.

        Returns:
            bool: _description_
        """
        if slope in ['POS', 'NEG']:
            #NOTE: Ovo je bug. POS je setovalo negativnu ivicu pa je ovako sredjeno
            if slope == 'POS':
                return self.__write_data(f'ARM:LAY2:SLOP NEG')
            if slope == 'NEG':
                return self.__write_data(f'ARM:LAY2:SLOP POS')
        else:
            return False

    def set_arm2_source(self, source) -> bool:
        """Source of ARM signal

        Args:
            source (_type_): BUS = Receipt of *TRG or GET\n
            EXT = Conforming rear panel trigger edge\n
            HOLD = Arming cannot occur unless a immediate or signal command is received\n
            IMM = The process does not stop at the event detector in this layer\n
            INT = Trigger from the signal being measured at the Level
            on the Slope set by the set_level, set_slope and set_coupling commands. \n
            LINE = trigger derived from the mains input. Triggers occur at
            the line frequency rate or multiples of that rate if the trigger
            system cycle time exceeds the line frequency.\n
            MAN = when the TRIG key is pushed\n
            SYNC = Arms when the multimeter's output buffer is
            empty, and the controller requests data.\n
            TIM = at the interval set by set_timer. On the first of
            set_count passes, arming is immediate, subsequent arms occur at TIMer intervals

        Returns:
            bool: status
        """
        if source in ['BUS', 'EXT', 'HOLD', 'IMM', 'INT', 'LINE', 'MAN', 'SYNC', 'TIM']:
            return self.__write_data(f'ARM:LAY2:SOUR {source}')
        else:
            return False
        
    def get_arm2_source(self) -> str:
        """Returns the source setting.

        Returns:
            str: source
        """
        return self.__get_data('ARM:LAY2:SOUR?')

    def set_arm2_timer(self, timer=2E-7) -> bool:
        """Sets the interval between TIMer events. Only active if Source = timer.

        Args:
            timer (float, optional): Can be from 20 ns up to 4_000_000 s. Defaults to 2E-7(200 ns).

        Returns:
            bool: status
        """
        try:
            timer = float(timer)
            if timer>=0 and timer<=4_000_000:
                return self.__write_data(f'ARM:LAY2:TIM {timer}')
            else:
                return False
        except:
            return False
    
    def get_arm2_timer(self) -> str:
        """Returns the timer setting

        Returns:
            str: timer interval
        """
        return self.__get_data('ARM:LAY2:TIM?')

    def set_trigger_count(self, number_of_passes = 1) -> bool:
        """Specifies the number of passes through layer and subordinate
            layers before control flows up to the superior layer.

        Args:
            number_of_passes (int, str, optional): Min = 1,Max = 10_000_000. Defaults to 1.

        Returns:
            bool: status
        """
        try:
            number_of_passes = int(number_of_passes)
            if number_of_passes >= 1 and number_of_passes<=10_000_000:
                return self.__write_data(f'TRIG:COUN {number_of_passes}')
            else:
                return False
        except:
            return False
        
    def get_trigger_count(self) -> str:
        """Returns the Count setting.

        Returns:
            str: count
        """
        return self.__get_data(f'TRIG:COUN?')
    

    def set_trigger_coupling(self, coupling = 'AC') -> bool:
        """Sets the coupling used with INTernal bus source. Coupling can 
        be set in any layer but will always be the same for all layers.
        Note that The Signal level parameters can be set in any layer
        but will always be the same for all layers.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """

        return self.__write_data(f'TRIG:COUP {coupling}')
    
    def get_trigger_coupling(self) -> str:
        """Returns the coupling settings. 

        Returns:
            str: coupling settings.
        """
    
        return self.__get_data('TRIG:COUP?')


    def set_trigger_delay_auto(self, delay = 'ON') -> bool:
        """Sets the auto delay setting.

        Args:
            delay (str, optional): When ON, the time delay between source event detection and
            flow passing to the subordinate layer is determined
            automatically (the DMM sets an appropriate delay needed for
            settling after a configuration change). Default = ON. Defaults to 'ON'.

        Returns:
            bool: status
        """

        if delay in ['ON', 'OFF']:
            return self.__write_data(f'TRIG:DEL:AUTO {delay}')
        else:
            return False
        
    def get_trigger_delay_auto(self) -> str:
        """Returns the auto delay setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """

        return self.__get_data('TRIG:DEL:AUTO?')

    def set_trigger_delay(self, delay = 0) -> bool:
        """Set the time delay between source event detection and flow
            passing to the subordinate layer.

        Args:
            delay (str, optional): Delay can be manually set for a fixed time of 30 ns to
            4,000,000 seconds. Resolution is 10 ns for delays up to 40 seconds. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            delay = float(delay)
            if delay>=0 and delay<=4_000_000:
                return self.__write_data(f'TRIG:DEL {delay}')
            else:
                return False
        except:
            return False
        
    def get_trigger_delay(self) -> str:
        """Returns the delay setting in seconds.

        Returns:
            str: delay
        """

        return self.__get_data('TRIG:DEL?')

    def set_trigger_event_count(self, event_count=1) -> bool:
        """Event count is an integer value to specify how many ARM events
            must be recognised before DELay is started on the downwards
            transit through the layer. ECOunt provides ARM event division.

        Args:
            event_count (int, str, optional): Can be integer value in range [1,10_000_000]. Defaults to 1.

        Returns:
            bool: status
        """

        try:
            event_count = int(event_count)
            if event_count>=0 and event_count<=10_000_000:
                return self.__write_data(f'TRIG:ECO {event_count}')
            else:
                return False
        except:
            return False

    def get_trigger_event_count(self) -> str:
        """Returns the event counter setting

        Returns:
            str: event counter
        """

        return self.__get_data('TRIG:ECO?')
    

    def set_trigger_external_trigger_polarity(self, trigger_edge = 'NEG', signal_type  = 'TTL') -> bool:
        """Sets the polarity of the External trigger edge and signal type. Note that The
        Ext Trig parameters can be set in any layer but will always be the same for all layers.

        Args:
            trigger_edge (str, optional): Can be "NEG" for negative edge or "POS" for positive edge. Defaults to "NEG".
            signal_type (str, optional): Can be "TTL" for TTL or "BIP" for bipolar signal type. Defaults to "TTL".

        Returns:
            bool: status
        """

        if (signal_type in ['TTL', 'BIP']) and (trigger_edge in ['POS', 'NEG']):
            return self.__write_data(f'TRIG:EXT {trigger_edge},{signal_type}')
        else:
            return False
        
    def get_trigger_external_trigger_polarity(self) -> str:
        """Returns the external edge polarity and edge type settings.

        Returns:
            str: external edge polarity and edge type settings.
        """

        return self.__get_data('TRIG:EXT?')
    
    def set_trigger_filter(self, filter = 'OFF') -> bool:
        """Turns the filter in the event detector path ON or OFF. The filter
            affects both the signal and event detector paths.

        Args:
            filter (str, optional): Can be 'ON' or 'OFF'. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if filter in ['ON', 'OFF']:
            return self.__write_data(f'TRIG:FILT {filter}')
        else:
            return False
        
    def get_trigger_filter(self) -> str:
        """Returns the filter state.

        Returns:
            str: filter state 0 for OFF or 1 for ON 
        """
        return self.__get_data('TRIG:FILT?')
    
    def set_trigger_holdoff_auto(self, auto='ON') -> bool:
        """When ON, the holdoff period is set Automatically.

        Args:
            auto (str, optional): Can be 'ON' for enabling or 'OFF' for disabling auto holdoff period. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if auto in ['ON','OFF']:
            return self.__write_data(f'TRIG:HOLD:AUTO {auto}')
        else:
            return False
        
    def get_trigger_holdoff_auto(self) -> str:
        """Returns the state of HOLDoff:AUTO

        Returns:
            str: 1 = ON, 2 = OFF
        """

        return self.__get_data('TRIG:HOLD:AUTO?')

    def set_trigger_holdoff(self, holdoff_delay = 0) -> bool:
        """Manually sets the HOLDoff period.

        Args:
            delay (str, optional): Delay can be manually set  Default 0, Maximum 100 s. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            holdoff_delay = float(holdoff_delay)
            if holdoff_delay>=0 and holdoff_delay<=100:
                return self.__write_data(f'TRIG:HOLD {holdoff_delay}')
            else:
                return False
        except:
            return False
        
    # CHANGED: renamed from get_trigger_delay (duplicate) to get_trigger_holdoff
    def get_trigger_holdoff(self) -> str:
        """Return the holdoff period.

        Returns:
            str: holdoff delay
        """

        return self.__get_data('TRIG:HOLD?')

    def set_trigger_immediate_special_event(self) -> bool:
        """Modifies event detection behaviour. If the system is waiting for
            an event in this layer, this one-time command bypasses event
            detection ECOUNT and DELay causing immediate exit from the
            layer on the downward path. If not waiting at the event detector
            the command is ignored and error -221 issued.

        Returns:
            bool: status
        """
        return self.__write_data('TRIG:IMM')
    
    def set_trigger_signal_level(self, percentage=0) -> bool:
        """Sets the percentage of range at which arming occurs when Source is INTernal.
           Note that The Signal level parameters can be set in any layer but will always 
           be the same for all layers.

        Args:
            percentage (int, optional): Can be integer in range Min -200 % or Max = 200 %. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            percentage = int(percentage)
            if percentage>=-200 and percentage<=200:
                return self.__write_data(f'TRIG:LEV {percentage}')
            else:
                return False
        except:
            return False

    def get_trigger_signal_level(self) -> str:
        """Returns the level setting as a percentage of range.

        Returns:
            str: percentage
        """

        return self.__get_data('TRIG:LEV?')
    
    def set_trigger_default_reset(self) -> bool:
        """Reset the trigger system to default settings. :RESet does not change the state of init continuous.

        Returns:
            bool: status
        """

        return self.__write_data('TRIG:RES')

    def set_trigger_signal_special_event(self) -> bool:
        """Modifies event detection behaviour. If the system is waiting for
            an event in this layer this one-time command bypasses event
            detection. Otherwise, the command is ignored and error -221
            issued.

        Returns:
            bool: status
        """
        return self.__write_data('TRIG:SIGN')

    def set_trigger_internal_slope(self, slope='POS') -> bool:
        """Sets the signal slope that causes the event detector to be
           satisfied if Soure is Internal. See also set_signal_level
            and set_coupling. Note that The Signal level parameters can be 
            set in any layer but will always be the same for all layers.

        Args:
            slope (str, optional): Can be 'POS' for positive edge or 'NEG'. Defaults to 'POS'.

        Returns:
            bool: _description_
        """
        if slope in ['POS', 'NEG']:
            #NOTE: Ovo je bug. POS je setovalo negativnu ivicu pa je ovako sredjeno
            if slope == 'POS':
                return self.__write_data(f'TRIG:SLOP NEG')
            if slope == 'NEG':
                return self.__write_data(f'TRIG:SLOP POS')
        else:
            return False

    def set_trigger_source(self, source) -> bool:
        """Source of ARM signal

        Args:
            source (_type_): BUS = Receipt of *TRG or GET\n
            EXT = Conforming rear panel trigger edge\n
            HOLD = Arming cannot occur unless a immediate or signal command is received\n
            IMM = The process does not stop at the event detector in this layer\n
            INT = Trigger from the signal being measured at the Level
            on the Slope set by the set_level, set_slope and set_coupling commands. \n
            LINE = trigger derived from the mains input. Triggers occur at
            the line frequency rate or multiples of that rate if the trigger
            system cycle time exceeds the line frequency.\n
            MAN = when the TRIG key is pushed\n
            SYNC = Arms when the multimeter's output buffer is
            empty, and the controller requests data.\n
            TIM = at the interval set by set_timer. On the first of
            set_count passes, arming is immediate, subsequent arms occur at TIMer intervals

        Returns:
            bool: status
        """
        if source in ['BUS', 'EXT', 'HOLD', 'IMM', 'INT', 'LINE', 'MAN', 'SYNC', 'TIM']:
            return self.__write_data(f'TRIG:SOUR {source}')
        else:
            return False
        
    def get_trigger_source(self) -> str:
        """Returns the source setting.

        Returns:
            str: source
        """
        return self.__get_data('TRIG:SOUR?')

    def set_trigger_timer(self, timer=2E-7) -> bool:
        """Sets the interval between TIMer events. Only active if Source = timer.

        Args:
            timer (float, optional): Can be from 20 ns up to 4_000_000 s. Defaults to 2E-7(200 ns).

        Returns:
            bool: status
        """
        try:
            timer = float(timer)
            if timer>=0 and timer<=4_000_000:
                return self.__write_data(f'TRIG:TIM {timer}')
            else:
                return False
        except:
            return False
    
    def get_trigger_timer(self) -> str:
        """Returns the timer setting

        Returns:
            str: timer interval
        """
        return self.__get_data('TRIG:TIM?')

    def fetch_data(self) -> list:
        """FETCh? retrieves the last valid measurement or block of
        measurements resulting from a single trigger system transition
        from Idle, through the ARM and Trigger layers back to Idle. The
        number of readings are exactly the product of the ARM2:COUNt, ARM1:COUNt and
        TRIGger:COUNt values. The system will not respond if the
        number of triggers received is less than the product of the trigger
        and two arm count settings.

        Returns:
            list: FETCh? or FETCh? 1 returns the Primary result.
        """
        try:
            format = self.get_memory_format().strip()

            if format == 'PACK,4':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC?', datatype='i', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC?', datatype='i', is_big_endian=False)
            elif format == 'PACK':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC?', datatype='h', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC?', datatype='h', is_big_endian=False)
            elif format == 'ASC':
                return [float(x) for x in self.__get_data('FETC?').split(',')]
            else:
                return None
        except Exception as e:
            print(e)
            return False
        
    def fetch_secondary_data(self) -> list:
        """FETCh? retrieves the last valid measurement or block of
        measurements resulting from a single trigger system transition
        from Idle, through the ARM and Trigger layers back to Idle. The
        number of readings are exactly the product of the ARM2:COUNt, ARM1:COUNt and
        TRIGger:COUNt values. The system will not respond if the
        number of triggers received is less than the product of the trigger
        and two arm count settings.

        Returns:
            list: If the active function provides a secondary reading this can be obtained with
            this function.
        """
        try:
            format = self.get_memory_format().strip()

            if format == 'PACK,4':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC? 2', datatype='i', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC? 2', datatype='i', is_big_endian=False)
            elif format == 'PACK':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC? 2', datatype='h', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC? 2', datatype='h', is_big_endian=False)
            elif format == 'ASC':
                return [float(x) for x in self.__get_data('FETC? 2').split(',')]
            else:
                return None
        except Exception as e:
            print(e)
            return False

    def fetch_front_data_scan_mode(self) -> list:
        """FETCh? retrieves the last valid measurement or block of
        measurements resulting from a single trigger system transition
        from Idle, through the ARM and Trigger layers back to Idle. The
        number of readings are exactly the product of the ARM2:COUNt, ARM1:COUNt and
        TRIGger:COUNt values. The system will not respond if the
        number of triggers received is less than the product of the trigger
        and two arm count settings.

        Returns:
            list: Returns the value at the front terminals in a Scan measurement mode.
        """
        try:
            format = self.get_memory_format().strip()

            if format == 'PACK,4':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC? 3', datatype='i', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC? 3', datatype='i', is_big_endian=False)
            elif format == 'PACK':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC? 3', datatype='h', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC? 3', datatype='h', is_big_endian=False)
            elif format == 'ASC':
                return [float(x) for x in self.__get_data('FETC? 3').split(',')]
            else:
                return None
        except Exception as e:
            print(e)
            return False
        
    def fetch_rear_data_scan_mode(self) -> list:
        """FETCh? retrieves the last valid measurement or block of
        measurements resulting from a single trigger system transition
        from Idle, through the ARM and Trigger layers back to Idle. The
        number of readings are exactly the product of the ARM2:COUNt, ARM1:COUNt and
        TRIGger:COUNt values. The system will not respond if the
        number of triggers received is less than the product of the trigger
        and two arm count settings.

        Returns:
            list: Returns the value at the rear terminals in a Scan measurement mode.
        """
        try:
            format = self.get_memory_format().strip()

            if format == 'PACK,4':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC? 4', datatype='i', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC? 4', datatype='i', is_big_endian=False)
            elif format == 'PACK':
                endianness = self.get_endianness()
                if endianness == 'NORM':
                    return self.__get_binary_data('FETC? 4', datatype='h', is_big_endian=True)
                elif endianness == 'SWAP':
                    return self.__get_binary_data('FETC? 4', datatype='h', is_big_endian=False)
            elif format == 'ASC':
                return [float(x) for x in self.__get_data('FETC? 4').split(',')]
            else:
                return None
        except Exception as e:
            print(e)
            return False

    def fetch_timestamp_offset(self) -> list:
        """FETCh? retrieves the last valid measurement or block of
        measurements resulting from a single trigger system transition
        from Idle, through the ARM and Trigger layers back to Idle. The
        number of readings are exactly the product of the ARM2:COUNt, ARM1:COUNt and
        TRIGger:COUNt values. The system will not respond if the
        number of triggers received is less than the product of the trigger
        and two arm count settings.

        Returns:
            list: Returns the timestamp offset
        """

        return self.__get_data('FETC? 5')

    def set_active_terminals(self, terminal='FRON') -> bool:
        """Sets the active terminals.

        Args:
            terminal (str, optional): Can be FRON for front terminal, REAR for rear terminal,
            SCAN simultaneously taking measuremnts from front and rear terminal and ISOL 
            state of isolation (deselects all INPUT terminals). Defaults to 'FRON'.

        Returns:
            bool: _description_
        """

        if terminal in ['FRON', 'REAR', 'SCAN', 'ISOL']:
            return self.__write_data(f'ROUT:TERM {terminal}')
        else:
            return False

    def get_active_terminals(self) -> str:
        """Returns the active terminals

        Returns:
            str: Currently active terminals.
        """

        return self.__get_data('ROUT:TERM?')

    def set_input_scan(self, mode = 'DIFF') -> bool:
        """Alternately measures at front and rear terminals reporting the
        Difference, Division, or Ratio. Difference = F-R, Division = F/R,
        Ratio = (F-R)/R.

        Args:
            mode (str, optional): Can be DIFF for diference, DIV for division
            and RAT for ratio. Defaults to 'DIFF'.

        Returns:
            bool: status
        """

        if mode in ['DIFF', 'DIV', 'RAT']:
            return self.__write_data(f'ROUT:INP:SCAN:CALC {mode}')
        else:
            return False

    def get_input_scan(self) -> str:
        """Returns the SCAN calculation type

        Returns:
            str: returns scan calculation type
        """

        return  self.__get_data('ROUT:INP:SCAN:CALC?')
    
    def set_input_front_delay(self, delay=0) -> bool:
        """Sets the Scanning front settling delay (seconds). Only apply in
        SCAN mode.  Each Function and range
        has its own unique, optimized AUTO setting.

        Args:
            delay (int, str, optional): Min = 0, Max = 65,000. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            delay = float(delay)
            if delay >= 0 and delay <= 65000:
                return self.__write_data(f'ROUT:INP:FDEL {delay}')
            else:
                return False
        except:
            return False
        
    def get_input_front_delay(self) -> str:
        """Returns the  Scanning front settling delay (seconds).

        Returns:
            str: delay
        """

        return self.__get_data('ROUT:INP:FDEL?')

    def set_input_front_auto_delay(self, auto = 'OFF') -> bool:
        """Configures the Scanning front settling AUTO delay to ON or OFF.

        Args:
            auto (str, optional): Can be ON for enabling and OFF for disabling front auto delay. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if auto in ['ON', 'OFF']:
            return self.__write_data(f'ROUT:INP:FDEL:AUTO {auto}')
        else:
            return False
        
    def get_input_front_auto_delay(self) -> str:
        """Returns the scanning front delay

        Returns:
            str: AUTO state: 0 = OFF, 1 = ON
        """

        return self.__get_data('ROUT:INP:FDEL:AUTO?')

    def set_input_rear_delay(self, delay=0) -> bool:
        """Sets the Scanning rear settling delay (seconds). Only apply in
        SCAN mode.  Each Function and range
        has its own unique, optimized AUTO setting.

        Args:
            delay (int, str, optional): Min = 0, Max = 65,000. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            delay = float(delay)
            if delay >= 0 and delay <= 65000:
                return self.__write_data(f'ROUT:INP:RDEL {delay}')
            else:
                return False
        except:
            return False
        
    def get_input_rear_delay(self) -> str:
        """Returns the  Scanning rear settling delay (seconds).

        Returns:
            str: delay
        """

        return self.__get_data('ROUT:INP:RDEL?')

    def set_input_rear_auto_delay(self, auto = 'OFF') -> bool:
        """Configures the Scanning rear settling AUTO delay to ON or OFF.

        Args:
            auto (str, optional): Can be ON for enabling and OFF for disabling rear auto delay. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if auto in ['ON', 'OFF']:
            return self.__write_data(f'ROUT:INP:RDEL:AUTO {auto}')
        else:
            return False
        
    def get_input_rear_auto_delay(self) -> str:
        """Returns the scanning rear delay

        Returns:
            str: AUTO state: 0 = OFF, 1 = ON
        """

        return self.__get_data('ROUT:INP:RDEL:AUTO?')

    def set_input_guard_state(self, state='OFF') -> bool:
        """Configures External Guard ON or OFF.

        Args:
            state (str, optional): ON enables external guard or OFF disables external guard. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if state in ['ON', 'OFF']:
            return self.__write_data(f'ROUT:INP:GUAR {state}')
        else:
            return False

    def get_input_guard_state(self) -> str:
        """Returns the state of the External Guard

        Returns:
            str: 0 = OFF, 1 = ON
        """

        return self.__get_data('ROUT:INP:GUAR?')
    

    def set_resistance_function(self)-> bool:
        """Sets function to 2-wire Resistance

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "RES"')
    
    def set_resistance_aperture(self, apper = 'DEF') -> bool:
        """Sets the ADC aperture value in seconds or to the MIN, MAX or default setting

        Args:
            apper (str, optional): ADC aperture value in seconds or MIN|MAX|DEF. The smallest time aperture is 0 seconds with
            200 ns increments and has an upper time limit of 10 seconds. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            apper = float(apper)
            if apper<=10 and apper>=0:
                return self.__write_data(f'RES:APER {apper}')
            else:
                return False
        except ValueError:
            if (apper in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'RES:APER {apper}')
            else:
                return False

    def get_resistance_aperture(self) -> str:
        """Gets the ADC aperture value in seconds or to the MIN, MAX, or Default setting.

        Returns:
            str: ADC aperture value in seconds.
        """
        return self.__get_data(f'RES:APER?')

    def set_resistance_aperture_mode(self, mode='AUTO') -> bool:
        """Sets the aperture mode.

        Args:
            mode (str, optional): Mode can be AUTO, FAST or MAN (manual). Defaults to "AUTO".

        Returns:
            bool: status
        """

        if mode in ['AUTO','FAST','MAN']:
            return self.__write_data(f'RES:APER:MODE {mode}')
        else:
            return False
        
    def get_resistance_aperture_mode(self) -> str:
        """Gets the aperture mode and it can be AUTO, FAST or MAN (manual).

        Returns:
            str: aperture mode.
        """
        return self.__get_data(f'RES:APER:MODE?')

    def set_resistance_nplc(self, nplc = 'DEF') -> bool:
        """Sets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Args:
            nplc (str, optional): Can be MIN, MAX, DEF or can be in range [0.01, 500]. Defaults to 'DEF'. 
            The smallest aperture that can be set by PLC is 0.01.

        Returns:
            bool: status
        """
        try:
            nplc = float(nplc)
            if nplc<=500 and nplc>=0.01:
                return self.__write_data(f'RES:NPLC {nplc}')
            else:
                return False
        except ValueError:
            if (nplc in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'RES:NPLC {nplc}')
            else:
                return False

    def get_resistance_nplc(self) -> str:
        """Gets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Returns:
            str: number of power line cycles
        """
        return self.__get_data(f'RES:NPLC?')
    

    def set_resistance_autorange(self, autorange='ON') -> bool:
        """Turns Auto range ON or OFF.

        Args:
            autorange (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if autorange in ['ON', 'OFF']:
            return self.__write_data(f'RES:RANG:AUTO {autorange}')
        else:
            return False
        
    def get_resistance_autorange(self) -> str:
        """Gets autorange status.

        Returns:
            str: Returns 1 for Auto range ON, 0 for auto range OFF.
        """
        return self.__get_data(f'RES:RANG:AUTO?')

    def set_resistance_range(self, range='DEF') -> bool:
        """Set maximum expected value or min, max or default range.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or can be [1, 10, 100, 1E3, 1E4, 1E5, 1E6, 1E7, 1E8, 1E9, 1E10]. 
            Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range<=1E10 and range>=1:
                return self.__write_data(f'RES:RANG {range}')
            else:
                return False
        except ValueError:
            if (range in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'RES:RANG {range}')
            else:
                return False

    def get_resistance_range(self) -> str:
        """Returns the selected range, or if specified, the MIN, MAX, or Default range

        Returns:
            str: Resistance range
        """
        return self.__get_data(f'RES:RANG?')
    
    def set_resistance_resolution(self, res='DEF') -> bool:
        """Set maximum expected value or min, max or default resolution;

        Args:
            resolution (str, optional): Can be 'MIN', 'MAX', 'DEF' or user defined number. Defaults to 'DEF'.

        Returns:
            bool: status
        """ 

        try:
            res = float(res)
            if res<=1E9 and res>=0:
                return self.__write_data(f'RES:RES {res}')
            else:
                return False
        except ValueError:
            if (res in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'RES:RES {res}')
            else:
                return False
            
    def get_resistance_resolution(self) -> str:
        """Returns the selected resolution, or if specified, the minimum, maximum or default range.

        Returns:
            str: resolution
        """

        return self.__get_data(f'RES:RES?')
    
    def set_resistance_filter_state(self, state) -> bool:
        """Turns the input filter ON or OFF.

        Args:
            state (str): Can be ON or OFF.

        Returns:
            bool: status
        """

        if state in ['ON', 'OFF']:
            return self.__write_data(f'RES:FILT {state}')
        else:
            return False
        
    def get_resistance_filter_state(self) -> str:
        """Returns the filter setting

        Returns:
            str: 0 = OFF, 1 = ON
        """

        return self.__get_data(f'RES:FILT?')
    
    def set_resistance_mode(self, mode='NORM') -> bool:
        """Sets the 2-wire Ohms mode

        Args:
            mode (str, optional): NORM for normal mode and HIV for high voltage mode. Defaults to 'NORM'.

        Returns:
            bool: status
        """
        if mode in ['NORM', 'HIV']:
            return self.__write_data(f'RES:MODE {mode}')
        else:
            return False
        

    def get_resistance_mode(self) -> str:
        """Returns the 2-wire Ohms mode setting

        Returns:
            str: mode
        """

        # CHANGED: was __write_data (bug), should be __get_data
        return self.__get_data(f'RES:MODE?')
    
    def set_resistance_low_current_state(self, state) -> bool:
        """Sets the Low current mode

        Args:
            state (str): Can be ON or OFF for enabling or disabling losw current mode.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'RES:LOWI {state}')
        else:
            return False
        
    def get_resistance_low_current_state(self) -> str:
        """Returns the low current mode setting

        Returns:
            str: low current mode setting state
        """

        return self.__get_data('RES:LOWI?')

    def set_four_wire_resistance_function(self)-> bool:
        """Sets function to 4-wire Resistance

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "FRES"')
    
    def set_four_wire_resistance_aperture(self, apper = 'DEF') -> bool:
        """Sets the ADC aperture value in seconds or to the MIN, MAX or default setting

        Args:
            apper (str, optional): ADC aperture value in seconds or MIN|MAX|DEF. The smallest time aperture is 0 seconds with
            200 ns increments and has an upper time limit of 10 seconds. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            apper = float(apper)
            if apper<=10 and apper>=0:
                return self.__write_data(f'FRES:APER {apper}')
            else:
                return False
        except ValueError:
            if (apper in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'FRES:APER {apper}')
            else:
                return False

    def get_four_wire_resistance_aperture(self) -> str:
        """Gets the ADC aperture value in seconds or to the MIN, MAX, or Default setting.

        Returns:
            str: ADC aperture value in seconds.
        """
        return self.__get_data(f'FRES:APER?')

    def set_four_wire_resistance_aperture_mode(self, mode='AUTO') -> bool:
        """Sets the aperture mode.

        Args:
            mode (str, optional): Mode can be AUTO, FAST or MAN (manual). Defaults to "AUTO".

        Returns:
            bool: status
        """

        if mode in ['AUTO','FAST','MAN']:
            return self.__write_data(f'FRES:APER:MODE {mode}')
        else:
            return False
        
    def get_four_wire_resistance_aperture_mode(self) -> str:
        """Gets the aperture mode and it can be AUTO, FAST or MAN (manual).

        Returns:
            str: aperture mode.
        """
        return self.__get_data(f'FRES:APER:MODE?')

    def set_four_wire_resistance_nplc(self, nplc = 'DEF') -> bool:
        """Sets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Args:
            nplc (str, optional): Can be MIN, MAX, DEF or can be in range [0.01, 500]. Defaults to 'DEF'. 
            The smallest aperture that can be set by PLC is 0.01.

        Returns:
            bool: status
        """
        try:
            nplc = float(nplc)
            if nplc<=500 and nplc>=0.01:
                return self.__write_data(f'FRES:NPLC {nplc}')
            else:
                return False
        except ValueError:
            if (nplc in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'FRES:NPLC {nplc}')
            else:
                return False

    def get_four_wire_resistance_nplc(self) -> str:
        """Gets the ADC aperture in number of power line cycles or to the MIN, MAX or Default plc setting.

        Returns:
            str: number of power line cycles
        """
        return self.__get_data(f'FRES:NPLC?')
    

    def set_four_wire_resistance_autorange(self, autorange='ON') -> bool:
        """Turns Auto range ON or OFF.

        Args:
            autorange (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if autorange in ['ON', 'OFF']:
            return self.__write_data(f'FRES:RANG:AUTO {autorange}')
        else:
            return False
        
    def get_four_wire_resistance_autorange(self) -> str:
        """Gets autorange status.

        Returns:
            str: Returns 1 for Auto range ON, 0 for auto range OFF.
        """
        return self.__get_data(f'FRES:RANG:AUTO?')

    def set_four_wire_resistance_range(self, range='DEF') -> bool:
        """Set maximum expected value or min, max or default range.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or can be [1, 10, 100, 1E3, 1E4, 1E5, 1E6, 1E7, 1E8, 1E9, 1E10]. 
            Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range<=1E10 and range>=1:
                return self.__write_data(f'FRES:RANG {range}')
            else:
                return False
        except ValueError:
            if (range in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'FRES:RANG {range}')
            else:
                return False

    def get_four_wire_resistance_range(self) -> str:
        """Returns the selected range, or if specified, the MIN, MAX, or Default range

        Returns:
            str: Resistance range
        """
        return self.__get_data(f'FRES:RANG?')
    
    def set_four_wire_resistance_resolution(self, res='DEF') -> bool:
        """Set maximum expected value or min, max or default resolution;

        Args:
            resolution (str, optional): Can be 'MIN', 'MAX', 'DEF' or user defined number. Defaults to 'DEF'.

        Returns:
            bool: status
        """ 

        try:
            res = float(res)
            if res<=1E9 and res>=0:
                return self.__write_data(f'FRES:RES {res}')
            else:
                return False
        except ValueError:
            if (res in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'FRES:RES {res}')
            else:
                return False
            
    def get_four_wire_resistance_resolution(self) -> str:
        """Returns the selected resolution, or if specified, the minimum, maximum or default range.

        Returns:
            str: resolution
        """

        return self.__get_data(f'FRES:RES?')
    
    def set_four_wire_resistance_filter_state(self, state) -> bool:
        """Turns the input filter ON or OFF.

        Args:
            state (str): Can be ON or OFF.

        Returns:
            bool: status
        """

        if state in ['ON', 'OFF']:
            return self.__write_data(f'FRES:FILT {state}')
        else:
            return False
        
    def get_four_wire_resistance_filter_state(self) -> str:
        """Returns the filter setting

        Returns:
            str: 0 = OFF, 1 = ON
        """

        return self.__get_data(f'FRES:FILT?')
    
    def set_four_wire_resistance_mode(self, mode='NORM') -> bool:
        """Sets the 4-wire Ohms mode

        Args:
            mode (str, optional): NORM for normal mode, HIV for high voltage mode
            and TRUE for true mode. Defaults to 'NORM'.

        Returns:
            bool: status
        """
        if mode in ['NORM', 'HIV', 'TRUE']:
            return self.__write_data(f'FRES:MODE {mode}')
        else:
            return False
        

    def get_four_wire_resistance_mode(self) -> str:
        """Returns the 4-wire Ohms mode setting

        Returns:
            str: mode
        """

        # CHANGED: was __write_data (bug), should be __get_data
        return self.__get_data(f'FRES:MODE?')
    
    def set_four_wire_resistance_low_current_state(self, state) -> bool:
        """Sets the Low current mode

        Args:
            state (str): Can be ON or OFF for enabling or disabling losw current mode.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'FRES:LOWI {state}')
        else:
            return False
        
    def get_four_wire_resistance_low_current_state(self) -> str:
        """Returns the low current mode setting

        Returns:
            str: low current mode setting state
        """

        return self.__get_data('FRES:LOWI?')

    def set_ac_voltage_bandwidth(self, band = "WIDE") -> bool:
        """Sets the operating mode of the AC voltage function.

        Args:
            band (str, optional): WIDE for wide bandwidth or EHF for enhanced high frequency bandwidth. Defaults to "WIDE".

        Returns:
            bool: status
        """
        if band in ['WIDE', 'EHF']:
            return self.__write_data(f'VOLT:AC:BWID {band}')
        else:
            return False
        
    def get_ac_voltage_bandwidth(self) -> str:
        """Returns the operating mode of the AC voltage function.

        Returns:
            str: bandwidth
        """
        return self.__get_data(f'VOLT:AC:BWID?')
    
    def set_ac_voltage_counter_bandwith_limit(self, limit = 'ON') -> bool:
        """Turns the Counter bandwidth limit ON or OFF.

        Args:
            limit (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """

        if limit in ['ON', 'OFF']:
            return self.__write_data(f'VOLT:AC:COUN:BLIM {limit}')
        else:
            return False
        
    def get_ac_voltage_counter_bandwith_limit(self) -> str:
        """Returns the Counter bandwidth limit setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """

        return self.__get_data(f'VOLT:AC:COUN:BLIM?')
    
    def set_ac_voltage_counter_coupling_secondary(self, coupling = 'AC') -> bool:
        """Set the coupling path for the secondary frequency measurement. 
        Forced to AC if the signal path coupling is AC.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """
        if coupling in ['AC', 'DC']:
            return self.__write_data(f'VOLT:AC:COUN:COUP {coupling}')
        else:
            return False
        
    def get_ac_voltage_counter_coupling_secondary(self) -> str:
        """Returns the coupling path for the secondary frequency measurement.

        Returns:
            str: AC or DC
        """
        return self.__get_data(f'VOLT:AC:COUN:COUP?')
    
    def set_ac_voltage_auto_counter_gate(self, state = 'ON') -> bool:
        """Turn Auto selection of counter gate ON or OFF

        Args:
            state (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'VOLT:AC:COUNT:GATE:AUTO {state}')
        else:
            return False
        
    def get_ac_voltage_auto_counter_gate(self) -> str:
        """Returns the Auto selection of counter gate.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data(f'VOLT:AC:COUNT:GATE:AUTO?')
    
    def set_ac_voltage_secondary_frequency_gate(self, range = 0) -> bool:
        """Sets the secondary frequency counter measurement gate.

        Args:
            range (int, optional): Can be MIN, MAX, DEF or 1E-3, 10E-3, 0.1, 1. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range<=1 and range>=0:
                return self.__write_data(f'VOLT:AC:COUN:GATE {range}')
            else:
                return False
        except ValueError:
            if (range in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:AC:COUN:GATE {range}')
            else:
                return False
    
    def get_ac_voltage_secondary_frequency_gate(self) -> str:
        """Returns the secondary frequency counter measurement gate.

        Returns:
            str: frequency gate
        """
        return self.__get_data(f'VOLT:AC:COUN:GATE?')
    
    def set_ac_voltage_coupling_and_impedance(self, coupling_and_impedance = 'AC1M') -> bool:
        """Sets the coupling and impedance of the AC voltage function.

        Args:
            coupling_and_impedance (str, optional): Can be AC1M, AC10M, DC1M, DC10M, DCAUTO. Defaults to 'AC1M'.

        Returns:
            bool: status
        """
        if coupling_and_impedance in ['AC1M', 'AC10M', 'DC1M', 'DC10M', 'DCAUTO']:
            return self.__write_data(f'VOLT:AC:COUP:SIGN {coupling_and_impedance}')
        else:
            return False
        
    def get_ac_voltage_coupling_and_impedance(self) -> str:
        """Returns the coupling and impedance of the AC voltage function.

        Returns:
            str: coupling and impedance.
        """
        return self.__get_data(f'VOLT:AC:COUP:SIGN?')

    def set_ac_voltage_input_rms_filter(self, nrf= 'MIN') -> bool:
        """Sets the input filter to value or to the minimum, maximum or
        default setting. The filter setting range is 0.1 Hz to 1 kHz, the
        discrete settings are: 0.1 Hz, 1 Hz, 10 Hz, 40 Hz, 100 Hz, 1 kHz.
        The discrete setting closest to <nrf> will be selected.

        Args:
            nrf (str, optional): Can be DEF, MIN, MAX or can be in range [0.1, 1, 10, 40, 100, 1000]. Defaults to 'MIN'.

        Returns:
            bool: status
        """
        try:
            nrf = float(nrf)
            if nrf in [0.1, 1, 10, 40, 100, 1000]:
                return self.__write_data(f'VOLT:AC:FILT {nrf}')
            else:
                return False
        except ValueError:
            if (nrf in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:AC:FILT {nrf}')
            else:
                return False
            
    def get_ac_voltage_input_rms_filter(self) -> str:
        """Returns the input filter setting.

        Returns:
            str: input filter setting.
        """
        return self.__get_data(f'VOLT:AC:FILT?')
    
    def set_ac_voltage_autorange(self, autorange='ON') -> bool:
        """Turns Auto range ON or OFF.

        Args:
            autorange (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if autorange in ['ON', 'OFF']:
            return self.__write_data(f'VOLT:AC:RANG:AUTO {autorange}')
        else:
            return False
        
    def get_ac_voltage_autorange(self) -> str:
        """Gets autorange status.

        Returns:
            str: Returns 1 for Auto range ON, 0 for auto range OFF.
        """
        return self.__get_data(f'VOLT:AC:RANG:AUTO?')
    
    def set_ac_voltage_function(self)-> bool:
        """Sets function to ACV

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "VOLT:AC"')

    def set_ac_voltage_range(self, range='DEF') -> bool:
        """Set maximum expected value or MIN, MAX, or Default range.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or can be [0.01, 0.1, 1, 10, 100, 1000]. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range<=1000 and range>=0.001:
                return self.__write_data(f'VOLT:AC:RANG {range}')
            else:
                return False
        except ValueError:
            if (range in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:AC:RANG {range}')
            else:
                return False
            
    def get_ac_voltage_range(self) -> str:
        """Returns the selected range, or if specified, the MIN, MAX, or Default range

        Returns:
            str: AC voltage range
        """
        return self.__get_data(f'VOLT:AC:RANG?')
    
    def set_ac_voltage_resolution(self, res='DEF') -> bool:
        """Set maximum expected value or min, max or default resolution;
        for example, range is 1 V, Resolution res = 0.0001 (100 μV),
        the measurement is returned with a resolution of +1.000E-4

        Args:
            resolution (str, optional): Can be 'MIN', 'MAX', 'DEF' or user defined number. Defaults to 'DEF'.

        Returns:
            bool: status
        """ 

        try:
            res = float(res)
            if res<=100 and res>=0:
                return self.__write_data(f'VOLT:AC:RES {res}')
            else:
                return False
        except ValueError:
            if (res in ['DEF', 'MIN', 'MAX']): 
                return self.__write_data(f'VOLT:AC:RES {res}')
            else:
                return False
            
    def get_ac_voltage_resolution(self) -> str:
        """Returns the selected resolution, or if specified, the minimum, maximum or default range.

        Returns:
            str: resolution
        """

        return self.__get_data(f'VOLT:AC:RES?')
    
    def set_ac_voltage_secondary_reading_type(self, type='OFF') -> bool:
        """Sets the secondary reading type:
            OFF = Secondary reading is not shown
            FREQuency = Secondary reading is frequency
            PERiod = Secondary reading is period
            PTP = Secondary reading is peak-to-peak
            PPEak = Secondary reading is positive peak
            NPEak = Secondary reading is negative peak
            CFACtor = Secondary reading is the crest factor

        Args:
            type (str, optional): Can be OFF, FREQuency, PERiod, PTP, PPEak, NPEak or CFACtor. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if type in ['OFF', 'FREQuency', 'PERiod', 'PTP', 'PPEak', 'NPEak', 'CFACtor', 'FREQ', 'PER', 'PPE', 'NPE', 'CFAC']:
            return self.__write_data(f'VOLT:AC:SEC {type}')
        else:
            return False
        
    def get_ac_voltage_secondary_reading_type(self) -> str:
        """Returns the selected secondary reading setting.
        
        Returns:
            str: OFF, FREQuency, PERiod, PTP, PPEak, NPEak or CFACtor
        """
        return self.__get_data(f'VOLT:AC:SEC?')
    
    def set_ac_voltage_secondary_method(self, method = 'MEAS') -> bool:
        """Set the method by which the secondary peak-to-peak value is calculated
        MEASured = The measured positive peak minus the measured negative peak value
        SINe = The peak to peak of a sine wave calculated from the rms value
        SQUare = The peak to peak of a square wave calculated from the rms value
        TRIange = The peak to peak of a triangle waveform calculated from the rms value
        TRUNcated = The peak to peak of a truncated sine wave calculated from the rms value

        Returns:
            bool: status
        """
        if method in ['MEAS', 'SINe', 'SQUare', 'TRIange', 'TRUNcated', 'MEASured', 'SIN', 'SQU', 'TRI', 'TRUN']:
            return self.__write_data(f'VOLT:AC:SEC:METH {method}')
        else:
            return False
        
    def get_ac_voltage_secondary_method(self) -> str:
        """Returns the selected peak to peak method.

        Returns:
            str: MEAS, SINe, SQUare, TRIange, TRUNcated, MEASured, SIN, SQU, TRI, TRUN
        """
        return self.__get_data(f'VOLT:AC:SEC:METH?')

    def get_memory_average(self) -> str:
        """Returns the average of elements in memory/record in the statistics calculation.

        Returns:
            str: average
        """

        return self.__get_data('CALC:SST:AVER?')
    
    def get_memory_count(self) -> str:
        """Returns the count of elements in memory/record in the statistics calculation.

        Returns:
            str: memory count
        """

        return self.__get_data('CALC:SST:COUN?')
    
    def get_memory_max(self) -> str:
        """Returns the maximum value

        Returns:
            str: maximum value
        """

        return self.__get_data('CALC:SST:MAX?')

    def get_memory_min(self) -> str:
        """Returns the minimum value

        Returns:
            str: minimum value
        """

        return self.__get_data('CALC:SST:MIN?')
    

    def set_memory_stdev_ppm(self, ppm = False) -> bool:
        """Sets the Standard Deviation value or Standard Deviation in ppm

        Args:
            ppm (bool, optional): False = Standard Deviation value or True = Standard Deviation value in ppm.
            Defaults to False.

        Returns:
            bool: status
        """

        if ppm == True:
            return self.__write_data('CALC:SST:SDEV PPM')
        elif ppm == False:
            return self.__write_data('CALC:SST:SDEV')
        else:
            return False

    def get_memory_stdev(self) -> str:
        """Returns the standard deviation

        Returns:
            str: standard deviation
        """

        return self.__get_data('CALC:SST:SDEV?')
    
    def get_memory_readings_span(self) -> str:
        """Retuns the span of the readings

        Returns:
            str: span of the readings (Max – Min)
        """

        return self.__get_data('CALC:SST:SPAN?')
    
    def set_statistics_state(self, state='OFF') -> bool:
        """Turns statistics state ON or OFF.

        Args:
            state (str, optional): ON enables or OFF disables statistics. Defaults to 'OFF'.

        Returns:
            bool: status
        """

        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:SST:STAT {state}')
        else:
            return False

    def get_statistics_state(self) -> str:
        """Returns the statistics state.

        Returns:
            str: statistics state
        """

        return self.__get_data('CALC:SST:STAT?')

    # -------------------------------------------------------------------------
    # AC Current (CURR:AC)
    # -------------------------------------------------------------------------

    def set_current_ac_function(self) -> bool:
        """Sets function to ACI

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "CURR:AC"')

    def set_current_ac_range(self, range='DEF') -> bool:
        """Set maximum expected value or min, max or default range.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or a value in [10E-6 .. 30]. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range <= 30 and range >= 10E-6:
                return self.__write_data(f'CURR:AC:RANG {range}')
            else:
                return False
        except ValueError:
            if range in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'CURR:AC:RANG {range}')
            else:
                return False

    def get_current_ac_range(self) -> str:
        """Returns the selected ACI range.

        Returns:
            str: ACI range
        """
        return self.__get_data('CURR:AC:RANG?')

    def set_current_ac_autorange(self, autorange='ON') -> bool:
        """Turns Auto range ON or OFF for ACI.

        Args:
            autorange (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if autorange in ['ON', 'OFF']:
            return self.__write_data(f'CURR:AC:RANG:AUTO {autorange}')
        else:
            return False

    def get_current_ac_autorange(self) -> str:
        """Gets ACI autorange status.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CURR:AC:RANG:AUTO?')

    def set_current_ac_resolution(self, res='DEF') -> bool:
        """Set ACI resolution.

        Args:
            res (str, optional): Can be 'MIN', 'MAX', 'DEF' or a numeric value. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            res = float(res)
            if res >= 0:
                return self.__write_data(f'CURR:AC:RES {res}')
            else:
                return False
        except ValueError:
            if res in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'CURR:AC:RES {res}')
            else:
                return False

    def get_current_ac_resolution(self) -> str:
        """Returns the selected ACI resolution.

        Returns:
            str: resolution
        """
        return self.__get_data('CURR:AC:RES?')

    def set_current_ac_filter(self, nrf='DEF') -> bool:
        """Sets the AC current RMS filter value.
        The filter setting range is 0.1 Hz to 1 kHz. Discrete settings: 0.1, 1, 10, 40, 100, 1000 Hz.

        Args:
            nrf (str, optional): Can be 'DEF', 'MIN', 'MAX' or one of [0.1, 1, 10, 40, 100, 1000]. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            nrf = float(nrf)
            if nrf in [0.1, 1, 10, 40, 100, 1000]:
                return self.__write_data(f'CURR:AC:FILT {nrf}')
            else:
                return False
        except ValueError:
            if nrf in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'CURR:AC:FILT {nrf}')
            else:
                return False

    def get_current_ac_filter(self) -> str:
        """Returns the AC current filter setting.

        Returns:
            str: filter setting
        """
        return self.__get_data('CURR:AC:FILT?')

    def set_current_ac_coupling(self, coupling='AC') -> bool:
        """Set the AC current signal path coupling.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """
        if coupling in ['AC', 'DC']:
            return self.__write_data(f'CURR:AC:COUP {coupling}')
        else:
            return False

    def get_current_ac_coupling(self) -> str:
        """Returns the AC current coupling setting.

        Returns:
            str: AC or DC
        """
        return self.__get_data('CURR:AC:COUP?')

    def set_current_ac_secondary_reading_type(self, type='OFF') -> bool:
        """Sets the ACI secondary reading type.
            OFF, FREQuency, PERiod, PTP, PPEak, NPEak, CFACtor

        Args:
            type (str, optional): Secondary reading type. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if type in ['OFF', 'FREQuency', 'PERiod', 'PTP', 'PPEak', 'NPEak', 'CFACtor',
                    'FREQ', 'PER', 'PPE', 'NPE', 'CFAC']:
            return self.__write_data(f'CURR:AC:SEC {type}')
        else:
            return False

    def get_current_ac_secondary_reading_type(self) -> str:
        """Returns the selected ACI secondary reading type.

        Returns:
            str: secondary reading type
        """
        return self.__get_data('CURR:AC:SEC?')

    def set_current_ac_counter_bandwidth_limit(self, limit='OFF') -> bool:
        """Turn the frequency path bandwidth limit ON or OFF for ACI.

        Args:
            limit (str, optional): Can be ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if limit in ['ON', 'OFF']:
            return self.__write_data(f'CURR:AC:COUN:BLIM {limit}')
        else:
            return False

    def get_current_ac_counter_bandwidth_limit(self) -> str:
        """Returns the frequency path bandwidth limit state for ACI.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CURR:AC:COUN:BLIM?')

    def set_current_ac_counter_coupling(self, coupling='AC') -> bool:
        """Set the frequency path coupling for ACI secondary frequency measurement.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """
        if coupling in ['AC', 'DC']:
            return self.__write_data(f'CURR:AC:COUN:COUP {coupling}')
        else:
            return False

    def get_current_ac_counter_coupling(self) -> str:
        """Returns the ACI frequency path coupling.

        Returns:
            str: AC or DC
        """
        return self.__get_data('CURR:AC:COUN:COUP?')

    def set_current_ac_auto_counter_gate(self, state='ON') -> bool:
        """Turn Auto selection of counter gate ON or OFF for ACI.

        Args:
            state (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CURR:AC:COUN:GATE:AUTO {state}')
        else:
            return False

    def get_current_ac_auto_counter_gate(self) -> str:
        """Returns the ACI counter gate auto setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CURR:AC:COUN:GATE:AUTO?')

    # -------------------------------------------------------------------------
    # Capacitance (CAP)
    # -------------------------------------------------------------------------

    def set_capacitance_function(self) -> bool:
        """Sets function to Capacitance.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "CAP"')

    def set_capacitance_range(self, range='DEF') -> bool:
        """Set maximum expected value or min, max or default range for Capacitance.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or a numeric value. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range >= 0:
                return self.__write_data(f'CAP:RANG {range}')
            else:
                return False
        except ValueError:
            if range in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'CAP:RANG {range}')
            else:
                return False

    def get_capacitance_range(self) -> str:
        """Returns the capacitance range.

        Returns:
            str: capacitance range
        """
        return self.__get_data('CAP:RANG?')

    def set_capacitance_autorange(self, autorange='ON') -> bool:
        """Turns Auto range ON or OFF for Capacitance.

        Args:
            autorange (str, optional): Can be ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if autorange in ['ON', 'OFF']:
            return self.__write_data(f'CAP:RANG:AUTO {autorange}')
        else:
            return False

    def get_capacitance_autorange(self) -> str:
        """Gets capacitance autorange status.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CAP:RANG:AUTO?')

    def set_capacitance_resolution(self, res='DEF') -> bool:
        """Set capacitance resolution.

        Args:
            res (str, optional): Can be 'MIN', 'MAX', 'DEF' or a numeric value. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            res = float(res)
            if res >= 0:
                return self.__write_data(f'CAP:RES {res}')
            else:
                return False
        except ValueError:
            if res in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'CAP:RES {res}')
            else:
                return False

    def get_capacitance_resolution(self) -> str:
        """Returns the selected capacitance resolution.

        Returns:
            str: resolution
        """
        return self.__get_data('CAP:RES?')

    def set_capacitance_low_current(self, state='OFF') -> bool:
        """Selects Low current mode for capacitance.

        Args:
            state (str, optional): Can be ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CAP:LOWI {state}')
        else:
            return False

    def get_capacitance_low_current(self) -> str:
        """Returns capacitance Low Current mode.

        Returns:
            str: 0 = OFF, 1 = ON
        """
        return self.__get_data('CAP:LOWI?')

    # -------------------------------------------------------------------------
    # Frequency (FREQ)
    # -------------------------------------------------------------------------

    def set_frequency_function(self) -> bool:
        """Sets function to Frequency.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "FREQ"')

    def set_frequency_gate(self, gate='DEF') -> bool:
        """Set gate time to the numeric value in seconds or to min, max or default setting.

        Args:
            gate (str, optional): Can be 'MIN', 'MAX', 'DEF' or a numeric value in seconds. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            gate = float(gate)
            if gate >= 0:
                return self.__write_data(f'FREQ:GATE {gate}')
            else:
                return False
        except ValueError:
            if gate in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'FREQ:GATE {gate}')
            else:
                return False

    def get_frequency_gate(self) -> str:
        """Returns the selected frequency gate setting.

        Returns:
            str: gate time in seconds
        """
        return self.__get_data('FREQ:GATE?')

    def set_frequency_coupling(self, coupling='AC') -> bool:
        """Sets the frequency path to ac or dc coupled.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """
        if coupling in ['AC', 'DC']:
            return self.__write_data(f'FREQ:COUP {coupling}')
        else:
            return False

    def get_frequency_coupling(self) -> str:
        """Returns the frequency coupling setting.

        Returns:
            str: AC or DC
        """
        return self.__get_data('FREQ:COUP?')

    def set_frequency_bandwidth_limit(self, state='OFF') -> bool:
        """Sets the frequency bandwidth limit ON or OFF.

        Args:
            state (str, optional): Can be ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'FREQ:BWLIM {state}')
        else:
            return False

    def get_frequency_bandwidth_limit(self) -> str:
        """Returns the frequency bandwidth limit setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('FREQ:BWLIM?')

    def set_frequency_route_signal(self, route='BNC') -> bool:
        """Sets the Frequency input path.

        Args:
            route (str, optional): Can be BNC, ACI or ACV. Defaults to 'BNC'.

        Returns:
            bool: status
        """
        if route in ['BNC', 'ACI', 'ACV']:
            return self.__write_data(f'FREQ:ROUT:SIGN {route}')
        else:
            return False

    def get_frequency_route_signal(self) -> str:
        """Returns the Frequency input path setting.

        Returns:
            str: BNC, ACI or ACV
        """
        return self.__get_data('FREQ:ROUT:SIGN?')

    def set_frequency_bnc_impedance(self, impedance='50R') -> bool:
        """Sets the impedance for the rear panel BNC input for Frequency.

        Args:
            impedance (str, optional): Can be 50R or HIGH. Defaults to '50R'.

        Returns:
            bool: status
        """
        if impedance in ['50R', 'HIGH']:
            return self.__write_data(f'FREQ:ROUT:BNC:IMP {impedance}')
        else:
            return False

    def get_frequency_bnc_impedance(self) -> str:
        """Returns the impedance for the rear panel BNC input for Frequency.

        Returns:
            str: 50R or HIGH
        """
        return self.__get_data('FREQ:ROUT:BNC:IMP?')

    def set_frequency_bnc_threshold(self, threshold='DEF') -> bool:
        """Set frequency BNC threshold (-5.0 V to 5.0 V).

        Args:
            threshold (str, optional): Can be 'DEF', 'MIN', 'MAX' or numeric value in range [-5.0, 5.0]. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            threshold = float(threshold)
            if -5.0 <= threshold <= 5.0:
                return self.__write_data(f'FREQ:ROUT:BNC:THR {threshold}')
            else:
                return False
        except ValueError:
            if threshold in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'FREQ:ROUT:BNC:THR {threshold}')
            else:
                return False

    def get_frequency_bnc_threshold(self) -> str:
        """Returns the frequency BNC threshold setting.

        Returns:
            str: threshold value
        """
        return self.__get_data('FREQ:ROUT:BNC:THR?')

    # -------------------------------------------------------------------------
    # Period (PER)
    # -------------------------------------------------------------------------

    def set_period_function(self) -> bool:
        """Sets function to Period.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "PER"')

    def set_period_gate(self, gate='DEF') -> bool:
        """Set period gate time in seconds or to min, max or default setting.

        Args:
            gate (str, optional): Can be 'MIN', 'MAX', 'DEF' or a numeric value. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            gate = float(gate)
            if gate >= 0:
                return self.__write_data(f'PER:GATE {gate}')
            else:
                return False
        except ValueError:
            if gate in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'PER:GATE {gate}')
            else:
                return False

    def get_period_gate(self) -> str:
        """Returns the selected period gate setting.

        Returns:
            str: gate time in seconds
        """
        return self.__get_data('PER:GATE?')

    def set_period_coupling(self, coupling='AC') -> bool:
        """Sets the Period path to ac or dc coupled.

        Args:
            coupling (str, optional): Can be AC or DC. Defaults to 'AC'.

        Returns:
            bool: status
        """
        if coupling in ['AC', 'DC']:
            return self.__write_data(f'PER:COUP {coupling}')
        else:
            return False

    def get_period_coupling(self) -> str:
        """Returns the period coupling setting.

        Returns:
            str: AC or DC
        """
        return self.__get_data('PER:COUP?')

    def set_period_bandwidth_limit(self, state='OFF') -> bool:
        """Sets the period bandwidth limit ON or OFF.

        Args:
            state (str, optional): Can be ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'PER:BWLIM {state}')
        else:
            return False

    def get_period_bandwidth_limit(self) -> str:
        """Returns the period bandwidth limit setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('PER:BWLIM?')

    def set_period_route_signal(self, route='BNC') -> bool:
        """Sets the Period input path.

        Args:
            route (str, optional): Can be BNC, ACI or ACV. Defaults to 'BNC'.

        Returns:
            bool: status
        """
        if route in ['BNC', 'ACI', 'ACV']:
            return self.__write_data(f'PER:ROUT:SIGN {route}')
        else:
            return False

    def get_period_route_signal(self) -> str:
        """Returns the Period input path setting.

        Returns:
            str: BNC, ACI or ACV
        """
        return self.__get_data('PER:ROUT:SIGN?')

    def set_period_bnc_impedance(self, impedance='50R') -> bool:
        """Sets the impedance for the rear panel BNC input for Period.

        Args:
            impedance (str, optional): Can be 50R or HIGH. Defaults to '50R'.

        Returns:
            bool: status
        """
        if impedance in ['50R', 'HIGH']:
            return self.__write_data(f'PER:ROUT:BNC:IMP {impedance}')
        else:
            return False

    def get_period_bnc_impedance(self) -> str:
        """Returns the impedance for the rear panel BNC input for Period.

        Returns:
            str: 50R or HIGH
        """
        return self.__get_data('PER:ROUT:BNC:IMP?')

    # -------------------------------------------------------------------------
    # Temperature - RTD / TRTD / FRTD
    # -------------------------------------------------------------------------

    def set_temperature_rtd_function(self, wires=2) -> bool:
        """Sets function to RTD temperature (2, 3 or 4-wire PRT).

        Args:
            wires (int, optional): Number of wires: 2 = RTD, 3 = TRTD, 4 = FRTD. Defaults to 2.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires in mapping:
            return self.__write_data(f'FUNC "{mapping[wires]}"')
        else:
            return False

    def set_temperature_rtd_aperture(self, wires=2, apper='DEF') -> bool:
        """Sets the ADC aperture for RTD/TRTD/FRTD temperature measurement.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.
            apper (str, optional): Aperture in seconds or MIN|MAX|DEF. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return False
        try:
            apper = float(apper)
            if apper >= 0:
                return self.__write_data(f'{mapping[wires]}:APER {apper}')
            else:
                return False
        except ValueError:
            if apper in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'{mapping[wires]}:APER {apper}')
            else:
                return False

    def get_temperature_rtd_aperture(self, wires=2) -> str:
        """Returns the RTD aperture setting.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.

        Returns:
            str: aperture in seconds
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return None
        return self.__get_data(f'{mapping[wires]}:APER?')

    def set_temperature_rtd_aperture_mode(self, wires=2, mode='AUTO') -> bool:
        """Sets the aperture mode for RTD/TRTD/FRTD.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.
            mode (str, optional): AUTO, FAST or MAN. Defaults to 'AUTO'.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return False
        if mode in ['AUTO', 'FAST', 'MAN']:
            return self.__write_data(f'{mapping[wires]}:APER:MODE {mode}')
        else:
            return False

    def get_temperature_rtd_aperture_mode(self, wires=2) -> str:
        """Returns the aperture mode for RTD/TRTD/FRTD.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.

        Returns:
            str: aperture mode
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return None
        return self.__get_data(f'{mapping[wires]}:APER:MODE?')

    def set_temperature_rtd_nplc(self, wires=2, nplc='DEF') -> bool:
        """Sets the ADC aperture in number of power line cycles for RTD.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.
            nplc (str, optional): Can be MIN, MAX, DEF or numeric. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return False
        try:
            nplc = float(nplc)
            if nplc >= 0:
                return self.__write_data(f'{mapping[wires]}:NPLC {nplc}')
            else:
                return False
        except ValueError:
            if nplc in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'{mapping[wires]}:NPLC {nplc}')
            else:
                return False

    def get_temperature_rtd_nplc(self, wires=2) -> str:
        """Returns the RTD aperture in PLCs.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.

        Returns:
            str: number of power line cycles
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return None
        return self.__get_data(f'{mapping[wires]}:NPLC?')

    def set_temperature_rtd_r0(self, wires=2, r0=100) -> bool:
        """Set the reference resistance value for RTD (25 or 100 Ohm).

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.
            r0 (int, optional): Reference resistance, 25 or 100 Ohm. Defaults to 100.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return False
        if r0 in [25, 100]:
            return self.__write_data(f'{mapping[wires]}:RES:RO {r0}')
        else:
            return False

    def get_temperature_rtd_r0(self, wires=2) -> str:
        """Returns the reference resistance value for RTD.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.

        Returns:
            str: reference resistance (25 or 100 Ohm)
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return None
        return self.__get_data(f'{mapping[wires]}:RES:RO?')

    def set_temperature_rtd_resolution(self, wires=2, res='DEF') -> bool:
        """Set RTD resolution.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.
            res (str, optional): Can be 'MIN', 'MAX', 'DEF' or 0.0001|0.001|0.01|0.1. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return False
        try:
            res = float(res)
            if res >= 0:
                return self.__write_data(f'{mapping[wires]}:RES {res}')
            else:
                return False
        except ValueError:
            if res in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'{mapping[wires]}:RES {res}')
            else:
                return False

    def get_temperature_rtd_resolution(self, wires=2) -> str:
        """Returns the RTD resolution.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.

        Returns:
            str: resolution
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return None
        return self.__get_data(f'{mapping[wires]}:RES?')

    def set_temperature_rtd_units(self, wires=2, units='C') -> bool:
        """Set temperature units for RTD measurement.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.
            units (str, optional): C or CEL = Celsius, F or FAR = Fahrenheit, K = Kelvin. Defaults to 'C'.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return False
        if units in ['C', 'CEL', 'F', 'FAR', 'K']:
            return self.__write_data(f'{mapping[wires]}:UNIT {units}')
        else:
            return False

    def get_temperature_rtd_units(self, wires=2) -> str:
        """Returns the RTD temperature units.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.

        Returns:
            str: temperature units
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return None
        return self.__get_data(f'{mapping[wires]}:UNIT?')

    def set_temperature_rtd_secondary_state(self, wires=2, state='OFF') -> bool:
        """Turns the secondary reading (voltage) ON or OFF for RTD.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return False
        if state in ['ON', 'OFF']:
            return self.__write_data(f'{mapping[wires]}:SEC {state}')
        else:
            return False

    def get_temperature_rtd_secondary_state(self, wires=2) -> str:
        """Returns the state of the secondary reading for RTD.

        Args:
            wires (int, optional): 2, 3 or 4 wire RTD. Defaults to 2.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        mapping = {2: 'TEMP:RTD', 3: 'TEMP:TRTD', 4: 'TEMP:FRTD'}
        if wires not in mapping:
            return None
        return self.__get_data(f'{mapping[wires]}:SEC?')

    # -------------------------------------------------------------------------
    # Temperature - Thermocouple (TC)
    # -------------------------------------------------------------------------

    def set_temperature_tc_function(self) -> bool:
        """Sets function to thermocouple temperature measurement.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "TEMP:TC"')

    def set_temperature_tc_type(self, tc_type='K') -> bool:
        """Sets the thermocouple type.

        Args:
            tc_type (str, optional): One of J, R, E, N, U, C, L, T, B, K, S. Defaults to 'K'.

        Returns:
            bool: status
        """
        if tc_type in ['J', 'R', 'E', 'N', 'U', 'C', 'L', 'T', 'B', 'K', 'S']:
            return self.__write_data(f'TEMP:TC:TYPE {tc_type}')
        else:
            return False

    def get_temperature_tc_type(self) -> str:
        """Returns the thermocouple type.

        Returns:
            str: TC type (J|R|E|N|U|C|L|T|B|K|S)
        """
        return self.__get_data('TEMP:TC:TYPE?')

    def set_temperature_tc_aperture(self, apper='DEF') -> bool:
        """Sets the ADC aperture for thermocouple measurement.

        Args:
            apper (str, optional): Aperture in seconds or MIN|MAX|DEF. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            apper = float(apper)
            if apper >= 0:
                return self.__write_data(f'TEMP:TC:APER {apper}')
            else:
                return False
        except ValueError:
            if apper in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'TEMP:TC:APER {apper}')
            else:
                return False

    def get_temperature_tc_aperture(self) -> str:
        """Returns the thermocouple aperture setting.

        Returns:
            str: aperture in seconds
        """
        return self.__get_data('TEMP:TC:APER?')

    def set_temperature_tc_aperture_mode(self, mode='AUTO') -> bool:
        """Sets the aperture mode for thermocouple.

        Args:
            mode (str, optional): AUTO, FAST or MAN. Defaults to 'AUTO'.

        Returns:
            bool: status
        """
        if mode in ['AUTO', 'FAST', 'MAN']:
            return self.__write_data(f'TEMP:TC:APER:MODE {mode}')
        else:
            return False

    def get_temperature_tc_aperture_mode(self) -> str:
        """Returns the aperture mode for thermocouple.

        Returns:
            str: aperture mode
        """
        return self.__get_data('TEMP:TC:APER:MODE?')

    def set_temperature_tc_nplc(self, nplc='DEF') -> bool:
        """Sets the ADC aperture in number of power line cycles for thermocouple.

        Args:
            nplc (str, optional): Can be MIN, MAX, DEF or numeric. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            nplc = float(nplc)
            if nplc >= 0:
                return self.__write_data(f'TEMP:TC:NPLC {nplc}')
            else:
                return False
        except ValueError:
            if nplc in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'TEMP:TC:NPLC {nplc}')
            else:
                return False

    def get_temperature_tc_nplc(self) -> str:
        """Returns the thermocouple aperture in PLCs.

        Returns:
            str: number of power line cycles
        """
        return self.__get_data('TEMP:TC:NPLC?')

    def set_temperature_tc_resolution(self, res='DEF') -> bool:
        """Set thermocouple resolution.

        Args:
            res (str, optional): Can be 'MIN', 'MAX', 'DEF' or 0.0001|0.001|0.01|0.1. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            res = float(res)
            if res >= 0:
                return self.__write_data(f'TEMP:TC:RES {res}')
            else:
                return False
        except ValueError:
            if res in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'TEMP:TC:RES {res}')
            else:
                return False

    def get_temperature_tc_resolution(self) -> str:
        """Returns the thermocouple resolution.

        Returns:
            str: resolution
        """
        return self.__get_data('TEMP:TC:RES?')

    def set_temperature_tc_units(self, units='C') -> bool:
        """Set temperature units for thermocouple measurement.

        Args:
            units (str, optional): C or CEL = Celsius, F or FAR = Fahrenheit, K = Kelvin. Defaults to 'C'.

        Returns:
            bool: status
        """
        if units in ['C', 'CEL', 'F', 'FAR', 'K']:
            return self.__write_data(f'TEMP:TC:UNIT {units}')
        else:
            return False

    def get_temperature_tc_units(self) -> str:
        """Returns the thermocouple temperature units.

        Returns:
            str: temperature units
        """
        return self.__get_data('TEMP:TC:UNIT?')

    def set_temperature_tc_secondary_state(self, state='ON') -> bool:
        """Turns the secondary reading (voltage) ON or OFF for thermocouple.

        Args:
            state (str, optional): ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'TEMP:TC:SEC {state}')
        else:
            return False

    def get_temperature_tc_secondary_state(self) -> str:
        """Returns the state of the secondary reading for thermocouple.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('TEMP:TC:SEC?')

    # -------------------------------------------------------------------------
    # Digitize (DIG)
    # -------------------------------------------------------------------------

    def set_digitize_voltage_function(self) -> bool:
        """Sets function to digitize voltage.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "DIG:VOLT"')

    def set_digitize_current_function(self) -> bool:
        """Sets function to digitize current.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "DIG:CURR"')

    def set_digitize_aperture(self, apper='DEF') -> bool:
        """Sets the ADC aperture value for Digitize in seconds or to MIN, MAX, Default.
        Default is 0, maximum is 0.003 seconds.

        Args:
            apper (str, optional): Aperture in seconds [0, 0.003] or MIN|MAX|DEF. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            apper = float(apper)
            if 0 <= apper <= 0.003:
                return self.__write_data(f'DIG:APER {apper}')
            else:
                return False
        except ValueError:
            if apper in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'DIG:APER {apper}')
            else:
                return False

    def get_digitize_aperture(self) -> str:
        """Returns the Digitize aperture setting.

        Returns:
            str: aperture in seconds
        """
        return self.__get_data('DIG:APER?')

    def set_digitize_voltage_range(self, range='DEF') -> bool:
        """Sets the maximum expected voltage value for Digitize.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or a numeric value. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range >= 0:
                return self.__write_data(f'DIG:VOLT:RANG {range}')
            else:
                return False
        except ValueError:
            if range in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'DIG:VOLT:RANG {range}')
            else:
                return False

    def get_digitize_voltage_range(self) -> str:
        """Returns the Digitize voltage range.

        Returns:
            str: voltage range
        """
        return self.__get_data('DIG:VOLT:RANG?')

    def set_digitize_current_range(self, range='DEF') -> bool:
        """Sets the maximum expected current value for Digitize.

        Args:
            range (str, optional): Can be 'MIN', 'MAX', 'DEF' or a numeric value. Defaults to 'DEF'.

        Returns:
            bool: status
        """
        try:
            range = float(range)
            if range >= 0:
                return self.__write_data(f'DIG:CURR:RANG {range}')
            else:
                return False
        except ValueError:
            if range in ['DEF', 'MIN', 'MAX']:
                return self.__write_data(f'DIG:CURR:RANG {range}')
            else:
                return False

    def get_digitize_current_range(self) -> str:
        """Returns the Digitize current range.

        Returns:
            str: current range
        """
        return self.__get_data('DIG:CURR:RANG?')

    def set_digitize_voltage_coupling(self, coupling='DC1M') -> bool:
        """Set the voltage path coupling and input impedance for Digitize.
        AC1M = AC Coupling 1MΩ, AC10M = AC Coupling 10MΩ,
        DC1M = DC Coupling 1MΩ, DC10M = DC Coupling 10MΩ,
        DCAuto = DC Coupling maximum available impedance.

        Args:
            coupling (str, optional): Can be AC1M, AC10M, DC1M, DC10M or DCAuto. Defaults to 'DC1M'.

        Returns:
            bool: status
        """
        if coupling in ['AC1M', 'AC10M', 'DC1M', 'DC10M', 'DCAuto']:
            return self.__write_data(f'DIG:VOLT:COUP:SIGN {coupling}')
        else:
            return False

    def get_digitize_voltage_coupling(self) -> str:
        """Returns the Digitize voltage coupling and input impedance setting.

        Returns:
            str: coupling/impedance setting
        """
        return self.__get_data('DIG:VOLT:COUP:SIGN?')

    def set_digitize_current_coupling(self, coupling='DC') -> bool:
        """Sets the Digitize current signal coupling path to AC or DC.

        Args:
            coupling (str, optional): AC or DC. Defaults to 'DC'.

        Returns:
            bool: status
        """
        if coupling in ['AC', 'DC']:
            return self.__write_data(f'DIG:CURR:COUP {coupling}')
        else:
            return False

    def get_digitize_current_coupling(self) -> str:
        """Returns the Digitize current coupling path.

        Returns:
            str: AC or DC
        """
        return self.__get_data('DIG:CURR:COUP?')

    def set_digitize_filter(self, filter_bw='3MHZ') -> bool:
        """Sets the Digitize low pass filter bandwidth.
        OFF = no filter, 100Khz = 100 kHz filter, 3MHZ = 3 MHz filter (default).

        Args:
            filter_bw (str, optional): Can be OFF, 100Khz or 3MHZ. Defaults to '3MHZ'.

        Returns:
            bool: status
        """
        if filter_bw in ['OFF', '100Khz', '3MHZ']:
            return self.__write_data(f'DIG:FILT {filter_bw}')
        else:
            return False

    def get_digitize_filter(self) -> str:
        """Returns the Digitize low pass filter setting.

        Returns:
            str: filter bandwidth
        """
        return self.__get_data('DIG:FILT?')

    # -------------------------------------------------------------------------
    # RF Power (POW)
    # -------------------------------------------------------------------------

    def set_power_function(self) -> bool:
        """Sets function to RF Power measurement.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC "POW"')

    def set_power_average(self, avg='AUTO') -> bool:
        """Set the number of readings to average for RF power.

        Args:
            avg (str, optional): Can be AUTO or a numeric value. Defaults to 'AUTO'.

        Returns:
            bool: status
        """
        if avg == 'AUTO':
            return self.__write_data('POW:AVER AUTO')
        else:
            try:
                avg = int(avg)
                if avg >= 1:
                    return self.__write_data(f'POW:AVER {avg}')
                else:
                    return False
            except:
                return False

    def get_power_average(self) -> str:
        """Returns the number of readings being averaged for RF power.

        Returns:
            str: average count
        """
        return self.__get_data('POW:AVER?')

    def set_power_frequency(self, freq=0.0) -> bool:
        """Sets the frequency at which to measure RF power.

        Args:
            freq (float, optional): Frequency in Hz. Defaults to 0.0.

        Returns:
            bool: status
        """
        try:
            freq = float(freq)
            if freq >= 0:
                return self.__write_data(f'POW:FREQ {freq}')
            else:
                return False
        except:
            return False

    def get_power_frequency(self) -> str:
        """Returns the set RF power frequency.

        Returns:
            str: frequency in Hz
        """
        return self.__get_data('POW:FREQ?')

    def get_power_sensor_identity(self) -> str:
        """Returns the identity of the RF sensor.

        Returns:
            str: sensor identity
        """
        return self.__get_data('POW:IDEN?')

    def set_power_relative_mode(self, relative=False) -> bool:
        """Selects Relative (True) or Absolute (False) RF power measurements.

        Args:
            relative (bool, optional): True = Relative, False = Absolute. Defaults to False.

        Returns:
            bool: status
        """
        if relative is True:
            return self.__write_data('POW:REL REL')
        elif relative is False:
            return self.__write_data('POW:REL ABS')
        else:
            return False

    def get_power_relative_mode(self) -> str:
        """Returns whether RF power measurement is relative or absolute.

        Returns:
            str: 1 = Relative, 0 = Absolute
        """
        return self.__get_data('POW:REL?')

    def set_power_relative_reference(self, ref='LREAD') -> bool:
        """Sets the reference value or the last reading as reference for relative power measurements.

        Args:
            ref (str, optional): Numeric value or 'LREAD' to use last reading. Defaults to 'LREAD'.

        Returns:
            bool: status
        """
        if ref == 'LREAD':
            return self.__write_data('POW:REL:REF LREAD')
        else:
            try:
                ref = float(ref)
                return self.__write_data(f'POW:REL:REF {ref}')
            except:
                return False

    def get_power_relative_reference(self) -> str:
        """Returns the RF power reference level.

        Returns:
            str: reference level
        """
        return self.__get_data('POW:REL:REF?')

    def set_power_units(self, units='DBM') -> bool:
        """Sets the RF power units.

        Args:
            units (str, optional): DBM, WATTs, VRMS, VPPK or DBUV. Defaults to 'DBM'.

        Returns:
            bool: status
        """
        if units in ['DBM', 'WATTs', 'VRMS', 'VPPK', 'DBUV']:
            return self.__write_data(f'POW:UNIT {units}')
        else:
            return False

    def get_power_units(self) -> str:
        """Returns the selected RF power units.

        Returns:
            str: power units
        """
        return self.__get_data('POW:UNIT?')

    # -------------------------------------------------------------------------
    # CALCulate: Average (rolling/block)
    # -------------------------------------------------------------------------

    def set_average_state(self, state='OFF') -> bool:
        """Turns CALCulate:AVERage ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:AVER:STAT {state}')
        else:
            return False

    def get_average_state(self) -> str:
        """Returns the state of CALCulate:AVERage.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:AVER:STAT?')

    def set_average_count(self, count=16) -> bool:
        """Sets the number of readings in the average. Default 16, Min 1, Max 10000.

        Args:
            count (int, optional): Number of readings to average [1, 10000]. Defaults to 16.

        Returns:
            bool: status
        """
        try:
            count = int(count)
            if 1 <= count <= 10000:
                return self.__write_data(f'CALC:AVER:COUN {count}')
            else:
                return False
        except:
            return False

    def get_average_count(self) -> str:
        """Returns the number of readings being averaged.

        Returns:
            str: average count
        """
        return self.__get_data('CALC:AVER:COUN?')

    def set_average_tcontrol(self, mode='MOV') -> bool:
        """Sets the averaging control mode.
        MOVing = rolling average; REPeat = block average.

        Args:
            mode (str, optional): MOV or REP. Defaults to 'MOV'.

        Returns:
            bool: status
        """
        if mode in ['MOV', 'REP', 'MOVing', 'REPeat']:
            return self.__write_data(f'CALC:AVER:TCON {mode}')
        else:
            return False

    def get_average_tcontrol(self) -> str:
        """Returns the averaging control setting (MOV or REP).

        Returns:
            str: MOV or REP
        """
        return self.__get_data('CALC:AVER:TCON?')

    # -------------------------------------------------------------------------
    # CALCulate: Limits
    # -------------------------------------------------------------------------

    def set_limit_state(self, state='OFF') -> bool:
        """Turns Limit checking ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:LIM:STAT {state}')
        else:
            return False

    def get_limit_state(self) -> str:
        """Returns the Limit state.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:LIM:STAT?')

    def set_limit_upper(self, value=1.999999999e15) -> bool:
        """Sets the upper limit value.

        Args:
            value (float, optional): Upper limit. Defaults to +1.999999999e15.

        Returns:
            bool: status
        """
        try:
            value = float(value)
            return self.__write_data(f'CALC:LIM:UPP {value}')
        except:
            return False

    def get_limit_upper(self) -> str:
        """Returns the upper limit value.

        Returns:
            str: upper limit
        """
        return self.__get_data('CALC:LIM:UPP?')

    def set_limit_upper_state(self, state='OFF') -> bool:
        """Turn the upper limit ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:LIM:UPP:STAT {state}')
        else:
            return False

    def get_limit_upper_state(self) -> str:
        """Returns the upper limit state.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:LIM:UPP:STAT?')

    def set_limit_lower(self, value=-1.99999999e15) -> bool:
        """Sets the lower limit value.

        Args:
            value (float, optional): Lower limit. Defaults to -1.99999999e15.

        Returns:
            bool: status
        """
        try:
            value = float(value)
            return self.__write_data(f'CALC:LIM:LOW {value}')
        except:
            return False

    def get_limit_lower(self) -> str:
        """Returns the lower limit value.

        Returns:
            str: lower limit
        """
        return self.__get_data('CALC:LIM:LOW?')

    def set_limit_lower_state(self, state='OFF') -> bool:
        """Turn the lower limit ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:LIM:LOW:STAT {state}')
        else:
            return False

    def get_limit_lower_state(self) -> str:
        """Returns the lower limit state.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:LIM:LOW:STAT?')

    def get_limit_fail(self) -> str:
        """Returns whether the last reading was outside limits.

        Returns:
            str: 1 = outside limits, 0 = within limits
        """
        return self.__get_data('CALC:LIM:FAIL?')

    def clear_limit_flags(self) -> bool:
        """Immediately clears all limit flags.

        Returns:
            bool: status
        """
        return self.__write_data('CALC:LIM:CLE:IMM')

    # -------------------------------------------------------------------------
    # CALCulate: Math (mx - c) / z
    # -------------------------------------------------------------------------

    def set_math_state(self, state='OFF') -> bool:
        """Turns Math (mx - c)/z calculation ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:MATH:STAT {state}')
        else:
            return False

    def get_math_state(self) -> str:
        """Returns the Math state.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:MATH:STAT?')

    def set_math_mfactor(self, value='LREAD') -> bool:
        """Sets the m variable for Math calculation. Default 1.

        Args:
            value (str, optional): Numeric value or 'LREAD' to use last reading. Defaults to 'LREAD'.

        Returns:
            bool: status
        """
        if value == 'LREAD':
            return self.__write_data('CALC:MATH:MFAC LREAD')
        else:
            try:
                value = float(value)
                return self.__write_data(f'CALC:MATH:MFAC {value}')
            except:
                return False

    def get_math_mfactor(self) -> str:
        """Returns the m variable value.

        Returns:
            str: m value
        """
        return self.__get_data('CALC:MATH:MFAC?')

    def set_math_mfactor_state(self, state='OFF') -> bool:
        """Turns the multiply by m operation ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:MATH:MFAC:STAT {state}')
        else:
            return False

    def get_math_mfactor_state(self) -> str:
        """Returns the state of m multiplication.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:MATH:MFAC:STAT?')

    def set_math_cfactor(self, value='LREAD') -> bool:
        """Sets the c variable for Math calculation. Default 1.

        Args:
            value (str, optional): Numeric value or 'LREAD' to use last reading. Defaults to 'LREAD'.

        Returns:
            bool: status
        """
        if value == 'LREAD':
            return self.__write_data('CALC:MATH:CFAC LREAD')
        else:
            try:
                value = float(value)
                return self.__write_data(f'CALC:MATH:CFAC {value}')
            except:
                return False

    def get_math_cfactor(self) -> str:
        """Returns the c variable value.

        Returns:
            str: c value
        """
        return self.__get_data('CALC:MATH:CFAC?')

    def set_math_cfactor_state(self, state='OFF') -> bool:
        """Turns the subtract c operation ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:MATH:CFAC:STAT {state}')
        else:
            return False

    def get_math_cfactor_state(self) -> str:
        """Returns the state of c subtraction.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:MATH:CFAC:STAT?')

    def set_math_zfactor(self, value='LREAD') -> bool:
        """Sets the z variable for Math calculation. Default 1.

        Args:
            value (str, optional): Numeric value or 'LREAD' to use last reading. Defaults to 'LREAD'.

        Returns:
            bool: status
        """
        if value == 'LREAD':
            return self.__write_data('CALC:MATH:ZFAC LREAD')
        else:
            try:
                value = float(value)
                return self.__write_data(f'CALC:MATH:ZFAC {value}')
            except:
                return False

    def get_math_zfactor(self) -> str:
        """Returns the z variable value.

        Returns:
            str: z value
        """
        return self.__get_data('CALC:MATH:ZFAC?')

    def set_math_zfactor_state(self, state='OFF') -> bool:
        """Turns the divide by z operation ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:MATH:ZFAC:STAT {state}')
        else:
            return False

    def get_math_zfactor_state(self) -> str:
        """Returns the state of z division.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:MATH:ZFAC:STAT?')

    def set_math_munits(self, units='PERCent') -> bool:
        """Sets the units for Math calculations.
        PERCent = (mx-c) in percent of z
        DB50 = Relative to 1 mW in 50Ω
        DB75 = Relative to 1 mW in 75Ω
        DB600 = Relative to 1 mW in 600Ω
        DB = Relative to 1

        Args:
            units (str, optional): PERCent, DB50, DB75, DB600 or DB. Defaults to 'PERCent'.

        Returns:
            bool: status
        """
        if units in ['PERCent', 'DB50', 'DB75', 'DB600', 'DB']:
            return self.__write_data(f'CALC:MATH:MUNIT {units}')
        else:
            return False

    def get_math_munits(self) -> str:
        """Returns the Math units setting.

        Returns:
            str: units
        """
        return self.__get_data('CALC:MATH:MUNIT?')

    def set_math_munits_state(self, state='OFF') -> bool:
        """Turns MUNits ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'OFF'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'CALC:MATH:MUNIT:STAT {state}')
        else:
            return False

    def get_math_munits_state(self) -> str:
        """Returns the MUNits setting.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('CALC:MATH:MUNIT:STAT?')

    def reset_math(self) -> bool:
        """Reset Math factors to defaults.

        Returns:
            bool: status
        """
        return self.__write_data('CALC:MATH:RES')

    # -------------------------------------------------------------------------
    # CONFigure / MEASure commands
    # -------------------------------------------------------------------------

    def configure(self, meter_fn, param1=None, param2=None) -> bool:
        """Configure the DMM for a specific measurement function.
        Also resets the trigger system to single-shot mode (see manual Note 1).

        Args:
            meter_fn (str): Measurement function, e.g. 'VOLT:DC', 'CURR:AC', 'RES', 'FRES',
                            'FREQ', 'PER', 'CAP', 'TEMP:TC', 'TEMP:RTD', etc.
            param1 (str, optional): Range or first parameter. Defaults to None.
            param2 (str, optional): Resolution or second parameter. Defaults to None.

        Returns:
            bool: status
        """
        cmd = f'CONF:{meter_fn}'
        if param1 is not None:
            cmd += f' {param1}'
            if param2 is not None:
                cmd += f',{param2}'
        return self.__write_data(cmd)

    def get_configure(self) -> str:
        """Returns the setup configured by the last CONFigure or MEASure command.

        Returns:
            str: configuration string e.g. '"VOLT +1.0E+0,+1.0E-4"'
        """
        return self.__get_data('CONF?')

    def measure(self, meter_fn, param1=None, param2=None) -> list:
        """Configure and immediately trigger + fetch a measurement.
        Equivalent to ABORt; CONFigure:<meter_fn>; READ?

        Args:
            meter_fn (str): Measurement function, e.g. 'VOLT:DC', 'CURR:DC', 'RES', etc.
            param1 (str, optional): Range. Defaults to None.
            param2 (str, optional): Resolution. Defaults to None.

        Returns:
            list: measurement result(s)
        """
        cmd = f'MEAS:{meter_fn}?'
        if param1 is not None:
            cmd += f' {param1}'
            if param2 is not None:
                cmd += f',{param2}'
        try:
            result = self.__get_data(cmd)
            if result is not None:
                return [float(x) for x in result.strip().split(',')]
            return None
        except Exception as e:
            print(e)
            return None

    def fetch_now(self, num_readings=None) -> list:
        """Recalls readings from memory, removing them from the buffer.
        If num_readings is not provided or fewer readings exist, all available are returned.

        Args:
            num_readings (int, optional): Number of readings to retrieve. Defaults to None (all).

        Returns:
            list: list of readings
        """
        cmd = 'FNOW?'
        if num_readings is not None:
            cmd += f' {int(num_readings)}'
        try:
            result = self.__get_data(cmd)
            if result is not None:
                return [float(x) for x in result.strip().split(',')]
            return None
        except Exception as e:
            print(e)
            return None

    # -------------------------------------------------------------------------
    # ROUTE: Trigger output and output slope
    # -------------------------------------------------------------------------

    def set_trigger_output(self, mode='ACO') -> bool:
        """Configures the rear panel TRIG OUT waveform.
        OFF = Pulses disabled
        ACO = Pulse at end of acquisition, start of run down (default)
        APE = Squarewave active during acquisition
        BCO = Multiple reading burst complete
        EVE = Limit exceeded
        RCO = ADC conversion complete

        Args:
            mode (str, optional): OFF, ACO, APE, BCO, EVE or RCO. Defaults to 'ACO'.

        Returns:
            bool: status
        """
        if mode in ['OFF', 'ACO', 'APE', 'BCO', 'EVE', 'RCO']:
            return self.__write_data(f'ROUT:TOUT {mode}')
        else:
            return False

    def get_trigger_output(self) -> str:
        """Returns the rear panel TRIG OUT setting.

        Returns:
            str: TRIG OUT mode
        """
        return self.__get_data('ROUT:TOUT?')

    def trigger_output_once(self) -> bool:
        """Causes a single pulse from the rear panel TRIG OUT connector.

        Returns:
            bool: status
        """
        return self.__write_data('ROUT:TOUT:ONC')

    def set_trigger_output_slope(self, slope='NEG') -> bool:
        """Sets the polarity of the rear panel TRIG OUT waveform.

        Args:
            slope (str, optional): POSitive or NEGative. Defaults to 'NEG'.

        Returns:
            bool: status
        """
        if slope in ['POS', 'NEG', 'POSitive', 'NEGative']:
            return self.__write_data(f'ROUT:TOUT:SLOP {slope}')
        else:
            return False

    def get_trigger_output_slope(self) -> str:
        """Returns the polarity of the rear panel TRIG OUT waveform.

        Returns:
            str: POSitive or NEGative
        """
        return self.__get_data('ROUT:TOUT:SLOP?')

    # -------------------------------------------------------------------------
    # IEEE 488.2 / SCPI Status
    # -------------------------------------------------------------------------

    def set_event_status_enable(self, enable_value=0) -> bool:
        """Enable bits in the standard event status register (*ESE).

        Args:
            enable_value (int, optional): Sum of bit values to enable. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            enable_value = int(enable_value)
            return self.__write_data(f'*ESE {enable_value}')
        except:
            return False

    def get_event_status_enable(self) -> str:
        """Retrieve standard event enable register (*ESE?).

        Returns:
            str: enable register value
        """
        return self.__get_data('*ESE?')

    def get_event_status_register(self) -> str:
        """Retrieve and clear the standard event status register (*ESR?).

        Returns:
            str: event status register value
        """
        return self.__get_data('*ESR?')

    def set_service_request_enable(self, enable_value=191) -> bool:
        """Enable bits in the status byte register (*SRE).

        Args:
            enable_value (int, optional): Sum of bit values to enable. Defaults to 191.

        Returns:
            bool: status
        """
        try:
            enable_value = int(enable_value)
            return self.__write_data(f'*SRE {enable_value}')
        except:
            return False

    def get_service_request_enable(self) -> str:
        """Retrieve bits in the status byte register (*SRE?).

        Returns:
            str: service request enable register
        """
        return self.__get_data('*SRE?')

    def get_status_byte(self) -> str:
        """Retrieve the status byte summary register (*STB?).

        Returns:
            str: status byte
        """
        return self.__get_data('*STB?')

    def set_operation_complete(self) -> bool:
        """Set 'Operation Complete' bit in Standard event register (*OPC).

        Returns:
            bool: status
        """
        return self.__write_data('*OPC')

    def get_operation_complete(self) -> str:
        """Returns '1' in output buffer after all pending operations complete (*OPC?).

        Returns:
            str: '1' when complete
        """
        return self.__get_data('*OPC?')

    def get_options(self) -> str:
        """Retrieve the instrument options (*OPT?).

        Returns:
            str: option string
        """
        return self.__get_data('*OPT?')

    def set_power_on_status_clear(self, enable=1) -> bool:
        """Power-on status clear OFF or ON (*PSC).

        Args:
            enable (int, optional): 0 = OFF, 1 = ON. Defaults to 1.

        Returns:
            bool: status
        """
        if enable in [0, 1]:
            return self.__write_data(f'*PSC {enable}')
        else:
            return False

    def get_power_on_status_clear(self) -> str:
        """Retrieve power-on status clear setting (*PSC?).

        Returns:
            str: 0 or 1
        """
        return self.__get_data('*PSC?')

    def trigger_bus(self) -> bool:
        """Trigger a reading via the bus (*TRG).

        Returns:
            bool: status
        """
        return self.__write_data('*TRG')

    def self_test(self) -> str:
        """Perform self-test (*TST?). Returns '0' if the test succeeds, '1' if the test fails.

        Returns:
            str: '0' = pass, '1' = fail
        """
        return self.__get_data('*TST?')

    def wait_for_complete(self) -> bool:
        """Wait for all pending operations to complete (*WAI).

        Returns:
            bool: status
        """
        return self.__write_data('*WAI')

    def get_operation_condition(self) -> str:
        """Returns the contents of the OPERation Condition register.
        Bit 4 (MEASuring) is false when the trigger system is in IDLE, true otherwise.

        Returns:
            str: operation condition register value
        """
        return self.__get_data('STAT:OPER:COND?')

    def get_operation_event(self) -> str:
        """Returns the OPERation Event register (set true if event has occurred).

        Returns:
            str: operation event register value
        """
        return self.__get_data('STAT:OPER:EVEN?')

    def set_operation_enable(self, nrf=0) -> bool:
        """Sets which OPERational register bits cause the OPER bit in the Status byte to be set.

        Args:
            nrf (int, optional): Sum of bit values to enable. Min=0, Max=32768. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            nrf = int(nrf)
            if 0 <= nrf <= 32768:
                return self.__write_data(f'STAT:OPER:ENAB {nrf}')
            else:
                return False
        except:
            return False

    def get_operation_enable(self) -> str:
        """Returns the sum of the bit values of the enabled OPERational register bits.

        Returns:
            str: enable register value
        """
        return self.__get_data('STAT:OPER:ENAB?')

    def get_questionable_event(self) -> str:
        """Returns the QUEStionable Event register.

        Returns:
            str: questionable event register value
        """
        return self.__get_data('STAT:QUES:EVEN?')

    def set_questionable_enable(self, nrf=0) -> bool:
        """Sets which QUEStionable register bits cause the QUES bit in the Status byte to be set.

        Args:
            nrf (int, optional): Sum of bit values to enable. Min=0, Max=32768. Defaults to 0.

        Returns:
            bool: status
        """
        try:
            nrf = int(nrf)
            if 0 <= nrf <= 32768:
                return self.__write_data(f'STAT:QUES:ENAB {nrf}')
            else:
                return False
        except:
            return False

    def get_questionable_enable(self) -> str:
        """Returns the sum of the bit values of the enabled QUEStionable register bits.

        Returns:
            str: enable register value
        """
        return self.__get_data('STAT:QUES:ENAB?')

    def preset_status_registers(self) -> bool:
        """Sets Enable bits for both OPERational and QUEStionable registers to False.

        Returns:
            bool: status
        """
        return self.__write_data('STAT:PRES')

    # -------------------------------------------------------------------------
    # Zero / ZClear
    # -------------------------------------------------------------------------

    def zero_range(self, scope='RANG') -> str:
        """Removes residual offsets. Applies to active range or all functions.
        Returns '0' for success, '1' for failure.

        Args:
            scope (str, optional): RANG for active range, ALL for all functions. Defaults to 'RANG'.

        Returns:
            str: '0' = success, '1' = failure
        """
        if scope in ['RANG', 'ALL']:
            return self.__get_data(f'ZERO? {scope}')
        else:
            return None

    def zclear_range(self, scope='RANG') -> str:
        """Clears zero offsets. Applies to active range or all functions.
        Returns '0' for success, '1' for failure.

        Args:
            scope (str, optional): RANG for active range, ALL for all functions. Defaults to 'RANG'.

        Returns:
            str: '0' = success, '1' = failure
        """
        if scope in ['RANG', 'ALL']:
            return self.__get_data(f'ZCLE? {scope}')
        else:
            return None

    # -------------------------------------------------------------------------
    # SCPI version / system info
    # -------------------------------------------------------------------------

    def get_scpi_version(self) -> str:
        """Returns the SCPI version in the form YYY.V.

        Returns:
            str: SCPI version
        """
        return self.__get_data('SYST:VERS?')

    def set_gpib_address(self, address) -> bool:
        """Set the GPIB bus address.

        Args:
            address (int): GPIB address in range [1, 30].

        Returns:
            bool: status
        """
        try:
            address = int(address)
            if 1 <= address <= 30:
                return self.__write_data(f'SYST:COMM:GPIB:ADDR {address}')
            else:
                return False
        except:
            return False

    def get_gpib_address(self) -> str:
        """Returns the GPIB bus address.

        Returns:
            str: GPIB address
        """
        return self.__get_data('SYST:COMM:GPIB:ADDR?')

    def set_lan_ip_address(self, ip_address) -> bool:
        """Sets the Ethernet IP address.

        Args:
            ip_address (str): IP address in form xxx.xxx.xxx.xxx.

        Returns:
            bool: status
        """
        return self.__write_data(f'SYST:COMM:LAN:IPAD {ip_address}')

    def get_lan_ip_address(self) -> str:
        """Returns the Ethernet IP address.

        Returns:
            str: IP address
        """
        return self.__get_data('SYST:COMM:LAN:IPAD?')

    def set_lan_gateway(self, gateway) -> bool:
        """Sets the Ethernet gateway address.

        Args:
            gateway (str): Gateway address in form xxx.xxx.xxx.xxx.

        Returns:
            bool: status
        """
        return self.__write_data(f'SYST:COMM:LAN:GAT {gateway}')

    def get_lan_gateway(self) -> str:
        """Returns the Ethernet gateway address.

        Returns:
            str: gateway address
        """
        return self.__get_data('SYST:COMM:LAN:GAT?')

    def set_lan_subnet_mask(self, mask) -> bool:
        """Sets the Ethernet subnet mask.

        Args:
            mask (str): Subnet mask in form xxx.xxx.xxx.xxx.

        Returns:
            bool: status
        """
        return self.__write_data(f'SYST:COMM:LAN:SMAS {mask}')

    def get_lan_subnet_mask(self) -> str:
        """Returns the Ethernet subnet mask.

        Returns:
            str: subnet mask
        """
        return self.__get_data('SYST:COMM:LAN:SMAS?')

    def set_lan_dhcp(self, state='ON') -> bool:
        """Turn DHCP ON or OFF.

        Args:
            state (str, optional): ON or OFF. Defaults to 'ON'.

        Returns:
            bool: status
        """
        if state in ['ON', 'OFF']:
            return self.__write_data(f'SYST:COMM:LAN:DHCP {state}')
        else:
            return False

    def get_lan_dhcp(self) -> str:
        """Returns the DHCP state.

        Returns:
            str: 1 = ON, 0 = OFF
        """
        return self.__get_data('SYST:COMM:LAN:DHCP?')

    def get_lan_mac_address(self) -> str:
        """Returns the MAC address.

        Returns:
            str: MAC address
        """
        return self.__get_data('SYST:COMM:LAN:MAC?')

    def set_lan_port(self, port=3490) -> bool:
        """Sets the Ethernet control port.

        Args:
            port (int, optional): Port number [1024, 65535]. Defaults to 3490.

        Returns:
            bool: status
        """
        try:
            port = int(port)
            if 1024 <= port <= 65535:
                return self.__write_data(f'SYST:COMM:LAN:CONT {port}')
            else:
                return False
        except:
            return False

    def get_lan_port(self) -> str:
        """Returns the Ethernet control port.

        Returns:
            str: port number
        """
        return self.__get_data('SYST:COMM:LAN:CONT?')

    @staticmethod
    def list_instruments() -> str:
        rm = pyvisa.ResourceManager()
        return rm.list_resources()

    # =========================================================================
    # CALibration subsystem
    # Ref: Fluke 8588A/8558A Service Manual, Table 6 – Command Summary
    # =========================================================================

    def cal_get_secure_mode(self) -> str:
        """Returns the current calibration adjustment mode.

        Returns:
            str: 'FACTory', 'USER', or 'NONe'
        """
        return self.__get_data('CAL:SEC?')

    def cal_enter(self, passcode: str = '123456') -> bool:
        """Enables calibration adjustment mode (unlocks the CAL subsystem).

        Args:
            passcode (str): Calibration passcode. Factory default is '123456'.

        Returns:
            bool: True if command was sent successfully.
        """
        return self.__write_data(f'CAL:SEC:PASS {passcode}')

    def cal_exit(self) -> bool:
        """Exits calibration adjustment mode and locks the CAL subsystem.

        Returns:
            bool: True if command was sent successfully.
        """
        return self.__write_data('CAL:SEC:EXIT')

    def cal_get_store_date(self, store: str = 'CERTified') -> str:
        """Returns the date of the last calibration adjustment for the given store.

        Args:
            store (str): 'CERTified' or 'BASeline'. Defaults to 'CERTified'.

        Returns:
            str: Date in format <year>,<month>,<day>,<Hours>,<Minutes>,<seconds>
        """
        if store not in ('CERTified', 'BASeline'):
            return None
        return self.__get_data(f'CAL:STOR:DAT? {store}')

    def cal_set_active_store(self, store: str = 'CERTified') -> bool:
        """Sets the active calibration store.

        Args:
            store (str): 'CERTified' (default) or 'BASeline'.

        Returns:
            bool: status
        """
        if store not in ('CERTified', 'BASeline'):
            return False
        return self.__write_data(f'CAL:STOR:USE {store}')

    def cal_get_active_store(self) -> str:
        """Returns the active calibration store.

        Returns:
            str: 'CERTified' or 'BASeline'
        """
        return self.__get_data('CAL:STOR:USE?')

    def cal_copy_to_baseline(self) -> bool:
        """Copies the Certified calibration stores over the Baseline stores.

        Returns:
            bool: status
        """
        return self.__write_data('CAL:COPY:BAS')

    def cal_get_target_description(self) -> str:
        """Returns the target name as a quoted string with the current calibration
        point description (e.g. step name and required input).

        Returns:
            str: Target description string.
        """
        return self.__get_data('CAL:TARG:DESC?')

    def cal_get_target_input(self) -> str:
        """Returns the target input field description as a quoted string.
        Describes what signal must be applied to the instrument terminals.

        Returns:
            str: Input field description.
        """
        return self.__get_data('CAL:TARG:INP?')

    def cal_set_target_step(self, step: int) -> bool:
        """Navigates to a specific calibration adjustment step number.

        Args:
            step (int): Step number as listed in Table 2 of the Service Manual
                        (e.g. 201, 202, ... 704).

        Returns:
            bool: status
        """
        try:
            step = int(step)
            return self.__write_data(f'CAL:TARG:STEP {step}')
        except (ValueError, TypeError):
            return False

    def cal_set_target_value(self, value: float) -> bool:
        """Sets the target (reference) value for the current calibration step.
        Use this when the reference standard has a non-nominal value
        (e.g. exact resistance of a standard resistor).

        Args:
            value (float): Exact reference value in the step's native units.

        Returns:
            bool: status
        """
        try:
            value = float(value)
            return self.__write_data(f'CAL:TARG:VAL {value}')
        except (ValueError, TypeError):
            return False

    def cal_get_target_value(self) -> str:
        """Returns the current target (reference) value for the active calibration step.

        Returns:
            str: Target value as a numeric string.
        """
        return self.__get_data('CAL:TARG:VAL?')

    def cal_trigger(self) -> str:
        """Initiates the calibration adjustment for the current step.
        Equivalent to pressing F2 (Adjust) on the front panel.

        Returns:
            str: '0' = success, '1' = failure
        """
        return self.__get_data('CAL:TRIG?')

    def cal_adjust_step(self, step: int, target_value: float = None,
                        timeout: float = 60.0) -> bool:
        """High-level helper: navigate to a step, optionally set the target value,
        trigger the adjustment, and wait for completion.

        Args:
            step (int): Calibration step number (e.g. 203).
            target_value (float, optional): Non-nominal reference value to set before
                adjusting. Pass None to keep the nominal (default) target. Defaults to None.
            timeout (float): Maximum seconds to wait for the instrument to respond.
                Defaults to 60.0.

        Returns:
            bool: True if adjustment succeeded (instrument returned '0'), False otherwise.
        """
        if not self.cal_set_target_step(step):
            return False
        time.sleep(0.5)

        if target_value is not None:
            if not self.cal_set_target_value(target_value):
                return False
            time.sleep(0.2)

        # Allow extra time for long-duration adjustments (e.g. ADC characterisation)
        old_timeout = self.__inst.timeout
        self.__inst.timeout = int(timeout * 1000)
        result = self.cal_trigger()
        self.__inst.timeout = old_timeout

        if result is None:
            return False
        return result.strip() == '0'