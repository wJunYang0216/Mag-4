# NUCLEO-F446RE interface — PCB revision E

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
| 10 | +3V3 | 3.3V output | CN7-16 | Nucleo supplies INA240 and fault pull-up |
| 11 | +5V | 5V output | CN7-18 | Nucleo supplies U5 logic buffer |
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

## Current measurement

R9 remains **50 milliohms (0.05 ohm)**. J5 is a raw shunt voltage header:

- J5-1: CURRENT_SENSE+, R9's Q1/source side.
- J5-2: CURRENT_SENSE-, R9's ground side.
- Nominal difference: **50 mV per ampere**, with no gain or added input protection on J5.

The STM32F446RE has single-ended ADC inputs. J5 is not a plug-in differential ADC pair, and CURRENT_SENSE- is not a negative-supply pin. Use the existing INA240A1 output through J3-7 to PA0 for normal firmware measurement. Keep J5 for external differential instrumentation or a deliberately designed analog front end; do not connect it to ordinary digital inputs.

Nominal relationships, with 3.3V INA240 supply and R9=50mΩ:

`V_I_ADC = 1.65 V + I_polarization × 1 V/A`

`I_polarization = (V_I_ADC - measured_zero_current_voltage) / (20 × 0.05 Ω)`

Use the actual ADC reference/supply and calibrate zero offset. At about 1A the nominal output is about 2.65V. The 12-bit ADC input must remain inside its analog supply/reference range; do not assume a 5V-tolerant digital pin is 5V-tolerant in analog mode. The 100Ω/10nF filter remains fitted; choose ADC sampling time and rate using ST's ADC settling guidance and test with the cable attached.

The user-linked Susumu MSREM2512S-0L50-F4P0 is **0.5mΩ**, not 50mΩ. It illustrates the right component class but has not been substituted: it would reduce the raw signal by 100x and require gain/calibration changes. Its recommended land pattern also needs checking before substituting it into a generic 2512 footprint.

**This shunt still measures polarization current only.** Clamp/discharge current bypasses R9. A zero reading cannot authorize receive mode by itself. Use a validated decay/settling delay or revise the hardware to measure the discharge path.

## Firmware behavior required

1. Initialize POL, TG, RX, SH, DP and RESET LOW before enabling the measurement sequence. Configure PA0 as analog and PC7 as an input.
2. During polarization, TG must be LOW before POL goes HIGH. Isolate the receiver with RX LOW and apply the planned blanking/clamp controls.
3. End polarization by taking POL LOW. Enforce break-before-make dead time before TG can go HIGH. Validate dead time against actual MOSFET/driver switching and coil discharge.
4. Allow clamp discharge, damping and amplifier recovery before opening the signal path. SH/RESET must be released for reception. The earlier short LTspice pulse is an electrical test, not proof of adequate nuclear polarization time.
5. POL and TG must never be HIGH together. The added buffer does not prevent this. FF monitors ADG5412F faults; it is not an overcurrent trip. No firmware implementation or hardware bench verification is included in this revision.

## References checked

- ST UM1724 Rev 17, Tables 19/29: https://www.st.com/resource/en/user_manual/dm00105823-stm32-nucleo-32-boards-stmicroelectronics.pdf
- STM32F446xC/E datasheet, ADC and GPIO characteristics: https://www.st.com/resource/en/datasheet/stm32f446re.pdf
- LTC1693: https://www.analog.com/media/en/technical-documentation/data-sheets/1693fa.pdf
- LTC1693-5: https://www.analog.com/media/en/technical-documentation/data-sheets/16935f.pdf
- TI SN74AHCT125, PW pin map and electrical limits: https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf
- ADG5412F: https://www.analog.com/media/en/technical-documentation/data-sheets/ADG5412F_5413F.pdf
- Susumu MSREM datasheet: https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6348/20240605MSRseriesdatasheetxlsx88.pdf
