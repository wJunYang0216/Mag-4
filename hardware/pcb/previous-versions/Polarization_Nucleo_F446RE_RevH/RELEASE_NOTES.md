# Rev H — integrated polarization driver with floating receive output

## What to fabricate
One 120 x 80 mm, 2-layer PCB. Suggested standard first-build stackup: FR-4, 1.6 mm, 1 oz copper. Four 3.2 mm mounting holes. This replaces RevG plus the separate adapter for this build. Do not order the earlier adapter as well. Manufacturing files represent an untested first hardware revision, not validated instrument performance.

## Connectors
- J2: actual external coil. Pin 1 COIL_A, pin 2 COIL_B. This is a 2.54 mm header footprint; use a suitable rated mating harness or soldered wire connection, not the old 5.08 mm terminal block.
- J4: amplifier output. Pin 1 SIG+ to INA818 IN+, pin 2 SIG- to INA818 IN-, pin 3 GND to amplifier ground. Both signal pins are isolated from driver/ground through K1 during receive. This output bypasses the old single-ended AC-coupling and blanking circuit.
- J3: existing Nucleo 1x12 header. Pin 3 / PB10 (D6), previously RX, now ALSO commands the receive relay. No extra MCU GPIO required. J3 pin 11 supplies +5 V for the relay and existing circuitry. Allow about 21 mA additional relay current.
- J3 pin 7 / PA0 remains I_ADC. J3 pin 8 / PC7 remains the OLD ADG5412F fault output. It does not report relay position or the INA818's readiness.
- J5: raw floating shunt sense terminals. Neither is ground. Do not connect directly to MCU ADC.
- J6 and J7: retained DNP test footprints only. Do not populate for normal assembly. J6 is the legacy single-ended receiver node. J7 is the driver-side connector that USED TO BE the coil connector. DO NOT connect the external coil to J7, because that bypasses relay isolation.

## Relay and current paths
K1 = G6K-2P DC5, through-hole DPDT, non-latching. Coil pins 1 (+5 V), 8 (Q6 collector). Contact commons: 3 and 6. Rest contacts: 2 and 7. Operated contacts: 4 and 5. The G6K-2P-Y has different lead pitch and must NOT be substituted into this footprint. K1 holes are 0.85 mm with 2.54 mm longitudinal and 5.08 mm row spacing.

RX LOW: COIL_A connects to COIL_TOP, and COIL_B connects to BOTTOM. Polarization/discharge paths still include R9 (0.25 ohm, 2 W). RX HIGH: COIL_A connects to SIG+, COIL_B connects to SIG-. Driver MOSFETs, clamp, shunt amplifier and grounded blanking network remain on the disconnected driver side. GND is separate from both signal conductors.

New relay-current branches use 1.2 mm copper. The added bottom-current bridge uses 0.6 mm drilled vias. Existing dedicated shunt sense wiring is retained. R9 measures polarization and clamp discharge. Once K1 transfers, I_ADC cannot indicate current in the isolated coil.

## MCU sequence — required firmware change
1. Set POL LOW before changing RX. At startup, keep POL LOW and RX LOW. Allow relay return to settle before enabling any pulse.
2. With RX LOW and the relay settled in its rest position, apply the existing polarization sequence. Preserve Q4/Q5 break-before-make timing.
3. Turn POL LOW, execute discharge/damping, and leave RX LOW until discharge has ended. Use calibrated current measurements plus a validated minimum recovery interval. The old 20 mA threshold alone does not establish safe transfer or microvolt receiver recovery.
4. Set RX HIGH only after the current and residual voltage are sufficiently low. Allow relay movement/contact bounce and INA818 recovery before acquisition. Manufacturer 3 ms operate time does not include every system settling effect.
5. Before the next polarization, set RX LOW, keep POL LOW, and wait for relay return/contact settling. D3's flyback clamp can extend release time beyond the bare-relay value. Measure this on the bench.

No MCU firmware is flashed by this revision. No hardware relay-position feedback, relay-to-POL interlock, or Q4/Q5 interlock is implemented. Incorrect firmware can interrupt inductive current or connect the receiver at the wrong time. Reset/power-failure behavior still requires bench validation. Do not infer these interlocks from a clean DRC report.

## INA818 integration boundary
The amplifier IC is known, but its supply rails, gain, REF connection and protection circuit are unknown. The driver intentionally does NOT force either signal pin to ground or to an assumed bias voltage. The INA818 board must provide a DC bias-current return path and a valid input common-mode voltage (TI datasheet section 9.1.2). The REF pin controls output reference; it is not a substitute for input bias return. The device's ±60 V input protection specification is not a guarantee of recovery time, allowable repeated transient energy, or microvolt accuracy.

Do not connect an unreviewed receiver to the energized coil circuit. Test driver/relay with a resistor load first, then characterize coil transfer voltage and receiver recovery. Position this board away from the sensing bottle: K1's coil is energized during receive and can introduce a magnetic field. The datasheet minimum-load reference is 10 uA at 10 mV; microvolt contact noise/offset must be measured. These uncertainties remain after fabrication.

## Validation performed
- Schematic intended-net audit and board pin-net audit: 164 physical pins.
- DRC with schematic parity: zero reported violations, zero unconnected pads, zero parity issues at export.
- ERC: zero errors, one retained warning for U2 VSS on -12 V (intentional).
- Layout image visually inspected. No assembled-board measurements or new LTspice simulation of the relay circuit are included. Earlier RevG waveforms do not validate RevH receiver performance.
- Existing configured ignored checks are listed in drc.txt and erc.txt; these are not blanket proofs of correctness.

## Added assembly parts
K1 G6K-2P DC5; Q6 2N3904 (E-B-C TO-92, verify purchased variant pinout); D3 1N4148; R20 1 kohm; R21 100 kohm; C10 100 nF; J2 1x02 and J4 1x03 2.54 mm headers. J6/J7 DNP. See BOM_RevH.csv for all footprints. Prices/stock have not been refreshed in this fabrication package.

Sources:
https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6k.pdf
https://www.ti.com/lit/ds/symlink/ina818.pdf
