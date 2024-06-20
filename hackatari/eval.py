# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
import random
import matplotlib.pyplot as plt
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from hackatari.core import HackAtari
from ocatari import OCAtari
from ocatari.vision.utils import mark_bb, make_darker
from ocatari.vision.spaceinvaders import objects_colors
from ocatari.vision.pong import objects_colors
from ocatari.utils import load_agent, parser, make_deterministic
import time

parser.add_argument("-g", "--game", type=str, required=True,
                    help="game to evaluate (e.g. 'Pong')")
parser.add_argument('-m', '--modifs', nargs='+', default=[],
                    help='List of the modifications to be brought to the game')
parser.add_argument('-t', '--track', type=bool, required=False, default=True)   

opts = parser.parse_args()

if opts.track:
    import wandb
    model_name = opts.path.split('.')[0]
    run_name = f"{model_name}_{opts.game}_org"
    run = wandb.init(
        project="HackAtari_eval_f25",
        name=run_name,
        monitor_gym=True,
        save_code=False,
    )


#env_org = HackAtari(opts.game, render_mode='rgb_array', obs_mode='dqn')
env_hacked = HackAtari(opts.game, opts.modifs, render_mode="rgb_array", obs_mode="dqn")

# RUN env_org
# env = env_org
# observation, info = env.reset()

# if opts.path:
#     agent = load_agent(opts, env.action_space.n)
#     print(f"{opts.game}: Loaded agents from {opts.path}")

# for i in range(11):
#     done = False
#     crew = 0
#     while not done:
#         action = agent.draw_action(env.dqn_obs)
#         obs, reward, terminated, truncated, info = env.step(action)
#         crew += reward

#         if terminated or truncated:
#             print(f"{opts.game} (O): Reward is episode {i} is", crew, f"Length is episode {i} is",info["episode_frame_number"])
#             if opts.track:
#                 run.log({f"{opts.game}_reward": crew, f"{opts.game}_episode_length": info["episode_frame_number"]})
#             observation, info = env.reset()
#             done = True

# env.close()
if opts.track:
#     run.finish()


    model_name = opts.path.split('.')[0]
    run_name = f"{model_name}_{opts.game}_hack"
    run = wandb.init(
        project="HackAtari_eval_f25",
        name=run_name,
        monitor_gym=True,
        save_code=False,
    )
env = env_hacked
obs, info = env.reset()

if opts.path:
    agent = load_agent(opts, env.action_space.n)
    #print(f"Loaded agents from {opts.path}")

for i in range(11):
    done = False
    crew = 0
    while not done:
        #import ipdb; ipdb.set_trace()
        action = agent.draw_action(env.dqn_obs)
        obs, reward, terminated, truncated, info = env.step(action)
        crew += reward

        if terminated or truncated:
            print(f"{opts.game} (H): Reward is episode {i} is", crew, f"Length is episode {i} is",info["episode_frame_number"])
            if opts.track:
                run.log({f"{opts.game}_reward": crew, f"{opts.game}_episode_length": info["episode_frame_number"]})
            observation, info = env.reset()
            done = True

env.close()
if opts.track:
    run.finish()
