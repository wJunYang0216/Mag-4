# Floating coil relay adapter — engineering draft

This is a NEW inline adapter, not a replacement or reroute of RevG. Do not fabricate yet. Receiver protection, input bias, relay contact behavior at microvolt level, switching faults and magnetic interference remain unvalidated.

## Wiring
- Disconnect the physical coil from RevG J2. Connect RevG J2-1 to adapter J1-1 (DRIVER_A), and J2-2 to adapter J1-2 (DRIVER_B).
- Connect the coil to adapter J2-1 (COIL_A) and J2-2 (COIL_B).
- Adapter J3-1 = SIG+, J3-2 = SIG-, J3-3 = GND. Connect these to the teammate amplifier IN+, IN-, and ground. The amplifier must provide suitable input bias return and protection. No amplifier compatibility test has been performed.
- Adapter J4-1 = regulated +5 V, J4-2 = RX_SELECT from a spare 3.3 V MCU output, J4-3 = GND. Confirm the spare GPIO with the MCU teammate. Do not reuse an assigned pin without updating firmware.
- Leave the OLD RevG signal connector J4 disconnected from the amplifier. The adapter bypasses the old single-ended receive path and its AC coupling/protection. Do not connect both outputs.

## Operation
K1 deenergized connects COM3 to NC2 and COM6 to NC7: coil remains connected to driver, R9 and discharge clamp. K1 energized connects COM3 to NO4 and COM6 to NO5: both coil ends connect directly to SIG+/SIG-. Neither signal is tied to ground on the adapter.

Keep K1 deenergized through polarization and the entire discharge. Turn off polarization, verify current has decayed to the calibrated zero range, and allow a validated settling interval. Only then assert RX_SELECT. Allow relay travel, bounce and receiver settling before acquisition. Before the next pulse, deassert RX_SELECT and wait for confirmed/validated return settling before enabling the driver. Do not use the earlier 20 mA example as proof that it is safe to transfer to the amplifier: residual inductive energy and transient voltage must be measured.

Current measurement remains valid during polarization/discharge. During reception, R9 stays on the driver side and does NOT measure the now-disconnected coil. A zero ADC reading after relay transfer cannot indicate coil status.

## Candidate components
K1: Omron G6K-2P DC5, DPDT through-hole, non-latching. Datasheet carry rating 2 A; 1 A at 30 VDC resistive switching rating. It must transfer only with drive off and essentially zero current. 3 ms operate/release specification does not establish complete settling, particularly with a flyback diode. Manufacturer minimum-load reference is 10 uA at 10 mV, so microvolt performance is NOT guaranteed by that specification.
Q6: 2N3904, TO-92 E-B-C footprint (verify purchased manufacturer pinout).
D3: 1N4148 flyback diode, cathode to +5 V.
R20: 1 kohm base resistor; R21: 100 kohm base pulldown.
C10: 100 nF local bypass. Connectors: J1/J2 1x02 and J3/J4 1x03, 2.54 mm.

## Required validation
- Verify real relay contact pinout and break-before-make behavior against manufacturer drawing and continuity measurements before assembly.
- Validate all three states with a resistor load before connecting the inductive coil or amplifier.
- Check relay transfer under controller reset and 5 V power loss. Default return to driver can occur unexpectedly; a hardware drive inhibit / interlock is still required before release.
- Relay coil is energized during reception. Keep the driver/adapter away from the sensing bottle and measure magnetic interference, drift and contact noise. Consider a latching relay if the field proves unacceptable.
- Model and measure amplifier common mode, input bias return, residual coil voltage, protection and recovery. The old receiver waveform does not validate this circuit.
- PCB routing checks are geometric/connectivity checks only; this is not a tested instrument design.

Manufacturer reference: https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6k.pdf
