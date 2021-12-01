import random
import risk_map
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""
def avoid_walls(my_head: Dict[str,int],possible_moves: List[str],gridsize: int) -> List[str]:
  for move in range(len(possible_moves)-1):
    if my_head['y'] == gridsize-1 and 'up' in possible_moves:
      possible_moves.remove('up')  
      print('----DELETED UP')
    if my_head['y'] == 0 and 'down' in possible_moves:
      possible_moves.remove('down')  
      print('----DELETED down')
    if my_head['x'] == 0 and 'left' in possible_moves:
      possible_moves.remove('left')  
      print('----DELETED left')
    if my_head['x'] == gridsize-1 and 'right' in possible_moves:
      possible_moves.remove('right')  
      print('----DELETED right')
  
  print (f'---------------------\n {possible_moves}\n')
  return possible_moves

#change to avoid snakes - create array of all snake that isnt tail and check pos in question against it
def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
  """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
  """
  my_neck = my_body[1]
  for move in possible_moves:
    if move == 'up' and my_neck["y"] > my_head["y"]:
      possible_moves.remove("up")
    elif move == 'down' and my_neck["y"] < my_head["y"]:
      possible_moves.remove("down")
    elif move == 'left' and my_neck["x"] < my_head["x"]:
      possible_moves.remove("left")
    elif move == 'right' and my_neck["x"] > my_head["x"]:
      possible_moves.remove("right")

  return possible_moves

def check_for_food(my_head: Dict[str, int],my_health: int, possible_moves: List[str],food_list: List[dict]) -> List[str]:
  #define what transforms are around the head
  transform = {'left': {'x':-1,'y':0},'right':{'x':1,'y':0},'up':{'x':0,'y':1},'down':{'x':0,'y':-1}}
  #create a dict to catch any positive hits on the food
  found_food = {'found' : False, 'direction' : ''}
  
  for move in possible_moves:
    #Check all spaces around the head using the transform offsets
    x = int(my_head['x'] + transform[move]['x'])
    y = int(my_head['y'] + transform[move]['y'])
    pos = {'x':x,'y': y}
    if pos in food_list:
      found_food['found'] = True
      print('YUM!!!!!!!')
      found_food['direction'] = move
  if my_health < 40 and found_food['found']:
    newmoves = []
    newmoves.add(move)
    return newmoves
  else:
    return possible_moves





def choose_move(data: dict) -> str:
    
    possible_moves = ["up", "down", "left", "right"]
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    #print('\n'*13)
    
    '''print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")'''
    my_risk_map = risk_map.Heatmap(data)
    
    #print(f'Safest Path : {my_risk_map.safest_path(my_head["x"],my_head["x"])}')
    #Using min() + list comprehension + values()
    # Finding min value keys in dictionary
  

    
    my_risk_map.init_enemy_snakes(data)
    my_risk_map.box_blur(1)
    my_risk_map.init_food(data)
    my_risk_map.init_my_snake(data)
    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = my_risk_map.safest_path(my_head["x"],my_head["y"])
    print(f' Possible moves: {possible_moves}')
    #possible_moves = avoid_walls(my_head, possible_moves, data["board"]["height"]) 
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    #possible_moves = check_for_food(my_head,data['you']['health'],possible_moves, data['board']['food'])
    

    if len(possible_moves) >0:
      move = random.choice(possible_moves)

   
    my_risk_map.print()
    
    print(f"MOVE {data['turn']}")
    #print(f"\n\n{data['game']['id']} MOVE {data['turn']}:\n {move} picked from all valid options in {possible_moves}\n\n")

    return move
