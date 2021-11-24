def frameTranslator(frames: dict, gameId: str, snakeName: str) -> dict:

  # print(frames["Frames"][0])

  frame = frames["Frames"][0]

  snakes = []
  you = {}

  for snake in frame["Snakes"]:
    if snake["Name"] == snakeName:
      # print("I found snake "+snakeName)
      you = translateSnake(snake)
    else:
      if snake["Death"] == None:
        snakes.append(snake)

  snakes.insert(0, you);

  food = []
  hazards = []

  for foodElt in frame["Food"]:
    food.append({'x': foodElt["X"], 'y': foodElt["Y"]})
  for hazardElt in frame["Hazards"]:
    hazards.append({'x': hazardElt["X"], 'y': hazardElt["Y"]})
  

  game = {
    'game': {
      'id': gameId,
      'ruleset': {
        'name': "standard",
        'version': "v.1.2.3",
      },
      'timeout': 500,
    },
    'turn': frame["Turn"],
    'board': {
      'height': 11,
      'width': 11,
      'food': food,
      'snakes': snakes,
      'hazards': hazards,
    },
    'you': you,
  }

  return game


def translateSnake(frame: dict) -> dict :

  body = []
    
  for bodyElt in frame["Body"]:
    body.append({'x': bodyElt["X"], 'y': bodyElt["Y"]})

  snake = {
      'id': frame["ID"],
      'name': frame["Name"],
      'health': frame["Health"],
      'body': body,
      'latency': "0",
      'head': body[0],
      'length': 0,
      'shout': "",
      'squad': "",
    }

  return snake
