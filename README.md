# 🎫 Ticket Tracker

A simple ticket tracking application with a Python Flask backend and HTML frontend. Demonstrates a basic Kanban-style workflow for managing tickets.

## 🎯 Features

- **Create Tickets**: Add new tickets with title, description, and due date
- **Kanban Board**: Track tickets across stages (To Do, In Progress, Review, Completed)
- **Simple API**: RESTful Python Flask backend for CRUD operations
- **JSON Storage**: Tickets stored in a simple JSON file
- **Containerized**: Ready for deployment to Azure Container Apps

## 📁 Project Structure

```
ticket-tracker/
├── src/
│   ├── index.html              # Create ticket page
│   ├── board.html              # Ticket board/Kanban view
│   ├── app.py                  # Flask API server
│   ├── requirements.txt        # Python dependencies
│   └── tickets_data.json       # Ticket storage
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── scripts/
│   └── setup-azure.sh          # Azure resource setup script
├── Dockerfile                  # Container definition
└── README.md                   # This file
```

## 🚀 Quick Start

### Run Locally

```bash
# Install dependencies
cd src
pip install -r requirements.txt

# Run the server
python app.py
```

Open http://localhost:80 in your browser.

### Run with Docker

```bash
# Build the image
docker build -t ticket-tracker .

# Run the container
docker run -p 80:80 ticket-tracker
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tickets` | Get all tickets |
| GET | `/api/tickets/:id` | Get a specific ticket |
| POST | `/api/tickets` | Create a new ticket |
| PUT | `/api/tickets/:id` | Update a ticket |
| DELETE | `/api/tickets/:id` | Delete a ticket |

### Create Ticket Example

```bash
curl -X POST http://localhost:80/api/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix bug", "description": "Fix the login bug", "due_date": "2026-02-15"}'
```

## ☁️ Deploy to Azure

### Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) installed
- Azure subscription
- GitHub repository

### Step 1: Set Up Azure Resources

```bash
# Login to Azure
az login

# Run the setup script
chmod +x scripts/setup-azure.sh
./scripts/setup-azure.sh
```

The script will output all the secrets you need for GitHub.

### Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

| Secret Name | Description |
|-------------|-------------|
| `AZURE_CONTAINER_REGISTRY` | Your ACR login server (e.g., `myacr.azurecr.io`) |
| `REGISTRY_USERNAME` | ACR admin username |
| `REGISTRY_PASSWORD` | ACR admin password |
| `AZURE_RESOURCE_GROUP` | Resource group name |
| `AZURE_CREDENTIALS` | Service principal JSON (full output) |
| `GH_TOKEN` | GitHub Token for repo access - issue and PR creation |
| `COPILOT_GITHUB_TOKEN` | Finegrained PAT for copilot access |

### Step 3: Push and Deploy

```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

## 🔄 CI/CD Workflow Diagram

The project uses a two-stage workflow with automated testing, deployment, and self-healing capabilities:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Push to main                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         test.yml (Unit Tests)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  • Run pytest with coverage                                          │    │
│  │  • Generate coverage reports (XML, HTML, JSON)                       │    │
│  │  • Check coverage against 90% threshold                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
        ┌───────────────────┐               ┌───────────────────┐
        │   Tests Pass ✅    │               │   Tests Fail ❌    │
        └───────────────────┘               └───────────────────┘
                    │                                   │
        ┌───────────┴───────────┐                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────────┐     ┌───────────────┐
│ Coverage ≥90% │     │  Coverage <90%    │     │ No Deployment │
└───────────────┘     └───────────────────┘     └───────────────┘
        │                       │
        │                       ▼
        │             ┌─────────────────────────────────────────┐
        │             │      coverage-analysis job               │
        │             │  ┌─────────────────────────────────┐    │
        │             │  │ • Analyze code with Copilot CLI  │    │
        │             │  │ • Identify uncovered code areas  │    │
        │             │  │ • Create GitHub issue 🧪         │    │
        │             │  │ • Assign to @copilot             │    │
        │             │  └─────────────────────────────────┘    │
        │             └─────────────────────────────────────────┘
        │                       │
        └───────────┬───────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      deploy.yml (Build & Deploy)                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  • Build Docker image                                                │    │
│  │  • Push to Azure Container Registry                                  │    │
│  │  • Deploy to Azure Container Apps                                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
        ┌───────────────────┐               ┌───────────────────┐
        │  Deploy Success ✅ │               │  Deploy Fail ❌   │
        └───────────────────┘               └───────────────────┘
                    │                                   │
                    ▼                                   ▼
            ┌───────────┐               ┌─────────────────────────────────────┐
            │   Done!   │               │         auto-heal job                │
            └───────────┘               │  ┌─────────────────────────────┐    │
                                        │  │ • Capture deployment logs    │    │
                                        │  │ • Analyze with Copilot CLI   │    │
                                        │  │ • Create GitHub issue 🔴     │    │
                                        │  │ • Assign to @copilot         │    │
                                        │  └─────────────────────────────┘    │
                                        └─────────────────────────────────────┘
```

