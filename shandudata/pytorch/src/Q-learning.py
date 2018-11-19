import numpy as np
import random

reward = np.array([[0, -10, 0, -1, -1],
                   [0, 10, -1, 0, -1],
                   [-1, 0, 0, 10, -10],
                   [-1, 0, -10, 0, 10]])

q_matrix = np.zeros((4, 5))


transition_matrix = np.array([[-1, 2, -1, 1, 0],
                              [-1, 3, 0, -1, 1],
                              [0, -1, -1, 3, 2],
                              [1, -1, 2, -1, 3]])

valid_actions = np.array([[1, 3, 4],
                          [1, 2, 4],
                          [0, 3, 4],
                          [0, 2, 4]])

gamma = 0.8

for i in range(10):
    start_state = np.random.choice([0, 1, 2], size=1)[0] # 随机初始起点
    current_state = start_state
    while current_state != 3: # 判断是否到达终点
        action = random.choice(valid_actions[current_state]) # greedy 随机选择当前状态下的有效动作
        next_state = transition_matrix[current_state][action] # 通过选择的动作得到下一个状态
        future_rewards = []
        for action_nxt in valid_actions[next_state]:
            future_rewards.append(q_matrix[next_state][action_nxt]) # 得到下一个状态所有可能动作的奖励
        q_state = reward[current_state][action] + gamma * max(future_rewards) # bellman equation
        q_matrix[current_state][action] = q_state # 更新 q 矩阵
        current_state = next_state # 将下一个状态变成当前状态
        
    print('episode: {}, q matrix: \n{}'.format(i, q_matrix))
    print()
    