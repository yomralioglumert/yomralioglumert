import json, os, urllib.request
from pathlib import Path
from datetime import datetime, timezone
from html import escape
ROOT=Path(__file__).resolve().parents[1]
QUERY='''query($login:String!){user(login:$login){repositories(privacy:PUBLIC,ownerAffiliations:[OWNER]){totalCount} contributionsCollection {totalCommitContributions totalPullRequestContributions totalIssueContributions contributionCalendar {totalContributions weeks {contributionDays {date contributionCount weekday}}}}}}'''
def fetch():
    req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':QUERY,'variables':{'login':os.getenv('PROFILE_LOGIN','yomralioglumert')}}).encode(),headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Content-Type':'application/json','User-Agent':'OUTATIME'},method='POST')
    with urllib.request.urlopen(req,timeout=30) as response: result=json.load(response)
    if result.get('errors') or not result.get('data',{}).get('user'): raise RuntimeError('GitHub GraphQL returned no complete user data')
    return result['data']['user']
def render(user=None):
    c=user['contributionsCollection'] if user else None
    cal=c['contributionCalendar'] if c else None
    vals=[c['totalCommitContributions'],c['totalPullRequestContributions'],user['repositories']['totalCount'],cal['totalContributions']] if user else ['—']*4
    s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 310" role="img" aria-label="GitHub telemetry"><rect width="800" height="310" rx="12" fill="#080c12" stroke="#354354"/><g font-family="monospace">','<text x="24" y="28" fill="#75baff" font-size="14" letter-spacing="2">DMC-12 / TELEMETRY</text>']
    for i,(label,value) in enumerate(zip(['COMMITS','PULL REQUESTS','PUBLIC REPOS','CONTRIBUTIONS'],vals)):
        x=24+i*190
        s.append(f'<rect x="{x}" y="43" width="182" height="78" rx="5" fill="#101923" stroke="#27394e"/><text x="{x+12}" y="62" fill="#9aafc8" font-size="11">{label}</text><text x="{x+12}" y="101" fill="#75baff" font-size="30">{value}</text>')
    s.append('<text x="24" y="147" font-size="12" fill="#a9bbd0">CONTRIBUTION MATRIX / PAST YEAR</text>')
    if cal:
        weeks=cal['weeks']; step=min(14,752/max(len(weeks),1)); colors=['#17212d','#12345c','#185991','#2687cf','#75caff']
        for i,w in enumerate(weeks):
            for d in w['contributionDays']:
                n=d['contributionCount']; level=0 if n==0 else 1 if n<3 else 2 if n<6 else 3 if n<10 else 4
                s.append(f'<rect x="{24+i*step:.2f}" y="{161+d["weekday"]*15}" width="{step-2:.2f}" height="12" rx="2" fill="{colors[level]}"><title>{escape(d["date"])}: {n} contributions</title></rect>')
        footer='SYNC '+datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')+' / API-VISIBLE CONTRIBUTIONS'
    else:
        s.append('<text x="400" y="215" text-anchor="middle" fill="#9aafc8" font-size="15">AWAITING FIRST GITHUB SYNC</text>'); footer='NO LIVE DATA YET'
    s.append(f'<text x="24" y="291" fill="#9aafc8" font-size="11">{footer}</text></g></svg>')
    return '\n'.join(s)
if __name__=='__main__':
    import sys
    user=None if '--placeholder' in sys.argv else fetch()
    (ROOT/'assets/telemetry.svg').write_text(render(user),encoding='utf-8')
