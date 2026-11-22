#!/usr/bin/env bash
set -euo pipefail

echo "=================================================="
echo "   Setting up Antigravity Remote Agent (Method 1) "
echo "=================================================="

# 1. Install prerequisites
echo "[1/4] Installing system dependencies (python3, tmux, curl, jq, git)..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip tmux git curl jq
elif command -v dnf &> /dev/null; then
    sudo dnf install -y python3 python3-pip tmux git curl jq
fi

# 2. Install Antigravity CLI (agy)
echo "[2/4] Checking Antigravity CLI (agy)..."
if ! command -v agy &> /dev/null; then
    echo "Installing Antigravity CLI..."
    curl -fsSL https://antigravity.google/install.sh | bash
    export PATH="$HOME/.local/bin:$HOME/.gemini/bin:$PATH"
else
    echo "Antigravity CLI (agy) is already installed."
fi

# 3. Configure autonomous permissions in settings.json
echo "[3/4] Configuring Antigravity CLI autonomous settings..."
SETTINGS_DIR="$HOME/.gemini/antigravity-cli"
SETTINGS_FILE="$SETTINGS_DIR/settings.json"
mkdir -p "$SETTINGS_DIR"

if [ ! -f "$SETTINGS_FILE" ]; then
    cat <<EOF > "$SETTINGS_FILE"
{
  "toolExecutionPolicy": "always-proceed",
  "sandboxMode": true,
  "internetAccessPolicy": "allow"
}
EOF
else
    # Update existing settings with jq if present
    tmp=$(mktemp)
    jq '.toolExecutionPolicy = "always-proceed" | .sandboxMode = true' "$SETTINGS_FILE" > "$tmp" && mv "$tmp" "$SETTINGS_FILE"
fi

# 4. Make scripts executable
chmod +x ./start_agent.sh 2>/dev/null || true

echo "=================================================="
echo "Setup complete!"
echo ""
echo "Next Steps:"
echo "1. Authenticate agy:"
echo "   agy auth"
echo "   (or export GEMINI_API_KEY=\"your-key\" in ~/.bashrc)"
echo ""
echo "2. Start your remote agent session:"
echo "   ./start_agent.sh"
echo "=================================================="
