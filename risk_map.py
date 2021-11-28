def average_3x3(x_pointer,y_pointer,orig_image):
    #find average of 3x3 grid
    total = 0
    num_counted = 0
    image_size = len(orig_image[0])-1 #size of the origional 2d grid
    
    for i in range(3):
      for j in range(3):
        # search a 3x3 grid centred on current pointer
        cx = x_pointer+ (i - 1)
        cy = y_pointer+ (j - 1)
        
        
        #if pixel is within the origional images limits, add it to the total.
        if (cx >=0 and cx <= image_size) and (cy >=0 and cy <= image_size):
            if i==1 and j == 1:
                total += orig_image[cx][cy] #add centre pixel again so it doesnt average out as much
            total += orig_image[cx][cy] 
            num_counted +=1
                
    #print(f' from num counted {num_counted}, total is {total} for x{x_pointer} and y{y_pointer} so result : {total // num_counted}')        
    return total / num_counted

    
def box_blur(orig_image):
    image_size = len(orig_image)
    temp_blurred_image = [[0 for x in range(image_size)] for x in range(image_size)]
    
    cx,cy = 0,0
    for x in orig_image:
      cy = 0
      for y in x:
        temp_blurred_image[cx][cy] = int(average_3x3(cx,cy,orig_image))
        cy+=1
      cx +=1
      
    return(temp_blurred_image)

def generate_riskmap(data):
  #create a 2d array with high numbers assigned to risky

