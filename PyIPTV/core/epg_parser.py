import xml.etree.ElementTree as ET
from datetime import datetime

def parse_epg(filename):
    """
    Parse un fichier EPG au format XMLTV.
    Retourne {tvg_id: [ {'start':..., 'stop':..., 'title':...}, ... ]}
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    progs = {}
    for prog in root.findall('programme'):
        channel = prog.get('channel')
        start = prog.get('start')
        stop = prog.get('stop')
        title_elem = prog.find('title')
        title = title_elem.text if title_elem is not None else ''
        # Formatage lisible
        try:
            start_fmt = datetime.strptime(start[:12], "%Y%m%d%H%M")
            stop_fmt = datetime.strptime(stop[:12], "%Y%m%d%H%M")
            start_str = start_fmt.strftime("%d/%m %H:%M")
            stop_str = stop_fmt.strftime("%H:%M")
        except Exception:
            start_str = start
            stop_str = stop
        item = {'start': start_str, 'stop': stop_str, 'title': title}
        progs.setdefault(channel, []).append(item)
    return progs