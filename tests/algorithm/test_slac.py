import pytest

from rljax.algorithm.slac import SLAC, SlacObservation


def _test_slac(env, algo):
    ob = SlacObservation(env.observation_space, env.action_space, 8)
    state = env.reset()
    ob.reset_episode(state)
    algo.buffer.reset_episode(state)

    # Test step() method.
    algo.step(env, ob)

    # Test select_action() method.
    action = algo.select_action(ob)
    assert env.action_space.contains(action)

    # Test is_update() method.
    assert isinstance(algo.is_update(), bool)


@pytest.mark.mujoco
@pytest.mark.slow
@pytest.mark.parametrize("d2rl", [(False), (True)])
def test_slac(d2rl):
    from rljax.env.mujoco.dmc import make_dmc_env

    env = make_dmc_env("cheetah", "run", 4, 1, 64)
    algo = SLAC(
        num_agent_steps=100000,
        state_space=env.observation_space,
        action_space=env.action_space,
        seed=0,
        d2rl=d2rl,
    )
    _test_slac(env, algo)