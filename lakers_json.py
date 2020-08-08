import json

'''Add or remove player to dictionary then run to update json for player
stats that will be scraped in laker_ind_stats'''

Players = {
  'KCP':'https://www.basketball-reference.com/players/c/caldwke01/gamelog/2020/', #Kentavious Caldwell-Pope
  'DW':'https://www.basketball-reference.com/players/h/howardw01/gamelog/2020/', #Dwight Howard
  'DG': 'https://www.basketball-reference.com/players/g/greenda02/gamelog/2020/', #Danny Green
  'JM': 'https://www.basketball-reference.com/players/m/mcgeeja01/gamelog/2020/', #JaVale McGee
  'LBJ': 'https://www.basketball-reference.com/players/j/jamesle01/gamelog/2020/', #Lebron James
  'AC': 'https://www.basketball-reference.com/players/c/carusal01/gamelog/2020/', #Alex Caruso
  'AD': 'https://www.basketball-reference.com/players/d/davisan02/gamelog/2020/', #Anthony Davis
  'KK': 'https://www.basketball-reference.com/players/k/kuzmaky01/gamelog/2020/', #Kyle Kuzma
  'AB': 'https://www.basketball-reference.com/players/b/bradlav01/gamelog/2020/', #Avery bradley
  'RR': 'https://www.basketball-reference.com/players/r/rondora01/gamelog/2020/', #Rajon Rondo
  'JD': 'https://www.basketball-reference.com/players/d/dudleja01/gamelog/2020/', #Jared Dudley
  'DIW': 'https://www.basketball-reference.com/players/w/waitedi01/gamelog/2020/', #Dion Waiters
  'JR': 'https://www.basketball-reference.com/players/s/smithjr01/gamelog/2020/'  #JR Smith
}

j = json.dumps(Players, indent=4)
with open('laker_players.json', 'w') as f:
    f.write(j)
    f.close()
