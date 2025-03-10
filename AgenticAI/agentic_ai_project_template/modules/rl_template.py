import gym

# Initialize the environment
env = gym.make("CartPole-v1")
state = env.reset()

# Simulate agent's decision-making process
for step in range(100):
    env.render()
    action = env.action_space.sample()  # Random action
    next_state, reward, done, _ = env.step(action)

    if done:
        state = env.reset()
env.close()