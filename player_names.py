import json

'''Add or remove player to dictionary then run to update json for names
for player graph script'''

Players = {
  'KCP': 'Kentavious Caldwell-Pope',
  'DW': 'Dwight Howard',
  'DG': 'Danny Green',
  'JM': 'JaVale McGee',
  'LBJ': 'Lebron James',
  'AC': 'Alex Caruso',
  'AD': 'Anthony Davis',
  'KK': 'Kyle Kuzma',
  'AB': 'Avery bradley',
  'RR': 'Rajon Rondo',
  'JD': 'Jared Dudley',
  'DIW': 'Dion Waiters',
  'JR': 'JR Smith'
}

j = json.dumps(Players, indent=4)
with open('player_names.json', 'w') as f:
    f.write(j)
    f.close()
