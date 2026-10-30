# Revision G simulation: Newark 0.25 ohm shunt

Open **Koehler_AWG19_Newark_025R.asc** in LTspice and click Run. Keep the local `.asy` files and `vendor` folder beside it. The matching `.cir` is also included. Do not use the earlier SelectedDiodes or FullCurrent files for the new board values.

RSHUNT represents PCB R9, Bourns **CRG2512-FZ-R250E-2**, 0.25 ohm, 2 W, 1%. XU4 uses TI's INA241A1 model through a pin-order adapter. RADC is PCB R10 (1k), RADCLOAD is PCB R19 (1.5k), and CADC is C2 (10n). Amplifier power is 5 V; REF1 is 3.3 V and REF2 is ground. The nominal ADC transfer is 0.99 V + 1.5 V/A.

Local ADI gate-driver and analog-switch models are included, with their original notices. The input stimuli represent buffered 5 V POL/TG and 3.3 V analog-switch control levels. U5's propagation and startup behavior are not modeled. The selected TVS and diode are engineering approximations in selected_diodes.lib, not manufacturer-qualified SPICE models. The external receiver remains a 100k / 10p placeholder; there is no proton signal source or receiver amplifier.

The default transient runs for 70 ms with a 100 ns maximum timestep. This file uses ideal timed controls, not closed-loop MCU firmware. The comparator-like current-low decision was evaluated afterward from the saved ADC trace at 20 ksample/s.

## Measured nominal results

| Quantity | Result |
|---|---:|
| Coil current at 24 ms | 0.991753 A |
| Shunt current at 24 ms | 0.991749 A |
| Shunt loss at 24 ms | 0.24589 W |
| Zero-current ADC voltage at 3 ms | 0.990122 V |
| ADC voltage at 24 ms | 2.477735 V |
| ADC min / max over run | 0.98280 / 2.47781 V |
| Sense-input min / max | -0.82154 / 11.99989 V |
| BOTTOM peak | 39.79497 V |
| Current-low: below 20 mA for 5 samples, 20 ksample/s | 25.85 ms absolute, about 0.85 ms after drive off |
| Max absolute RX voltage, 60-70 ms | 10.8076 mV |

The shunt and coil currents match through the main discharge; small differences include amplifier bias current and coil parasitic capacitance. The ADC filter adds a small delay: at 25.4 ms actual coil current is 0.32083 A and the inferred ADC current is about 0.33030 A. That delay is included in the threshold example.

The run completed through 70 ms with finite saved traces. LTspice reported operating-point gmin stepping and relaxed transient tolerances around switch-off. These nominal results establish topology and ADC scaling, not tolerance-corner, stability, noise, pulse-rating, or hardware validation. Retain the log when reviewing the switching transient.

The 20 ms polarization pulse is an electrical test. The current-low result is **not** a receiver-ready result: the modeled millivolt residue is much larger than a microvolt proton signal.

`Newark_025R_Results.json` contains the numerical checks. `Newark_025R_trace.csv` contains uniformly sampled output data at 10 us intervals. The CSV does not replace the raw solver trace for examining fast spikes. Run `check_newark.py` with Python and NumPy after simulation to repeat the numerical checks.

Sources:
- https://www.newark.com/bourns/crg2512-fz-r250e-2/res-r25-1-2w-metal-strip-2512/dp/57AK7393
- https://www.bourns.com/docs/product-datasheets/CRG2512.pdf
- https://www.ti.com/lit/ds/symlink/ina241a.pdf
- TI INA241A1 PSpice model: https://www.ti.com/lit/zip/sbomc99
