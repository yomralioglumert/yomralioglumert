from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from html import escape
now = datetime.now(ZoneInfo('Europe/Istanbul'))
months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
rows = [('DESTINATION TIME','OCT','21','2015','07','28','PM','#ff514a'),('PRESENT TIME',months[now.month-1],f'{now.day:02}',str(now.year),now.strftime('%I'),now.strftime('%M'),now.strftime('%p'),'#57ef91'),('LAST TIME DEPARTED','NOV','05','1955','06','00','AM','#ffb447')]
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 340" role="img" aria-label="DeLorean time circuits"><rect width="800" height="340" rx="14" fill="#111820"/><rect x="8" y="8" width="784" height="324" rx="10" fill="#080c12" stroke="#354354"/>']
for i,(label,*vals,color) in enumerate(rows):
 y=22+i*103
 s.append(f'<g font-family="monospace"><rect x="22" y="{y}" width="756" height="94" rx="6" fill="#131a21" stroke="#354354"/>')
 for x,w,heading,val in zip([42,166,246,418,526,644],[112,68,152,96,96,108],['MONTH','DAY','YEAR','HOUR','MIN','AM/PM'],vals):
  s.append(f'<text x="{x+w/2}" y="{y+14}" text-anchor="middle" font-size="10" fill="#adb9c8">{heading}</text><rect x="{x}" y="{y+20}" width="{w}" height="43" rx="4" fill="#04070a"/><text x="{x+w/2}" y="{y+52}" text-anchor="middle" font-size="30" font-weight="bold" fill="{color}">{escape(val)}</text>')
 s.append(f'<text x="400" y="{y+84}" text-anchor="middle" font-size="12" letter-spacing="3" fill="{color}">{label}</text></g>')
s.append('</svg>')
Path(__file__).resolve().parents[1].joinpath('assets/time-circuits.svg').write_text('\n'.join(s))
