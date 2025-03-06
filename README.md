## WAT.ai Political LLM team

We're testing AI agent architectures for analysing political legislation. Our method is to test decision-making in objective environments like scorable games. We use this to improve the agent's decision-making ability. This finally lets us see if good decision-making ability in these simulated environments generalises to political legislation.

## Abstract
This paper explores the generalisability of LLMs as decision-making assistants. We propose an assessment framework where retrieval-augmented generation (RAG) architectures are compared in gamified environments. By comparing objective win rates in games like Monopoly and Werewolf, we assess the efficacy of architectural options like reflection or multi-agent roles. This allows us to then apply the best performing architectures to the real-life context of legislative analysis. With this method, we find that the RAG architectures explored do not show generalisability across decision-making contexts.

**Keywords:** AI, decision-making, game agents, RAG

## Experiment Overview
We tested different agent architectures, memory architectures, and agent behaviors using two popular games: Monopoly and Werewolf. These environments serve as objective platforms for evaluating decision-making skills that are transferable to more complex real-world applications, such as political legislation analysis.

## Architectures tested
**Agent Architectures:**
- **Courtroom Architecture**: Two lawyers present counterarguments to a judge.
- **Fast-Mind-Slow-Mind Architecture**: A lightweight LLM makes most decisions, calling in a more complex LLM for difficult decisions.

**Memory Architectures:**
- **Vectorstore Memory**: A simple memory system that stores past decisions made.
- **Reflection Architecture**: A system that summarizes relevant insights from past decisions before storing them in memory.

**Test Matrix:**
We conducted tests based on a 2 x 2 x 2 matrix:
- 2 Agent Architectures
- 2 Memory Architectures
- 2 Games (Monopoly and Werewolf)

In each case, the average win rate in these games is used as a proxy for the agent's decision-making ability.

## How to Run the Experiment

### Prerequisites  
Ensure you have Python 3.12 ≥ installed.

### **1. Clone the Repository**  
Open a terminal and run:  
```bash
git clone https://github.com/Madhav-Malhotra/political-chatbot.git
cd political-chatbot 
```

### **2. Create and Activate a Virtual Environment**  
It is recommended to create a virtual environment to manage dependencies. Run:  
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### **3. Install Dependencies**  
Install the required Python packages:

To run a **Monopoly** experiment -> 
```bash
pip install -r experiments/monopoly/requirements.txt
```
To run a **Werewolf** experiment -> 
```bash
pip install -r experiments/werewolf/requirements.txt
```

### **4. Set up .env File**
Make a .env file in the root directory and add OPENAI_API_KEY.
```bash
OPENAI_API_KEY=YOUR_API_KEY
```
### **5. Choose Experiement to Run**
From the experiments folder, determine which game and architecture you would like to run. Choose the notebook corresponding to your choice and press `Run All` to begin the experiment. 

To look at your **results**, see the logs folder under the experiment, which includes the decisions made by the LLM as well as its behaviour throughout the run. 