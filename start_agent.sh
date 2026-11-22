#!/usr/bin/env bash
# Runner script to start or re-attach to the Antigravity remote agent session in tmux

SESSION_NAME="agy-agent"

# Ensure agy is on PATH
export PATH="$HOME/.local/bin:$HOME/.gemini/bin:$PATH"

if ! command -v agy &> /dev/null; then
    echo "Error: 'agy' command not found. Run ./setup_remote_agent.sh first."
    exit 1
fi

# Check if session already exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Attaching to existing '$SESSION_NAME' session..."
    tmux attach-session -t "$SESSION_NAME"
else
    echo "Starting new Antigravity session in tmux named '$SESSION_NAME'..."
    tmux new-session -s "$SESSION_NAME" "agy"
fi
