#TO DO:
'''
implement enemies -blur- enemies - me
implement head weighting
Implement reduction of risk with distance (risk multiplier)
MAke heatmap and foodmap a subclass of 'map'
Implement love of food (without see-through snakes)
make it aware of hazards
Search for closing volumes and fill with risk.
 
'''


#Heatmap Module for Kims Heatmap driven Battlesnake
class Heatmap:
  def __init__(self,data):
    #print(data)
    self.directions = {'up':(0,1),'right': (1,0),'down': (0,-1), 'left':(-1,0)}
    self.size = data['board']['height']
    self.map = [[0 for x in range(self.size)] for x in range(self.size)]
    self.max_steps = 10
    self.threshold = 20
    self.weight_body=20
    self.weight_head =30
    #print(data)
    weight=0
    is_my_snake = False

    # TO-DO - FIGURE OUT WHY THE HEATMAP IS NOT BEING GENERATED PROPERLY
    #for some reason the snake isnt getting onto the heatmap
    for snake in data['board']['snakes']:
        
      #check if its my snake and if not assign weighting
      if True: #snake['id'] == data['you']['id']:
        #assign map square to a value is it has sanke on it (INVERTING Y)
        for segment in snake['body']:
          self.map[(self.size-1) - segment['y']][segment['x']] = self.weight_body
        '''self.map[self.size - data['you']['head']['y']-1][self.size - data['you']['head']['x']] = self.weight_head
        for segment in data['you']['body']:
          self.map[self.size -segment['y']-1][segment['x']] = self.weight_body+1
        '''
      '''else:
        for segment in snake['body']:
          i = 0
          if i ==0:
            self.map[segment['y']][segment['x']] = self.weight_head
            i +=1
          else:
            self.map[segment['y']][segment['x']] = self.weight_body
      ''' 
       
    #self.box_blur(1)
    #now put my snake on the map
    


        #print(f"value at segment {self.map[segment['x']][segment['y']]}")

  def print(self):
    print('----------\n')
    for x in self.map:
      print(x)

  def average_3x3(self,x_pointer,y_pointer):
    #find average of 3x3 grid
    total = 0
    num_counted = 0
    
    for i in range(3):
      for j in range(3):
        # search a 3x3 grid centred on current pointer
        cx = x_pointer+ (i - 1)
        cy = y_pointer+ (j - 1)
        
        #if pixel is within the origional maps limits, add it to the total.
        if (cx >=0 and cx <= self.size-1) and (cy >=0 and cy <= self.size-1):
            if i==1 and j == 1:
                total += self.map[cx][cy] #add centre pixel again so it doesnt average out as much
            total += self.map[cx][cy] 
            num_counted +=1
            
    return total / num_counted

  
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
        
        
  def calc_lines(self, xpos, ypos):
    start_xpos, start_ypos = xpos, ypos
    result = {}
    line_sum = 0
    
    change_direction = False
 
    for direction in self.directions:
        #print(f'direction is {direction}')
        #initiate the variables for the start of each line
        num_steps = 1
        xpos,ypos = start_xpos,start_ypos
        while not change_direction:
          #take one step down the line - added here s head is never counted.
          change_direction = False
          
          xpos += self.directions[direction][0]
          ypos += self.directions[direction][1]
          
          if (((num_steps <= self.max_steps) and not ((xpos <0 or xpos > self.size-1) or (ypos < 0 or ypos > self.size-1)))) and line_sum <= self.threshold:
             
            line_sum += self.map[self.size -1 -ypos][xpos]
            
            num_steps +=1
          else:
            change_direction = True
            #print(f'num steps is {num_steps}')
            if num_steps <= 1:
                risk = 100
            else:
                risk = (line_sum / num_steps) *4
                
        #result.update({direction :{'total' : line_sum, 'steps' : num_steps, 'risk' : risk}})
        print(f'{direction} has a risk of : {risk}')
        result.update({direction : risk})
        line_sum = 0
        num_steps = 1
        change_direction = False    
        
    print(f'result : {result}')        
    return result

  def safest_path(self,xpos,ypos):
    risk_dict = self.calc_lines(xpos,ypos)
    #print(f'risk Dict = {risk_dict}')
    temp = min(risk_dict.values())
    result = [key for key in risk_dict if risk_dict[key] == temp]
    return result
          
 
  


