import gym
import math
import numpy as np

from gym_ssl.grsim_ssl.grSimClient import grSimClient


class GrSimSSLEnv(gym.Env):
    """
    Using cartpole env description as base example for our documentation
    Description:
        A pole is attached by an un-actuated joint to a cart, which moves along
        a frictionless track. The pendulum starts upright, and the goal is to
        prevent it from falling over by increasing and reducing the cart's
        velocity.
    Source:
        This environment corresponds to the version of the cart-pole problem
        described by Barto, Sutton, and Anderson
    Observation:
        Type: Box(3)
        Num     Observation                  Min                     Max
        0       id 0 Blue Team Robot X       -Inf                    Inf
        1       id 0 Blue Team Robot Y       -Inf                    Inf
        2       id 0 Blue Team Robot Angle   -3.1416                 3.1416

    Actions:
        Type: Box(3)
        Num     Action                        Min                     Max
        0       id 0 Blue Team Robot Vx       -1                      1
        1       id 0 Blue Team Robot Vy       -1                      1
        2       id 0 Blue Team Robot Omega    -1                      1
        Note: The amount the velocity that is reduced or increased is not
        fixed; it depends on the angle the pole is pointing. This is because
        the center of gravity of the pole increases the amount of energy needed
        to move the cart underneath it
    Reward:
        Reward is 1 for every step taken, including the termination step
    Starting State:
        All observations are assigned a uniform random value in [-0.05..0.05]
    Episode Termination: 
        Pole Angle is more than 12 degrees.
        Cart Position is more than 2.4 (center of the cart reaches the edge of
        the display).
        Episode length is greater than 200.
        Solved Requirements:
        Considered solved when the average return is greater than or equal to
        195.0 over 100 consecutive trials.
    """

    def __init__(self):
        self.client = grSimClient()

        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        # Observation Space thresholds
        obsSpaceThresholds = np.array([np.finfo(np.float32).max,
                                       np.finfo(np.float32).max,
                                       math.pi], dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=-obsSpaceThresholds, high=obsSpaceThresholds)

        print('Environment initialized')

    def step(self, actions):
        self.client.send(actions[0], actions[1], actions[2])

        data = self.client.receive()
        while 0 not in [robot.robot_id for robot in data.detection.robots_blue]:
            data = self.client.receive()

        for robot in data.detection.robots_blue:
            if robot.robot_id == 0:
                observation = np.array([robot.x, robot.y, robot.orientation], dtype=np.float32)
        return observation, 0, False, {}

    def reset(self):
        print('Environment reset')
