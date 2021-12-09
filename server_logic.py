import random
import risk_map
from typing import List, Dict
print_info = True


#avoid other snakes is going haywire!!!


def avoid_walls(my_head: Dict[str,int],possible_moves: List[str],gridsize: int) -> List[str]:
  for move in range(len(possible_moves)-1):
    if my_head['y'] == gridsize-1 and 'up' in possible_moves:
      possible_moves.remove('up')  
    if my_head['y'] == 0 and 'down' in possible_moves:
      possible_moves.remove('down')  
    if my_head['x'] == 0 and 'left' in possible_moves:
      possible_moves.remove('left')  
    if my_head['x'] == gridsize-1 and 'right' in possible_moves:
      possible_moves.remove('right')  

  return possible_moves

#change to avoid snakes - create array of all snake that isnt tail and check pos in question against it
def avoid_all_snakes(data, possible_moves: List[str]) -> List[str]:
  directions = {'up':(0,1),'right': (1,0),'down': (0,-1), 'left':(-1,0)}
  moves = possible_moves.copy()
  next_heads = []

  for dir in possible_moves:
    #print(f"checking {dir} out of {possible_moves}")
    temp_x = data['you']['head']['x'] + directions[dir][0]
    temp_y = data['you']['head']['y'] + directions[dir][1]

    #print(f"Current head { data['you']['head']['x']}, {data['you']['head']['y']} and current offset is {temp_x},{temp_y} for {dir}")
    for snake in data['board']['snakes']:
      if snake['id'] != data['you']['id']:
        #print(f" Snake {snake['name']} is not me")
        for dir in directions:
          next_heads.append((snake['body'][0]['x']+directions[dir][0],snake['body'][0]['y']+directions[dir][1]))
          #print(f"{snake['name'][0]} {snake['body']}")
          # print(f'{next_heads} is next heads')
          #iterate through the body but not the tail
      
      for i,segment in enumerate(snake['body']):
        #print(f"{segment} is {i} " )
        if (i <= len(snake['body'])-1) and (temp_x == segment['x'] and temp_y == segment['y']): 
          # or ((temp_x,temp_y) in next_heads)): 
          if dir in possible_moves:
            if print_info: 
              print(f"Removed {dir} to avoid snake {snake['name']}")
            possible_moves.remove(dir)
            
   
    possible_moves = moves
  return possible_moves

def direction_of(here, there):
  dirs = []
  if here[0] < there[0]:
    dirs.append('right')
  elif here[0] > there[0]:
    dirs.append('left')
  
  if here[1] < there[1]:
    dirs.append('up')
  elif here[1] > there[1]:
    dirs.append('down')

  return dirs #return a list of all the directions between the two coordinates

def is_against_wall(my_head,size):
  #check if segment position is against a wall
  is_head_against_a_wall = (my_head['x'] <= 0 or my_head['x'] >= size or my_head['y'] <= 0 or my_head['y'] >= size) 
  return is_head_against_a_wall

def avoid_deathtraps(my_head,data,possible_directions):
  size = size = data['board']['height']-1
  if is_against_wall(my_head,size) and not is_against_wall(data['you']['body'][1],size) :
    for i in range(len(data['you']['body'])-1):
      if is_against_wall(data['you']['body'][i],size) and i>0:
        head_tup = (data['you']['head']['x'],data['you']['head']['y'])
        touch_tup = (data['you']['body'][i]['x'],data['you']['body'][i]['y'])
        danger_dirs = direction_of(head_tup,touch_tup)
        print(f'DEATHTRAP RISK DETECTED! - {danger_dirs}')
        for dir in danger_dirs:
          if dir in possible_directions:
            print(f'Removed {dir} as this was a deathtrap.')
            possible_directions.remove(dir)
        return possible_directions
  return possible_directions
        

def choose_move(data: dict) -> str:
    
    possible_moves = ["up", "down", "left", "right"]
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
   
    my_risk_map = risk_map.Riskmap(data)
    my_risk_map.init_enemy_snakes(data)
    my_risk_map.init_my_snake(data)
    my_risk_map.init_hazards(data)
    my_risk_map.init_food(data)
    
    possible_moves = avoid_walls(my_head,possible_moves,my_risk_map.size)
    print('\n')
    
    if print_info:
      print(f"MOVE {data['turn']}")
    
      print(f'Possible moves after only wall avoidance {possible_moves}')
    
    #possible_moves = avoid_all_snakes(data, possible_moves)
    
    if print_info :
      print(f'Possible moves before risk mapping - before deathtraps {possible_moves}')
    
    # Deal with the really stupid death scenarios that confuse the riskmap setup
    possible_moves = avoid_deathtraps(my_head,data,possible_moves)
    #then choose from the remaining paths

    if print_info :
      print(f'Possible moves before risk mapping - after deathtraps {possible_moves}')

    possible_moves = my_risk_map.safest_path(my_head["x"],my_head["y"],possible_moves)
    
    if print_info :
      print(f'Possible moves after: {possible_moves}')


    if len(possible_moves) >0:
      move = random.choice(possible_moves)
    else:
      move = 'down' # No options left... snakies going down!!!

   
    if print_info:
      my_risk_map.print()
    
    
    #print(f"\n\n{data['game']['id']} MOVE {data['turn']}:\n {move} picked from all valid options in {possible_moves}\n\n")

    return move
