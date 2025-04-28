🎲 Todo Roulette – Flexible, Gamified Task Manager (MVP)

Todo Roulette is a task management app built for students, freelancers, and remote workers who want a flexible, fun, and adaptive way to organize their days.
It mixes work, study, and self-care activities — and shuffles tasks randomly to avoid decision fatigue and maintain balance.
⚠️ This is an early MVP version that runs locally.

## What It Does (Current MVP)

✅ Shuffle tasks randomly ("Task Roulette")
✅ Group tasks into must-do, want-to-do, and later categories
✅ Track real-time work sessions
✅ Break work into focused intervals with manual break suggestions
✅ Save and load task progress automatically

## Project Structure

File | Purpose
main.py | Core logic: task loading, shuffling, work session tracking, updating task status.
start.py | Starts a new session: initializes task list and handles Streamlit + ngrok tunnel.
tasks.json | Example database of categorized tasks (must-do, want-to-do, later).
base.css | Styling file intended for future UI improvements (currently not actively used).
Todo Roulette Overview.rtf | Vision document outlining long-term goals, positioning, and marketing ideas.

## Planned Future Features (Not Yet Implemented)

📆 Manual calendar input and scheduling

📊 Visual analytics (work vs break vs mus/want task percentages)

🎯 Fun/Self-Care balancing system (automated suggestions at automated time intervals)

🔗 Calendar syncing (Google Calendar integration) - if not needed will not implement - annying to always have to integrate everything and overcomplicate tools

🧠 AI-powered task prioritization that analyses your personal behaviours

📱 Mobile & Desktop app (Flutter or React Native)

## Setup Requirements

Make sure you have **Python 3.7+** installed.  
Then install the necessary packages:
pip install streamlit pyngrok

Clone the repository:
git clone https://github.com/your-username/todo-roulette.git
cd todo-roulette

Run the session starter and click the link the terminal spits out:
python start.py

## Vision

Todo Roulette aims to redefine productivity for flexible workers and students by:
- Promoting a healthy balance between work, study, and fun
- Reducing decision fatigue through gamified random task selection while managing realistic task time estimates
- Adapting to real-life flexible schedules, instead of forcing rigid planning

## Contribute 
If you want to contribute or use this project, please reach out first!

## Autor

Anna Papanakli