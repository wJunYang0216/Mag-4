# ECE455 AWG19 polarization driver PCB — revision E - NUCLEO-F446RE engineering draft

Open `Polarization_Nucleo_F446RE_RevE.kicad_pro` in KiCad 10, then open the PCB and schematic from the project manager. `Polarization_Nucleo_F446RE_RevE.kicad_pcb` can also be opened directly in PCB Editor. All files should remain in the same folder.

## What is included

- Editable, routed 100 x 80 mm, two-copper-layer board; nominal 1.6 mm thickness.
- 42 circuit footprints, four 3.2 mm mounting holes, rear ground pour, connector pin labels.
- 1.2 mm main polarization-current tracks and approximately 0.25 mm signal/control tracks; 0.20 mm default clearance, 0.65/0.30 mm vias. These are layout choices, not a validated thermal/fabricator specification.
- Paired connected schematic with footprint assignments and local symbol library.
- KiCad schematic PDF, PCB layout SVG/PNG and 3D preview.
- `footprint_assignments.csv`, `drc.json`, and `verification.json` for review.

This revision adds J5 raw shunt sense pins, expands J3 to a 12-pin NUCLEO-F446RE cable interface, and adds U5 SN74AHCT125PWR with C9 and R11-R18 for logic-level translation and default-low controls. The MCU remains external. See NUCLEO_WIRING.md for the exact wiring and power instructions. No discharge-current sensor or hardware interlock was added. The PCB uses Q1/Q4/Q5 corresponding to the earlier simulated M1/M4/M5.

## Validation performed

KiCad 10.0.6 DRC with schematic parity: **0 violations, 0 unconnected items, 0 schematic-parity issues**. All 137 intended physical pin-to-net assignments were separately checked in both the schematic netlist and PCB. The four mounting holes are board-only mechanical items. NC pins retain the schematic's individual unconnected net names.

DRC does not establish electrical functionality, noise performance, thermal margin, safe switching sequence, or suitability for manufacturing. No Gerber manufacturing release has been issued.

## Connectors

| Connector | Pin order | Purpose |
|---|---|---|
| J1 | 1 +12V input, 2 -12V input, 3 +3.3V MONITOR/OUTPUT, 4 GND | External regulated +/-12V; J1-3 must not be driven by an external supply |
| J2 | 1 TOP, 2 BOTTOM | External coil: 11.430016 ohms, 25.92669 mH |
| J3 | 1 POL_3V3, 2 TG_3V3, 3 RX, 4 SH, 5 DP, 6 RESET, 7 I_ADC, 8 FF, 9 GND, 10 +3.3V, 11 +5V, 12 GND | Nucleo cable; logic supplies come FROM Nucleo. See NUCLEO_WIRING.md |
| J4 | 1 RX_IN, 2 GND | External amplifier input |

## Before ordering a board

1. **Current sensing remains polarization-only.** R9 is 0.05 ohm in Q1's source return. Coil discharge bypasses it. Do not use a zero current reading to declare discharge complete. Measuring both paths requires a schematic change and corresponding PCB revision. Nominal INA240A1 output is 1.65V + 1V/A. Dedicated sense branches are included; ground-return coupling and sensor accuracy still require bench validation.
2. **D1 and D2 are not selected parts.** D1 has a provisional SMB footprint and D2 a provisional SMA footprint. The simulated idealized 43V clamp is not equivalent to buying a TVS with “43” in its part number. Check maximum coil-node voltage, tolerance, pulse energy, recovery, capacitance and the ADG5412F source-pin limits using the exact ordered parts. The original approximately 45V simulation result is not a hardware voltage guarantee.
3. **MCU switching and startup remain unfinished.** Prevent Q4/Q5 overlap, validate logic-high levels against the LTC1693 input thresholds, and validate power-up/reset behavior with the added default-low resistors. There is no hardware interlock or automatic overcurrent shutdown. Preserve receiver isolation during polarization and discharge, then allow amplifier recovery before sampling.
4. **Confirm the orderable BOM against these footprints.** U4 specifically uses INA240A1PW TSSOP-8; the SOIC package has a different pinout. Check all MOSFET pinouts, TO-220 tab clearances and thermal requirements. IRF530/IRF9640 are the simulated alternatives. Connectors use provisional Phoenix MKDS 5.08mm and 2.54mm header footprints.
5. **Review passive specifications.** R9 uses a generic 2512 footprint; choose a suitable low-inductance shunt with compatible pads, tolerance and pulse rating. Other resistors/capacitors use provisional 0805 footprints. Choose capacitor voltage ratings from worst-case node voltage, not just nominal rail voltage. Review C1 dielectric, leakage, microphonics and DC-bias effects for the very small receive signal; a different technology may require a larger footprint.
6. **Review analog noise and switching recovery.** Receiver and driver are separated on this board, but no microvolt-level noise qualification has been performed. Bench-test leakage, coupling, grounding and recovery with the teammate's amplifier. The prior simulation had convergence warnings and residual receiver voltage.
7. Confirm enclosure size, cable direction, copper weight, stackup, trace-temperature rise, manufacturer capabilities and assembly clearances. The placement is a prototype starting point without an enclosure specification.

The 3D preview uses generic KiCad package models and is not proof of selected part fit.

J5: pin 1 CURRENT_SENSE+ and pin 2 CURRENT_SENSE- expose the raw 50 mOhm shunt. Use J3-7 / PA0 for amplified current measurement; the STM32F446RE ADC is single-ended. A wiring table and source references are in NUCLEO_WIRING.md.

Schematic ERC retains one intentional warning: ADG5412F VSS connects to -12V, not ground. Layout changes and the 5V buffer have not been included in a new LTspice run or verified on hardware.

