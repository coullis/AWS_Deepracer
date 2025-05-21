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
    is_left_of_center = params['is_left_of_center']
    
    #initialize reward
    reward = 1.0

    #punish going off track, or going backwards
    if not all_wheels_on_track:
        reward *= 0.1
    if is_offtrack:
        return 0.001
    if is_reversed:
        return 0.001

    #reward smooth steering
    if abs(steering_angle) < 10:
        reward += 0.5  
    elif abs(steering_angle) < 20:
        reward += 0.2  
    else:
        reward *= 0.9

    #reward going straight in straight sectors
    if closest_waypoints[0] in [1,2,3,4,5,6,7,8,9,10,11,12,30,31,32,33,44,45,46,47,48,49,50]:
        reward += (30 - abs(steering_angle))/30
    #reward speeding in straight sectors
    if closest_waypoints[0] in [1,2,3,4,5,6,7,8,9,10,11,12,22,23,24,25,30,31,32,36,37,38,43,44,45,46,47,48,54,55,56]:
        reward += speed/10
    #reward staying on the right lane before a left turn
    if closest_waypoints[0] in [4,5,6,7,8,9,10,11,12,13,14,26,27,28,29,30,31,32,33,45,46,47,48,49,50] and not is_left_of_center:
        reward += 0.5
    #reward staying on the left lane before a right turn
    if closest_waypoints[0] in [17,18,19,20,21,22,23,35,36,37,38,39,40,41,42,43] and is_left_of_center:
        reward += 0.5

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