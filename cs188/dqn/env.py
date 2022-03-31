import gym
from model.dqn import DQN
import torch
import random

Action_space = 2
State_space = 3
Learning_rate = 1e-3

def get_action(env, action_prob):
    if random.random() < 0.3:
        return env.action_space.sample()
    else:
        return env.action_space

if __name__ == '__main__':
    env = gym.make('CartPole-v0')
    print(env.observation_space)
    print(env.action_space)
    dqn_net = DQN(Action_space, State_space, Learning_rate)
    optim = torch.optim.SGD(dqn_net.parameters(), lr=dqn_net.learning_rate)
    loss_fn = torch.nn.MSELoss()

    for _ in range(1000):
        env.render()
        env.step(env.action_space.sample())
    env.close()


    env.reset()

    # for _ in range(100):
    #     env.render()
    #     env.step(env.action_space.sample())
    # env.close()








