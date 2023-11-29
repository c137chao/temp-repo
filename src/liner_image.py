import util

def imagine_layer(fibera, radius, image):
    bound = -1

    maxWaterHeight = 0
    minAirHeight = radius*2

    for fiber in fibera:
        if fiber[2] == 0 and fiber[1] > maxWaterHeight:
            maxWaterHeight = fiber[1]
        if fiber[2] == 1 and fiber[1] < minAirHeight:
            minAirHeight = fiber[1]
    print("min air:", minAirHeight, "maxwater:", maxWaterHeight)

    bound = (maxWaterHeight + minAirHeight)//2

    # print("bound ", dx, dy)
    for x in range(radius*2):
        for y in range(radius*2):
            if not util.in_cycle(x, y, 125):
                image[x, y] = 0.5
                continue
            if x < bound:
                image[x, y] = 0
            else:
                image[x, y] = 1
                
    # util.show_image("g3 linear-imagine", image)

    return