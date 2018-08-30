#INFX 511 --- Assignment 3 --- Sahil Aggarwal

import turtle 
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

def get_max_value(file, feature):
    """
    Gets maximum value of feature in input file
    Takes:
    file name along with path, entered by the user and which feature to consider
    Returns: Maximum value of that feature
    """
    obs = count_observations(file)
    max_val=-1*math.inf
    with open(file) as file1:
        for i in range(obs): # compare each value with max value
            next(file1)
            if(feature == 1):
                val = file1.readline()
                if(int(val)>max_val):
                    max_val=int(val)
                next(file1)
            elif(feature == 2):
                next(file1)
                val = file1.readline()
                if(int(val)>max_val):
                    max_val=int(val)
            else:
                print("Invalid feature")
    return max_val

def count_observations(file_path):
    """
    Counts the number of observations in the file
    Takes:file_path: Path of the file
    Returns: number of observations in the file
    """
    lines, obs= 0, 0
    with open(file_path) as file:
        for line in file:
            lines = lines + 1
            if(lines%3==0):
                obs+=1
    return (obs)
    
def draw_axes(my_turtle, title, file):
    """
    Draws x and y axis for the chart and give the chart title on top
    Takes:
    my_turtle, file, title
    Returns:
    width: width of the chart
    pixels:pixels per ytick
    start_x, stary_y
    """
    width, height, start_x, start_y  = draw_x_axis(my_turtle) # create x axis
    draw_y_axis(my_turtle, height, start_x, start_y) # create y axis
    pixels = draw_y_tick_marks(my_turtle, height, start_x, start_y, file) # draw ytick marks
    ctitle(my_turtle, title, start_x, start_y + height)
    return (width, pixels, start_x, start_y)

def draw_x_axis(my_turtle):
    """
    Draws the axes for the chart
    Takes:
    my_turtle
    Returns:
    width, height, x and y.
    """
    val = 0.85
    
    width = val * WINDOW_WIDTH # use val to  set the chart size
    height = val * WINDOW_HEIGHT # use val to set the chart size
    start_x = width*(1-val)/2
    start_y = height*(1-val)/2
    my_turtle.penup()       # do not draw while moving
    my_turtle.goto(start_x, start_y)  # walk to coordinates
    my_turtle.pendown()     # start drawing again
    my_turtle.forward(width)   # move forward
    return (width, height, start_x, start_y)

def draw_y_axis(my_turtle, height, start_x, start_y):
    """
    Draws y axis
    Takes:
    my_turtle, height, start_x and start_y
    """
    my_turtle.penup()       # do not draw while moving
    my_turtle.goto(start_x, start_y)  # walk to coordinates
    my_turtle.pendown()     # start drawing again
    my_turtle.left(90)      # turn left
    my_turtle.forward(height)  # move forward

def draw_y_tick_marks(my_turtle, height, start_x, start_y, file):
    """
    Draws tick marks and write labels for y-axis
    Takes:
    my_turtle, height of chart, start_x, start_y, file location
    Returns:
    pixels_per_val: Number of pixels used per ytick
    """
    ticks = 10
    max_value = get_max_value(file, 1) 
    tick_val = round(max_value/ticks,2) # calculate labels
    pixels = height/max_value  # calculate number of pixels to move for one ytick
    pixels_per_label = max_value / ticks * pixels # calculate number of pixels moved for each ytick 
    
    for i in range(ticks+1):
        my_turtle.penup()       
        my_turtle.goto(start_x, start_y+pixels_per_label*(i))
        my_turtle.pendown()
        my_turtle.left(90)
        my_turtle.forward(12)
        my_turtle.penup()
        my_turtle.forward(20)
        my_turtle.pendown()
        my_turtle.write(round(tick_val*i,2), font = ("Arial", 9, "normal"))
        my_turtle.penup()
        my_turtle.right(180)
        my_turtle.forward(10)
        my_turtle.left(90)
    return pixels

def draw_rectangle(my_turtle, x, y, width, height, position):
    """
    Draws x and y axis for the chart
    Takes:
    my_turtle, starting x point of rectangle, starting y of the rectangle, width, height, position of value in the file
    """
    my_turtle.begin_fill()
    col = choose_color(position)
    my_turtle.color('black', col)
    my_turtle.penup()
    my_turtle.goto(x, y)
    my_turtle.pendown()
    my_turtle.forward(height)
    my_turtle.right(90)
    my_turtle.forward(width)
    my_turtle.right(90)
    my_turtle.forward(height)
    my_turtle.right(90)
    my_turtle.forward(width)
    my_turtle.end_fill()

def draw_bars(my_turtle, file, width, pixels, start_x, start_y):
    """
    Draw bars for the chart
    Takes:
    my_turtle, location of the file, width of the chart, pixels per ytick, start_x and start_y
    
    """
   
    obs = count_observations(file)
    value = 0.8
    width = (width/obs) * value # calculate width of each bar
    x = ((1-value)/2)*width + start_x
    y = start_y
    with open(file) as file1:
        for i in range(obs):
            name = file1.readline()
            val = file1.readline()
            next(file1)
            draw_rectangle(my_turtle, x, y, width, int(val)*pixels,i)
            draw_xaxis_labels(my_turtle, name, width)
            x = x + width/value
            
def draw_xaxis_labels(my_turtle, label, width):
    """
    Draws x-axis labels for the chart
    Takes:
    my_turtle, label on x-axis for each bar, width of each bar 
    """
    my_turtle.penup()
    my_turtle.left(90)
    my_turtle.forward(40)
    my_turtle.left(90)
    my_turtle.forward(width/2)
    my_turtle.left(90)
    my_turtle.pendown()
    my_turtle.write(label, font = ("Arial", 10, "normal"), align ='center')

def ctitle(my_turtle, title, x, y):
    """
    Writes the chart title
    Takes:
    my_turtle, title, x coordinat, y coordinate
    """
    my_turtle.penup()
    my_turtle.goto(x+20, y+10)
    my_turtle.pendown()
    my_turtle.write(title.upper(), font = ("Arial", 20, "normal"))

def choose_color(position):
    """
    Chooses color for each bar based on the index of each observation
    Takes position : observation number in the file
    """
    list_colors = ['#FF2B81', '#FFE014', '#445DE8', '#65E837', '#A063FF']
    
    while(position >= len(list_colors)):
        position = position - len(list_colors)
    return list_colors[position]
    
#inputs from the user
file = input("What file do you want to visualize? ")
title = input("Name of chart? ")

# Define window size as constants
window = turtle.Screen()  # create a window for the turtle to draw on
window.setup(WINDOW_WIDTH, WINDOW_HEIGHT)  # specify window size (width, height)
window.setworldcoordinates(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)  # coordinate system: origin at lower-left

# Create the turtle
my_turtle = turtle.Turtle()
my_turtle.speed("fastest")  # how fast the turtle should move

window.title('Turtle')  # the title to show at the top of the window


width, pixels, start_x, start_y = draw_axes(my_turtle, title, file)
draw_bars(my_turtle, file, width, pixels, start_x, start_y)

# hide turtle after processing is done
my_turtle.hideturtle()

window.mainloop()


