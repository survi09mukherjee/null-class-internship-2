
#!/usr/bin/env bash
# Create a GitHub repo from this folder and push it.
# Requires GitHub CLI (gh) installed and authenticated, and git configured.
set -e
REPO_NAME=${1:-dynamic-kb-chatbot-template}
DESCRIPTION=${2:-"Dynamic KB chatbot template (RAG, ingestion scheduler, vectorstore abstraction)"}
# Create remote repo and push
gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --source=. --remote=origin --push
echo "Repository created and pushed: $REPO_NAME"
