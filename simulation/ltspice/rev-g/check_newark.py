from pathlib import Path
import re,json,csv
import numpy as np
p=Path(__file__).resolve().parent
b=(p/'Koehler_AWG19_Newark_025R.raw').read_bytes();mark='Binary:\n'.encode('utf-16-le');k=b.index(mark);h=b[:k].decode('utf-16-le');n=int(re.search(r'No. Variables: (\d+)',h)[1]);a=np.frombuffer(b[k+len(mark):],dtype=np.dtype([('t','<f8'),('v','<f4',(n-1,))]));names=re.findall(r'^\s*\d+\s+(\S+)\s+\S+',h,re.M)[1:];t=a['t'];d=dict(zip(names,a['v'].T))
assert t[-1]>=.07-1e-9
assert all(np.isfinite(v).all() for v in d.values())
v=lambda name,at:float(np.interp(at,t,d[name]))
zero=v('V(i_adc)',.003)
out={'end_s':float(t[-1]),'coil_A_24ms':v('I(LCOIL)',.024),'shunt_A_24ms':v('I(RSHUNT)',.024),'adc_V_24ms':v('V(i_adc)',.024),'adc_zero_V_3ms':zero,'shunt_W_24ms':v('I(RSHUNT)',.024)**2*.25,'bottom_max_V':float(d['V(bottom)'].max()),'adc_min_V':float(d['V(i_adc)'].min()),'adc_max_V':float(d['V(i_adc)'].max()),'sense_input_min_V':float(min(d['V(top)'].min(),d['V(coil_top)'].min())),'sense_input_max_V':float(max(d['V(top)'].max(),d['V(coil_top)'].max())),'rx_60_70ms_max_V':float(np.max(np.abs(d['V(rx_in)'][t>=.06])))}
out['discharge_samples']=[{'time_ms':at*1000,'coil_A':v('I(LCOIL)',at),'shunt_A':v('I(RSHUNT)',at),'adc_V':v('V(i_adc)',at),'inferred_A':(v('V(i_adc)',at)-zero)/1.5} for at in [.02505,.0252,.0254,.0256,.0258,.026]]
samples=np.arange(.02505,.030,.00005);count=0;qualified=None
for ts in samples:
 current=(v('V(i_adc)',ts)-zero)/1.5
 count=count+1 if abs(current)<.02 else 0
 if count>=5:qualified=float(ts);break
out['example_20mA_5_samples_20kHz_qualified_ms']=qualified*1000 if qualified else None
assert .8<out['coil_A_24ms']<1.1
assert 2<out['adc_V_24ms']<3.1
assert 0<=out['adc_min_V'] and out['adc_max_V']<3.3
assert -5<out['sense_input_min_V'] and out['sense_input_max_V']<110
assert qualified and qualified>.0255
assert all(abs(s['coil_A']-s['shunt_A'])<.002 for s in out['discharge_samples'])
ts=np.arange(0,.07000001,.00001)
coil,shunt,adc,rx=[np.interp(ts,t,d[n]) for n in ['I(LCOIL)','I(RSHUNT)','V(i_adc)','V(rx_in)']]
with (p/'Newark_025R_trace.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['time_ms','coil_A','shunt_A','adc_V','inferred_A','rx_V'])
 w.writerows(zip(ts*1000,coil,shunt,adc,(adc-zero)/1.5,rx))
(p/'Newark_025R_Results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
