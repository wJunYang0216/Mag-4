# LTspice — Rev G

Open `Koehler_AWG19_Newark_025R.asc` in LTspice. Keep the `.asy` files and `vendor/` folder beside it.

This simulation uses the 0.25-ohm shunt and INA241A1 current sensor. It does not include the Rev I relay.

Saved results are in `Newark_025R_Results.json` and `Newark_025R_trace.csv`. After running the simulation, use `python check_newark.py` to analyze the generated `.raw` file. The script requires NumPy.

See [NEWARK_REV_G.md](NEWARK_REV_G.md) for the original simulation notes.
