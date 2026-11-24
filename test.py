
from quoridor_sim.quoridor_env import QuoridorEnv

env = QuoridorEnv()

print("Quoridor environment created!")
print("Observation:", env.observation_space)
print("Actions:", env.action_space)
