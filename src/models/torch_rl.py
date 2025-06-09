"""
torch_rl.py

Module: PyTorch Reinforcement Learning Agent
Author: Corey Leath

Implements a DQN agent in PyTorch to generate trading signals based
on historical market data. Trains with a simple replay buffer.
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import pandas as pd

class DQNAgent(nn.Module):
    def __init__(self, state_dim, action_dim):
        """
        Args:
            state_dim (int): Dimension of the state space.
            action_dim (int): Number of possible actions.
        """
        super(DQNAgent, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.net(x)

def load_data():
    """
    Load features CSV and prepare state-action pairs.
    Returns:
        states (np.ndarray), next_states (np.ndarray), rewards (np.ndarray)
    """
    df = pd.read_csv("data/processed/features.csv", parse_dates=['timestamp'])
    # Example: use close price returns as reward
    prices = df['close'].values
    returns = np.diff(prices) / prices[:-1]
    states = returns[:-1].reshape(-1, 1)
    next_states = returns[1:].reshape(-1, 1)
    # Simplify: reward = next return, action space=3 (buy/hold/sell)
    rewards = next_states.flatten()
    return states, next_states, rewards

def train_agent(num_episodes=100, batch_size=32, gamma=0.99):
    # Prepare environment data
    states, next_states, rewards = load_data()
    state_dim = states.shape[1]
    action_dim = 3  # buy, hold, sell

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    agent = DQNAgent(state_dim, action_dim).to(device)
    optimizer = optim.Adam(agent.parameters(), lr=1e-3)
    criterion = nn.MSELoss()
    memory = deque(maxlen=10000)

    # Populate initial memory
    for i in range(len(states)):
        action = random.randrange(action_dim)
        memory.append((states[i], action, rewards[i], next_states[i]))

    # Training loop
    for episode in range(num_episodes):
        batch = random.sample(memory, batch_size)
        state_batch = torch.tensor([b[0] for b in batch], dtype=torch.float32).to(device)
        action_batch = torch.tensor([b[1] for b in batch], dtype=torch.long).to(device)
        reward_batch = torch.tensor([b[2] for b in batch], dtype=torch.float32).to(device)
        next_state_batch = torch.tensor([b[3] for b in batch], dtype=torch.float32).to(device)

        # Compute Q-values and targets
        q_values = agent(state_batch).gather(1, action_batch.unsqueeze(1)).squeeze()
        with torch.no_grad():
            next_q_values = agent(next_state_batch).max(1)[0]
        target_q = reward_batch + gamma * next_q_values

        # Optimize
        loss = criterion(q_values, target_q)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (episode + 1) % 10 == 0:
            print(f"[RL] Episode {episode+1}/{num_episodes}, Loss: {loss.item():.4f}")

    # Save agent
    os.makedirs("models", exist_ok=True)
    model_path = "models/torch_rl_agent.pth"
    torch.save(agent.state_dict(), model_path)
    print(f"[RL] Saved DQN agent to {model_path}")

def main():
    train_agent()

if __name__ == "__main__":
    main()

git add src/models/torch_rl.py
git commit -m "Add PyTorch DQN reinforcement learning agent module"
git push
