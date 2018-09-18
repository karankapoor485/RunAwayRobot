#!/usr/bin/python

import math
import random
import robot
import unittest
import multiprocessing as mproc

try:
    import studentMain1
except Exception as e:
    print "Error importing studentMain1:", e

try:
    import studentMain2
except Exception as e:
    print "Error importing studentMain2:", e

try:
    import studentMain3
except Exception as e:
    print "Error importing studentMain3:", e

try:
    import studentMain4
except Exception as e:
    print "Error importing studentMain4:", e


PI = math.pi

GLOBAL_SEEDS = [None,
                None,
                'air_nomads',
                'water_tribes',
                'earth_kingdom',
                'fire_nation']

TIME_LIMIT = 5  # seconds

CREDIT_PER_PASS = 2.5  # points

GLOBAL_PARAMETERS = [None,
                     {'test_case': 1,
                      'target_x': 6.38586153722,
                      'target_y': 13.4105567386,
                      'target_heading': 2.47241215877,
                      'target_period': -25,
                      'target_speed': 3.79845282159,
                      'hunter_x': -4.15461096841,
                      'hunter_y': -0.3225704554,
                      'hunter_heading': 2.53575760878},
                     {'test_case': 2,
                      'target_x': 16.585052609,
                      'target_y': 9.0679044122,
                      'target_heading': -1.35786342037,
                      'target_period': -37,
                      'target_speed': 1.28476921126,
                      'hunter_x': 10.8662448888,
                      'hunter_y': 14.7856356957,
                      'hunter_heading': 0.356152836897},
                     {'test_case': 3,
                      'target_x': 14.2062592559,
                      'target_y': -18.0245447208,
                      'target_heading': -2.38262617883,
                      'target_period': -49,
                      'target_speed': 1.83862303037,
                      'hunter_x': -2.82628668059,
                      'hunter_y': -8.94637942004,
                      'hunter_heading': -0.220346285164},
                     {'test_case': 4,
                      'target_x': -11.8110077747,
                      'target_y': -18.6564535804,
                      'target_heading': -1.96611401851,
                      'target_period': 43,
                      'target_speed': 1.63703150728,
                      'hunter_x': -11.6275149175,
                      'hunter_y': 5.79288354591,
                      'hunter_heading': -0.167236690344},
                     {'test_case': 5,
                      'target_x': 15.6527729222,
                      'target_y': -0.647477557818,
                      'target_heading': 2.53763865986,
                      'target_period': -25,
                      'target_speed': 3.30090641473,
                      'hunter_x': 4.89061164952,
                      'hunter_y': -3.67364934482,
                      'hunter_heading': 0.69375353171},
                     {'test_case': 6,
                      'target_x': 4.19064615709,
                      'target_y': -1.18147110409,
                      'target_heading': -1.64836474843,
                      'target_period': 15,
                      'target_speed': 3.83139058798,
                      'hunter_x': 1.58465033057,
                      'hunter_y': -11.608873745,
                      'hunter_heading': -1.71836625476},
                     {'test_case': 7,
                      'target_x': -14.9126298507,
                      'target_y': 9.77381651339,
                      'target_heading': -2.6049812496,
                      'target_period': 15,
                      'target_speed': 1.87228826655,
                      'hunter_x': -1.73542429642,
                      'hunter_y': 15.2209669071,
                      'hunter_heading': -3.11279669928},
                     {'test_case': 8,
                      'target_x': -7.36186590331,
                      'target_y': -16.8073975689,
                      'target_heading': -0.521095102947,
                      'target_period': 16,
                      'target_speed': 1.99556521539,
                      'hunter_x': -12.4391297878,
                      'hunter_y': -17.4403250837,
                      'hunter_heading': -2.7562509168},
                     {'test_case': 9,
                      'target_x': 8.12973829475,
                      'target_y': -10.7703982486,
                      'target_heading': -1.99007409394,
                      'target_period': 50,
                      'target_speed': 2.79327564984,
                      'hunter_x': -6.10424606902,
                      'hunter_y': -18.9750820343,
                      'hunter_heading': -0.0275542431845},
                     {'test_case': 10,
                      'target_x': -18.2934552906,
                      'target_y': 16.3903453417,
                      'target_heading': 0.345582694568,
                      'target_period': -16,
                      'target_speed': 3.99258090205,
                      'hunter_x': -18.1103477129,
                      'hunter_y': 5.2801933801,
                      'hunter_heading': 1.29663175758}]


