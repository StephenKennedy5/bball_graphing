'''Graph any player in the nba from the 2019-2020 season'''
import pandas as pd
from matplotlib import pyplot as plt
import json
import PySimpleGUI as sg

'''Choose team you want to select player from'''
def choose_team():
    with open('player_stats.json') as f:
      data = json.load(f)
    team_names = list(data.keys())

    choices = team_names

    layout = [  [sg.Text('What team you want to graph?')],
            [sg.Listbox(choices, size=(15, len(choices)), key='_team_')],
            [sg.Button('Ok')]  ]

    window = sg.Window('Pick a team', layout)

    while True:                  # the event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Ok':
            if values['_team_']:    # if something is highlighted in the list
                team = str(values['_team_']).strip('[]')[1:-1]
                break

    window.close()

    f.close()
    return team, data

'''Choose player of choice from team'''
def choose_player(team, data):
    choices = list(data[team].keys())

    layout =[
              [sg.Text('What player you want to graph?')],
              [sg.Listbox(choices, size=(25, len(choices)), key='_player_')],
              [sg.Button('Submit')]
            ]

    window = sg.Window('Pick a player', layout)

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Submit':
            if values['_player_']:
                player = str(values['_player_']).strip('[]')[1:-1]
                break

    window.close()

    return player

'''Returns data frame from bball ref of player stats'''
def get_stats(data, team, player):
    df = pd.read_html(data[team][player],skiprows=(21,42,63),
            na_values =['Inactive','Did Not Play', 'Did Not Dress'])[-1]

    return df

'''Chooose what stats you want to graph'''
def choose_stats(df):
    category= ['PTS','FG%','AST','TRB','G','MP','FG','FGA','3P','3PA','FT','FTA','FT%','ORB',
                    'DRB','STL','BLK','TOV','PF','GmSc','+/-']
    colors = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']
    graph_styles = ['classic','Solarize_Light2','dark_background','fast','bmh',
                    'fivethirtyeight','ggplot','seaborn','seaborn-bright','seaborn-darkgrid']

    layout = [
        [sg.Text('What categories you want to compare?',size=(30,1),
                justification ='center',pad=((10,0),0))],
        [sg.InputText('Enter Title of Graph Here',key='-title-',justification='center')],
        [sg.InputCombo(category, size=(20, 1),tooltip='x-axis', key='-x-axis-',default_value='PTS'),
            sg.InputCombo(category, size=(20,1),tooltip='y-axis', key='-y-axis-',default_value='FG%')],
        [sg.Slider(range=(1,df['G'].max()),orientation='h',
                    size=(34,20),default_value =1, key='-games-min-')],
        [sg.Slider(range=(1,df['G'].max()),orientation='h',
                    size=(34,20),default_value =df['G'].max(), key='-games-max-')],
        [sg.InputCombo(colors, size=(20, 1),tooltip='color of graph', key='-colors-',default_value='Greys')],
        [sg.Listbox(graph_styles,size=(30,3),key='-graph_styles-')],
        [sg.Button('Submit')]
            ]

    window = sg.Window('Customize your graph', layout)

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
                games_min = values['-games-min-']
                games_max = values['-games-max-']
                break

    window.close()

    df = df[df['G'].between(games_min,games_max)]

    return df,inputx,inputy,COLOR,Title,graph_style

'''Creates graph'''
def make_graph(df,inputx,inputy,COLOR,Title,graph_style):
    plt.style.use(graph_style)
    plt.scatter(df[inputx],df[inputy], c=df['G'], cmap=COLOR, edgecolor='black',
            linewidth=1, alpha= 0.6, s=df['FGA']*20)
    plt.title(Title)
    plt.xlabel(inputx)
    plt.ylabel(inputy)
    plt.xlim(0,(df[inputx].max())*(1.1))
    plt.ylim(0,(df[inputy].max())*(1.1))
    cbar = plt.colorbar()
    cbar.set_label('Games Played')
    plt.tight_layout()
    plt.show()


team, data = choose_team()
player = choose_player(team,data)
df = get_stats(data,team,player)
df,inputx,inputy,COLOR,Title,graph_style = choose_stats(df)
make_graph(df,inputx,inputy,COLOR,Title,graph_style)
