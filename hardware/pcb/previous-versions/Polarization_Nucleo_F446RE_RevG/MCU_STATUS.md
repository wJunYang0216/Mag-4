# MCU status integration

The MCU already knows which mode it commanded. Rev G adds a measurement that can confirm current during polarization and its decay during discharge. It does not sense every possible hardware failure.

## Inputs

- Sample PA0 / ADC1_IN0 from driver J3-7. Use a timer-triggered ADC with suitable acquisition time; 20 ksample/s is an initial test rate, not a validated firmware requirement.
- Read PC7 from J3-8: FF is active LOW. It reports ADG5412F source faults and can assert during normal clamp discharge. Require it to clear before reception; do not treat an expected clamp-period assertion as an unexpected polarization fault.
- Use the actual measured ADC reference voltage, not an assumed exact 3.300 V. Calibrate the zero-current baseline after the hardware is settled. Nominal zero is 0.99 V, approximately code 1229 for a 12-bit, 3.3 V ADC. Nominal sensitivity is 1.5 V/A, about 1861 codes/A. Calibrate gain with a known current; R9 tolerance is 1%.

## Suggested status logic for the MCU teammate

| Status | Evidence / action |
|---|---|
| IDLE | Drive off; receiver isolated; wait for settled zero-current baseline. Reject an implausible baseline or stale ADC. |
| POLARIZING | POL asserted after TG is off and dead time has elapsed. Confirm current rises into an expected band. Hold for the separately determined polarization duration. A plateau alone does not prove nuclear polarization. |
| DISCHARGING | POL off, RX isolated and blanking retained. Apply TG only after validated dead time. Monitor current as it decays. |
| CURRENT_LOW | Example qualification: absolute calibrated current below 20 mA for five consecutive 50 us samples. Reset the counter whenever the threshold is exceeded. This is a current condition, not receiver-ready. |
| SETTLING | Release damping and receiver clamps in the planned order; include settling after every transition. Any new current excursion resets qualification. Require FF clear. |
| ACQUIRING | Enter only after the complete receiver switching sequence and a bench-validated recovery interval. Collect the external receiver amplifier signal. |
| FAULT | Missing current during polarization, current above the validated limit, discharge timeout, implausible/stale ADC, or persistent FF before acquisition. Stop drive and keep RX isolated. |

Current-low calculation:

```text
voltage = adc_code * measured_vref / 4095
current_A = (voltage - calibrated_zero_V) / calibrated_V_per_A
low_count = low_count + 1 if abs(current_A) < 0.020 else 0
current_low = low_count >= 5
```

The nominal 20 mA window is roughly baseline +/-30 mV, or +/-37 ADC codes. This is resolvable electrically; noise and offsets on the assembled system still need measurement. A zero reading at power-up must not qualify a cycle before the MCU has observed valid polarization current and commanded switch-off.

The nominal output range is asymmetric: zero occurs at 0.99 V. A 5 V-powered amplifier followed by the 0.6 divider limits its normal high output to about 3 V. Allow for actual 5 V rail tolerance, divider tolerance and analog output swing. A saturated ADC/current channel is a fault condition, not a valid numerical current.

## Timing demonstrated in LTspice

The supplied test drives polarization from 5 to 25 ms, applies TG after 100 us break-before-make, releases DP at 37 ms, SH at 38.98 ms, enables RX at 39 ms, and releases RESET at 40 ms. These are ideal stimulus times. The test does **not** implement a closed-loop MCU; the current-low decision is evaluated from the saved analog trace.

The initial qualification example is reached about 0.85 ms after switch-off. Do not simply open RX at that instant. The existing receiver model still shows about 10.8 mV residual after the later switches operate. There is no validated microvolt recovery delay yet, and this board has no microvolt-level readiness detector.

## Bench acceptance checks

1. Use a current-limited supply and a known load before connecting the final coil; verify 0.99 V zero and about 2.49 V at 1 A.
2. Compare the amplified ADC estimate with a rated differential measurement across R9 during drive and discharge.
3. Check actual gate dead time and that Q4/Q5 never conduct together; MCU command states alone do not prove this.
4. Measure receiver recovery after each damping/blanking transition with the actual amplifier. Use that measurement to set the settling interval and acquisition timing.

No firmware has been flashed or bench tested by this update.
