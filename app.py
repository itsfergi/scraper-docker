from flask import Flask
import subprocess
import os
import converter
import threading

app = Flask(__name__)

platforms = ['3do', '3ds', 'amiga',
    'amigacd32', 'amstradcpc', 'apple2', 'arcade',
    'arcadia', 'astrocde', 'atari800', 'atari2600',
    'atari5200', 'atari7800', 'atarijaguar',
    'atarijaguarcd', 'atarilynx', 'atarist',
    'atomiswave', 'c16', 'c64', 'c128', 'channelf',
    'coco', 'coleco', 'daphne', 'dragon32',
    'dreamcast', 'easyrpg', 'fba', 'fds',
    'gameandwatch', 'gamegear', 'gb', 'gba', 'gbc',
    'gc', 'genesis', 'intellivision', 'mame-advmame',
    'mame-libretro', 'mame-mame4all', 'mastersystem',
    'megacd', 'megadrive', 'moto', 'msx', 'msx2',
    'n64', 'naomi', 'nds', 'neogeo', 'neogeocd',
    'nes', 'ngp', 'ngpc', 'openbor', 'oric', 'pc',
    'pc88', 'pc98', 'pcfx', 'pcengine', 'pcenginecd',
    'pokemini', 'ports', 'ps2', 'psp', 'psx',
    'saturn', 'scummvm', 'sega32x', 'segacd',
    'sg-1000', 'snes', 'steam', 'switch', 'ti99',
    'trs-80', 'vectrex', 'vic20', 'videopac',
    'virtualboy', 'wii', 'wiiu', 'wonderswan',
    'wonderswancolor', 'x68000', 'x1', 'zmachine',
    'zx81', 'zxspectrum']


@app.get("/update")
def updateall():
    output = {}
    threads=[]
    for platform in platforms:
        threads.append(threading.Thread(target=update_multithread, args=(platform, output )))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    return output

def update_multithread(platform, output):
    output[platform] = update(platform)

@app.get("/update/<platform>")
def update(platform):
    if(getmedia(platform) == 0):
        updategamelist(platform)
        createSetups(platform)
        return {platform : " media + gamlist was updated"}
    return {platform : " folder does not exitst"}
    
def getmedia(platform):
    return subprocess.run(["Skyscraper", "-p", platform, "-s", "screenscraper"]).returncode
    
def updategamelist(platform):
    return subprocess.run(["Skyscraper", "-p", platform]).returncode
    
def getXmlFile(platform):
    return f"/roms/{platform}/gamelist.xml"

def getOutPutFile(platform):
    return f"/tmp/{platform}.tmp"
    
def getAllConfigs(platform):
    result = []
    for root, dirs, files in os.walk("/roms/.metadata/"):
        if f"{platform}.conf" in files:
            result.append((root, os.path.join(root, f"{platform}.conf")))
    return result
        
def concatOutputfileAndConfigs(platform):
    gamefile = getOutPutFile(platform)
    for root, conf in getAllConfigs(platform):
        with open(conf, "r") as f:
            conf_data = f.read()
        with open(gamefile, "r") as f:
            game_data = "\n" + f.read()
        path = conf_data.split("dir: ")[1].split("\n")[0]
        game_data = game_data.replace("/roms/"+ platform, path)
        with open(os.path.join(root, f"{platform}.metadata.txt"), "w") as f:
            f.write(conf_data + game_data)
            
def createSetups(platform):
    converter.convertToTxt(xmlfile=getXmlFile(platform), outputfile=getOutPutFile(platform))
    concatOutputfileAndConfigs(platform)

    
