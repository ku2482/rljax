**WARNING: Rljax is currently in a beta version and being actively improved. Any contributions are welcome :)**

# RL Algorithms in JAX
Rljax is a collection of RL algorithms written in JAX.

## Setup
You can install dependencies simply by executing the following. To use GPUs, CUDA (10.0, 10.1, 10.2 or 11.0) must be installed.
```bash
pip install https://storage.googleapis.com/jax-releases/`nvcc -V | sed -En "s/.* release ([0-9]*)\.([0-9]*),.*/cuda\1\2/p"`/jaxlib-0.1.55-`python3 -V | sed -En "s/Python ([0-9]*)\.([0-9]*).*/cp\1\2/p"`-none-manylinux2010_x86_64.whl jax==0.2.0
pip install -e .
```

If you don't have a GPU, please executing the following instead.
```bash
pip install jaxlib==0.1.55 jax==0.2.0
pip install -e .
```

If you want to use a [MuJoCo](http://mujoco.org/) physics engine, please install [mujoco-py](https://github.com/openai/mujoco-py).
```bash
pip install mujoco_py==2.0.2.11
```

## Algorithm
Currently, following algorithms have been implemented.

| **Algorithm** | **Action Space** | **Vector State** | **Pixel State** | **PER**[[11]](#reference) | **DisCor**[[12]](#reference) |
| :--                            | :--                | :--:               | :--:               | :--:                       | - |
| PPO[[1]](#reference)           | Continuous         | :heavy_check_mark: | -                  | -                          | - |
| DDPG[[2]](#reference)          | Continuous         | :heavy_check_mark: | -                  | :heavy_check_mark:         | - |
| TD3[[3]](#reference)           | Continuous         | :heavy_check_mark: | -                  | :heavy_check_mark:         | - |
| SAC[[4,5]](#reference)         | Continuous         | :heavy_check_mark: | -                  | :heavy_check_mark:         | :heavy_check_mark: |
| DQN[[6]](#reference)           | Discrete           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:         | :heavy_check_mark: |
| QR-DQN[[7]](#reference)        | Discrete           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:         | - |
| IQN[[8]](#reference)           | Discrete           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:         | - |
| FQF[[9]](#reference)           | Discrete           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:         | - |
| SAC-Discrete[[10]](#reference) | Discrete           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:         | - |

## Example
All algorithms can be trained in a few lines of codes.

<details>
<summary>Getting started</summary>

Here is a quick example of how to train DQN on `CartPole-v0`.

```Python
import gym

from rljax.algorithm import DQN
from rljax.trainer import Trainer

NUM_STEPS = 20000
SEED = 0

env = gym.make("CartPole-v0")
env_test = gym.make("CartPole-v0")

algo = DQN(
    num_steps=NUM_STEPS,
    state_space=env.observation_space,
    action_space=env.action_space,
    seed=SEED,
    batch_size=256,
    start_steps=1000,
    update_interval=1,
    update_interval_target=400,
    eps_decay_steps=0,
    loss_type="l2",
    lr=1e-3,
)

trainer = Trainer(
    env=env,
    env_test=env_test,
    algo=algo,
    log_dir="/tmp/rljax/dqn",
    num_steps=NUM_STEPS,
    eval_interval=1000,
    seed=SEED,
)
trainer.train()
```

</details>

<details>
<summary>Simple examples</summary>

Below shows that our algorithms successfully learning the discrete action environment `CartPole-v0` ([code](https://github.com/ku2482/rljax/blob/master/examples/train_continuous_easy.py)) and the continuous action environment `InvertedPendulum-v2` ([code](https://github.com/ku2482/rljax/blob/master/examples/train_discrete_easy.py)).

<img src="https://user-images.githubusercontent.com/37267851/94993592-08dbf700-05cd-11eb-8bf0-a40f8e0567d0.png" title="CartPole-v0" width=400><img src="https://user-images.githubusercontent.com/37267851/94993625-4fc9ec80-05cd-11eb-8c2d-a0bf0c791086.png" title="InvertedPendulum-v2" width=400>

</details>

<details>
<summary>MuJoCo(Gym)</summary>

I benchmarked my implementations in environments from MuJoCo's `-v3` task suites, following [Spinning Up's benchmarks](https://spinningup.openai.com/en/latest/spinningup/bench.html) ([code](https://github.com/ku2482/rljax/blob/master/examples/train_mujoco.py)).

<img src="https://user-images.githubusercontent.com/37267851/94887999-b0b0d200-04b2-11eb-9a37-7e2b87dfa71a.png" title="HalfCheetah-v3" width=400><img src="https://user-images.githubusercontent.com/37267851/94888002-b1e1ff00-04b2-11eb-87da-243f39d325b6.png" title="Walker2d-v3" width=400>

</details>


## Reference
[[1]](https://arxiv.org/abs/1707.06347) Schulman, John, et al. "Proximal policy optimization algorithms." arXiv preprint arXiv:1707.06347 (2017).

[[2]](https://arxiv.org/abs/1509.02971) Lillicrap, Timothy P., et al. "Continuous control with deep reinforcement learning." arXiv preprint arXiv:1509.02971 (2015).

[[3]](https://arxiv.org/abs/1802.09477) Fujimoto, Scott, Herke Van Hoof, and David Meger. "Addressing function approximation error in actor-critic methods." arXiv preprint arXiv:1802.09477 (2018).

[[4]](https://arxiv.org/abs/1801.01290) Haarnoja, Tuomas, et al. "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor." arXiv preprint arXiv:1801.01290 (2018).

[[5]](https://arxiv.org/abs/1812.05905) Haarnoja, Tuomas, et al. "Soft actor-critic algorithms and applications." arXiv preprint arXiv:1812.05905 (2018).

[[6]](https://www.nature.com/articles/nature14236?wm=book_wap_0005) Mnih, Volodymyr, et al. "Human-level control through deep reinforcement learning." nature 518.7540 (2015): 529-533.

[[7]](https://arxiv.org/abs/1710.10044) Dabney, Will, et al. "Distributional reinforcement learning with quantile regression." Thirty-Second AAAI Conference on Artificial Intelligence. 2018.

[[8]](https://arxiv.org/abs/1806.06923) Dabney, Will, et al. "Implicit quantile networks for distributional reinforcement learning." arXiv preprint. 2018.

[[9]](https://arxiv.org/abs/1911.02140) Yang, Derek, et al. "Fully Parameterized Quantile Function for Distributional Reinforcement Learning." Advances in Neural Information Processing Systems. 2019.

[[10]](https://arxiv.org/abs/1910.07207) Christodoulou, Petros. "Soft Actor-Critic for Discrete Action Settings." arXiv preprint arXiv:1910.07207 (2019).

[[11]](https://arxiv.org/abs/1511.05952) Schaul, Tom, et al. "Prioritized experience replay." arXiv preprint arXiv:1511.05952 (2015).

[[12]](https://arxiv.org/abs/2003.07305) Kumar, Aviral, Abhishek Gupta, and Sergey Levine. "Discor: Corrective feedback in reinforcement learning via distribution correction." arXiv preprint arXiv:2003.07305 (2020).
