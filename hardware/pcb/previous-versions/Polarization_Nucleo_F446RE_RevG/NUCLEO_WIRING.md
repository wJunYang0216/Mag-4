# NUCLEO-F446RE interface — PCB revision G

This board connects by a **12-wire cable** to the NUCLEO-F446RE. It is not a mechanically stackable Arduino shield. J3 is a 1x12, 2.54 mm header; its square pad is pin 1. Do not confuse driver-board J3 pin numbers with Nucleo connector numbers.

The following is the assigned firmware/harness mapping. Coordinate these pin assignments with the MCU teammate before using other peripherals on the same pins.

| Driver J3 pin | Signal | Nucleo MCU pin | Nucleo connector and pin | Firmware use |
|---|---|---|---|---|
| 1 | POL_3V3 | PA8 / D7 | CN10-23 | GPIO output; HIGH requests polarization |
| 2 | TG_3V3 | PA9 / D8 | CN10-21 | GPIO output; HIGH grounds coil TOP via Q5 |
| 3 | RX | PB10 / D6 | CN10-25 | GPIO output; HIGH connects receiver path |
| 4 | SH | PB4 / D5 | CN10-27 | GPIO output; HIGH grounds PRE |
| 5 | DP | PB5 / D4 | CN10-29 | GPIO output; HIGH enables 10k damping path |
| 6 | RESET | PA10 / D2 | CN10-33 | GPIO output; HIGH grounds RX_IN; **not MCU NRST** |
| 7 | I_ADC | PA0 / A0 | CN7-28, also CN8-1 | Analog input, ADC1_IN0; no digital pull-up/down |
| 8 | FF | PC7 / D9 | CN10-19 | GPIO input; ADG5412F open-drain fault flag, active LOW; board has 10k pull-up to 3.3V |
| 9 | GND | GND | CN7-20 | Common ground |
| 10 | +3V3 | 3.3V output | CN7-16 | Nucleo supplies U4 reference and fault pull-up |
| 11 | +5V | 5V output | CN7-18 | Nucleo supplies U4 INA241 and U5 logic buffer |
| 12 | GND | GND | CN10-20 | Additional ground return |

CN7/CN10 mapping is from ST UM1724 Rev 17, Table 29; Arduino aliases are from Table 19. PA13/PA14 (SWD), PA2/PA3 (ST-LINK UART), and PA5 (user LED) are not assigned here. Use SWD debug rather than JTAG if using PB4 for SH.

## Power wiring

Power the Nucleo through its normal documented USB/ST-LINK supply arrangement. Take its switched board +5V output from **CN7-18**, not VIN or E5V. Connect the cable grounds before applying external driver power.

J1 is now:

| J1 pin | Connection |
|---|---|
| 1 | External regulated +12V input |
| 2 | External regulated -12V input |
| 3 | **3.3V monitor/output from the Nucleo rail; leave unconnected to external supplies** |
| 4 | Common ground |

Do not connect an independent 3.3V supply to J1-3 while using Nucleo 3.3V on J3-10. Do not put 12V, -12V, or coil-node voltages on a Nucleo pin. The Nucleo does not supply the coil current. Review the Nucleo manual's power-source/jumper instructions for the actual board revision before changing its power source.

## Why U5 was added

The LTC1693 driver input high threshold can reach 3.1V. STM32 output-high specifications do not provide a comfortable guaranteed margin for a direct 3.3V connection. **SN74AHCT125PWR**, powered at 5V, accepts a 2.0V minimum high input and drives the two gate-control nets POL and TG at 5V. Its outputs only connect to the gate drivers, never back to MCU pins. AHCT is intentional: do not substitute a 5V HC/AHC part with a higher input threshold.

U5 channels 1/2 are enabled continuously. Unused channels have defined input/enable levels and unconnected outputs. C9 is local bypass. R11-R16 are 100k GPIO pulldowns, and R17/R18 are 10k pulldowns on the buffered driver inputs. These establish intended low defaults; they do not implement a hardware interlock or prove glitch-free power sequencing under every condition.

ADG5412F controls RX/SH/DP/RESET remain 3.3V GPIO signals. Its digital input thresholds support those levels with the specified supplies.

## Current measurement and status

Use J3-7 / PA0 for the amplified current input. Nominally 0.99 V at zero current and 1.5 V/A. See README.md and MCU_STATUS.md for Rev G scaling, qualification logic, and limitations. J5 is a floating high-common-mode differential shunt connection; never connect it directly to Nucleo pins.
