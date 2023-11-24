import util

def imagine_layer(fibera, radius, image):
    bound = -1

    maxWaterHeight = 0
    minAirHeight = radius*2

    for fiber in range(fibera):
        if fiber.val == 0 and fiber.y > maxWaterHeight:
            maxWaterHeight = fiber.y
        if fiber.val == 1 and fiber.y < minAirHeight:
            minAirHeight = fiber.y


    bound = (maxWaterHeight + minAirHeight)//2

    # print("bound ", dx, dy)
    for x in range(radius*2):
        for y in range(radius*2):
            if not util.in_cycle(x, y, 125):
                image[x, y] = [255, 255, 255]
                continue
            if x < bound:
                image[x, y, 0] = 0
                image[x, y, 1] = 0
                image[x, y, 2] = 255
            else:
                image[x, y, 0] = 255
                image[x, y, 1] = 0
                image[x, y, 2] = 0
                
    util.show_image("g3 linear-imagine", image)

    return