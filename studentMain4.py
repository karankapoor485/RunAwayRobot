# ----------
# Part Four
#
# Again, you'll track down and recover the runaway Traxbot. 
# But this time, your speed will be about the same as the runaway bot. 
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3. Again, try to catch the target in as few steps as possible.

from robot import *
from math import *
from matrix import *
import random

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.

    if OTHER is None:
        
        xy_estimate = target_measurement
        angle = 0
        measurements_num = 0
        
        step_total = 0
        angle_step_total = 0
        turning = atan2(xy_estimate[1] - hunter_position[1], xy_estimate[0] - hunter_position[0])
        current_turning = turning
        distance = distance_between(hunter_position, xy_estimate)

        
    else:
        measurements_num_old = OTHER[0]
        target_measurement_old = OTHER[1]
        angle_old = OTHER[2]
        step_total = OTHER[3]
        angle_step_total = OTHER[4]
        turning_old = OTHER[5]

        measurements_num = measurements_num_old + 1

        step_size = distance_between(target_measurement, target_measurement_old)
        step_total += step_size
        
        average_step = step_total / measurements_num


        angle = atan2(target_measurement[1]-target_measurement_old[1],target_measurement[0]-target_measurement_old[0])
        angle_step = angle - angle_old
        
        
        angle_step_total += angle_trunc(angle_step)
        average_angle_step = angle_step_total / measurements_num

        new_angle = angle + average_angle_step

        #calculate estimate for next position
        
        x_estimate = target_measurement[0]+ average_step*cos(new_angle)
        y_estimate = target_measurement[1]+ average_step*sin(new_angle)
        xy_estimate = (x_estimate,y_estimate)

        ############## estimate next n positions ##############################
        next_positions = [xy_estimate]

        next_n = 15
        prev_n_angle = new_angle

        #min_distance_to_hunter = 9999999999999
        #min_position = None
        min_distance_to_hunter = distance_between(hunter_position, xy_estimate)
        min_position = 0

        if min_distance_to_hunter < max_distance:
            reachable = True
        else:
            reachable = False

        while reachable is False:

            for n in range(1,next_n):
                prev_n_angle += average_angle_step
                nx_estimate = next_positions[n-1][0]+ average_step*cos(prev_n_angle)
                ny_estimate = next_positions[n-1][1]+ average_step*sin(prev_n_angle)
                next_positions.append((nx_estimate,ny_estimate))

                distance = distance_between(hunter_position, [nx_estimate,ny_estimate])# / (1+0.5*n)

                if distance < (n+1)*max_distance:
                    min_distance_to_hunter = distance
                    min_position = n
                    reachable = True
                    break
                elif n is next_n -1:
                    min_distance_to_hunter = distance
                    min_position = n
                    reachable = True


       



        #hunter movement 

        distance = min_distance_to_hunter# * (1+0.5*min_position)
        
        #turning = current_turning - prev_turning
        heading_to_target = get_heading(hunter_position, next_positions[min_position])
        #heading_to_target = get_heading(hunter_position, target_measurement)
        turning = heading_to_target - hunter_heading

        if distance > max_distance:
            distance = max_distance




        
    OTHER = [measurements_num, target_measurement, angle, step_total, angle_step_total, turning]


    return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
#     """Returns True if your next_move_fcn successfully guides the hunter_bot
#     to the target_bot. This function is here to help you understand how we 
#     will grade your submission."""
#     max_distance = 0.98 * target_bot.distance # 1.94 is an example. It will change.
#     separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
#     caught = False
#     ctr = 0

#     # We will use your next_move_fcn until we catch the target or time expires.
#     while not caught and ctr < 1000:

#         # Check to see if the hunter has caught the target.
#         hunter_position = (hunter_bot.x, hunter_bot.y)
#         target_position = (target_bot.x, target_bot.y)
#         separation = distance_between(hunter_position, target_position)
#         if separation < separation_tolerance:
#             print "You got it right! It took you ", ctr, " steps to catch the target."
#             caught = True