class RunawaySimulator:
    """Run student submission code.

    Attributes:
        robot_steps(Queue): synchronized queue to store robot steps.
        robot_found(Queue): synchronized queue to store if robot found.
        robot_error(Queue): synchronized queue to store exception messages.
    """
    def __init__(self):
        self.robot_steps = mproc.Queue(1)
        self.robot_found = mproc.Queue(1)
        self.robot_error = mproc.Queue(1)

    def _reset(self):
        """Reset submission results.
        """
        while not self.robot_steps.empty():
            self.robot_steps.get()

        while not self.robot_found.empty():
            self.robot_found.get()

        while not self.robot_error.empty():
            self.robot_found.get()

    @staticmethod
    def distance(p, q):
        """Calculate the distance between two points.

        Args:
            p(tuple): point 1.
            q(tuple): point 2.

        Returns:
            distance between points.
        """
        x1, y1 = p
        x2, y2 = q

        dx = x2 - x1
        dy = y2 - y1

        return math.sqrt(dx**2 + dy**2)

    @staticmethod
    def truncate_angle(t):
        """Truncate angle between pi and -pi.

        Args:
            t(float): angle to truncate.

        Returns:
            truncated angle.
        """
        return ((t + PI) % (2 * PI)) - PI

    def simulate_without_hunter(self, estimate_next_pos, params):
        """Run simulation only to locate lost bot.

        Args:
            estimate_next_pos(func): Student submission function to estimate next robot position.
            params(dict): Test parameters.

        Raises:
            Exception if error running submission.
        """
        self._reset()

        target = robot.robot(params['target_x'],
                             params['target_y'],
                             params['target_heading'],
                             2.0 * PI / params['target_period'],
                             params['target_speed'])
        target.set_noise(0.0,
                         0.0,
                         params['noise_ratio'] * params['target_speed'])

        tolerance = params['tolerance_ratio'] * target.distance
        other_info = None
        steps = 0

        random.seed(GLOBAL_SEEDS[params['part']])

        try:
            while steps < params['max_steps']:
                target_meas = target.sense()

                estimate, other_info = estimate_next_pos(target_meas, other_info)

                target.move_in_circle()
                target_pos = (target.x, target.y)

                separation = self.distance(estimate, target_pos)
                if separation < tolerance:
                    self.robot_found.put(True)
                    self.robot_steps.put(steps)
                    return

                steps += 1

            self.robot_found.put(False)
            self.robot_steps.put(steps)

        except Exception as exp:
            self.robot_error.put(exp.message)

    def simulate_with_hunter(self, next_move, params):
        """Run simulation to locate lost bot and catch with hunter.

        Args:
            next_move(func): Student submission function for hunters next move.
            params(dict): Test parameters.

        Raises:
            Exception if error running submission.
        """
        self._reset()

        target = robot.robot(params['target_x'],
                             params['target_y'],
                             params['target_heading'],
                             2.0 * PI / params['target_period'],
                             params['target_speed'])
        target.set_noise(0.0,
                         0.0,
                         params['noise_ratio'] * params['target_speed'])

        hunter = robot.robot(params['hunter_x'],
                             params['hunter_y'],
                             params['hunter_heading'])

        tolerance = params['tolerance_ratio'] * target.distance
        max_speed = params['speed_ratio'] * params['target_speed']
        other_info = None
        steps = 0

        random.seed(GLOBAL_SEEDS[params['part']])

        try:
            while steps < params['max_steps']:
                hunter_pos = (hunter.x, hunter.y)
                target_pos = (target.x, target.y)

                separation = self.distance(hunter_pos, target_pos)
                if separation < tolerance:
                    self.robot_found.put(True)
                    self.robot_steps.put(steps)
                    return

                target_meas = target.sense()
                turn, dist, other_info = next_move(hunter_pos, hunter.heading, target_meas, max_speed, other_info)

                dist = min(dist, max_speed)
                dist = max(dist, 0)
                turn = self.truncate_angle(turn)

                hunter.move(turn, dist)
                target.move_in_circle()

                steps += 1

            self.robot_found.put(False)
            self.robot_steps.put(steps)

        except Exception as exp:
            self.robot_error.put(exp.message)


NOT_FOUND = "Part {} - Test Case {}: robot took {} step(s) which exceeded the {} allowable step(s)."


