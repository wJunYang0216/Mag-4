# Mag-4

ECE 455 final project — proton-precession magnetometer development.

Mag-4 aims to measure magnetic field from the precession signal of a polarized sample. The intended measurement cycle energizes the polarization coil, turns off and damps the coil current, transfers the coil to a receiver, and acquires the signal for frequency estimation. This repository contains the beginnings of the final project documentation and the available polarization-driver design files.

## Current scope and status

The available hardware is the **Rev I polarization-driver PCB**, a 100 × 100 mm, two-layer board interfacing with a **NUCLEO-F446RE**. It includes the coil power stage, turn-off clamp, damping circuitry, current sensing, and a DPDT relay that transfers both coil terminals to a floating receive output for an external INA818 amplifier.

The included **Rev G LTspice simulation** documents the earlier driver and current-sense topology. It uses an AWG 19 coil model of 11.430016 ohms and 25.92669 mH. It does not model the Rev I relay or validate the final receiver.

This is an ongoing design, not a demonstrated complete magnetometer. The saved PCB checks report zero DRC violations and zero unconnected pads at export. Bench measurements, relay timing, receiver recovery, firmware, and complete system integration remain pending. See the [Rev I release notes](hardware/pcb/rev-i/RELEASE_NOTES.md) for detailed constraints.

## Repository organization

| Folder | Contents |
|---|---|
| [docs/](docs/project-overview.md) | System description, design status, and validation plan |
| [hardware/pcb/rev-i/](hardware/pcb/rev-i/) | Editable KiCad schematic, PCB, project, custom symbols and footprints, BOM, schematic PDF, layout preview, Gerbers, and saved checks |
| [hardware/mechanical/](hardware/mechanical/) | Status of enclosure and coil mechanical CAD |
| [simulation/ltspice/rev-g/](simulation/ltspice/rev-g/) | LTspice schematic/netlist, local symbols and models, saved simulation results, and Python analysis code |
| [firmware/](firmware/) | MCU implementation status and required sequencing interface |

## Main design files

- [KiCad project](hardware/pcb/rev-i/Polarization_Nucleo_F446RE_RevI.kicad_pro)
- [Editable schematic](hardware/pcb/rev-i/Polarization_Nucleo_F446RE_RevI.kicad_sch) and [schematic PDF](hardware/pcb/rev-i/Schematic_RevI.pdf)
- [PCB layout](hardware/pcb/rev-i/Polarization_Nucleo_F446RE_RevI.kicad_pcb)
- [Bill of materials](hardware/pcb/rev-i/BOM_RevI.csv)
- [Gerbers and drill files](hardware/pcb/rev-i/Gerbers/)
- [LTspice schematic](simulation/ltspice/rev-g/Koehler_AWG19_Newark_025R.asc) and [netlist](simulation/ltspice/rev-g/Koehler_AWG19_Newark_025R.cir)
- [Simulation analysis code](simulation/ltspice/rev-g/check_newark.py)

## Open the designs

**PCB:** Open the `.kicad_pro` file in KiCad 10 with its standard libraries installed. Keep `Project.kicad_sym`, `ProjectFootprints.pretty`, and both library-table files in the same folder. Read the release notes before assembly or using the fabrication outputs. `BOM_RevH.csv` is retained because the inherited release notes reference it; `BOM_RevI.csv` is the current BOM.

**Simulation:** Open `Koehler_AWG19_Newark_025R.asc` in LTspice and run the transient simulation. Keep the local `.asy` files and `vendor/` folder beside it. The existing notes record a successful run in LTspice 24.1.9. See [simulation instructions](simulation/ltspice/rev-g/README.md) for results and analysis.

**Firmware and mechanical CAD:** No implementation or mechanical CAD files were present in the available project package. Their folders explicitly record this status; they should be updated as those files become available.

## PCB preview

![Rev I polarization-driver PCB layout](hardware/pcb/rev-i/layout.png)

## Next milestones

1. Review assembly, connector wiring, and component choices against the Rev I release notes.
2. Implement and review MCU sequencing, calibration, and fault handling.
3. Test with a current-limited supply and resistor load, then characterize coil discharge and relay transfer.
4. Integrate the receiver and measure recovery before collecting precession signals.
5. Add firmware, mechanical CAD, measured results, and final operating instructions.

Third-party SPICE model files retain their original notices. No repository-wide license is assigned in this initial documentation commit.
