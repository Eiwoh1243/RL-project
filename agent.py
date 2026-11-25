import torch
from torch import nn
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
import numpy as np
from quoridor_env.quoridor_sim.quoridor_env import QuoridorEnv
from visual import draw_board
import copy
import random
from collections import deque
from pathlib import Path
import json
import pickle
import time

## ---- Constants ---- ##
# Free to change
invalid_reward,valid_reward = -2.5,0.5
win_reward,lose_reward = 20,-20

env = QuoridorEnv()
env.reset()
state = env.game.get_state()

# -------------------------------------------------------------- Model and Replay Buffer -------------------------------------------------------------- #

class Agent(nn.Module):
    def __init__(self,turn):
        super().__init__()
        self.turn = turn
        self.cnnh = nn.Sequential(
            nn.Conv2d(1,16,kernel_size=2,stride=1,padding=0),
            nn.ReLU(),
            nn.Conv2d(16,16,kernel_size=2,stride=1,padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Flatten(),
        )
        self.cnnv = nn.Sequential(
            nn.Conv2d(1,16,kernel_size=2,stride=1,padding=0),
            nn.ReLU(),
            nn.Conv2d(16,16,kernel_size=2,stride=1,padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Flatten(),
        )
        self.action0 = nn.Sequential(
            nn.Linear(294,256),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.Sigmoid(),
            nn.Linear(256,256),
            nn.ReLU(),
        )
        self.action1 = nn.Sequential(
            nn.Linear(256,256),
            nn.ReLU(),
            nn.Linear(256,256),
            nn.Sigmoid(),
            nn.Linear(256,256),
            nn.ReLU(),
            nn.Linear(256,243),
        )

    def forward(self, Estate: torch.Tensor) -> torch.Tensor:
        splt = torch.split(Estate,81)
        hwalls,vwalls,rest = splt[0].reshape((-1,1,9,9)),splt[1].reshape((-1,1,9,9)),splt[2].reshape((-1,6))
        h_res, v_res, rest = self.cnnh(hwalls), self.cnnv(vwalls), rest
        X = torch.cat((h_res,v_res,rest),dim=1)
        return self.action1(self.action0(X))

class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)
        self.saved = None

    def push(self, Estate, action, reward, Enext_state, done):
        self.buffer.append(
            (Estate, action, reward, Enext_state, done)
        )

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        """ if self.saved == None:
            self.saved = random.sample(self.buffer, batch_size)
        batch = self.saved """

        states, actions, rewards, next_states, dones = zip(*batch)

        return (
            torch.stack(states).permute((1,0)),
            torch.stack(actions).squeeze(),
            torch.stack(rewards),
            torch.stack(next_states).permute((1,0)),
            torch.stack(dones),
        )

    def __len__(self):
        return len(self.buffer)
    
    def count(self):
        counts = torch.zeros(243)

        for sample in self.buffer:
            counts[sample[1].item()] += 1

        return counts

# -------------------------------------------------------------- Training Functions -------------------------------------------------------------- #

def models_equal(model1, model2):
    sd1 = model1.state_dict()
    sd2 = model2.state_dict()

    if sd1.keys() != sd2.keys():
        return False

    for key in sd1:
        if not torch.equal(sd1[key], sd2[key]):
            return False

    return True

def encode(state: dict) -> torch.Tensor:
    """
    Encodes the state dict, provided by `env.game.get_state() -> state: dict`, into a torch tensor as input for the models

    Args:
        state (dict): State of the environment
    Returns:
        torch.Tensor: Of size 243
    """

    hwalls = [
        # Blocks Vertical
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
    ]
    vwalls = [
        # Blocks Horizontal
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
    ]
    for (y,x) in state["horiz_walls"]:
        hwalls[x][y] = 1
        hwalls[x][y+1] = 1
    for (x,y) in state["vert_walls"]:
        vwalls[x][y] = 1
        vwalls[x][y+1] = 1

    Estate = torch.cat(
        (
            torch.Tensor(hwalls).reshape((-1,)),
            torch.Tensor(vwalls).reshape((-1,)),
            torch.Tensor(state["positions"]).reshape((-1,)),
            torch.Tensor(state["walls_remaining"]),
        ),
        dim=0)
    return Estate

def distance(player: int) -> int:
    """
    Calculates the distance of `player` to the `_check_win_condition` of the game environment

    Args:
        player (int): The integer associated with the given player
    Returns:
        int: Distance to the nearest win position
    """

    ## Copied and modified from env.game._can_reach_goal()
    board = env.game.board
        
    start = env.game.positions[player]
    queue = deque([start])
    visited = {start}
    distance = -1
    
    while queue:
        old_queue = copy.deepcopy(queue)
        new_queue = deque([])
        while old_queue:
            x, y = old_queue.popleft()
            
            # Check if current position satisfies win condition
            if env.game._check_win_position(player, (x, y)):
                return distance
                
            # Explore all adjacent positions
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                # Check bounds
                if not (0 <= nx < env.game.board_size and 0 <= ny < env.game.board_size):
                    continue
                    
                # Check if already visited
                if (nx, ny) in visited:
                    continue
                    
                # Check for wall blocking
                if board.wall_blocks((x, y), (nx, ny)):
                    continue
                    
                # Check if position is occupied (simple check)
                if (nx, ny) in env.game.positions:
                    continue
                    
                visited.add((nx, ny))
                new_queue.append((nx, ny))

        distance += 1
        queue = copy.deepcopy(new_queue)
    
    return

def action_selection(model: Agent, epsilon=0.7, check=False) -> int:
    """
    Returns the action selected, either by the model, or by random choice. With `epsilon` denoting the probability of choosing at random.

    Args:
        model (Agent): The model/agent that will 'select' the action
        epsilon (int): The probability of choosing at random, instead of choosing using the model
        check (int): Used to check the return of the model
    Returns:
        int: The action selected
    """

    if np.random.rand() > 0.7 or check:
        Estate = encode(env.game.get_state())
        if check:
            with torch.no_grad():
                ret = model(Estate)
                print(ret)
                print(ret.max() - ret.min())
            return torch.argmax(ret)
        else:
            action = torch.argmax(model(Estate))
            return int(action)
    else:
        legact = random.choice(env.game.legal_moves())
        action = 0
        action += 0 if legact[0] == "move" else 81
        try:
            action += 0 if legact[3] == "v" else 81
        except IndexError:
            pass
        action += legact[1] * 9 + legact[2]
        return int(action)

def perform(turn: int, action: int, replay: ReplayBuffer) -> None:
    """
    Performs the `action` selected for the given `turn` onto the game environment, pushes the replay into the specified `replay` buffer

    Args:
        turn (int): The turn/integer associated with the model
        action (int): The action to perform
        replay (ReplayBuffer): The model's associated replay buffer
    """

    global invalid_reward,valid_reward,win_reward,lose_reward
    if action < 81:
        ## Move
        x = int(action // 9)
        y = int(action % 9)
        parsed = ("move",x,y)
    else:
        temp = action - 81
        if temp < 81:
            x = int(temp // 9)
            y = int(temp % 9)
            parsed = ("wall",x,y,"v")
        else:
            temp -= 81
            x = int(temp // 9)
            y = int(temp % 9)
            parsed = ("wall",x,y,"h")

    state = env.game.get_state()
    try:
        env.game.step(parsed)
        new_state = env.game.get_state()
        if new_state['winner'] != None and new_state['winner'] == turn:
            reward = win_reward
            done = 1
        elif new_state['winner'] != None:
            reward = lose_reward
            done = 1
        else:
            d1 = distance(int((turn+1)%2))
            d2 = distance(turn)
            reward = valid_reward + (d1 if d1 != None else 0) - (d2 if d2 != None else invalid_reward)
            done = 0
        replay.push(
            encode(state),
            torch.IntTensor([action]),
            torch.Tensor([reward]),
            encode(new_state),
            torch.Tensor([done]))
    except ValueError:
        d1 = distance(int((turn+1)%2))
        d2 = distance(turn)
        reward = invalid_reward + (d1 if d1 != None else 0) - (d2 if d2 != None else invalid_reward)
        replay.push(
            encode(state),
            torch.IntTensor([action]),
            torch.Tensor([reward]),
            encode(env.game.get_state()),
            torch.Tensor([0]))

def train_step(current_net: Agent, target_net: Agent, replay_buffer: ReplayBuffer, batch_size: int=25000, gamma: float=0.99) -> int:
    """
    Performs a 'training step', and updates the model according to how DQNs operate

    Args:
        current_net (Agent): The main DQN
        target_net (Agent): The target DQN
        replay_buffer (ReplayBuffer): The model's replay buffer
        batch_size (int): The population of the batch
        gamma (float): Weight of how important future Q-values are
    Returns:
        int: The loss during this training step
    """

    if len(replay_buffer) < batch_size:
        return current_net

    optimizer = torch.optim.Adam(current_net.parameters(),lr=0.01)

    states, actions, rewards, next_states, dones = (
        replay_buffer.sample(batch_size)
    )
    #before = current_net.action[10].weight.clone()

    # Q(s,a)
    current_q = current_net(states)
    current_q = current_q.gather(1,actions.unsqueeze(1)).squeeze(1)

    with torch.no_grad():
        next_q = target_net(next_states).max(dim=1)[0]

        target_q = rewards + gamma * next_q * (1 - dones)

    loss = ((current_q - target_q) ** 2).mean()

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    #print("current_q =", current_q[:10])
    #print("target_q  =", target_q[:10][0])
    """ after = current_net.action[10].weight
    print((after - before).abs().mean())
    print(loss) """

    return loss.item()

## Main
def training(arep: ReplayBuffer=None, brep: ReplayBuffer=None, save_model: bool=True) -> (Agent, Agent):
    """
    Main training loop

    Args:
        arep (Agent): Initialized replay buffer for model 'a'
        brep (Agent): Initialized replay buffer for model 'b'
        save_model (bool): Sets whether the trained models will be saved into the `/model` directory
    Returns:
        Agent: Trained model 'a'
        Agent: Trained model 'b'
    """

    batch_size = 25000

    ac = Agent(0)
    at = copy.deepcopy(ac)
    if arep == None:
        arep = ReplayBuffer()

    bc = Agent(1)
    bt = copy.deepcopy(bc)
    if brep == None:
        brep = ReplayBuffer()
    times = []

    print("Training:")
    for game in tqdm(range(30)):
        aloss,bloss = [],[]
        env.reset()
        for i in range(100):
            action = action_selection(ac,0)
            perform(ac.turn, action, arep)

            if env.game.get_state()["winner"] != None:
                break

            action = action_selection(bc,0)
            perform(bc.turn, action, brep)

            if env.game.get_state()["winner"] != None:
                break
        times.append(i)

        if game % 2 == 0:
            #before = action_selection(ac,True)
            #ac = train_step(ac,at,arep,batch_size)
            loss = train_step(ac,at,arep,batch_size)
            at = copy.deepcopy(ac)
            aloss.append(loss)
            #after = action_selection(ac,True)
            #print((after - before).abs().mean())

            #bc = train_step(bc,bt,brep,batch_size)
            loss = train_step(bc,bt,brep,batch_size)
            bt = copy.deepcopy(bc)
            bloss.append(loss)

    print(times)
    
    if save_model:
        save_models()
    
    return ac,bc

# -------------------------------------------------------------- Replay Buffers -------------------------------------------------------------- #

def pre_buffer():
    """
    Initializes a replay buffer for both models. Ensures that every action has at least 200 replay instances, for better training. Saved into a pickle file in `/buffers`
    """

    arep,brep = ReplayBuffer(),ReplayBuffer()
    env.reset()
    selected = 0
    print("Pre_Buffer:")
    for i in tqdm(range(50)):
        print(f"Episode {i}")
        for _ in tqdm(range(1000)):
            perform(0,(selected % 243),arep)
            if env.game.get_state()["winner"] == None:
                env.reset()

            perform(1,(selected % 243),brep)
            if env.game.get_state()["winner"] == None:
                env.reset()

            selected += 1

    buffer_dir = Path("buffers")
    buffer_dir.mkdir(parents=True,exist_ok=True)

    buffer_pth = buffer_dir / "arep.pkl"
    with open(buffer_pth, "wb") as f:
        pickle.dump(arep, f)
    
    buffer_pth = buffer_dir / "brep.pkl"
    with open(buffer_pth, "wb") as f:
        pickle.dump(brep, f)

def load_buffer() -> (ReplayBuffer, ReplayBuffer):
    """
    Loads and returns the buffers from `/buffers`

    Returns:
        ReplayBuffer: Replay buffer for model 'a'
        ReplayBuffer: Replay buffer for model 'b'
    """

    buffer_dir = Path("buffers")
    buffer_dir.mkdir(parents=True,exist_ok=True)

    buffer_pth = buffer_dir / "arep.pkl"
    with open(buffer_pth, "rb") as f:
        arep = pickle.load(f)
    
    buffer_pth = buffer_dir / "brep.pkl"
    with open(buffer_pth, "rb") as f:
        brep = pickle.load(f)
    
    return arep,brep

# -------------------------------------------------------------- Saving and Loading Models -------------------------------------------------------------- #

def save_models():
    """
    Saves the (global) models `ac` and `bc` into `/models`
    """
    MODEL_DIR = Path("models")
    MODEL_DIR.mkdir(parents=True,exist_ok=True)

    MODEL_FILE_NAME = "ac_0.pth"
    MODEL_FILE_PATH = MODEL_DIR / MODEL_FILE_NAME
    torch.save(obj=ac,f=MODEL_FILE_PATH)

    MODEL_FILE_NAME = "bc_0.pth"
    MODEL_FILE_PATH = MODEL_DIR / MODEL_FILE_NAME
    torch.save(obj=bc,f=MODEL_FILE_PATH)

def load_models(names=("ac_0","bc_0")) -> (Agent, Agent):
    """
    Loads the models `ac` and `bc` from `/models`

    Returns:
        Agent: Model `ac`
        Agent: Model `bc`
    """
    ac = Agent(0)
    bc = Agent(1)

    MODEL_DIR = Path("models")
    MODEL_DIR.mkdir(parents=True,exist_ok=True)

    MODEL_FILE_NAME = names[0]+".pth"
    MODEL_FILE_PATH = MODEL_DIR / MODEL_FILE_NAME
    ac = torch.load(MODEL_FILE_PATH,weights_only=False)

    MODEL_FILE_NAME = names[1]+".pth"
    MODEL_FILE_PATH = MODEL_DIR / MODEL_FILE_NAME
    bc = torch.load(MODEL_FILE_PATH,weights_only=False)

    return ac, bc

# -------------------------------------------------------------- Training -------------------------------------------------------------- #

## Leave commented, used to create the initial replay buffer (to accelerate learning)
#pre_buffer()

""" arep,brep = load_buffer()
ac,bc = training() """

# Leave un-comment for Testing to work
#exit(0)

# -------------------------------------------------------------- Testing Functions -------------------------------------------------------------- #

env = QuoridorEnv()
env.reset()

def perform(turn: int, actions: torch.Tensor, index: int=-1):
    """
    Overrides the old `perform()` function, to suit for testing purposes

    Args:
        turn (int): Turn/Integer associated with the give model
        actions (torch.Tensor): Tensor of actions sorted after `torch.argsort()` is applied
        index: Index for obtaining the specified action
    """

    action = actions[0][index]
    if action < 81:
        ## Move
        x = int(action // 9)
        y = int(action % 9)
        parsed = ("move",x,y)
    else:
        temp = action - 81
        if temp < 81:
            x = int(temp // 9)
            y = int(temp % 9)
            parsed = ("wall",x,y,"v")
        else:
            temp -= 81
            x = int(temp // 9)
            y = int(temp % 9)
            parsed = ("wall",x,y,"h")
    try:
        env.game.step(parsed)
    except ValueError:
        perform(turn,actions,index-1)

def action_selection(model: Agent) -> torch.Tensor:
    """
    Overrides the old `action_selection()` function, to suit for testing purposes

    Args:
        model (Agent): The given model
    Returns:
        torch.Tensor: Tensor of actions, sorted from least probable to most probable, according to the model's return
    """
    Estate = encode(env.game.get_state())
    actions = torch.argsort(model(Estate))
    return actions

## Main
def play_game(ac: Agent, bc: Agent):
    """
    Main testing loop

    Args:
        ac (Agent): Model `ac`
        bc (Agent): Model `bc`
    """

    for iter in range(30):
        actions = action_selection(ac)
        perform(ac.turn, actions)

        if env.game.get_state()["winner"] != None:
            break

        actions = action_selection(bc)
        perform(bc.turn, actions)

        if env.game.get_state()["winner"] != None:
            break

        draw_board(env.game.get_state())
        time.sleep(0.5)

# -------------------------------------------------------------- Testing -------------------------------------------------------------- #

# Un-comment to load, and test the models
""" ac,bc = load_models()
play_game(ac,bc) """

