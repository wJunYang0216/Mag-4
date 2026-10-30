# Revision G: coil-current feedback for NUCLEO-F446RE

Open **Polarization_Nucleo_F446RE_RevG.kicad_pro**. The schematic and routed two-layer, 100 x 80 mm PCB belong together. Earlier revisions are preserved.

## Changes

- R9 is **Bourns CRG2512-FZ-R250E-2**, 0.25 ohm, 2 W, 1%, 2512. Newark cut-tape part **57AK7393**. This is a passive shunt resistor; U4 provides the amplification.
- R9 moved into the **TOP -> R9 -> COIL_TOP -> coil** path. Both polarization and clamp discharge pass through it. Q1 source and its gate pulldown now return directly to ground.
- U4 changed to **INA241A1IDR**, gain 10, SOIC-8, supplied from the Nucleo's 5 V rail. This is a different pinout from INA240. The schematic and PCB use the new physical pin map, including grounding reserved pin 4.
- R10 is now 1 kohm, 0.1%; added R19, 1.5 kohm, 0.1%. Their divider reduces the amplifier output to 60%. C2 remains 10 nF; the nominal divider/filter time constant is 6 us.
- Dedicated Kelvin traces connect both shunt pads to U4 and J5. Main current traces are 1.2 mm; sense traces are 0.25 mm.
- The project includes a local **R_CRG2512** footprint using Bourns' recommended 2.1 x 4.0 mm pads and 4.1 mm gap.

## Current paths

Polarization: +12 V -> Q4 -> TOP -> R9 -> J2-1 -> external coil -> J2-2 -> BOTTOM -> Q1 -> GND.

Clamp discharge: BOTTOM -> D2 -> CLAMP_MID -> D1 in avalanche -> TOP -> R9 -> external coil -> BOTTOM. Current initially continues in the same direction through R9 after the drive switches turn off.

Signal mode: Q4/Q1 off, Q5 grounds TOP, receiver switching sequence releases damping/blanking. The coil's top return includes R9. The receive noise/loading effect of the shunt and amplifier inputs still requires bench evaluation.

## MCU feedback

J3-7 **I_ADC -> PA0 / A0** is the normal MCU current input. Nominally:

`V_I_ADC = 0.99 V + 1.5 V/A * I_coil`

`I_coil = (V_I_ADC - calibrated_zero_voltage) / 1.5`

J3-8 **FF -> PC7 / D9** is the ADG5412F active-low source-overvoltage fault flag. It is not a coil-current comparator, supply-good output, or universal board-health flag. A fault indication can occur normally during the high-voltage discharge interval.

J5-1 **CURRENT_SENSE+ = TOP** and J5-2 **CURRENT_SENSE- = COIL_TOP** remain available. Their differential signal is 0.25 V/A. **Neither is ground. Both can sit near 12 V; do not connect J5 directly to Nucleo ADC/GPIO pins.** Use J3-7, or rated external differential instrumentation.

See **MCU_STATUS.md** for the status logic and **NUCLEO_WIRING.md** for the cable assignments. This update provides feedback hardware and integration guidance; it does not flash or test Nucleo firmware.

## Validation and limits

The delivered PCB passed KiCad DRC with zero violations, zero unconnected pads, and zero schematic parity issues. The connectivity script verifies 140 physical pin-to-net assignments. ERC has zero errors and one retained warning: ADG5412F VSS is intentionally connected to -12 V rather than ground.

LTspice uses the specified 11.430016 ohm / 25.92669 mH coil, TI's INA241A1 model, ADI gate-driver/switch models, and engineering approximations for the selected diodes. See the accompanying simulation results. The diode models are not manufacturer-qualified models. No PCB parasitic extraction, thermal test, assembled-board test, or real proton signal is included.

Current decay alone does not certify microvolt receiver recovery. The modeled RX output remains around 10.8 mV at 60-70 ms. Receiver recovery and firmware timing must be validated with the actual amplifier and coil. The electrical 20 ms polarization pulse does not establish the sample's nuclear polarization time.

There is still no hardware interlock between Q4 and Q5 and no independent hardware overcurrent shutdown. Firmware must enforce break-before-make. Treat this as an engineering prototype, not a fabrication release or hardware-tested design.

## Parts and sources

- R9: https://www.newark.com/bourns/crg2512-fz-r250e-2/res-r25-1-2w-metal-strip-2512/dp/57AK7393
- Bourns land pattern, rating and derating: https://www.bourns.com/docs/product-datasheets/CRG2512.pdf
- U4: https://www.ti.com/product/INA241A/part-details/INA241A1IDR
- Amplifier pinout and electrical limits: https://www.ti.com/lit/ds/symlink/ina241a.pdf
- R10: Yageo RT0805BRD071KL, 1 kohm, 0.1%, 0805
- R19: Yageo RT0805BRD071K5L, 1.5 kohm, 0.1%, 0805

The initially considered Vishay 1 W part was replaced by the Bourns 2 W part after checking resistance-dependent power derating. Use the Bourns part in this revision. BOM_RevG.csv lists all footprints and values, with exact MPNs for the changed components; blank MPNs are not new purchasing approvals for unchanged generic components.
