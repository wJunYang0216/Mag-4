# Rev G LTspice driver simulation

Open `Koehler_AWG19_Newark_025R.asc` in LTspice and run. Keep the four local `.asy` symbols and the `vendor/` folder in place. The matching `.cir` file can be used as a netlist entry point. Local model dependencies are bundled with their existing notices.

See [NEWARK_REV_G.md](NEWARK_REV_G.md) for topology, assumptions, results, sources, and limitations. This earlier simulation uses a 0.25-ohm shunt and INA241A1 current monitor; it does not include the Rev I relay or external INA818 receiver.

## Included files

- `.asc` / `.cir`: editable circuit and simulation netlist.
- `.plt`: saved waveform plot settings.
- `.log`: retained nominal-run solver log, including convergence information.
- `Newark_025R_Results.json`: saved numerical measurements.
- `Newark_025R_trace.csv`: saved 10-us sampled trace, not a substitute for the full solver trace.
- `check_newark.py`: Python/NumPy analysis of the LTspice binary `.raw` result.
- `vendor/`: required model libraries and engineering diode approximations.

## Repeat the analysis

1. Install Python with NumPy (`python -m pip install numpy`).
2. Run the LTspice schematic to generate `Koehler_AWG19_Newark_025R.raw` in this folder.
3. Run `python check_newark.py` from this folder. It checks the saved waveform and regenerates the JSON and CSV.

The parser expects the UTF-16LE header and binary waveform format used by the recorded LTspice run. Raw solver outputs are generated locally and excluded from Git. Saved simulation data was copied from the existing project; this repository preparation did not rerun LTspice or establish hardware performance.
