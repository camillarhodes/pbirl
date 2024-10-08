import numpy as np
from typing import Tuple, Optional
from helpers import (
    check_transitions_rewards,
    ensure_policy_stochastic,
    random_argmax,
    tie_breaker_argmax,
)

def value_iteration(
    transitions: np.ndarray,
    rewards: np.ndarray,
    policy: Optional[np.ndarray] = None,
    rewards_tie_breaker: Optional[np.ndarray] = None,
    random_argmax_flag: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Perform value iteration"""
    assert not all(x is not None for x in [policy, rewards_tie_breaker])
    if rewards_tie_breaker is not None:
        q_opt_tie_breaker, _, _ = value_iteration(transitions, rewards_tie_breaker)
    horizon, n_states, n_actions = check_transitions_rewards(transitions, rewards)
    if policy is not None:
        policy = ensure_policy_stochastic(policy, horizon, n_states, n_actions)
    q_opt = np.zeros((horizon, n_states, n_actions))
    q_opt[horizon - 1] = rewards[horizon - 1]
    for h in range(horizon - 1, 0, -1):
        if policy is not None:
            vh = np.sum(q_opt[h] * policy[h], axis=1)
        else:
            vh = np.max(q_opt[h], axis=1)
        q_opt[h - 1] = rewards[h - 1] + transitions[h - 1] @ vh
    if policy is not None:
        v_opt = np.sum(q_opt * policy, axis=2)
        pi_opt = policy
    else:
        v_opt = np.max(q_opt, axis=2)
        if rewards_tie_breaker is not None:
            pi_opt = tie_breaker_argmax(q_opt, q_opt_tie_breaker, axis=2)
        else:
            if random_argmax_flag:
                pi_opt = random_argmax(q_opt, axis=2)
            else:
                pi_opt = np.argmax(q_opt, axis=2)
    return q_opt, v_opt, pi_opt

def policy_evaluation(
    transitions: np.ndarray,
    rewards: np.ndarray,
    policy: np.ndarray,
    random_argmax_flag: bool = True,
):
    return value_iteration(transitions, rewards, policy=policy, random_argmax_flag=random_argmax_flag)
