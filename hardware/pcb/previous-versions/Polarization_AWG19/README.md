# AWG 19 polarization driver, KiCad engineering draft

Open `Polarization_AWG19.kicad_pro` in KiCad 10, then open its schematic. Or open `Polarization_AWG19.kicad_sch` directly in the schematic editor. `Project.kicad_sym` and the library tables travel with the project. The PDF is a read-only preview.

This editable schematic transfers the current-sensor version of the LTspice design into physical components, with named nets joining the drawing blocks. Q1/Q4/Q5 correspond to LTspice M1/M4/M5 and the original S1/S4/S5 functions. U2 is one ADG5412F with four physical channels, rather than four physical ICs. U4 is the INA240A1PW TSSOP current sensor. Its pinout differs from the SOIC version.

External connections:

- J1: regulated +12 V, -12 V, +3.3 V and ground. The project does not design these power supplies.
- J2: external AWG 19 coil, TOP/BOTTOM. R = 11.430016 ohms and L = 25.92669 mH are coil parameters, not separate board parts.
- J3: MCU controls POL, TG, RX, SH, DP and RESET, plus I_ADC, FF, ground and the 3.3-V reference rail.
- J4: RX_IN and ground to the teammate's amplifier.

Simulation-only coil capacitance, receiver load and ADC load are omitted from the hardware sheet. Local supply bypass capacitors are added at the IC supplies. These bypass changes and real layout have not been simulated as a physical PCB.

Current sensing uses 0.05 ohm in Q1's source return and INA240A1 gain 20. Nominally I = (Vadc - 1.65 V) / (1 V/A). It measures polarization current only. Clamp/discharge current bypasses the shunt. Use Kelvin routing. The MCU ADC is assumed compatible with 3.3 V.

## Verification and limits

KiCad CLI loads the schematic and exports PDF/netlist. ERC reports zero errors and one warning: U2 VSS pin 4 is connected to -12 V rather than ground. This is intentional for the bipolar supply specified by ADG5412F. The warning is retained and not suppressed. The exported pin-to-net map is checked against the intended physical-pin mapping by check_connectivity.py.

This is a design draft, not a fabrication-ready board:

- D1 and D2 are explicit placeholders. Select real clamp parts and pulse-energy ratings. The cathodes join at CLAMP_MID, matching the simulation.
- IRF530/IRF9640 are the simulated alternatives, not validation of the earlier IRL540N/IRF9540N BOM.
- MCU firmware must guarantee Q4/Q5 dead time. There is no hardware interlock, automatic overcurrent shutdown, or finalized power-up/reset bias scheme.
- Validate MCU guaranteed logic levels, driver supply limits, receiver noise/recovery, and sensor calibration. The earlier simulation still has convergence warnings and about 10.87 mV receiver residual.
- Only IC/MOSFET package suggestions are assigned. Passive, diode and connector footprints and all orderable part numbers need final review.
- No PCB layout or manufacturing files have been made.

## Pinout references

- ADG5412F TSSOP: https://www.analog.com/media/en/technical-documentation/data-sheets/ADG5412F_5413F.pdf (Table 7)
- LTC1693-1 SOIC: https://www.analog.com/media/en/technical-documentation/data-sheets/1693fa.pdf
- LTC1693-5 MSOP: https://www.analog.com/media/en/technical-documentation/data-sheets/16935f.pdf
- INA240A1PW TSSOP: https://www.ti.com/lit/ds/symlink/ina240.pdf

Generic G-D-S MOSFET and diode/resistor/capacitor graphics derive from the installed KiCad symbol libraries. IC symbols are local project symbols with explicit physical pin numbers.
