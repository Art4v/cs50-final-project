# Forest Adventure - CS50 Final Project

Welcome to **Forest Adventure**, a text-based AI-powered adventure game where the player is trapped in a mysterious forest and must search for a lost treasure while navigating hazards and collecting items.

## Features

- Interactive text-based gameplay.
- AI-powered scene generation using Groq LLM API.
- Dynamic inventory and hazard system.
- Randomized events and outcomes.
- Win and lose conditions with increasing tension.
- Typing animation for immersive storytelling.

## How to Play

1. Run the Python script `adventure.py`.
2. Follow the on-screen instructions.
3. Choose options by typing the numbers 1-4.
4. Monitor your health and inventory as you progress.
5. The game ends when you either find the treasure (win) or die (lose).

## Setup

1. Make sure Python 3.12 or newer is installed.
2. Install the Groq Python library:
   ```bash
   pip install groq
   ```
3. Set your Groq API key as an environment variable:
   ```bash
   export GROQ_API_KEY=your_api_key_here   # macOS/Linux
   setx GROQ_API_KEY "your_api_key_here"  # Windows PowerShell
   ```
4. Run the game:
   ```bash
   python adventure.py
   ```

## Video Demo

You can find the video demo at:

https://www.youtube.com/watch?v=iFQdkbykKVw


## GitHub Repository

You can find the project source code and updates at: 

https://github.com/Art4v/cs50-final-project


## AI Usage

This project uses AI to generate dynamic text-based game scenes and summaries. Specifically:

Groq LLM API (llama-3.1-8b-instant) was used to generate story events, summarize past scenes, and manage game state updates.

AI was only used for scene creation and summarization, while all game logic, input handling, and state tracking were implemented manually in Python.

This acknowledges AI assistance while clarifying what was manually implemented, which aligns with CS50’s policies on transparency.

---

Enjoy your adventure in the mysterious forest!