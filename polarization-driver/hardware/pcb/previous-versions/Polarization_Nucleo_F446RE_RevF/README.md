# Selected diode revision — 2026-10-02

D1: Littelfuse SMBJ28A. DigiKey SMBJ28ALFCT-ND.
https://www.digikey.com/en/products/detail/littelfuse-inc/SMBJ28A/286002
D2: Vishay US1D-E3/61T. DigiKey US1D-E3/61TGICT-ND.
https://www.digikey.com/en/products/detail/vishay-general-semiconductor-diodes-division/US1D-E3-61T/1091567

Existing SMB and SMA footprints and all electrical connections are retained.
Both cathodes (pad 1, banded ends) connect to CLAMP_MID; D1 anode is TOP,
D2 anode is BOTTOM. PCB value fields and schematic values now identify ordered parts.

LTspice: open Koehler_AWG19_SelectedDiodes.asc in driver_package/current_sensor.
Keep INA240A1_local.asy and vendor/ beside the ASC. Installed LTspice ADG5412F
and LTC1693 symbols/models remain required. Original current-sensor files preserved.
The selected diodes use explicitly named APPROX models in vendor/selected_diodes.lib:
NOT manufacturer models, not a production/worst-case/thermal qualification.
TVS breakdown is set to the upper 25C datasheet endpoint; capacitance is assumed.
US1D recovery is not fitted. Repetition rate, temperature, lead inductance and
receiver recovery require bench verification. Old 45.43V result does not apply.

PCB remains an engineering draft: no hardware interlock, no discharge-current
measurement, remaining passive ratings need review, and noise performance untested.
The simulation does not incorporate the RevE/F Nucleo buffer circuitry.

Verified run: 70 ms complete; all saved values finite. Icoil(24ms)=1.008388 A; I_ADC=2.658147 V; BOTTOM peak=40.204784 V. Convergence tolerance-relaxation warnings near turn-off persist. Receiver residual remains about 10.9 mV.
