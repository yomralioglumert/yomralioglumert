from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from html import escape
now = datetime.now(ZoneInfo('Europe/Istanbul'))
months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
rows = [('DESTINATION TIME','OCT','21','2015','07','28','PM','#ff514a'),('PRESENT TIME',months[now.month-1],f'{now.day:02}',str(now.year),now.strftime('%I'),now.strftime('%M'),now.strftime('%p'),'#57ef91'),('LAST TIME DEPARTED','NOV','05','1955','06','00','AM','#ffb447')]
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 340" role="img" aria-label="DeLorean time circuits"><rect width="800" height="340" rx="14" fill="#111820"/><rect x="8" y="8" width="784" height="324" rx="10" fill="#080c12" stroke="#354354"/>']
segments = {'0':'abcdef','1':'bc','2':'abdeg','3':'abcdg','4':'bcfg','5':'acdfg','6':'acdefg','7':'abc','8':'abcdefg','9':'abcdfg'}
paths = ['M4 0H18L21 3 18 6H4L1 3Z','M19 5L22 8V19L19 22 16 19V8Z','M19 25L22 28V39L19 42 16 39V28Z','M4 40H18L21 43 18 46H4L1 43Z','M3 25L6 28V39L3 42 0 39V28Z','M3 5L6 8V19L3 22 0 19V8Z','M4 20H18L21 23 18 26H4L1 23Z']
def digits(value,x,y,w,color):
    out=[]
    for i,digit in enumerate(value):
        out.append(f'<g transform="translate({x+w/2-len(value)*10+i*20} {y}) scale(.78)">')
        for name,path in zip('abcdefg',paths):
            out.append(f'<path d="{path}" fill="{color if name in segments[digit] else "#20262b"}"/>')
        out.append('</g>')
    return ''.join(out)
for i,(label,*vals,color) in enumerate(rows):
 y=22+i*103
 s.append(f'<g font-family="monospace"><rect x="22" y="{y}" width="756" height="94" rx="6" fill="#131a21" stroke="#354354"/>')
 for x,w,heading,val in zip([42,166,246,418,526,644],[112,68,152,96,96,108],['MONTH','DAY','YEAR','HOUR','MIN','AM/PM'],vals):
  s.append(f'<text x="{x+w/2}" y="{y+14}" text-anchor="middle" font-size="10" fill="#adb9c8">{heading}</text><rect x="{x}" y="{y+20}" width="{w}" height="43" rx="4" fill="#04070a"/>')
  s.append(digits(val,x,y+24,w,color) if val.isdigit() else f'<text x="{x+w/2}" y="{y+52}" text-anchor="middle" font-size="27" font-weight="bold" fill="{color}">{escape(val)}</text>')
 s.append(f'<text x="400" y="{y+84}" text-anchor="middle" font-size="12" letter-spacing="3" fill="{color}">{label}</text></g>')
s.append('</svg>')
Path(__file__).resolve().parents[1].joinpath('assets/time-circuits.svg').write_text('\n'.join(s))
