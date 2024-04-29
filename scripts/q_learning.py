#!/usr/bin/env python3

import rospy
import numpy as np
import os
from q_learning_project.msg import QLearningReward, RobotMoveObjectToTag
import sys
import time
# Path of directory on where this file is located
path_prefix = os.path.dirname(__file__) + "/action_states/"

class QLearning(object):
    def __init__(self):
        # Initialize this node
        rospy.init_node("q_learning")

        # Fetch pre-built action matrix. This is a 2d numpy array where row indexes
        # correspond to the starting state and column indexes are the next states.
        #
        # A value of -1 indicates that it is not possible to get to the next state
        # from the starting state. Values 0-9 correspond to what action is needed
        # to go to the next state.
        #
        # e.g. self.action_matrix[0][12] = 5
        self.action_matrix = np.loadtxt(path_prefix + "action_matrix.txt")

        # Fetch actions. These are the only 9 possible actions the system can take.
        # self.actions is an array of dictionaries where the row index corresponds
        # to the action number, and the value has the following form:
        # { object: "pink", tag: 1}
        colors = ["pink", "green", "blue"]
        self.actions = np.loadtxt(path_prefix + "actions.txt")
        self.actions = list(map(
            lambda x: {"object": colors[int(x[0])], "tag": int(x[1])},
            self.actions
        ))


        # Fetch states. There are 64 states. Each row index corresponds to the
        # state number, and the value is a list of 3 items indicating the positions
        # of the pink, green, blue dumbbells respectively.
        # e.g. [[0, 0, 0], [1, 0 , 0], [2, 0, 0], ..., [3, 3, 3]]
        # e.g. [0, 1, 2] indicates that the green dumbbell is at block 1, and blue at block 2.
        # A value of 0 corresponds to the origin. 1/2/3 corresponds to the block number.
        # Note: that not all states are possible to get to.
        self.states = np.loadtxt(path_prefix + "states.txt")
        self.states = list(map(lambda x: list(map(lambda y: int(y), x)), self.states))


        # ********* New *********

        # Initialize the Q-table
        self.q_table = np.zeros((len(self.states), len(self.actions)))

        # Initialize the time to 0
        self.t_time = 0

        # Set the learning and discount rates
        self.alpha = 1  # Start with a smaller alpha
        self.gamma = 0.8  # Discount rate

        # Set initial state to 0
        self.current_state = 0

        # Set intial reward to 0
        self.current_reward = 0

        # Wait for subscriber
        self.wait_for_sub = 1

        # Set up publishers and subscribers
        self.reward_sub = rospy.Subscriber('/q_learning/reward', QLearningReward, self.receive_reward)
        self.action_pub = rospy.Publisher('/q_learning/robot_action', RobotMoveObjectToTag, queue_size=10)

        rospy.sleep(5)

    def select_action(self, state):
        # works
        valid_next_states = np.where(self.action_matrix[state] != -1)[0]
        #print(f"select_action:\tValid Next States for Current State ({state}) = {valid_next_states}")
        if len(valid_next_states):
            next_state_index = np.random.choice(valid_next_states)
            #print(f"select_action:\tNext State is {next_state_index}")
            action = self.action_matrix[state][next_state_index]
            #print(f"select_action:\tNext Action is {int(action)}")
            return int(action)
        else:
            return -1

    def save_q_matrix(self):
        # TODO: You'll want to save your q_matrix to a file once it is done to
        # avoid retraining
        np.savetxt(path_prefix + "q_matrix.csv", self.q_table, delimiter=',')

    def receive_reward(self, data):
        # callback
        self.current_reward = data.reward
        rospy.sleep(0.01)
        self.wait_for_sub = 0
        # print("Published reward: ", self.current_reward)

    def run(self):
        # algorithm
        

        # Initialize Q: self.q_table
        # Initialize t=0: self.t_time
        
        # while no value in Q has changed since last run
        last = self.q_table.copy()
        small_count = 0
        while True:
            
            # Select random action
            action = self.select_action(self.current_state)

            if action != -1:

                # self.[a][b] = action to go from a->b
                next_state = self.current_state
                for i, a in enumerate(self.action_matrix[self.current_state]):
                    if a == action:
                        next_state = i
                        break

                # Create action message
                action_msg = RobotMoveObjectToTag()
                action_msg.robot_object = self.actions[action]['object']
                action_msg.tag_id = self.actions[action]['tag']

                # Variable to track if callback has been called
                self.wait_for_sub = 1

                # Perform the action
                self.action_pub.publish(action_msg)

                # Wait till the callback has been called
                while self.wait_for_sub:
                    print(f"Wait for Subscriber:")
                    rospy.sleep(0.005)
                    time.sleep(0.005)

                # Get the reward from the callback
                reward = self.current_reward
                
                # Get the current Q-Value
                q_value = self.q_table[self.current_state][action]

                # Update the Q-Value
                q_update = self.alpha * (reward + self.gamma * np.max(self.q_table[next_state]) - q_value)
                q_value += q_update

                # Save the Q-Value to the table
                self.q_table[self.current_state][action] = q_value

                # Go to the next state
                self.current_state = next_state
            
            else:
                # If terminal get difference on q table
                diff = np.linalg.norm(last - self.q_table)
                last = self.q_table.copy()
                # If the difference on current table and the last table is small
                if diff <= 2:
                    small_count += 1
                    # Converge if there is small difference on Q-table 20 times in a row
                    if (small_count > 20):
                        break
                else:
                    # Reset the counter
                    small_count = 0

                # Start over from state 0
                self.current_state = 0
                
                print(f'table updated: {diff}, small: {small_count}', file=sys.stderr)
        print(self.q_table, file=sys.stderr)

if __name__ == "__main__":
    try:
        node = QLearning()
        rospy.sleep(1)
        node.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        node.save_q_matrix()
