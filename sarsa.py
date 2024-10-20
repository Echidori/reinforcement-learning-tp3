from collections import defaultdict
import random
import typing as t
import numpy as np
import gymnasium as gym


Action = int
State = int
Info = t.TypedDict("Info", {"prob": float, "action_mask": np.ndarray})
QValues = t.DefaultDict[int, t.DefaultDict[Action, float]]


class SarsaAgent:
    def __init__(
        self,
        learning_rate: float,
        gamma: float,
        legal_actions: t.List[Action],
    ):
        """
        SARSA  Agent

        You shoud not use directly self._qvalues, but instead of its getter/setter.
        """
        self.legal_actions = legal_actions
        self._qvalues: QValues = defaultdict(lambda: defaultdict(int))
        self.learning_rate = learning_rate
        self.gamma = gamma

    def get_qvalue(self, state: State, action: Action) -> float:
        """
        Returns Q(state,action)
        """
        return self._qvalues[state][action]

    def set_qvalue(self, state: State, action: Action, value: float):
        """
        Sets the Qvalue for [state,action] to the given value
        """
        self._qvalues[state][action] = value

    def get_value(self, state: State) -> float:
        """
        Compute your agent's estimate of V(s) using current q-values
        V(s) = max_a Q(s, a) over possible actions.
        """
        value = 0.0
        # BEGIN SOLUTION
        possible_q_values = [self.get_qvalue(state, action) for action in self.legal_actions]
        value = max(possible_q_values) if possible_q_values else 0.0
        # END SOLUTION
        return value

    def update(
        self, state: State, action: Action, reward: t.SupportsFloat, next_state: State
    ):
        """
        You should do your Q-Value update here (s'=next_state):
           TD_target(s') = R(s, a) + gamma * V(s')
           TD_error(s', a) = TD_target(s') - Q(s, a)
           Q_new(s, a) := Q(s, a) + alpha * TD_error(s', a)
        """
        q_value = 0.0
        # BEGIN SOLUTION
        next_action = self.get_action(next_state)
        current_q = self.get_qvalue(state, action)
        next_q = self.get_qvalue(next_state, next_action)
        q_value = current_q + self.learning_rate * (float(reward) + self.gamma * next_q - current_q)
        # END SOLUTION

        self.set_qvalue(state, action, q_value)

    def get_best_action(self, state: State) -> Action:
        """
        Compute the best action to take in a state (using current q-values).
        """
        possible_q_values = [
            self.get_qvalue(state, action) for action in self.legal_actions
        ]
        index = np.argmax(possible_q_values)
        best_action = self.legal_actions[index]
        return best_action

    def get_action(self, state: State) -> Action:
        """
        Compute the action to take in the current state, including exploration.
        """
        action = self.legal_actions[0]

        # BEGIN SOLUTION
        epsilon = 0.1
        if random.random() < epsilon:
            action = random.choice(self.legal_actions)
        else:
            action = self.get_best_action(state)
        # END SOLUTION

        return action
