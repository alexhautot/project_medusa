import math

def is_wall(dist_front, dist_up):
    angle = math.pi/4
    
    if dist_up < (dist_front/math.cos(angle)):
        return 'desk'
    else:
        return 'wall'


print(is_wall(10,5))
