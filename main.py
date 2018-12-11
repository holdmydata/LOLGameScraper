import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
from tkinter import ttk


#####GAMESCRAPER Analytical App#####

#####PANDAS WORK#####
file = 'gamelist.csv'
df = pd.read_csv(file, header=0)
df.columns = ['GameResult', 'GameType', 'GameLength', 'GameChamp', 'GameKill', 'GameDeath', 'GameAssist']
df1 = df[['GameChamp','GameKill','GameDeath','GameAssist']].groupby('GameChamp').mean()
df2 = df[['GameKill','GameDeath']]
df3 = df[['GameKill','GameDeath','GameAssist']]

#Design
SMALL_FONT = ("Calibri", 12)
LARGE_FONT = ("Arial", 16)

# Background Frame Setup
class GameScraperapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        #Add Icon
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "GameScraper")
        tk.Tk.wm_geometry(self,"1920x1080")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        username = ""
        self.frames = {}
        for Frames in (StartPage, RegChart, ScatterChart, ChampKillBar):
            frame = Frames(container, self)
            self.frames[Frames] = frame
            frame.grid(row=0, column = 0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, background='white')
        titlelabel = tk.Label(self, text="GameScraper", font=LARGE_FONT)
        titlelabel.pack(pady=10, padx=10)

     #Buttons

        button1 = ttk.Button(self, text="KDA Trends",
                            command=lambda: controller.show_frame(RegChart))
        button1.pack(pady=10, padx=10)
        button2 = ttk.Button(self, text="KDA Scatter",
                            command=lambda: controller.show_frame(ScatterChart))
        button2.pack(pady=10, padx=10)
        button3 = ttk.Button(self, text="Champ Stats",
                            command=lambda: controller.show_frame(ChampKillBar))
        button3.pack(pady=10, padx=10)

# Trend Line Charts for Recent History
class RegChart(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="KDA Trends", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="KDA Scatter",
                            command=lambda: controller.show_frame(ScatterChart))
        button2.pack()
        button3 = ttk.Button(self, text="Champ Stats",
                            command=lambda: controller.show_frame(ChampKillBar))
        button3.pack()
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        df3.plot(kind='line', ax=ax1)
        ax1.set_title('Avg Kills per Champion')

#Scatter Plot - Need: Regression Analysis (May Convert to Seaborn App)
class ScatterChart(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="KDA Scatter", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="KDA Trends",
                            command=lambda: controller.show_frame(RegChart))
        button2.pack()
        button3 = ttk.Button(self, text="Champ Stats",
                            command=lambda: controller.show_frame(ChampKillBar))
        button3.pack()
        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        df2.plot(kind='scatter', legend=True, x='GameKill', y='GameDeath', ax=ax1, color=["b","darkorange"], )
        ax1.legend()
        ax1.set_title('KDA Scatter')

#KDA Bar Chart for recent Champions Played - Want: Build in Sorting button for sorting K/D/A
class ChampKillBar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Avg Champ Kills", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="KDA Scatter",
                            command=lambda: controller.show_frame(ScatterChart))
        button2.pack()
        button3 = ttk.Button(self, text="KDA Trends",
                            command=lambda: controller.show_frame(RegChart))
        button3.pack()

        figure1 = plt.Figure(figsize=(5,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        df1.plot(kind='bar', ax=ax1)
        ax1.set_title('Champ Stats')
        canvas.show()
        toolbar = NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = GameScraperapp()
app.mainloop()


##SEABORN WORK FOR FUTURE REFERENCE##

#Pairs Regression
# def pairplot():
#     sns.pairplot(df, x_vars=["GameKill",'GameAssist'], y_vars='GameDeath', height=7, aspect=0.7, kind='reg')
#     plt.show()

#Regression
# def lmplot():
#     sns.lmplot(x='GameKill',y='GameDeath',data=df)
#     plt.show()

#Histogram
# def histogram():
#     sns.distplot(df[df.columns[4]])
#     plt.show()

#Bar Chart
# def barchart():
#     sns.barplot(x="GameChamp",y="GameDeath", data=df)
#     plt.show()

#Base Stats
# def basestats():
#     print("Average kills per game = "+ str(df['GameKill'].mean()))
#     print("Average deaths per game = " + str(df['GameDeath'].mean()))
#     print("Average assists per game = " + str(df['GameAssist'].mean()))
#     print("Most played champions = " + str(df['GameChamp'].value_counts().index[:3].tolist()))
######################