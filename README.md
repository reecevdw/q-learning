# q_learning_project


1. [Q-Learning Project Overview](#q_learning_project)
2. [Implementation Plan](#implementation_plan)
   - [Q-learning Algorithm](#q_learning_algorithm)
     - [Executing the Q-learning Algorithm](#executing_algorithm)
     - [Determining Q-matrix Convergence](#q_matrix_convergence)
     - [Actions Post-Convergence](#actions_post_convergence)
   - [Robot Perception](#robot_perception)
     - [Identifying Colored Objects](#identifying_colored_objects)
     - [Identifying AR Tags](#identifying_ar_tags)
   - [Robot Manipulation & Movement](#robot_manipulation_movement)
     - [Manipulating Objects](#manipulating_objects)
     - [Navigating and Object Placement](#navigating_object_placement)
   - [Timeline](#timeline)
3. [Writeup](#writeup)
   - [Objectives Description](#obj_desc)
   - [High Level Description](#hl_desc)
   - [Q-Learning Algorithm Description](#qlearn_desc)
4. [Perception](#percep_desc)
5. [Manipulation](#Manipulation_desc)
6. [Video](#video)
7. [Challenges](#challenges)
8. [Future Work](#Future)
9. [Takeaways](#takeaway)

<a name="q_learning_project"></a>
# Q-Learning Project Overview

In the Q-Learning Project, our team is focused on programming a robot to autonomously organize colored objects by using reinforcement learning to reach a specified goal state. This involves two main phases: a training phase where the robot iteratively refines its decision-making matrix (Q-matrix) through trial and error within a simulated environment, and an action phase where the robot applies its learned strategies to accurately pick up and place objects in front of designated AR tags. This computational approach aims to bridge theoretical learning algorithms with practical robotic tasks, culminating in a robot that not only understands its tasks but can also execute them with learned precision.

<a name="implementation_plan"></a>
# Implementation Plan

The name of our team is **reece-david** which is composed of *Reece VanDeWeghe* and *David Suh*.

<a name="q_learning_algorithm"></a>
## Q-learning algorithm

<a name="executing_algorithm"></a>
### Executing the Q-learning algorithm

- **Implementation**: Our approach will include iterative action selection, execution, and Q-value updates until the Q-matrix values begin to stabilize.
- **Testing**: We'll assess the execution by checking for a decrease in the variance of Q-value changes over iterations.

<a name="q_matrix_convergence"></a>
### Determining when the Q-matrix has converged

- **Implementation**: We will determine convergence by tracking the change in Q-values, considering convergence achieved when changes fall below a predefined threshold.
- **Testing**: The convergence criterion will be tested by running multiple training sessions and ensuring consistent Q-matrix outputs.

<a name="actions_post_convergence"></a>
### Once the Q-matrix has converged, how to determine which actions the robot should take to maximize expected reward

- **Implementation**: Post-convergence, we'll implement a policy extraction step where the robot selects the action with the highest Q-value in the current state.
- **Testing**: We'll simulate different states to test if the robot correctly identifies and takes the action leading to the highest reward.

<a name="robot_perception"></a>
## Robot perception

<a name="identifying_colored_objects"></a>
### Determining the identities and locations of the three colored objects
- **Implementation**: Use computer vision techniques to identify the colored objects based on their hues and shapes.
- **Testing**: Place the objects in various positions and lighting conditions to ensure accurate identification and localization.

<a name="identifying_ar_tags"></a>
### Determining the identities and locations of the three AR tags
- **Implementation**: Implement AR tag detection using available libraries tailored for AR recognition, mapping detected tags to their known identities.
- **Testing**: Test recognition under different angles and distances to ensure reliable detection.

<a name="robot_manipulation_movement"></a>
## Robot manipulation & movement

<a name="manipulating_objects"></a>
### Picking up and putting down the colored objects with the OpenMANIPULATOR arm
- **Implementation**: Code the precise control of the OpenMANIPULATOR arm to pick up objects based on the perceived locations and orientations.
- **Testing**: Perform pick-and-place actions with each colored object, testing for accuracy and reliability.

<a name="navigating_object_placement"></a>
### Navigating to the appropriate locations to pick up and put down the colored objects
- **Implementation**: Implement navigation algorithms that utilize the Q-matrix and perception data to move to the correct locations for object interaction.
- **Testing**: Navigate to each object and respective drop-off location to test the accuracy of the robot’s movements.

<a name="timeline"></a>
## Timeline
- **By April 16, 8:00pm CST**: Finalize and submit the Implementation Plan.
- **April 17 - April 19**: Develop and test the Q-learning algorithm; begin training for Q-matrix convergence.
- **By April 19, 8:00pm CST**: Ensure the Q-learning training is robust; confirm Q-matrix is correctly outputting to a `.csv` file; prepare the intermediate deliverable, including the objectives, high-level description, and Q-learning algorithm description.
- **April 20 - April 25**: Complete robot perception and manipulation modules; integrate all components; conduct extensive testing.
- **By April 26, 8:00pm CST**: Finalize all coding tasks; complete the writeup; produce gif/video demonstration; each team member completes the Partner Contributions Survey; prepare for final submission.

<a name="writeup"></a>
# Writeup
---
<a name="obj_desc"></a>
## Objective Description
The object of this project is to get a robot to place colored dumbbells at
corresponding AR tags in a two step process. Firsy, we use Q-Learning to learn
the optimal policy of how move which dumbbell where at a given state. Second,
we implement a movement system in the robot so that it can execute a given
action, e.g. move x dumbbeel to tag y, using AR tag and computer vision
dectection along with kinematics of the robot arm.

<a name="hl_desc"></a>
## High Level Description
We were able to use Q learning (reinformcement learning) to determine which
color goes to which tag. In particular, we use the fact that correct final
state provides a reward of 100 and otherwise 0 to stochastically calculate the
optimal move policy from any given state. This is done by assigning each
possible action from each possible state a value (this value being determined
via simulation), then we simply take the argmax of the values as the action we
should take. 

<a name="qlearn_desc"></a>
## Q-Learning Algorithm Description
* Selecting and executing actions for the robot (or phantom robot) to take:
  This code is handled by `select_action` and to some capacity `run`. We can
note that the valid moves from a state `s` is simple the elements of row
`action_matrix[s]` which are not -1. Thus we simply do a random sample of that
row after masking is -1 elements numpy style to get the next action. This
action can be "executed" (move state forward) by keeping the index of the
selected element, or we can simple iterate over `action_matrix[s]` again until
we find the index with action `a`. At this point we also publish the action to
the action publish endpoint.

* Updating the Q-matrix: This is pretty straight forward. As per the
  pseudocode, the only non-trivial values we need to find are the reward
(`r_t`) and the max term. The reward is gotten like so -- we have a callback
attached to the reward topic, which will set the class member `self.reward` to
the given amount. This value is read in (after a short sleep after publishing
the action) as the reward. As for the max of next state, we can simply take the
max of `q_table[next_state]`, which is precisely the value the algorithm asks for. We can then update `q_table[state][action]` as per the equation.

* Determining when to stop iterating through the Q-learning algorithm: We track
  the change in the Q matrix by taking the Frobenius norm of the difference
between current and last Q matrcies (this does require us to keep a copy of the
old matrix), and we stop iterating once the difference is less than a threshold
(1e-2) for 20 iterations. 

* Executing the path most likely to lead to receiving a reward after the
  Q-matrix has converged on the turtlebot: One can take the argmax along axis
1 of the Q matrix, and do a lookup on the `action_matrix` for the action
number.

<a name="percep_desc"></a>
## Perception Description

### Identifying the Locations and Identities of Each of the Colored Objects

#### Description
The system identifies colored objects by applying HSV color thresholds, which are more robust to variations in lighting compared to RGB thresholds. The thresholds for each color (blue, green, pink) are predefined in the `color_range` dictionary. This method isolates the relevant colored regions within the camera's field of view.

#### Code Implementation
- **Function `image_callback(self, msg)`**: This function processes the camera feed, converts the RGB images to HSV, and applies the color thresholds to detect and isolate colored objects. It uses OpenCV's `cv2.inRange()` to create masks for detected colors and `cv2.moments()` to find the centroids of these regions, providing the locations of the objects.

### Identifying the Locations and Identities of Each of the AR Tags

#### Description
AR tags are detected using the OpenCV ArUco library, which is specifically designed for marker detection. This method involves recognizing predefined patterns that can be easily identified and decoded, even from different angles and distances.

#### Code Implementation
- **Function `find_ar_tag(self, image)`**: Converts the image to grayscale and then uses the `aruco.detectMarkers()` function to detect AR tags in the image. This function identifies the corners of each tag and their IDs, which are crucial for further processing.
- **Function `image_callback(self, msg)`**: After processing for color object detection, this function also handles AR tag detection if an object is already being carried by the robot. It aligns the robot's motion towards the tag by calculating the position errors relative to the camera's field of view.

<a name="Manipulation_desc"></a>
## Robot Manipulation and Movement Description

### Moving to the Right Spot in Order to Pick Up a Colored Object

#### Description
The robot adjusts its position to approach and properly align with a detected colored object. This involves calculating the error in the object's position relative to the center of the camera's field of view and adjusting the robot's movement accordingly.

#### Code Implementation
- **Function `go_to(self, px_error)`**: Calculates the angular and linear movements needed based on the pixel error from the object's position to the center of the camera's view. It adjusts the robot's heading and forwards movement to position the robot in front of the object at an optimal distance for picking.
- **Function `send_movement(self, velocity, angular)`**: Sends velocity commands to the robot to adjust its position. This function is called within `go_to` to perform the actual movements.

### Picking Up the Colored Object

#### Description
Once properly aligned and positioned, the robot uses its arm and gripper to pick up the colored object. This involves lowering the arm, closing the gripper around the object, and then lifting the arm back up.

#### Code Implementation
- **Function `pick_object(self)`**: This function orchestrates the picking process. It first opens the gripper (`ungrip`), moves the arm to the 'down' position to reach the object (`move_arm` with `pos_name='down'`), closes the gripper to secure the object (`grip`), and then lifts the arm back up (`move_arm` with `pos_name='up'`).

### Moving to the Desired Destination (AR Tag) with the Colored Object

#### Description
After picking up the object, the robot locates the specified AR tag and navigates towards it. This includes continuously detecting the tag and adjusting the robot's trajectory to ensure it remains aligned with the tag.

#### Code Implementation
- **Part of `image_callback(self, msg)` and `go_to(self, px_error)`**: These functions are used again to detect the AR tag and adjust the robot's movement. The `find_ar_tag` function is invoked within `image_callback` to identify AR tags, and based on the tag's position, `go_to` is used to navigate towards it.

### Putting the Colored Object Back Down at the Desired Destination

#### Description
Upon reaching the designated AR tag, the robot performs the sequence to release the colored object. This involves positioning the arm and opening the gripper to place the object down gently.

#### Code Implementation
- **Function `drop_object(self)`**: Manages the release of the object. It moves the arm back to the 'down' position to lower the object (`move_arm` with `pos_name='down'`), opens the gripper to release it (`ungrip`), and then resets the arm to a neutral position (`move_arm` with `pos_name='reset'`).

<a name="Video"></a>
## Video

There was camera lag so there was some spinning due to the lag when getting the blue roll, but it evenutally worked showing that the code is resillient to lag.


https://github.com/Intro-Robotics-UChicago-Spring-2024/q-learning-project-reece-david/assets/77137055/c3cbb89f-125e-40de-879e-14e506708c73



<a name="challenges"></a>
## Challenges

During the project, we faced several challenges, particularly in the integration of different subsystems such as vision-based perception, movement control, and object manipulation. One significant challenge was achieving reliable object detection under varying lighting conditions, which initially led to inconsistent behavior during object manipulation tasks. We addressed this by refining our HSV thresholds and incorporating dynamic adjustments based on real-time environmental feedback. Additionally, precise control in navigation to approach and align with AR tags proved difficult due to latency and mechanical limitations of the robot's actuators. To mitigate these issues, we implemented more robust error handling and feedback loops in our control algorithms, enhancing the robot's responsiveness and accuracy.

<a name="Future"></a>
## Future Work

If provided with more time, several enhancements could be made to improve the robot's performance and capabilities. Firstly, integrating machine learning techniques for more sophisticated object recognition could address issues with object detection accuracy and robustness, especially in complex environments. Additionally, we would explore advanced path planning algorithms to optimize the robot's navigation around obstacles and through crowded spaces. This would involve using sensor fusion techniques to combine data from multiple sources, such as LiDAR and cameras, to create a more comprehensive perception system. Finally, improving the user interface for easier monitoring and control during operations could enhance usability and efficiency.

<a name="takeaway"></a>
## Takeaways

- **Thorough Testing and Incremental Development**: One key takeaway is the importance of thorough testing and incremental development in robotics projects. Initially, integrating all components at once led to overwhelming debugging tasks. By breaking down the project into smaller, manageable parts and integrating them step-by-step, we were better able to identify and fix issues systematically, which saved time and reduced complexity in troubleshooting.
  
- **Collaboration and Knowledge Sharing**: Another significant takeaway is the value of effective collaboration and knowledge sharing when working in pairs. Throughout this project, maintaining clear communication and dividing tasks based on individual strengths and learning goals not only accelerated our progress but also deepened our understanding of different aspects of the project. Regularly scheduled meetings to discuss progress, challenges, and next steps were crucial in keeping the project on track and ensuring both members were aligned and informed.