class CaseRunner(unittest.TestCase):
    """Run test case using specified parameters.

    Attributes:
        simulator(RunawaySimulator): Simulation.
    """
    @classmethod
    def setUpClass(cls):
        """Setup test class.
        """
        cls.simulator = RunawaySimulator()

    def run_with_params(self, k, test_params, test_method, student_method):
        """Run test case with parameters.

        Args:
            k(int): Test case global parameters.
            test_params(dict): Test parameters.
            test_method(func): Test function.
            student_method(func): Student submission function.
        """
        test_params.update(GLOBAL_PARAMETERS[k])

        test_process = mproc.Process(target=test_method, args=(student_method, test_params))

        error_message = ''
        steps = None
        robot_found = False

        try:
            test_process.start()
            test_process.join(TIME_LIMIT)
        except Exception as exp:
            error_message += exp.message + ' '

        if test_process.is_alive():
            test_process.terminate()
            error_message = ('Test aborted due to timeout. ' +
                             'Test was expected to finish in fewer than {} second(s).'.format(TIME_LIMIT))

        else:
            if not self.simulator.robot_error.empty():
                error_message += self.simulator.robot_error.get()

            if not self.simulator.robot_found.empty():
                robot_found = self.simulator.robot_found.get()

            if not self.simulator.robot_steps.empty():
                steps = self.simulator.robot_steps.get()

        self.assertFalse(error_message, error_message)
        self.assertTrue(robot_found, NOT_FOUND.format(test_params['part'],
                                                      test_params['test_case'],
                                                      steps,
                                                      test_params['max_steps']))


class Part1TestCase(CaseRunner):
    """Test Part 1

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_without_hunter
        self.student_method = studentMain1.estimate_next_pos

        self.params = dict()
        self.params['tolerance_ratio'] = 0.02
        self.params['part'] = 1
        self.params['max_steps'] = 10
        self.params['noise_ratio'] = 0.00

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


class Part2TestCase(CaseRunner):
    """Test Part 2

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_without_hunter
        self.student_method = studentMain2.estimate_next_pos

        self.params = dict()
        self.params['part'] = 2
        self.params['tolerance_ratio'] = 0.02
        self.params['max_steps'] = 1000
        self.params['noise_ratio'] = 0.05

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


class Part3TestCase(CaseRunner):
    """Test Part 3

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_with_hunter
        self.student_method = studentMain3.next_move

        self.params = dict()
        self.params['part'] = 3
        self.params['tolerance_ratio'] = 0.02
        self.params['max_steps'] = 1000
        self.params['noise_ratio'] = 0.05
        self.params['speed_ratio'] = 2.00

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


class Part4TestCase(CaseRunner):
    """Test Part 4

    Attributes:
        test_method(func): Test function.
        student_method(func): Student submission function.
        params(dict): Test parameters.
    """
    def setUp(self):
        """Setup for each test case.
        """
        self.test_method = self.simulator.simulate_with_hunter
        self.student_method = studentMain4.next_move

        self.params = dict()
        self.params['part'] = 4
        self.params['tolerance_ratio'] = 0.02
        self.params['max_steps'] = 1000
        self.params['noise_ratio'] = 0.05
        self.params['speed_ratio'] = 0.99

    def test_case01(self):
        self.run_with_params(1, self.params, self.test_method, self.student_method)

    def test_case02(self):
        self.run_with_params(2, self.params, self.test_method, self.student_method)

    def test_case03(self):
        self.run_with_params(3, self.params, self.test_method, self.student_method)

    def test_case04(self):
        self.run_with_params(4, self.params, self.test_method, self.student_method)

    def test_case05(self):
        self.run_with_params(5, self.params, self.test_method, self.student_method)

    def test_case06(self):
        self.run_with_params(6, self.params, self.test_method, self.student_method)

    def test_case07(self):
        self.run_with_params(7, self.params, self.test_method, self.student_method)

    def test_case08(self):
        self.run_with_params(8, self.params, self.test_method, self.student_method)

    def test_case09(self):
        self.run_with_params(9, self.params, self.test_method, self.student_method)

    def test_case10(self):
        self.run_with_params(10, self.params, self.test_method, self.student_method)


# Only run all of the test automatically if this file was executed from the command line.
# Otherwise, let Nose/py.test do it's own thing with the test cases.
if __name__ == "__main__":
    suites = map(lambda case: unittest.TestSuite(unittest.TestLoader().loadTestsFromTestCase(case)),
                 [Part1TestCase, Part2TestCase, Part3TestCase, Part4TestCase])

    total_passes = 0

    for i, suite in zip(range(1, 1+len(suites)), suites):
        print "====================\nTests for Part {}:".format(i)

        result = unittest.TestResult()
        suite.run(result)

        for x in result.errors:
            print x[0], x[1]
        for x in result.failures:
            print x[0], x[1]

        num_errors = len(result.errors)
        num_fails = len(result.failures)
        num_passes = result.testsRun - num_errors - num_fails
        total_passes += num_passes

        print "Successes: {}\nFailures: {}\n".format(num_passes, num_errors + num_fails)

    print "====================\nOverall Score: {}".format(total_passes * CREDIT_PER_PASS)
