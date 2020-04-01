import numpy as np

SQUARE_TYPES = ['empty', 'car']

class Square:
    def __init__(self, type, velocity=0, from_street=None):
        self.type = type
        self.velocity = velocity
        self.pos = 0
        # [0, 1, 2] ~ [north, south, west]
        self.from_street = from_street

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
street_north = [Square(SQUARE_TYPES[0]) for _ in range(13)]
street_south = [Square(SQUARE_TYPES[0]) for _ in range(13)]
street_west = [Square(SQUARE_TYPES[0]) for _ in range(13)]
# roundabout of radius 20m
roundabout = [Square(SQUARE_TYPES[0]) for _ in range(64)]
ra_exits = [0, 15, 31, 63]

streets = [street_north, street_south, street_west, roundabout]
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

        for s in range(len(streets) - 1):
            street = streets[s]
            curr = street[i]

            if curr.type == 'car':

                # advance car
                curr.pos += curr.velocity * dt

                if i == len(street_west) - 1 and s != 3:
                    nxt = roundabout[ra_exits[curr.from_street]]
                    # there's a car in the roundabout, so we wait
                    if nxt.type != 'empty':
                        curr.pos -= curr.velocity * dt
                    else:
                        # get into roundabout
                        roundabout[ra_exits[curr.from_street]] = curr
                        curr.pos = ra_exits[curr.from_street] * 200

                        street[i] = Square(SQUARE_TYPES[0])   
                else:
                    nxt = streets[s][i + 1]
                    # don't advance if there is a car in front
                    if nxt.type == 'car' and nxt.pos <= curr.pos:
                        curr.pos -= curr.velocity * dt
                if s == 3 and i == ra_exits[curr.from_street]:
                    # if at exit, despawn
                    street[i] = Square(SQUARE_TYPES[0])
                    counter[curr.from_street].append(time)

                if curr.pos // 200 > i and i < len(street_west) - 1:
                    street[i + 1]  = curr
                    street[i] = Square(SQUARE_TYPES[0])

    for j in range(len(roundabout) - 1):
        curr = roundabout[j]
        if curr.type != 'empty':
            # advance car
            curr.pos += curr.velocity * dt
            
            # unless there is a car in front:
            nxt = roundabout[i + 1]
            if nxt.type == 'car' and nxt.pos <= curr.pos:
                curr.pos -= curr.velocity * dt

            if j == ra_exits[curr.from_street]:
                # if at exit, despawn
                roundabout[j] = Square(SQUARE_TYPES[0])
                counter[curr.from_street].append(time)
            if curr.pos // 200 > j and j < len(roundabout) - 1:
                    roundabout[i + 1]  = curr
                    roundabout[i] = Square(SQUARE_TYPES[0])

    # spawn new cars
    if time >= next_from_n:
        #print(time, 'new car coming towards north')
        total_north += 1
        street_north[0] = Square(SQUARE_TYPES[1], 8.33, 0)
        next_from_n = time + (np.random.exponential(lambda_n) * 60)
    if time >= next_from_s:
        #print(time, 'new car coming towards south')
        total_south += 1
        street_south[0] = Square(SQUARE_TYPES[1], 8.33, 1)
        next_from_s = time + (np.random.exponential(lambda_n) * 60)
    if time >= next_from_w:
        #print(time, 'new car coming towards west')
        total_west += 1
        street_west[0] = Square(SQUARE_TYPES[1], 8.33, 2)
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