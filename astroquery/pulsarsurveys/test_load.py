import json
from astropy.table import Table, Column, MaskedColumn
import numpy as np
from astropy import units as u, constants as c

f=open("test.json")
out = json.load(f)

columns=['PSR',
         'RA',
         'Dec',
         'P',
         'DM',
         'survey',
         'retrieval date',
         'Distance']
units = [None,
         u.deg,
         u.deg,
         u.ms,
         u.pc/u.cm**3,
         None,
         None,
         u.deg]
         
data = {}
for col in columns:
    data[col] = []
        

for key in out.keys():
    if key in ['searchra','searchdec','searchrad','searchcoord','searchdm','searchdmtolerance','nmatches']:
        continue
    data['PSR'].append(key)
    data['RA'].append(out[key]['ra']['value'])
    data['Dec'].append(out[key]['dec']['value'])
    data['P'].append(out[key]['period']['value'])
    data['DM'].append(out[key]['dm']['value'])
    data['survey'].append(out[key]['survey']['value'])
    data['retrieval date'].append(out[key]['date']['value'])
    data['Distance'].append(out[key]['distance']['value'])
    
columndata = {}
for col, unit in zip(columns, units):
    if col in ['P', 'DM']:
        columndata[col] = MaskedColumn(data[col], name=col, unit=unit, mask=np.array(data[col])<0)
    else:
        columndata[col] = Column(data[col], name=col, unit=unit)
    
outtable = Table(columndata)
for key in out.keys():
    if key in ['searchra','searchdec','searchrad','searchcoord','searchdm','searchdmtolerance']:
        outtable.meta[key] = out[key]['value']
        
