import numpy as np

class ColorChampsQLearning:
    def __init__(self,num_states,num_actions,learning_rate=0.1,discount_factor=0.9,exploration_prob=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob

        self.q_table = np.zeros((num_states,num_actions))

    def action(self,state):
        # epsilon-greedy strategy
        if np.random.uniform(0,1) < self.exploration_prob:
            action = np.random.choice(self.num_actions)
        else:
            action = np.argmax(self.q_table[state,:])

        return action
    
    def update_table(self,state,action,reward,next_state):
        predict = self.q_table[state,action]
        target = reward + self.discount_factor * np.max(self.q_table[next_state,:])
       self.q_table[state, action] += self.learning_rate * (target - predict)