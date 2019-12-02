from PIL import Image, ImageDraw
import numpy as np 


a = np.zeros((10,10))

a[:,2:3] = 1
a[2:3,:] = 1

im = Image.new('RGB', (200,100), color = 'blue')
d = ImageDraw.Draw(im)
d.text((10,10), 'blue prince', fill = 'white')
d.text((10,30), 'scale = 1cm = 1px', fill = 'white')
for i in range(1,(a.shape[0]-1)):
    x = i*10 +100
    for j in range(1,(a.shape[1]-1)):

        y = j*10
        if (a[i,j] == 1 and (a[i-1,j]==1 or a[i+1,j]==1)):
            draw = ImageDraw.Draw(im)
            draw.line((x, y) + (x+10,y), fill='white')
        if (a[i,j] == 1 and (a[i,j-1]==1 or a[i,j+1]==1)):
            draw = ImageDraw.Draw(im)
            draw.line((x, y) + (x,y+10), fill='white')
        
im.save('blue_prints.png')

