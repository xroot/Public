import re
import xml.etree.ElementTree as ET


def m3u_ids(m3u_path):
    ids = set()
    with open(m3u_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith('#EXTINF'):
                m = re.search(r'tvg-id="([^"]+)"', line)
                if m:
                    ids.add(m.group(1))
    return ids


def epg_channels(epg_path):
    channels = set()
    tree = ET.parse(epg_path)
    root = tree.getroot()
    for prog in root.findall('programme'):
        channel = prog.get('channel')
        if channel:
            channels.add(channel)
    return channels


if __name__ == "__main__":
    m3u_file = input("Chemin du fichier M3U : ").strip()
    epg_file = input("Chemin du fichier EPG XML : ").strip()
    m3u = m3u_ids(m3u_file)
    epg = epg_channels(epg_file)
    print(f"\nM3U tvg-id ({len(m3u)}) :")
    print(sorted(m3u))
    print(f"\nEPG channel ({len(epg)}) :")
    print(sorted(epg))
    manquants = m3u - epg
    if manquants:
        print(f"\nATTENTION : {len(manquants)} chaînes M3U sans EPG correspondant :")
        print(manquants)
    else:
        print("\nTous les tvg-id M3U sont présents dans l'EPG.")
