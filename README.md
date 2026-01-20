# Forest Adventure - CS50 Final Project

## Introduction

Welcome to **Forest Adventure**, an immersive, text-based interactive fiction game developed as a final project for CS50: Introduction to Computer Science.

This project represents a fusion of classic text adventure nostalgia and modern artificial intelligence. By leveraging the power of Large Language Models (LLMs) via the **Groq API**, Forest Adventure moves beyond static decision trees. Instead, it generates unique descriptions, dynamic scenarios, and unpredictable outcomes every time you play. The player finds themselves trapped in a mysterious, shifting forest, tasked with the ultimate goal of locating a legendary lost treasure while managing their physical health and navigating a world teeming with potential hazards.

## Project Description and Motivation

The core motivation behind Forest Adventure was to explore how Python can interact with external APIs to create non-deterministic gameplay loops. In traditional text adventures, if a player chooses to "Go North," the result is hard-coded. In Forest Adventure, the result is "hallucinated" vividly by an AI based on the current context of the game.

This project utilizes Python for the game engine—handling the logic of probability, inventory management, win/lose states, and input validation—while outsourcing the creative writing and "Dungeon Master" duties to the Groq API. This separation of concerns allows for a robust game structure with limitless narrative possibilities.

## Technical Architecture & Code Explanation

The game is built as a single-script Python application (`adventure.py`) that acts as a bridge between the user and the LLM. Below is a detailed breakdown of how the code functions.

### 1. Libraries and Setup
The project relies on a minimal set of robust libraries:
* **`groq`**: The official Python client for interacting with the Groq API, chosen for its ultra-low latency inference (using `llama-3.1-8b-instant`).
* **`os`**: Used for securely retrieving the `GROQ_API_KEY` from environment variables.
* **`random`**: Essential for the game's stochastic nature (item drops, hazard encounters, and win/loss probability).
* **`time` & `sys`**: Used to create the custom "retro terminal" typing animation effects.

### 2. The Game Loop (`game()` function)
The core logic resides in an infinite `while` loop that only breaks upon a Win, Loss, or Exit condition.
* **State Tracking**: The game tracks `turn_count`, `inventory` (list), `hazards` (list), and `history` (chronological list of events).
* **Probability Logic**: Unlike games with fixed health bars, this game uses a **dynamic probability calculation** to determine the outcome of every turn.
    * *Win Chance*: `30 - 2 * turn_count` (The denominator decreases, making a win *more* likely as you survive longer).
    * *Loss Chance*: `25 - 2 * turn_count` (The risk of death also increases as the game progresses).
    * *Sudden Death*: If the player reaches **Turn 10**, the game forces a 50/50 coin flip for immediate victory or defeat.

### 3. Prompt Engineering (`build_prompt` function)
The most complex part of the code is the dynamic string construction for the LLM. The `build_prompt` function assembles a specific instructions set based on the game state:
* **Context Injection**: It feeds the AI the `inventory` list and `hazards` list so the story remains consistent (e.g., if you have a "lantern," the AI knows you can see in the dark).
* **Randomized Elements**: Before the prompt is sent, Python rolls a 4-sided die (`randint(1, 4)`).
    * There is a 25% chance to find an item (selected from `ITEMS`).
    * There is a 25% chance to encounter a hazard (selected from `HAZARDS`).
* **Instruction Injection**: If an item is found, the prompt explicitly tells the AI: *"Introduce the newly discovered item: silver dagger."* This ensures the narrative aligns with the Python-side inventory data.

### 4. Memory Compression (`summarise_scene` function)
To prevent the LLM's context window from overflowing (and to keep costs low), the game does not send the entire conversation history every time.
* Instead, after every turn, a **secondary API call** is made to a "Summarizer" instance of the model.
* It condenses the previous paragraph of text into a single factual sentence (e.g., *"Turn 3: The player chose to swim across the river and lost their map."*).
* This compressed history is appended to the `history` list and fed back into the main prompt, allowing the AI to "remember" long-term events without reading pages of text.

### 5. Immersion Features
The code includes custom functions `type()`, `typed_input()`, and `load()` to mimic the baud-rate delay of old CRT monitors. This forces the player to slow down and absorb the story, rather than skimming through instant text blocks.

## How to Play

### Getting Started
Once the game is launched, you will be greeted by the prologue. Read the text carefully, as it often contains clues about your environment.

### Controls
The game uses a numeric input system. When prompted, you will see a menu similar to this:
1. Search the hollow tree.
2. Walk towards the sound of water.
3. Climb the ridge to look for landmarks.
4. Check your inventory.

Simply type the number corresponding to your choice and press **Enter**.

### Strategy Guide
* **Manage Your Risk**: The probability math in the code favors those who survive longer. Early in the game, play safely.
* **Inventory Usage**: The prompt engineering specifically instructs the AI to include options that reference your inventory. Collecting items unlocks unique narrative paths.
* **Hazards**: If you trigger a "poisonous fog" or "wild animal" hazard, be careful—future narrative descriptions will become more ominous!

## Setup and Installation Instructions

Follow these detailed steps to get the game running on your local machine.

### Prerequisites
* **Python:** Ensure you have Python 3.12 or newer installed.
* **Groq API Key:** You will need a free API key from the Groq console.

### Installation Steps

1.  **Clone the Repository:**
    Download the project files to your local machine.
    ```bash
    git clone [https://github.com/Art4v/cs50-final-project.git](https://github.com/Art4v/cs50-final-project.git)
    cd cs50-final-project
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install the required Python libraries using the provided requirements file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    You must set your API Key for the code to function.
    
    * **macOS/Linux:**
        ```bash
        export GROQ_API_KEY=gsk_your_actual_api_key_here
        ```
    * **Windows (PowerShell):**
        ```powershell
        $env:GROQ_API_KEY="gsk_your_actual_api_key_here"
        ```

5.  **Run the Game:**
    ```bash
    python adventure.py
    ```

## Video Demo

To see the game in action, including the typing effects and AI responses, watch the full video demonstration here:

[**Watch the Forest Adventure Demo on YouTube**](https://www.youtube.com/watch?v=iFQdkbykKVw)

## GitHub Repository

The complete source code, including the Python logic and prompt engineering templates, allows for inspection and modification. You can fork or view the repository here:

[**https://github.com/Art4v/cs50-final-project**](https://github.com/Art4v/cs50-final-project)

## AI Usage Statement

In accordance with CS50's academic honesty and project guidelines, it is important to transparently declare the role of Artificial Intelligence in this project.

**What the AI (Groq/Llama 3) Does:**
* Generates the narrative text (the "story").
* Summarizes previous turns to maintain context.

**What the AI Does NOT Do (Manual Implementation):**
* **Game Logic:** The `main()` loop, state tracking, and probability calculations (`randint`) were written manually.
* **Prompt Engineering:** The `build_prompt` function structure was manually designed to constrain the AI's behavior.
* **API Integration:** The connection logic using the Groq SDK was manually implemented.

The project code was written by the student, with the AI serving as a "component" within the software architecture, much like a database or a graphics engine. AI Agents such as chatgpt were used for ideation, planning, and prompt generation, but were NOT used to write the code directly. 

---

**Credits:**
* Developed by Art4v
* Course: CS50x
* Special thanks to the Groq team for providing fast inference API access.