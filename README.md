## WAT.ai Political LLM team

We're testing AI agent architectures for analysing political legislation. Our method is to test decision-making in objective environments like scorable games. We use this to improve the agent's decision-making ability. This finally lets us see if good decision-making ability in these simulated environments generalises to political legislation.

## Architectures tested
- We're testing on two different games: monopoly and werewolf. 
- We're testing two different agentic architecture: a courtroom architecture (two lawyers present counterarguments to a judge) and a fast-mind-slow-mind architecture (a lightweight LLM makes most decisions, calling in a more complex LLM for difficult decisions).
- We're testing two different memory architectures: a simple vectorstore on past decisions made and a reflection architecture that summarises relevant insights from past decisions before storing them into memory.
- This results in a 2 x 2 x 2 test matrix, where we measure average win rate in the games as a proxy for decision-making ability.

