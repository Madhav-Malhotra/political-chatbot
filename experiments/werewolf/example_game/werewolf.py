# -*- coding: utf-8 -*-
"""A werewolf game implemented by agentscope."""

import sys
import os
from dotenv import load_dotenv

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functools import partial

from prompt import Prompts
from utils.werewolf_utils import (
    check_winning,
    update_alive_players,
    majority_vote,
    extract_name_and_id,
    n2s,
    set_parsers,
)
from agents.dict_dialog_agent import CustomDictDialogAgent
#from agents.custom_agent import CustomAgent
from agentscope.message import Msg
from agentscope.msghub import msghub
from agentscope.pipelines.functional import sequentialpipeline
import agentscope


# pylint: disable=too-many-statements
def main() -> None:
    """werewolf game"""
    # default settings
    HostMsg = partial(Msg, name="Moderator", role="assistant", echo=True)
    healing, poison = True, True
    MAX_WEREWOLF_DISCUSSION_ROUND = 3
    MAX_GAME_ROUND = 6

    # Register your custom class
    agentscope.agents.CustomDictDialogAgent = CustomDictDialogAgent
    #agentscope.agents.CustomAgent = CustomAgent

    # Load API keys from .env file
    load_dotenv()

    # Define the API keys
    openai_key = os.getenv("OPENAI_API_KEY")

    model_configs = [
        {
            "model_type": "openai_chat",
            "config_name": "gpt-4o-mini",
            "model_name": "gpt-4o-mini",
            "api_key": openai_key,
            "generate_args": {
                "temperature": 0.5
            }
        }
    ]

    agent_configs = [
        {
            "class": "CustomDictDialogAgent",
            "args": {
                "name": "Player1",
                "sys_prompt": "Act as a player in a werewolf game. You are Player1 and\nthere are totally 6 players, named Player1, Player2, Player3, Player4, Player5 and Player6.\n\nPLAYER ROLES:\nIn werewolf game, players are divided into two werewolves, two villagers, one seer and one witch. Note only werewolves know who are their teammates.\nWerewolves: They know their teammates' identities and attempt to eliminate a villager each night while trying to remain undetected.\nVillagers: They do not know who the werewolves are and must work together during the day to deduce who the werewolves might be and vote to eliminate them.\nSeer: A villager with the ability to learn the true identity of one player each night. This role is crucial for the villagers to gain information.\nWitch: A character who has a one-time ability to save a player from being eliminated at night (sometimes this is a potion of life) and a one-time ability to eliminate a player at night (a potion of death).\n\nGAME RULE:\nThe game is consisted of two phases: night phase and day phase. The two phases are repeated until werewolf or villager win the game.\n1. Night Phase: During the night, the werewolves discuss and vote for a player to eliminate. Special roles also perform their actions at this time (e.g., the Seer chooses a player to learn their role, the witch chooses a decide if save the player).\n2. Day Phase: During the day, all surviving players discuss who they suspect might be a werewolf. No one reveals their role unless it serves a strategic purpose. After the discussion, a vote is taken, and the player with the most votes is \"lynched\" or eliminated from the game.\n\nVICTORY CONDITION:\nFor werewolves, they win the game if the number of werewolves is equal to or greater than the number of remaining villagers.\nFor villagers, they win if they identify and eliminate all of the werewolves in the group.\n\nCONSTRAINTS:\n1. Your response should be in the first person.\n2. This is a conversational game. You should response only based on the conversation history and your strategy.\n\nYou are playing werewolf in this game.\n",
                "model_config_name": "gpt-4o-mini",
                "use_memory": True
            }
        },
        {
            "class": "CustomDictDialogAgent",
            "args": {
                "name": "Player2",
                "sys_prompt": "Act as a player in a werewolf game. You are Player2 and\nthere are totally 6 players, named Player1, Player2, Player3, Player4, Player5 and Player6.\n\nPLAYER ROLES:\nIn werewolf game, players are divided into two werewolves, two villagers, one seer and one witch. Note only werewolves know who are their teammates.\nWerewolves: They know their teammates' identities and attempt to eliminate a villager each night while trying to remain undetected.\nVillagers: They do not know who the werewolves are and must work together during the day to deduce who the werewolves might be and vote to eliminate them.\nSeer: A villager with the ability to learn the true identity of one player each night. This role is crucial for the villagers to gain information.\nWitch: A character who has a one-time ability to save a player from being eliminated at night (sometimes this is a potion of life) and a one-time ability to eliminate a player at night (a potion of death).\n\nGAME RULE:\nThe game is consisted of two phases: night phase and day phase. The two phases are repeated until werewolf or villager win the game.\n1. Night Phase: During the night, the werewolves discuss and vote for a player to eliminate. Special roles also perform their actions at this time (e.g., the Seer chooses a player to learn their role, the witch chooses a decide if save the player).\n2. Day Phase: During the day, all surviving players discuss who they suspect might be a werewolf. No one reveals their role unless it serves a strategic purpose. After the discussion, a vote is taken, and the player with the most votes is \"lynched\" or eliminated from the game.\n\nVICTORY CONDITION:\nFor werewolves, they win the game if the number of werewolves is equal to or greater than the number of remaining villagers.\nFor villagers, they win if they identify and eliminate all of the werewolves in the group.\n\nCONSTRAINTS:\n1. Your response should be in the first person.\n2. This is a conversational game. You should response only based on the conversation history and your strategy.\n\nYou are playing werewolf in this game.\n",
                "model_config_name": "gpt-4o-mini",
                "use_memory": True
            }
        },
        {
            "class": "CustomDictDialogAgent",
            "args": {
                "name": "Player3",
                "sys_prompt": "Act as a player in a werewolf game. You are Player3 and\nthere are totally 6 players, named Player1, Player2, Player3, Player4, Player5 and Player6.\n\nPLAYER ROLES:\nIn werewolf game, players are divided into two werewolves, two villagers, one seer and one witch. Note only werewolves know who are their teammates.\nWerewolves: They know their teammates' identities and attempt to eliminate a villager each night while trying to remain undetected.\nVillagers: They do not know who the werewolves are and must work together during the day to deduce who the werewolves might be and vote to eliminate them.\nSeer: A villager with the ability to learn the true identity of one player each night. This role is crucial for the villagers to gain information.\nWitch: A character who has a one-time ability to save a player from being eliminated at night (sometimes this is a potion of life) and a one-time ability to eliminate a player at night (a potion of death).\n\nGAME RULE:\nThe game is consisted of two phases: night phase and day phase. The two phases are repeated until werewolf or villager win the game.\n1. Night Phase: During the night, the werewolves discuss and vote for a player to eliminate. Special roles also perform their actions at this time (e.g., the Seer chooses a player to learn their role, the witch chooses a decide if save the player).\n2. Day Phase: During the day, all surviving players discuss who they suspect might be a werewolf. No one reveals their role unless it serves a strategic purpose. After the discussion, a vote is taken, and the player with the most votes is \"lynched\" or eliminated from the game.\n\nVICTORY CONDITION:\nFor werewolves, they win the game if the number of werewolves is equal to or greater than the number of remaining villagers.\nFor villagers, they win if they identify and eliminate all of the werewolves in the group.\n\nCONSTRAINTS:\n1. Your response should be in the first person.\n2. This is a conversational game. You should response only based on the conversation history and your strategy.\n\nYou are playing villager in this game.\n",
                "model_config_name": "gpt-4o-mini",
                "use_memory": True
            }
        },
        {
            "class": "CustomDictDialogAgent",
            "args": {
                "name": "Player4",
                "sys_prompt": "Act as a player in a werewolf game. You are Player4 and\nthere are totally 6 players, named Player1, Player2, Player3, Player4, Player5 and Player6.\n\nPLAYER ROLES:\nIn werewolf game, players are divided into two werewolves, two villagers, one seer and one witch. Note only werewolves know who are their teammates.\nWerewolves: They know their teammates' identities and attempt to eliminate a villager each night while trying to remain undetected.\nVillagers: They do not know who the werewolves are and must work together during the day to deduce who the werewolves might be and vote to eliminate them.\nSeer: A villager with the ability to learn the true identity of one player each night. This role is crucial for the villagers to gain information.\nWitch: A character who has a one-time ability to save a player from being eliminated at night (sometimes this is a potion of life) and a one-time ability to eliminate a player at night (a potion of death).\n\nGAME RULE:\nThe game is consisted of two phases: night phase and day phase. The two phases are repeated until werewolf or villager win the game.\n1. Night Phase: During the night, the werewolves discuss and vote for a player to eliminate. Special roles also perform their actions at this time (e.g., the Seer chooses a player to learn their role, the witch chooses a decide if save the player).\n2. Day Phase: During the day, all surviving players discuss who they suspect might be a werewolf. No one reveals their role unless it serves a strategic purpose. After the discussion, a vote is taken, and the player with the most votes is \"lynched\" or eliminated from the game.\n\nVICTORY CONDITION:\nFor werewolves, they win the game if the number of werewolves is equal to or greater than the number of remaining villagers.\nFor villagers, they win if they identify and eliminate all of the werewolves in the group.\n\nCONSTRAINTS:\n1. Your response should be in the first person.\n2. This is a conversational game. You should response only based on the conversation history and your strategy.\n\nYou are playing villager in this game.\n",
                "model_config_name": "gpt-4o-mini",
                "use_memory": True
            }
        },
        {
            "class": "CustomDictDialogAgent",
            "args": {
                "name": "Player5",
                "sys_prompt": "Act as a player in a werewolf game. You are Player5 and\nthere are totally 6 players, named Player1, Player2, Player3, Player4, Player5 and Player6.\n\nPLAYER ROLES:\nIn werewolf game, players are divided into two werewolves, two villagers, one seer and one witch. Note only werewolves know who are their teammates.\nWerewolves: They know their teammates' identities and attempt to eliminate a villager each night while trying to remain undetected.\nVillagers: They do not know who the werewolves are and must work together during the day to deduce who the werewolves might be and vote to eliminate them.\nSeer: A villager with the ability to learn the true identity of one player each night. This role is crucial for the villagers to gain information.\nWitch: A character who has a one-time ability to save a player from being eliminated at night (sometimes this is a potion of life) and a one-time ability to eliminate a player at night (a potion of death).\n\nGAME RULE:\nThe game is consisted of two phases: night phase and day phase. The two phases are repeated until werewolf or villager win the game.\n1. Night Phase: During the night, the werewolves discuss and vote for a player to eliminate. Special roles also perform their actions at this time (e.g., the Seer chooses a player to learn their role, the witch chooses a decide if save the player).\n2. Day Phase: During the day, all surviving players discuss who they suspect might be a werewolf. No one reveals their role unless it serves a strategic purpose. After the discussion, a vote is taken, and the player with the most votes is \"lynched\" or eliminated from the game.\n\nVICTORY CONDITION:\nFor werewolves, they win the game if the number of werewolves is equal to or greater than the number of remaining villagers.\nFor villagers, they win if they identify and eliminate all of the werewolves in the group.\n\nCONSTRAINTS:\n1. Your response should be in the first person.\n2. This is a conversational game. You should response only based on the conversation history and your strategy.\n\nYou are playing seer in this game.\n",
                "model_config_name": "gpt-4o-mini",
                "use_memory": True
            }
        },
        {
            "class": "CustomDictDialogAgent",
            "args": {
                "name": "Player6",
                "sys_prompt": "Act as a player in a werewolf game. You are Player6 and\nthere are totally 6 players, named Player1, Player2, Player3, Player4, Player5 and Player6.\n\nPLAYER ROLES:\nIn werewolf game, players are divided into two werewolves, two villagers, one seer and one witch. Note only werewolves know who are their teammates.\nWerewolves: They know their teammates' identities and attempt to eliminate a villager each night while trying to remain undetected.\nVillagers: They do not know who the werewolves are and must work together during the day to deduce who the werewolves might be and vote to eliminate them.\nSeer: A villager with the ability to learn the true identity of one player each night. This role is crucial for the villagers to gain information.\nWitch: A character who has a one-time ability to save a player from being eliminated at night (sometimes this is a potion of life) and a one-time ability to eliminate a player at night (a potion of death).\n\nGAME RULE:\nThe game is consisted of two phases: night phase and day phase. The two phases are repeated until werewolf or villager win the game.\n1. Night Phase: During the night, the werewolves discuss and vote for a player to eliminate. Special roles also perform their actions at this time (e.g., the Seer chooses a player to learn their role, the witch chooses a decide if save the player).\n2. Day Phase: During the day, all surviving players discuss who they suspect might be a werewolf. No one reveals their role unless it serves a strategic purpose. After the discussion, a vote is taken, and the player with the most votes is \"lynched\" or eliminated from the game.\n\nVICTORY CONDITION:\nFor werewolves, they win the game if the number of werewolves is equal to or greater than the number of remaining villagers.\nFor villagers, they win if they identify and eliminate all of the werewolves in the group.\n\nCONSTRAINTS:\n1. Your response should be in the first person.\n2. This is a conversational game. You should response only based on the conversation history and your strategy.\n\nYou are playing witch in this game.\n",
                "model_config_name": "gpt-4o-mini",
                "use_memory": True
            }
        }
    ]

    # read model and agent configs, and initialize agents automatically
    survivors = agentscope.init(
        model_configs=model_configs,
        agent_configs=agent_configs,
        project="Werewolf",
    )

    roles = ["werewolf", "werewolf", "villager", "villager", "seer", "witch"]
    wolves, witch, seer = survivors[:2], survivors[-1], survivors[-2]

    # start the game
    for _ in range(1, MAX_GAME_ROUND + 1):
        # night phase, werewolves discuss
        hint = HostMsg(content=Prompts.to_wolves.format(n2s(wolves)))
        with msghub(wolves, announcement=hint) as hub:
            set_parsers(wolves, Prompts.wolves_discuss_parser)
            for _ in range(MAX_WEREWOLF_DISCUSSION_ROUND):
                x = sequentialpipeline(wolves)
                if x.metadata.get("finish_discussion", False):
                    break

            # werewolves vote
            set_parsers(wolves, Prompts.wolves_vote_parser)
            hint = HostMsg(content=Prompts.to_wolves_vote)
            votes = [
                extract_name_and_id(wolf(hint).content)[0] for wolf in wolves
            ]
            # broadcast the result to werewolves
            dead_player = [majority_vote(votes)]
            hub.broadcast(
                HostMsg(content=Prompts.to_wolves_res.format(dead_player[0])),
            )

        # witch
        healing_used_tonight = False
        if witch in survivors:
            if healing:
                hint = HostMsg(
                    content=Prompts.to_witch_resurrect.format_map(
                        {
                            "witch_name": witch.name,
                            "dead_name": dead_player[0],
                        },
                    ),
                )
                set_parsers(witch, Prompts.witch_resurrect_parser)
                if witch(hint).metadata.get("resurrect", False):
                    healing_used_tonight = True
                    dead_player.pop()
                    healing = False
                    HostMsg(content=Prompts.to_witch_resurrect_yes)
                else:
                    HostMsg(content=Prompts.to_witch_resurrect_no)

            if poison and not healing_used_tonight:
                set_parsers(witch, Prompts.witch_poison_parser)
                x = witch(HostMsg(content=Prompts.to_witch_poison))
                if x.metadata.get("eliminate", False):
                    dead_player.append(extract_name_and_id(x.content)[0])
                    poison = False

        # seer
        if seer in survivors:
            hint = HostMsg(
                content=Prompts.to_seer.format(seer.name, n2s(survivors)),
            )
            set_parsers(seer, Prompts.seer_parser)
            x = seer(hint)

            player, idx = extract_name_and_id(x.content)
            role = "werewolf" if roles[idx] == "werewolf" else "villager"
            hint = HostMsg(content=Prompts.to_seer_result.format(player, role))
            seer.observe(hint)

        survivors, wolves = update_alive_players(
            survivors,
            wolves,
            dead_player,
        )
        if check_winning(survivors, wolves, "Moderator"):
            break

        # daytime discussion
        content = (
            Prompts.to_all_danger.format(n2s(dead_player))
            if dead_player
            else Prompts.to_all_peace
        )
        hints = [
            HostMsg(content=content),
            HostMsg(content=Prompts.to_all_discuss.format(n2s(survivors))),
        ]
        with msghub(survivors, announcement=hints) as hub:
            # discuss
            set_parsers(survivors, Prompts.survivors_discuss_parser)
            x = sequentialpipeline(survivors)

            # vote
            set_parsers(survivors, Prompts.survivors_vote_parser)
            hint = HostMsg(content=Prompts.to_all_vote.format(n2s(survivors)))
            votes = [
                extract_name_and_id(_(hint).content)[0] for _ in survivors
            ]
            vote_res = majority_vote(votes)
            # broadcast the result to all players
            result = HostMsg(content=Prompts.to_all_res.format(vote_res))
            hub.broadcast(result)

            survivors, wolves = update_alive_players(
                survivors,
                wolves,
                vote_res,
            )

            if check_winning(survivors, wolves, "Moderator"):
                break

            hub.broadcast(HostMsg(content=Prompts.to_all_continue))


if __name__ == "__main__":
    main()
