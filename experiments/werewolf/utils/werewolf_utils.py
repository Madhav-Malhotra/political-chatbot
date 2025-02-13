# -*- coding: utf-8 -*-
"""utils."""
import re
from typing import Union, Any, Sequence

import json

import numpy as np
from loguru import logger

from example_game.prompt import Prompts
from agentscope.agents import AgentBase
from agentscope.message import Msg


def check_winning(alive_agents: list, wolf_agents: list, host: str) -> bool:
    """check which group wins"""
    if len(wolf_agents) * 2 >= len(alive_agents):
        msg = Msg(host, Prompts.to_all_wolf_win, role="assistant")
        logger.chat(msg)
        return True
    if alive_agents and not wolf_agents:
        msg = Msg(host, Prompts.to_all_village_win, role="assistant")
        logger.chat(msg)
        return True
    return False


def update_alive_players(
    survivors: Sequence[AgentBase],
    wolves: Sequence[AgentBase],
    dead_names: Union[str, list[str]],
) -> tuple[list, list]:
    """update the list of alive agents"""
    if not isinstance(dead_names, list):
        dead_names = [dead_names]
    return [_ for _ in survivors if _.name not in dead_names], [
        _ for _ in wolves if _.name not in dead_names
    ]


def majority_vote(votes: list) -> Any:
    """majority_vote function"""
    votes_valid = [item for item in votes if item != "Abstain"]
    # Count the votes excluding abstentions.
    unit, counts = np.unique(votes_valid, return_counts=True)
    return unit[np.argmax(counts)]


def extract_name_and_id(name: str) -> tuple[str, int]:
    """extract player name and id from a string"""
    try:
        name = re.search(r"\b[Pp]layer\d+\b", name).group(0)
        idx = int(re.search(r"[Pp]layer(\d+)", name).group(1)) - 1
    except AttributeError:
        # In case Player remains silent or speaks to abstain.
        logger.warning(f"vote: invalid name {name}, set to Abstain")
        name = "Abstain"
        idx = -1
    return name, idx


def n2s(agents: Sequence[Union[AgentBase, str]]) -> str:
    """combine agent names into a string, and use "and" to connect the last
    two names."""

    def _get_name(agent_: Union[AgentBase, str]) -> str:
        return agent_.name if isinstance(agent_, AgentBase) else agent_

    if len(agents) == 1:
        return _get_name(agents[0])

    return (
        ", ".join([_get_name(_) for _ in agents[:-1]])
        + " and "
        + _get_name(agents[-1])
    )


def set_parsers(
    agents: Union[AgentBase, list[AgentBase]],
    parser_name: str,
) -> None:
    """Add parser to agents"""
    if not isinstance(agents, list):
        agents = [agents]
    for agent in agents:
        agent.set_parser(parser_name)


def _convert_to_str(content: Any) -> str:
    """Convert the content to string.

    Note:
        For prompt engineering, simply calling `str(content)` or
        `json.dumps(content)` is not enough.

        - For `str(content)`, if `content` is a dictionary, it will turn double
        quotes to single quotes. When this string is fed into prompt, the LLMs
        may learn to use single quotes instead of double quotes (which
        cannot be loaded by `json.loads` API).

        - For `json.dumps(content)`, if `content` is a string, it will add
        double quotes to the string. LLMs may learn to use double quotes to
        wrap strings, which leads to the same issue as `str(content)`.

        To avoid these issues, we use this function to safely convert the
        content to a string used in prompt.

    Args:
        content (`Any`):
            The content to be converted.

    Returns:
        `str`: The converted string.
    """

    if isinstance(content, str):
        return content
    elif isinstance(content, (dict, list, int, float, bool, tuple)):
        return json.dumps(content, ensure_ascii=False)
    else:
        return str(content)