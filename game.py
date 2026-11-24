
from quoridor_sim.quoridor_env import QuoridorEnv
from visual import draw_board

# Create environment
env = QuoridorEnv()

# Reset game
env.reset()

# Get actual game state
state = env.game.get_state()
print(env.game.get_state())
print(env.game.legal_moves())
env.game.step(("wall", 0, 2, 'h'))
state = env.game.get_state()

# Visualise
draw_board(state)
