import numpy as np
from car import Car

street_len = 200 # meters
# intersection length
is_len = 10 # meters
'''
street_west is one way and has only one lane.
This means there is no turning left from street_north and there is no turning
right from street_south.

Each street behaves as a queue, i.e. the first car in is the first car out.

street_len is the length of the street to the intersection (just before the lights.)
Since the behaviour of the street after the intersection dependends on the next
set of traffic lights, once the cars go through the intersection we are done with
them and we consider them a success (+1 to throughput).
'''
street_north_left = []
street_north_right = []
street_south_left = []
street_south_right = []
street_west = []

streets = {'nl': street_north_left,
            'nr': street_north_right,
            'sl': street_south_left,
            'sr': street_south_right,
            'w': street_west}

time = 0
dt = 1/60

traffic_timer = 180
change_light_time = time + traffic_timer
green_to_west = True

lambda_w = 3 #cars per minute
lambda_n = 6

next_from_w = time + (np.random.exponential(lambda_w) * 60)
next_from_n = time + (np.random.exponential(lambda_n) * 60)
next_from_s = time + (np.random.exponential(lambda_n) * 60)

total_north = 0
total_south = 0
total_west = 0
# counts the cars going through
# [[north], [south], [west]]
counter = {'nl': [],
            'nr': [],
            'sl': [],
            'sr': [],
            'w': []}

def is_at_intersection(car, tolerance=2):
    return car.pos >= street_len - tolerance and car.pos <= street_len

# hours to simulate
hours = 2
for t in range(int(hours * 60 * 60 * 60)):

    for s_key in streets:
        street = streets[s_key]
        for i in range(len(street)):
            curr = street[i]

            # advance car
            curr.pos += curr.velocity * dt

            # unless it's at the intersection and the light is red
            if is_at_intersection(curr):
                if s_key == 'w' and not green_to_west:
                    curr.pos -= curr.velocity * dt
                elif green_to_west:
                    curr.pos -= curr.velocity * dt
            
            nxt = street[i - 1]
            # unless there is a car in front (no overlapping)
            if i != 0 and nxt and curr.pos >= nxt.pos - nxt.length:
                curr.pos -= curr.velocity * dt

            # if car is through, despawn car
            if curr.pos >= street_len + is_len:
                street[i] = None

                counter[s_key].append(time)
    
        # remove despawned cars
        if None in street:
            streets[s_key] = list(filter(None, street))
        
        # spawn new cars
        if time >= next_from_n:
            total_north += 1
            if np.random.random() > 0.5:
                street_north_left.append(Car(8.33))
            else:
                street_north_right.append(Car(8.33))
            next_from_n = time + (np.random.exponential(lambda_n) * 60)
        if time >= next_from_s:
            total_south += 1
            if np.random.random() > 0.5:
                street_south_left.append(Car(8.33))
            else:
                street_south_right.append(Car(8.33))
            next_from_s = time + (np.random.exponential(lambda_n) * 60)
        if time >= next_from_w:
            total_west += 1
            street_west.append(Car(8.33))
            next_from_w = time + (np.random.exponential(lambda_w) * 60)

        if time >= change_light_time:
            change_light_time += traffic_timer
            green_to_west = not green_to_west

    if t % 60 == 0:
        #print(time//60, street_west)
        pass
    time += dt

#print stats
print('Totals')
print('north\tsouth\twest')
print('{}\t{}\t{}'.format(total_north, total_south, total_west))

total_cars = total_north + total_south + total_west
cars_through = sum([len(counter[k]) for k in counter])
print('cars through: {}'.format(cars_through))
print('throughput: {}'.format(str(cars_through/total_cars)))