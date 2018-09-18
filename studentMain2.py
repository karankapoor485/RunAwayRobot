# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random

# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    if OTHER is None:
        xy_estimate = measurement
        angle = 0
        
        measurements_num = 0
        
        step_total = 0
        
        angle_step_total = 0

        
    else:
        measurements_num_old = OTHER[0]
        measurement_old = OTHER[1]
        angle_old = OTHER[2]
        step_total = OTHER[3]
        angle_step_total = OTHER[4]

        measurements_num = measurements_num_old + 1

        step_length = distance_between(measurement, measurement_old)
        step_total += step_length
        step_average = step_total / measurements_num


        angle = atan2(measurement[1]-measurement_old[1],measurement[0]-measurement_old[0])
        angle_step = angle - angle_old
        print "Angle step", angle_step, (angle_step%(2*pi)), angle_trunc(angle_step)
        
        angle_step_total += angle_trunc(angle_step)
        #total_angle_step += abs(angle_step) / 2
        average_angle_step = angle_step_total / measurements_num

        #new_angle = angle * 2 - prev_angle
        new_angle = angle + average_angle_step
        #print "Average angle step", average_angle_step

        x_estimate = measurement[0]+ step_average*cos(new_angle)
        y_estimate = measurement[1]+ step_average*sin(new_angle)
        #x_estimate = measurement[0]+ step_size*cos(new_angle)
        #y_estimate = measurement[1]+ step_size*sin(new_angle)
        xy_estimate = (x_estimate,y_estimate)


        
    OTHER = [measurements_num, measurement, angle, step_total, angle_step_total]
    #print "OTHER", OTHER

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    #xy_estimate = (3.2, 9.1)
    return xy_estimate, OTHER

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
# def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
#     localized = False
#     distance_tolerance = 0.01 * target_bot.distance
#     ctr = 0
#     # if you haven't localized the target bot, make a guess about the next
#     # position, then we move the bot and compare your guess to the true
#     # next position. When you are close enough, we stop checking.
#     while not localized and ctr <= 1000:
#         ctr += 1
#         measurement = target_bot.sense()
#         position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
#         target_bot.move_in_circle()
#         true_position = (target_bot.x, target_bot.y)
#         error = distance_between(position_guess, true_position)
#         if error <= distance_tolerance:
#             print "You got it right! It took you ", ctr, " steps to localize."
#             localized = True
#         if ctr == 1000:
#             print "Sorry, it took you too many steps to localize the target."
#     return localized, ctr

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# def demo_grading_visual(estimate_next_pos_fcn, target_bot, OTHER = None):
#     localized = False
#     distance_tolerance = 0.01 * target_bot.distance
#     ctr = 0
#     # if you haven't localized the target bot, make a guess about the next
#     # position, then we move the bot and compare your guess to the true
#     # next position. When you are close enough, we stop checking.
#     #For Visualization
#     import turtle    #You need to run this locally to use the turtle module
#     window = turtle.Screen()
#     window.bgcolor('white')
#     size_multiplier= 25.0  #change Size of animation
#     broken_robot = turtle.Turtle()
#     broken_robot.shape('turtle')
#     broken_robot.color('green')
#     broken_robot.resizemode('user')
#     broken_robot.shapesize(0.1, 0.1, 0.1)
#     measured_broken_robot = turtle.Turtle()
#     measured_broken_robot.shape('circle')
#     measured_broken_robot.color('red')
#     measured_broken_robot.resizemode('user')
#     measured_broken_robot.shapesize(0.1, 0.1, 0.1)
#     prediction = turtle.Turtle()
#     prediction.shape('arrow')
#     prediction.color('blue')
#     prediction.resizemode('user')
#     prediction.shapesize(0.1, 0.1, 0.1)
#     prediction.penup()
#     broken_robot.penup()
#     measured_broken_robot.penup()
#     #End of Visualization
#     while not localized and ctr <= 1000:
#         ctr += 1
#         #raw_input()
#         measurement = target_bot.sense()
#         position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
#         target_bot.move_in_circle()
#         true_position = (target_bot.x, target_bot.y)
#         error = distance_between(position_guess, true_position)
#         if error <= distance_tolerance:
#             print "You got it right! It took you ", ctr, " steps to localize."
#             localized = True
#         if ctr == 1000:
#             print "Sorry, it took you too many steps to localize the target."
#         #More Visualization
#         measured_broken_robot.setheading(target_bot.heading*180/pi)
#         measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
#         measured_broken_robot.stamp()
#         broken_robot.setheading(target_bot.heading*180/pi)
#         broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
#         broken_robot.stamp()
#         prediction.setheading(target_bot.heading*180/pi)
#         prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
#         prediction.stamp()
#         #End of Visualization
#     return localized

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.
# test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
# measurement_noise = 0.05 * test_target.distance
# test_target.set_noise(0.0, 0.0, measurement_noise)

# #demo_grading(estimate_next_pos, test_target)
# #demo_grading_visual(estimate_next_pos, test_target)

# number_runs = 1000
# total_ctr = 0
# penalty = 1500
# total_fails = 0

# for i in range(number_runs):
#     completed, ctr = demo_grading(estimate_next_pos, test_target)
#     if completed:
#         total_ctr += ctr
#     else:
#         total_ctr += penalty
#         total_fails += 1

# average_ctr = total_ctr / number_runs

# print "Average_ctr: ", average_ctr
# print "Total Fails: ", total_fails


