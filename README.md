# Fluke 8588A Python Library (Unofficial)

[![PyPI version](https://badge.fury.io/py/fluke8588a.svg)](https://pypi.org/project/fluke8588a/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, Pythonic interface for controlling the **Fluke 8588A Reference Multimeter** using `pyvisa`.

## 🚀 Overview
The Fluke 8588A is one of the world's most stable reference multimeters. While it uses standard SCPI commands, managing high-speed digitizing, complex triggers, and metrology-grade configurations can be challenging. This library abstracts the low-level SCPI communication into an intuitive API, allowing metrologists and engineers to focus on data, not manuals.

## ⚠️ Safety Warning
The Fluke 8588A is a high-precision instrument capable of measuring high voltages (up to 1000V). This software is **unofficial** and interacts directly with the hardware.
* **Use at your own risk.** Incorrect automation loops can lead to unexpected instrument behavior.
* Always verify that your test setup and input signals do not exceed the instrument's maximum ratings before running automation scripts.

## 📦 Installation
```bash
pip install fluke8588a
```

## Quick start

```python
from fluke8588a import Fluke8588A

fluke8588a = Fluke8588A('GPIB0::23::INSTR', timeout=10_000)

fluke8588a.reset()
fluke8588a.set_voltage_dc_function()
fluke8588a.set_voltage_dc_range(10)
fluke8588a.set_voltage_dc_resolution('MIN')
fluke8588a.set_voltage_dc_autorange('OFF')
fluke8588a.set_voltage_dc_nplc(100)
fluke8588a.set_voltage_dc_aperture_mode('MAN')
fluke8588a.set_trigger_init_continuous('OFF')
fluke8588a.set_trigger_delay_auto('OFF')
fluke8588a.set_trigger_delay(0)
fluke8588a.set_trigger_source('IMM')
fluke8588a.set_trigger_count(1)
fluke8588a.set_arm1_source('IMM')
fluke8588a.set_arm1_count(1)
fluke8588a.set_arm2_source('IMM')
fluke8588a.set_arm2_count(1)

fluke8588a.set_trigger_init_immediate()

fluke8588a_data = fluke8588a.fetch_data()
```

### Requirements

1. Python 3.8+
2. pyvisa-py
3. A valid VISA backend (pyvisa-py, NI-VISA, or Keysight IO Libraries)

## 📜 Licensing & Attribution
This project is licensed under the **MIT License**.  
**Important:** If you use this library, you must keep the original copyright notice. If you modify it, please attribute the original work to [Đorđe Novaković](https://github.com/Hepek93). 