
'''
TO DO:
stop crashing into head and tails.
make it aware of hazards & 'the sauce'
Search for deathtraps -predict if tail will clear in time

 
'''

#risk map Module for Kims Rhinkals Battlesnake
class Riskmap:
  def __init__(self,data):
    
    self.directions = {'up':(0,1),'right': (1,0),'down': (0,-1), 'left':(-1,0)}
    self.size = data['board']['height']
    self.map = [[0 for x in range(self.size)] for x in range(self.size)]
    self.max_steps = 8
    self.threshold = 20
    self.weight_body= 50.0
    self.weight_head =150.0
    self.distance_multiplier = 2
    self.weight_food = -10
    weight=0
    is_my_snake = False


  def print(self):
    print('---------------------------------------------\n')
    for x in self.map:
      print(x)

  def average_3x3(self,x_pointer,y_pointer):
    #find average of 3x3 grid
    total = 0
    num_counted = 0
    
    for i in range(3):
      for j in range(3):
        # search a 3x3 grid centered on current pointer
        cx = x_pointer+ (i) #used to have a -1
        cy = y_pointer+ (j)  #used to have a -1
        
        #if pixel is within the origional maps limits, add it to the total.
        if (cx >=0 and cx <= self.size-1) and (cy >=0 and cy <= self.size-1):
            if i==1 and j == 1:
                total += self.map[cx][cy] #add centre pixel again so it doesnt average out as much
            total += self.map[cx][cy] 
            num_counted +=1
            
    return round(total / num_counted,1)

  
  def box_blur(self,iterations):
      temp_blurred_map = [[0 for x in range(self.size)] for x in range(self.size)]
      
      for i in range(iterations):            
        cx,cy = 0,0
        for x in self.map:
          cy = 0
          for y in x:
            temp_blurred_map[cx][cy] = self.average_3x3(cx,cy)
            cy+=1
          cx +=1
        for x in range(self.size):
          for y in range (self.size):
            self.map[x][y] = round(temp_blurred_map[x][y],1)
        
  #calc rays based on position in board space      
  def calc_lines(self, xpos, ypos,remaining_directions):
    start_xpos, start_ypos = xpos, ypos
    result = {}
    line_sum = 0
    change_direction = False
    #Remove any directions removed by other code
    '''for dir in remaining_directions:
      if dir not in self.directions:
        print(f'----REMOVING {dir}')
        self.directions.remove(dir)
    '''

    for direction in remaining_directions:

        #initiate the variables for the start of each line
        num_steps = 1
        xpos,ypos = start_xpos,start_ypos
        while not change_direction:
          #take one step down the line - added here s head is never counted.
          change_direction = False
          
          #shift one square in a direction
          xpos += self.directions[direction][0]
          ypos += self.directions[direction][1]
          
          if (((num_steps <= self.max_steps) and not ((xpos <0 or xpos > self.size-1) or (ypos < 0 or ypos > self.size-1)))) and line_sum <= self.threshold:
            #add each item to the total, but reduce the effect with distance
            '''if num_steps >2:
               line_sum += self.map[self.size -1 -ypos][xpos] / (num_steps/self.distance_multiplier)
            else:
              line_sum += self.map[self.size -1 -ypos][xpos]
            '''
            line_sum += self.map[self.size -1 -ypos][xpos] / (num_steps/self.distance_multiplier)
            num_steps +=1
          else:
            change_direction = True
            #print(f'num steps is {num_steps}')
            risk = round((line_sum / num_steps) *4,1)
                
        result.update({direction : risk})
        line_sum = 0
        num_steps = 1
        change_direction = False    
        
    #print(f'result : {result}')        
    return result

  def init_enemy_snakes(self,data):
    for snake in data['board']['snakes']:
          
      #check if its my snake and if not assign weighting
      #my_id = snake['id'] if snake['id'] == data['you']['id']
      for segment in snake['body']:
        if snake['id'] != data['you']['id']:
          self.map[(self.size-1) - segment['y']][segment['x']] = self.weight_body
    
    self.box_blur(1) #spread the risk
    #then re-instate the enemy snakes possible next turn head positions
    
    for snake in data['board']['snakes']:          
      if snake['id'] != data['you']['id']:
        for segment in snake['body']:
          self.map[(self.size-1) - segment['y']][segment['x']] = self.weight_body
        '''for dir in self.directions:
          self.map[self.size-1 - snake['head']['y'] + self.directions[dir][1]][snake['head']['x']+ self.directions[dir][0]] = self.weight_head '''
        

    

          
  def init_my_snake(self,data):
    for segment in data['you']['body']:
      self.map[(self.size-1) - segment['y']][segment['x']] = self.weight_body
  
  def init_food(self,data):
    self.weight_food = round(-10+(data['you']['health']/10),1)*2 #food attracts more as hunger strikes
    
    for segment in data['board']['food']:
      self.map[(self.size-1) - segment['y']][segment['x']] += round(self.weight_food,1)
  
  def check_for_deathtraps(data): 
    pass
    #Check if the head has arrived on a wall
    #Check if any other part of the snake is against a wall
    #v1 - if its enclosed, send the other way
    #v2 -check for food and see if path will be clear by the time head gets there


  def safest_path(self,xpos,ypos,directions):
    
    #detect safest direction by returning lowest risk value
    risk_dict = self.calc_lines(xpos,ypos,directions)
    if len(risk_dict) >0:
      temp = min(risk_dict.values())
      result = [key for key in risk_dict if risk_dict[key] == temp]
    else:
      result = "down"

    return result
          
 
  


