import math

'''
punish pointless steering
#punish going off the track
#punish slowing down for no reason
#reward high speed according to the distance between the heading vector and the next checkpoint
#reward keeping the opposite lane of the next curve (while not on currently on a curve)
#reward steering smoothly
'''
#rewarding behaviour based on clossest waypoints===============================================================================
def reward_function(params):
    # Read input parameters
    closest_waypoints = params['closest_waypoints']
    all_wheels_on_track = params['all_wheels_on_track']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
    steering_angle = params['steering_angle']
    speed = params['speed']
    
    #initialize reward
    reward = 1.0

    #punish going off track, or going backwards
    if not all_wheels_on_track:
        reward *= 0.01
    if is_offtrack:
        reward *= 0.001
    if is_reversed:
        reward *= 0.001

    #reward smooth steering
    

    #reward going straight in section 44-50
    if closest_waypoints[0] in [44,45,46,47,48,49,50]:
        reward += 1 - (abs(steering_angle)/100)
    #reward speeding in section 43-48
    if closest_waypoints[0] in [43, 44,45,46,47,48]:
        reward += speed/100
    
    return float(reward)

#going from checkpoing to checkpoint default example======================================================================================
def example_reward_function(params):
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize the reward with typical value
    reward = 1.0

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    return float(reward)