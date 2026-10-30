# Project overview

## Intended system

The measurement chain is: MCU control → polarization driver → sample coil → floating receive connection → external receiver/amplifier → acquisition and frequency estimation. A full measurement requires coordination between the driver, coil, amplifier, and MCU subsystems.

The driver energizes the coil from an external supply. After polarization, switching and damping remove stored coil energy. In Rev I, a DPDT relay transfers both coil conductors to the receiver. The NUCLEO-F446RE commands the sequence and samples the current-sense output. The external INA818 receiver integration remains a team interface; its gain, rails, bias return, protection, and recovery require confirmation.

## Revision boundaries

| Artifact | Revision | What it establishes |
|---|---|---|
| KiCad project, BOM, Gerbers | I | Current 100 × 100 mm integrated PCB design with floating relay output |
| Saved PCB verification | I | Design-file checks at export, not physical performance |
| LTspice schematic and numerical results | G | Earlier electrical driver/current-sense behavior with ideal timed controls |
| MCU firmware | Pending | No firmware implementation supplied |
| Mechanical CAD | Pending | No enclosure/coil CAD supplied |

Do not use Rev G receiver timing or residual-voltage results as validation of Rev I. The relay circuit has not been simulated in the included model. Detailed connector definitions and required timing are in the current PCB release notes.

## Initial validation plan

- Review BOM, component pinouts, connector harness, supply rails, and assembly choices.
- Power the driver with a current-limited supply and known resistor load first.
- Verify current-sensor zero and gain against an independent measurement.
- Measure switch dead time, discharge voltage/current, and relay operate/release settling.
- Establish receiver input bias, protection, and recovery using the actual amplifier.
- Validate reset and supply-failure behavior and then test a complete acquisition cycle.
- Record instruments, setup, firmware revision, waveforms, acceptance limits, and measured results here.

## Documentation still to add

Team responsibilities, final requirements, firmware build/flash instructions, mechanical drawings, complete system wiring, measured performance, and final demonstration results.
