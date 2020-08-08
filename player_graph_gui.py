import pandas as pd
from matplotlib import pyplot as plt
import json
import PySimpleGUI as sg
import numpy as np

def choose_player():
    with open('player_names.json') as f:
      data = json.load(f)
    laker_key = list(data.keys())
    laker_names = list(data.values())
    choices = laker_names

    layout = [  [sg.Text('What player you want to graph?')],
            [sg.Listbox(choices, size=(15, len(choices)), key='_players_')],
            [sg.Button('Ok')]  ]

    window = sg.Window('Pick a player', layout)

    while True:                  # the event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Ok':
            if values['_players_']:    # if something is highlighted in the list
                val = values['_players_']
                break

    window.close()

    val = str(val).strip('[]')
    for keys,value in data.items():
        if val[1:-1] == value:
            filename = keys+'_data.csv'
    return filename,val
    f.close()

def read_data(filename):
    df = pd.read_csv(filename, encoding= 'unicode_escape',
    na_values=['Inactive','Did Not Play', 'Did Not Dress'],index_col=False)
    games = df['G']
    attempts = df['FGA']
    return df,games,attempts

def choose_categories(df):

    choices = ['PTS','FG%','AST','TRB','G','MP','FG','FGA','3P','3PA','FT','FTA','FT%','ORB',
                    'DRB','STL','BLK','TOV','PF','GmSc','+/-']
    colors = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
    graph_styles = ['classic','Solarize_Light2','dark_background','fast','bmh',
                    'fivethirtyeight','ggplot','seaborn','seaborn-bright','seaborn-darkgrid']


    layout = [  [sg.Text('What categories you want to compare?',size=(30,1),
                    justification ='center',pad=((10,0),0))],
            [sg.InputText('Enter Title of Graph Here',key='-title-',justification='center')],
            [sg.InputCombo(choices, size=(20, 1),tooltip='x-axis', key='-x-axis-'),
                sg.InputCombo(choices, size=(20,1),tooltip='y-axis', key='-y-axis-')],
            [sg.InputCombo(colors, size=(20, 1),tooltip='color of graph', key='-colors-')],
            [sg.Listbox(graph_styles,size=(30,3),key='-graph_styles-')],
            [sg.Button('Submit')]  ]

    window = sg.Window('Pick a category', layout)

    while True:                  # the event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Submit':
            if values['-x-axis-'] and values['-y-axis-'] and values['-title-'] and values['-graph_styles-']:    # if something is highlighted in the list
                inputx = values['-x-axis-']
                inputy = values['-y-axis-']
                COLOR = values['-colors-']
                Title = values['-title-']
                graph_style = values['-graph_styles-']
                break

    window.close()
    return inputx, inputy, COLOR, Title, graph_style

def make_graph(df,inputx,inputy,val,COLOR,Title,graph_style):
    plt.style.use(graph_style)
    plt.scatter(df[inputx],df[inputy], c=games, cmap=COLOR, edgecolor='black',
            linewidth=1, alpha= 0.6, s=attempts*20)
    plt.title(Title)
    plt.xlabel(inputx)
    plt.ylabel(inputy)
    plt.xlim(0,(df[inputx].max())*(1.1))
    plt.ylim(0,(df[inputy].max())*(1.1))
    cbar = plt.colorbar()
    cbar.set_label('Games Played')
    plt.tight_layout()
    plt.show()


filename,val = choose_player()
df,games,attempts = read_data(filename)
inputx,inputy,COLOR,Title,graph_style = choose_categories(df)
make_graph(df,inputx,inputy,val,COLOR,Title,graph_style)
