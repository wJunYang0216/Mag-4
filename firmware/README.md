# Firmware status

No MCU source code was present in the available project files. This folder reserves the location for the NUCLEO-F446RE firmware, build configuration, and flashing instructions.

The current sequencing requirements are in [Rev I release notes](../hardware/pcb/rev-i/RELEASE_NOTES.md). In particular, keep POL LOW while transferring the relay, preserve power-switch break-before-make timing, complete discharge before receive transfer, and allow measured relay/receiver settling before acquisition. RX is PB10 (D6); current input is PA0; PC7 reports the legacy ADG5412F fault flag, not relay position.

The board provides no hardware relay-position feedback or relay-to-POL interlock. Earlier simulation stimuli and the Python analysis script are not executable MCU firmware. Add the implemented state machine, pin configuration, calibration, fault behavior, and build/flash instructions when available.
