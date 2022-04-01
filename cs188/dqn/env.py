import gym
import torch
import random
from collections import deque
import dqnnet
import numpy as np

Action_space = 2
State_space = 4
Episode = 1000
Steps = 200
Gamma = 0.99
Experience_pool_capacity = 300
Batch_size = 32
LR = 1e-3
Epsilon = 0.3
Update_Iter = 100


class ExperiencePool(object):
    def __init__(self, capacity):
        self.experience_pool = deque([], maxlen=capacity)

    def push(self, experience):
        self.experience_pool.append(experience)

    def sample(self, batch_size):
        return random.sample(self.experience_pool, batch_size)

    def __len__(self):
        return len(self.experience_pool)


class DQN(object):
    def __init__(self):
        self.eval_dqn = dqnnet.DQNnet(State_space, Action_space)
        self.target_dqn = dqnnet.DQNnet(State_space, Action_space)
        self.update_counter = 0  # update target counter
        self.optimizer = torch.optim.RMSprop(self.eval_dqn.parameters(), lr=LR)
        self.loss_fn = torch.nn.MSELoss()
        self.experience_pool = ExperiencePool(Experience_pool_capacity)

    def select_action(self, state):
        # () -> (1, State_dim)
        state = torch.unsqueeze(torch.FloatTensor(state), 0)
        if np.random.uniform() > Epsilon:
            actions_q = self.eval_dqn(state)
            # find max_q action's index
            action = torch.max(actions_q, 1)[1].data.numpy()[0]
        else:
            action = np.random.randint(0, Action_space)
        return action

    def store_transition(self, state, action, reward, next_state):
        self.experience_pool.push([state, action, reward, next_state])

    def batch_info(self, batch_transitions):
        b_s = []
        b_a = []
        b_r = []
        b_s_ = []
        for ex in batch_transitions:
            b_s.append(ex[0])
            b_a.append(ex[1])
            b_r.append(ex[2])
            b_s_.append(ex[3])
        return torch.FloatTensor(b_s), torch.LongTensor(b_a), \
                        torch.FloatTensor(b_r), torch.FloatTensor(b_s_)

    def training(self):
        # update target parameters
        if self.update_counter % Update_Iter == 0:
            self.target_dqn.load_state_dict(self.eval_dqn.state_dict())
            print(f"{self.update_counter}: copy")
        self.update_counter += 1

        # sample batch transitions
        batch_transitions = random.sample(self.experience_pool.experience_pool, Batch_size)
        batch_state, batch_action, batch_reward, batch_next_state = \
            self.batch_info(batch_transitions)

        # TODO: eval_q is the
        print(torch.unsqueeze(batch_action, 0).shape)
        eval_q = self.eval_dqn(batch_state).gather(0, torch.unsqueeze(batch_action, 0))
        print(eval_q.shape, batch_action.shape)
        q_next_max = torch.max(self.target_dqn(batch_next_state), 1)[0].detach()
        q_target = batch_reward + Gamma * q_next_max
        loss = self.loss_fn(eval_q, q_target)
        print(f"loss: {loss}")
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


if __name__ == '__main__':
    env = gym.make('CartPole-v0')
    print(env.observation_space)
    print(env.action_space)

    dqn = DQN()

    for i in range(Episode):
        s = env.reset()
        all_reward = 0
        while True:
            env.render()
            # select an action
            a = dqn.select_action(s)
            # observe next state
            next_s, r, done, info = env.step(a)
            all_reward += r
            # store the transition
            dqn.store_transition(s, a, r, next_s)
            if len(dqn.experience_pool) > Batch_size:
                dqn.training()
                if done:
                    print(f"episode {i} ; reward {all_reward} ")
                    break
            # execute the action and move to next state
            s = next_s
    env.close()

    torch.save(dqn.target_dqn.state_dict(), "./model1.pth")
    print("save and quit")

