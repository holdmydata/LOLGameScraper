###LEAGUE OF LEGENDS OP.GG SCRAPER - CODY COX ###

from bs4 import BeautifulSoup as bs
from selenium import webdriver as driver
import tkinter as tk
from tkinter import ttk

#Input User

SMALL_FONT = ("Calibri", 12)
LARGE_FONT = ("Arial", 16)

#Login tkinter page
root = tk.Tk()
root.geometry("300x100")
user = None
root.wm_title("GameScraper")
#Button click, closes Login window and runs GameScraper for CSV
def loginbtnclick():
    global user
    user = str(userInput.get("1.0","end-1c"))
    print(user)
    root.destroy()

userInput = tk.Text(root, height=1, width=10)
userInput.pack()

button1 = ttk.Button(root, text="Login",command=lambda: loginbtnclick())
button1.pack()
print(user)
root.mainloop()

#File Name/ Site Variables

username = user.replace(" ", "%20")
print(username)
filename = "gamelist.csv"
site = 'http://na.op.gg/summoner/userName=' + username
print(site)

#Grab Page
ffdriver = driver.Chrome(r"chromedriver.exe")
ffdriver.get(site)

#Iterate over webpage to retrieve up to 100 games
x = 0
while x < 5:
    try:
        ffdriver.find_element_by_link_text("Show More").click()
        ffdriver.implicitly_wait(10)
    except:
        break
    x + 1
#HTML Parsing
page_bs = bs(ffdriver.page_source, "html.parser")

#Grab Game List
GameListContainer = page_bs.findAll("div", {"class":"GameItemList"})
containers = page_bs.findAll("div", {"class":"GameItemWrap"})

#Open/Write CSV
f = open(filename, "w")
headers = "Game_Result, Game_Type, Game_Length, Champ_Played, Kills, Deaths, Assists\n"
f.write(headers)
# Find Results in Containers Loop
for container in containers:
    #Game Results
    GameResults = container.findAll("div", {"class":"GameResult"})
    GameResult = GameResults[0].text.strip()

    #Game Type
    GameTypes = container.findAll("div", {"class":"GameType"})
    GameType = GameTypes[0].text.strip()

    #Time Played
    GameLengths = container.findAll("div", {"class":"GameLength"})
    GameLength = GameLengths[0].text.strip()
    #Champion Played
    GameChamps = container.findAll("div", {"class":"ChampionName"})
    GameChamp = GameChamps[0].text.strip()
    # Kills
    GameKills = container.findAll("span", {"class": "Kill"})
    GameKill = GameKills[0].text.strip()
    # Deaths
    GameDeaths = container.findAll("span", {"class": "Death"})
    GameDeath = GameDeaths[0].text.strip()
    # Assists
    GameAssists = container.findAll("span", {"class": "Assist"})
    GameAssist = GameAssists[0].text.strip()
    #Write to CSV
    f.write(GameResult + "," + GameType + "," + GameLength + "," + GameChamp + "," + GameKill + "," +
            GameDeath + "," + GameAssist + "\n")

f.close()
print("File created called " + filename)
ffdriver.close()

exec(open('main.py').read())

