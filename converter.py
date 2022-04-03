import xml.etree.ElementTree as ET
import sys
from datetime import datetime


def convertDate(date):
  if date:
    date_obj = datetime.strptime(date, "%Y%m%dT%H%M%S")
    return str(date_obj.date())
  else:
    return date


def convertRating(rating):
  if rating:
    return str(int(float(rating)*100))+"%"
  else:
    return rating


class Game:
  def __init__(self, xml):
 
    self.args = {}
    self.files = []
    self.game = xml.findtext("name")
    self.args["publisher"] = xml.findtext("publisher")
    self.args["developer"] = xml.findtext("developer")
    self.args["genre"] = xml.findtext("genre")
    self.args["description"] = xml.findtext("desc").replace("\n\n","\n.\n").replace("\n", "\n\t")
    self.args["players"] = xml.findtext("players")
    self.args["release"] = convertDate(xml.findtext("releasedate"))
    self.args["rating"] = convertRating(xml.findtext("rating"))
    self.args["assets.banner"] = xml.findtext("marquee")
    self.args["assets.screenshot"] = xml.findtext("image")
    try:
      self.args["assets.logo"] = self.args["assets.screenshot"].replace("screenshots", "wheels")
    except:
      pass
    try:
      self.args["assets.boxFront"] = self.args["assets.screenshot"].replace("screenshots", "covers")
    except:
      pass

  def print(self):
    if self.game: 
      print("game: " + self.game)
    print("files: " + self.files.pop(0))
    for file in self.files:
      print("\t" + file)
    for arg, val in self.args.items():
      if val:
        print(arg + ": " + val)
  

def convertToTxt(xmlfile, outputfile):

  with open(outputfile, "w") as f:
    stdout = sys.stdout
    sys.stdout = f

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    game_objs = {}

    for game in root.findall('game'):
      name = game.findtext("name")
      path = game.findtext("path")
      game_objs.setdefault(name, Game(game)).files.append(path)
  
    for game in game_objs.values():
      print()
      game.print()

    sys.stdout = stdout
      

