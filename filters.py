import os
from random import choice, randrange, uniform
from math import sin, cos, pi, sqrt
import stddraw
from picture import Picture
from color import Color

def rotated_picture_size(source, theta):
    source_w = source.width()
    source_h = source.height()
    corner_cols = [0, source_w - 1]
    corner_rows = [0, source_h - 1]
    min_x = None
    min_y = None
    max_x = None
    max_y = None
    center_x = source_w // 2 + source_w % 2 
    center_y= source_h // 2 + source_h % 2
    for x in corner_cols:
        for y in corner_rows:
            source_col = (x - center_x) * cos(theta) - (y - center_y)*sin(theta) + center_x
            source_row= (x - center_x) * sin(theta) + (y - center_y) * cos(theta) + center_y
            if min_x is None or source_col < min_x:
                min_x = source_col
            if min_y is None or source_row < min_y:
                min_y = source_row
            if max_x is None or source_col > max_x:
                max_x = source_col
            if max_y is None or source_row > max_y:
                max_y = source_row 
    print(max_x, min_x, max_y, min_y)
    return (max_x, min_x, max_y, min_y)
             

def scale(source, target_width, target_height):
    target = Picture(target_width, target_height)
    for colT in range(target_width):
        for rowT in range(target_height):
            colS = colT * source.width() // target_width
            rowS = rowT * source.height() // target_height
            target.set(colT, rowT, source.get(colS, rowS))
    return target
            

def tiles(source, m, n):
    source_w = source.width()
    source_h = source.height()
    border_width = 3
    target = Picture(source_w, source_h)
    tiles_in_row = source_h // n
    tiles_in_column = source_w// m
    for i in range(source_h):
        for j in range(source_w):
            if j % m <= border_width and j >=border_width or i % n <= border_width and i >= border_width:
                target.set(j, i, Color(255, 255, 255))
            else:
                target.set(j, i, source.get(j, i))
    return target

def rotate(source, theta):
    
    source_w = source.width()
    source_h = source.height()

    
    center_x = source_w // 2 + source_w % 2 
    center_y= source_h // 2 + source_h % 2

    
    max_x, min_x, max_y, min_y = rotated_picture_size(source, theta)
    print(int(max_x - min_x), int(max_y - min_y))
    target_w = int(max_x - min_x)
    target_h = int(max_y - min_y)
    target = Picture(target_w, target_h )

    for i in range(target_h):
        for j in range(target_w):
            #source_col = (j - center_x) * cos(theta) - (i - center_y)*sin(theta) + center_x
            #source_row= (j - center_x) * sin(theta) + (i - center_y) * cos(theta) + center_y
            source_col = (j + min_x  - center_x) * cos(theta) - (i + min_y - center_y)*sin(theta) + center_x  
            source_row= (j + min_x - center_x) * sin(theta) + (i + min_y -center_y) * cos(theta) + center_y 
            
            try: 
                target.set(j,  i, source.get(int(source_col), int(source_row)))
            except:
                pass 
    return target 

def skrut(source):

    source_w = source.width()
    source_h = source.height()

    
    center_x = source_w // 2 + source_w % 2 
    center_y= source_h // 2 + source_h % 2

    target = Picture(source_w, source_h)

    for i in range(source_h):
        for j in range(source_w):
            theta = pi / 256 * sqrt((center_x - j)**2 + (center_y - i)**2)
            source_col = (j - center_x) * cos(theta) - (i - center_y)*sin(theta) + center_x

            source_row= (j - center_x) * sin(theta) + (i - center_y) * cos(theta) + center_y

            try: 
                target.set(j, i, source.get(int(source_col), int(source_row)))
            except:
                pass
    return target 

def glass_filter(source):
    
    source_w = source.width()
    source_h = source.height()

    target = Picture(source_w, source_h)

    for i in range(source_h):
        for j in range(source_w):
            source_col, source_row = (-1, -1)
            while source_col <=0 or source_col >= source_w or source_row <=0 or source_row >= source_h:
                source_col, source_row = j + randrange(-5, 5), i + randrange(-5, 5)
            target.set(j, i, source.get(source_col, source_row))
    return target

def wave(source):

    source_w = source.width()
    source_h = source.height()
    

    target = Picture(source_w, source_h)

    for i in range(source_h):
        for j in range(source_w):
            source_col = j
            source_row = int(i + 20* sin(2*pi*j/64))
            try:
                target.set(j, i, source.get(source_col, source_row))
            except:
                pass
    return target


def fade(source, target):
    width = source.width()
    height = source.height()
    pic = Picture(width, height)
    for t in range(12):
        for col in range(width):
            for row in range(height):
                c0 = source.get(col, row)
                cn = target.get(col, row)
                alpha = 1.0 * t / 11
                pic.set(col, row, blend(c0, cn, alpha))
        stddraw.picture(pic)
        stddraw.show(100)
            


def blend(c1, c2, alpha):
    r = (1 - alpha) * c1.getRed() + alpha* c2.getRed()
    g = (1 - alpha) * c1.getGreen() + alpha* c2.getGreen()
    b = (1 - alpha) * c1.getBlue() + alpha* c2.getBlue()
    return Color(int(r), int(g), int(b))


files = os.listdir('pictures')
filters_list = [fade, skrut, rotate, tiles, wave, glass_filter]
stddraw.setCanvasSize(800, 600)
for file in files:
    if file[-4:] in ('.jpg', '.png'):
        stddraw.clear()
        source_file = scale(Picture('pictures/' + file), 800, 600)
        
        filter = choice(filters_list) 
        if filter == tiles:
            stddraw.picture(scale(tiles(source_file, 50, 50 ), 800, 600))
        elif filter == rotate:
            stddraw.picture(scale(rotate(source_file, uniform(0, 2* pi)), 800 ,600))
        elif filter == fade:
            target_name = choice(files)
            fade(source_file, scale(Picture('pictures/' + target_name), 800, 600)) 
        else:
            stddraw.picture(scale(filter(source_file), 800, 600))
        stddraw.show(500)
        
