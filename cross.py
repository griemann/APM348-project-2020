import numpy as np

SQUARE_TYPES = ['empty', 'car']

class Square:
    def __init__(self, type, velocity=0):
        self.type = type
        self.velocity = velocity
        self.pos = 0

    def __str__(self):
        return '_' if self.type == SQUARE_TYPES[0] else 'C'
    
    def __repr__(self):
        return self.__str__()

time = 0
dt = 1/60 #update 60 times per sec

traffic_timer = 180
# traffic light
change_light = time + traffic_timer
green_to_west = True

# each square is 2 meters, so each car is 2m long
street_north = [Square(SQUARE_TYPES[0]) for _ in range(26)]
street_south = [Square(SQUARE_TYPES[0]) for _ in range(26)]
street_west = [Square(SQUARE_TYPES[0]) for _ in range(26)]

streets = [street_north, street_south, street_west]
street_names = ['north', 'south', 'west']

# the intersection is at 100m of the streets.
intersection_index = len(street_north) // 2

lambda_w = 3 # cars per minute
lambda_n = 6

# new car comming from street_west
next_from_w = time + (np.random.exponential(lambda_w) * 60)
next_from_n = time + (np.random.exponential(lambda_n) * 60)
next_from_s = time + (np.random.exponential(lambda_n) * 60)

total_north = 0
total_south = 0
total_west = 0
# counts the cars going through
# [[north], [south], [west]]
counter = [[], [], []]
for t in range(120 * 60 * 60):
    # advance time
    time += dt

    for i in range(len(street_west)):

        for s in range(len(streets)):
            street = streets[s]
            curr = street[i]

            if curr.type == 'car':
                # if i == intersection_index:
                #         print(time, s, 'at intersection')

                # advance car
                curr.pos += curr.velocity * dt
                
                # unless its at the intersection and the light is red
                if s == 3 and i == intersection_index - 1 and not green_to_west:
                    #print(time, 'car stopped at red light, west')
                    curr.pos -= curr.velocity * dt
                elif i == intersection_index - 1 and green_to_west:
                    #print(time, 'car stopped at red light, ' + street_names[s])
                    curr.pos -= curr.velocity * dt
                
                # unless there is a car in front
                nxt = streets[s][i + 1]
                if nxt.type == 'car' and nxt.pos <= curr.pos:
                    curr.pos -= curr.velocity * dt

                if i == len(street_west) - 2:
                    #despawn car
                    street[i] = Square(SQUARE_TYPES[0])
                    #print(time, 'despawned car from ' + street_names[s])
                elif curr.pos // 200 > i:
                    street[i + 1]  = curr
                    street[i] = Square(SQUARE_TYPES[0])
                    if i == intersection_index - 1:
                        print(time, 'crossed from ' +street_names[s])
                        counter[s].append(time)


    # spawn new cars
    if time >= next_from_n:
        #print(time, 'new car coming towards north')
        total_north += 1
        street_north[0] = Square(SQUARE_TYPES[1], 8.33)
        next_from_n = time + (np.random.exponential(lambda_n) * 60)
    if time >= next_from_s:
        #print(time, 'new car coming towards south')
        total_south += 1
        street_south[0] = Square(SQUARE_TYPES[1], 8.33)
        next_from_s = time + (np.random.exponential(lambda_n) * 60)
    if time >= next_from_w:
        #print(time, 'new car coming towards west')
        total_west += 1
        street_west[0] = Square(SQUARE_TYPES[1], 8.33)
        next_from_w = time + (np.random.exponential(lambda_w) * 60)
    
    if time >= change_light:
        change_light += traffic_timer
        green_to_west = not green_to_west
        #print(time, 'change light')

    #print every second
    if t % 60 == 0:
        # print(street_west)
        pass


# print stats
print(total_north, total_south, total_west)
[print(len(street_count)) for street_count in counter]

total_cars = total_north + total_south + total_west
cars_through = len(counter[0]) + len(counter[1]) + len(counter[2])
print('throughput: {}'.format(cars_through/total_cars))