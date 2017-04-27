import numpy as np
import random
from q_learning import QLearning
from maze import Maze
import sys


class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''
        # Starting location; bottom right corner
        self.location = [0, 11]
        # Starts heading up
        self.heading = 'up'
        # Dimensions of the maze
        self.maze_dim = maze_dim
        # Goal(square) for robot
        self.goal = [self.maze_dim / 2 - 1, self.maze_dim / 2]
        # Import maze environment for rewards
        self.maze = Maze( str(sys.argv[1]) )
        # Sensor direction according to rotation
        self.dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
                            'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
                            'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
                            'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
        # Going in reverse direction
        self.dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
                            'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}

    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        # Make a copy to preserve original [L, F, R]
        view = list(sensors)

        # Implement Q-Learning
        q_learn = QLearning(self.location, self.maze_dim)
        # Build state through sesnsor information
        state = q_learn.build_state(view)
        # Create state in Q-table if not already there
        q_learn.create_Q(state)
        # Take action according to state
        action = q_learn.choose_action(state)

        # Reset when robot reaches the goal
        if self.location[0] in self.goal and self.location[1] in self.goal:
            rotation = 'Reset'
            movement = 'Reset'
        else:
            # Up
            if action == 'up':
                rotation = 0
                movement = 1
            # Right
            elif action == 'right':
                rotation = 90
                movement = 1
            # Down
            elif action == 'down':
                rotation = 0
                movement = -1
            # Left
            elif action == 'left':
                rotation = -90
                movement = 1
            else:
                rotation = 0
                movement = 0

        # Apply reward for each action
        reward = self.maze.move(action)
        # Learn through the state, action, and reward
        q_learn.learn(state, action, reward)
        # Update the functions with the current state, action, reward
        q_learn.update(view)

        # Returns tuple (rotation, movement)
        return rotation, movement