### Workflow Summary

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `test.yml` | Push to main | Run unit tests, check coverage, trigger analysis if coverage < 90% |
| `deploy.yml` | After tests pass | Build Docker image, deploy to Azure Container Apps |

### Auto-Healing Features

1. **Low Coverage Detection**: If test coverage drops below 90%, Copilot CLI analyzes the codebase and creates an issue with suggestions for improving coverage
2. **Deployment Failure Recovery**: If deployment fails, Copilot CLI analyzes logs and creates an issue with root cause analysis and fix suggestions
3. **Automated Assignment**: Issues are automatically assigned to @copilot for AI-assisted resolution

## 🤖 Auto-Healing Feature

When a deployment fails, the workflow automatically:

1. **Captures Logs**: Collects Docker build output, Azure deployment logs, and container status
2. **Uploads Artifacts**: Stores failure logs for debugging
4. **Issue Creation**: Creates a detailed GitHub issue with:
   - AI-generated summary of the failure
   - Root cause analysis (when possible)
   - Suggested fixes
   - Full deployment logs
   - Links to the failed workflow run
   - Checklist for resolution

## 📋 Example Auto-Generated Issue

When a deployment fails, an issue like this is created:

> ## 🚨 Deployment Pipeline Failure
> 
> **Workflow Run:** [12345678](link)
> **Branch:** `main`
> **Commit:** `abc1234`
> 
> ---

> 
> ## 🤖 AI-Generated Analysis
> 
> **Summary:** The deployment failed due to a container health check timeout.
> 
> **Root Cause:** The application is not responding on port 80 within the expected timeframe.
> 
> **Suggested Fix:** 
> 1. Verify the Dockerfile exposes the correct port
> 2. Check if nginx is configured properly
> 3. Review the health check endpoint
> 
> ---
> 
> ## ✅ Next Steps
> - [ ] Review the AI analysis above
> - [ ] Check the full logs if needed
> - [ ] Identify and fix the root cause
> - [ ] Push a fix to trigger a new deployment
> - [ ] Close this issue once resolved

## 🛠️ Customization

### Using Different Container Registries

Update the workflow environment variables:

```yaml
env:
  AZURE_CONTAINER_REGISTRY: your-registry.azurecr.io
```

### Modifying the AI Prompt

Edit the prompt in `.github/workflows/deploy.yml`:

```yaml
PROMPT="Your custom prompt for analyzing failures..."
```

### Adding More Labels

Update the issue creation command:

```yaml
--label "bug,deployment,automated,priority-high"
```

### Slack/Teams Notifications

Add a notification step after issue creation:

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Deployment failed! Issue created: ${{ steps.create-issue.outputs.url }}"
      }
```

## 🔒 Security Notes

- Service principal has contributor access only to the specific resource group
- ACR credentials are stored as GitHub secrets
- Copilot CLI uses your GitHub token (already available in Actions)

## 📚 Resources

- [Azure Container Apps Documentation](https://learn.microsoft.com/en-us/azure/container-apps/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `docker build` and `docker run`
5. Submit a pull request

## 📝 License

MIT License - feel free to use this for your own projects!
