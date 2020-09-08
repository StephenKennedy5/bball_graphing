'''Graph any player in the nba from the 2019-2020 season'''
import pandas as pd
from matplotlib import pyplot as plt
import json
import PySimpleGUI as sg
import sys

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
    point_colors = ['G','FG%']
    radius = ['FGA','FG%','PTS','+/-']

    layout = [
        [sg.Text('What categories you want to compare?',
                justification ='center',pad=((10,0),0),font=(16))],
        [sg.InputText('Enter Title of Graph Here',key='-title-',justification='center')],
        [sg.Text('Enter X-axis and Y-axis values',justification ='center',font=(14))],
            [sg.InputCombo(category, size=(20, 1),tooltip='x-axis', key='-x-axis-',default_value='PTS'),
            sg.InputCombo(category, size=(20,1),tooltip='y-axis', key='-y-axis-',default_value='FG%')],

        [sg.Text('Games Played Sliders',justification ='center')],
        [sg.Slider(range=(1,df['G'].max()),orientation='h',
                size=(34,20),default_value =1, key='-games-min-')],
        [sg.Slider(range=(1,df['G'].max()),orientation='h',
                size=(34,20),default_value =df['G'].max(), key='-games-max-')],


        [sg.Text('How do you want to compare points to each other'),
            sg.InputCombo(point_colors, key= '-point-color-',size=(20,1),tooltip='Compare point colors',default_value='G')],
        [sg.Text('What stat to compare size of points'),
            sg.InputCombo(radius, key= '-radius-',size=(20,1),tooltip='Radius of circles',default_value='FGA')],

        [sg.Text('What color scheme to use for the graph:'),
            sg.InputCombo(colors, size=(20, 1),tooltip='color of graph', key='-colors-',default_value='Greys')],
        [sg.Text('What style of graph you want to use:'),
            sg.InputCombo(graph_styles,size=(30,1),key='-graph_styles-',default_value='classic')],
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
                point_color = values['-point-color-']
                rad = values['-radius-']
                break

    window.close()

    df = df[df['G'].between(games_min,games_max)]

    return df,inputx,inputy,COLOR,Title,graph_style,point_color,rad

'''Creates graph'''
def make_graph(df,inputx,inputy,COLOR,Title,graph_style,point_color,rad):
    df.reset_index(inplace=True)

    x = df[[inputx]]
    y = df[[inputy]]
    c = df[point_color]

    x.set_index(inputx,drop=True,inplace=True)
    y.set_index(inputy,drop=True,inplace=True)

    norm = plt.Normalize(1,4)
    cmap = plt.cm.Pastel1

    plt.style.use(graph_style)

    fig,ax = plt.subplots()

    sc = plt.scatter(x.index,y.index,c=c, cmap=COLOR,edgecolor='black',
                linewidth=1,alpha=0.6,s=df[rad]*20)

    ax.set_title(Title)
    ax.set_xlabel(inputx)
    ax.set_ylabel(inputy)
    ax.set_xlim(0,(df[inputx].max())*(1.1))
    ax.set_ylim(0,(df[inputy].max())*(1.1))
    cbar= plt.colorbar()
    cbar.set_label(point_color)
    plt.tight_layout()

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}, {}".format(" ".join(list(map(str,ind["ind"]+1))),
                               " ".join([df['Opp'][n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.8)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.show()

def master():
    layout = [
            [sg.Button('Choose player')],
            [sg.Button('Exit program')]
    ]

    window = sg.Window('Lets make some graphs?',layout)

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit program':
            sys.exit()
        if event == 'Choose player':
            window.close()
            team, data = choose_team()
            player = choose_player(team,data)
            df = get_stats(data,team,player)
            df,inputx,inputy,COLOR,Title,graph_style,point_color,rad = choose_stats(df)
            make_graph(df,inputx,inputy,COLOR,Title,graph_style,point_color,rad)
            master()

    window.close()

master()