#         # The target broadcasts its noisy measurement
#         target_measurement = target_bot.sense()

#         # This is where YOUR function will be called.
#         turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
#         # Don't try to move faster than allowed!
#         if distance > max_distance:
#             distance = max_distance

#         # We move the hunter according to your instructions
#         hunter_bot.move(turning, distance)

#         # The target continues its (nearly) circular motion.
#         target_bot.move_in_circle()

#         ctr += 1            
#         if ctr >= 1000:
#             print "It took too many steps to catch the target."
#     return caught, ctr

# def demo_grading_visual(hunter_bot, target_bot, next_move_fcn, OTHER = None):
#     """Returns True if your next_move_fcn successfully guides the hunter_bot
#     to the target_bot. This function is here to help you understand how we 
#     will grade your submission."""
#     max_distance = 0.98 * target_bot.distance # 1.94 is an example. It will change.
#     separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
#     caught = False
#     ctr = 0
#     #For Visualization
#     import turtle
#     window = turtle.Screen()
#     window.bgcolor('white')
#     chaser_robot = turtle.Turtle()
#     chaser_robot.shape('arrow')
#     chaser_robot.color('blue')
#     chaser_robot.resizemode('user')
#     chaser_robot.shapesize(0.3, 0.3, 0.3)
#     broken_robot = turtle.Turtle()
#     broken_robot.shape('turtle')
#     broken_robot.color('green')
#     broken_robot.resizemode('user')
#     broken_robot.shapesize(0.3, 0.3, 0.3)
#     size_multiplier = 15.0 #change Size of animation
#     chaser_robot.hideturtle()
#     chaser_robot.penup()
#     chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
#     chaser_robot.showturtle()
#     broken_robot.hideturtle()
#     broken_robot.penup()
#     broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
#     broken_robot.showturtle()
#     measuredbroken_robot = turtle.Turtle()
#     measuredbroken_robot.shape('circle')
#     measuredbroken_robot.color('red')
#     measuredbroken_robot.penup()
#     measuredbroken_robot.resizemode('user')
#     measuredbroken_robot.shapesize(0.1, 0.1, 0.1)
#     broken_robot.pendown()
#     chaser_robot.pendown()
#     #End of Visualization
#     # We will use your next_move_fcn until we catch the target or time expires.
#     while not caught and ctr < 1000:
#         # Check to see if the hunter has caught the target.
#         hunter_position = (hunter_bot.x, hunter_bot.y)
#         target_position = (target_bot.x, target_bot.y)
#         separation = distance_between(hunter_position, target_position)
#         if separation < separation_tolerance:
#             print "You got it right! It took you ", ctr, " steps to catch the target."
#             caught = True

#         # The target broadcasts its noisy measurement
#         target_measurement = target_bot.sense()

#         # This is where YOUR function will be called.
#         turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)

#         # Don't try to move faster than allowed!
#         if distance > max_distance:
#             distance = max_distance

#         # We move the hunter according to your instructions
#         hunter_bot.move(turning, distance)

#         # The target continues its (nearly) circular motion.
#         target_bot.move_in_circle()
#         #Visualize it
#         measuredbroken_robot.setheading(target_bot.heading*180/pi)
#         measuredbroken_robot.goto(target_measurement[0]*size_multiplier, target_measurement[1]*size_multiplier-100)
#         measuredbroken_robot.stamp()
#         broken_robot.setheading(target_bot.heading*180/pi)
#         broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
#         chaser_robot.setheading(hunter_bot.heading*180/pi)
#         chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
#         #End of visualization
#         ctr += 1            
#         if ctr >= 1000:
#             print "It took too many steps to catch the target."
#     return caught

def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

# target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
# measurement_noise = .05*target.distance
# target.set_noise(0.0, 0.0, measurement_noise)

# hunter = robot(-10.0, -10.0, 0.0)



