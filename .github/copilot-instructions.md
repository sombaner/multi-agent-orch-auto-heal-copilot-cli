# Copilot Instructions for Autohealing Demo

## Project Overview

This is a **Ticket Tracker** application - a simple Kanban-style ticket management system with auto-healing deployment capabilities. The application demonstrates:

- Python Flask REST API backend for CRUD operations
- HTML/JavaScript frontend with two views (ticket creation and Kanban board)
- JSON file-based storage
- Containerized deployment to Azure Container Apps
- Auto-healing GitHub Actions workflow that creates issues when deployments fail

## Repository Structure

```
autohealing_demo/
├── .github/
│   ├── agents/                      # Custom agent definitions
│   │   └── arch.agent.md           # Architecture agent
│   ├── workflows/
│   │   └── deploy.yml              # CI/CD with auto-healing
│   ├── copilot-instructions.md     # This file
│   └── copilot-setup-steps.yaml    # Environment setup
├── src/
│   ├── app.py                      # Flask API server
│   ├── index.html                  # Create ticket page
│   ├── board.html                  # Kanban board view
│   ├── requirements.txt            # Python dependencies
│   └── tickets_data.json           # Ticket data storage
├── scripts/
│   └── setup-azure.sh              # Azure resource setup
├── Dockerfile                      # Container definition
└── README.md                       # Documentation
```

## Technology Stack

- **Backend**: Python 3.11 with Flask 3.0.0
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Storage**: JSON file-based (tickets_data.json)
- **Container**: Docker with Python 3.11-slim base image
- **Deployment**: Azure Container Apps
- **CI/CD**: GitHub Actions with automated issue creation on failures

## Coding Standards

### Python (Backend)

- **Style**: Follow PEP 8 style guide
- **Docstrings**: Use Google-style docstrings for functions and classes
- **Type Hints**: Not currently used, maintain consistency
- **Error Handling**: Use try-except blocks for file operations and return appropriate HTTP status codes
- **API Responses**: Always return JSON with appropriate status codes
  - 200: Success
  - 201: Resource created
  - 400: Bad request (missing fields)
  - 404: Resource not found
- **Date/Time**: Use ISO 8601 format via `datetime.now().isoformat()`

### Frontend (HTML/JavaScript)

- **HTML**: Use semantic HTML5 elements
- **CSS**: Inline styles are acceptable for this simple project
- **JavaScript**: Vanilla JS, no frameworks
- **API Calls**: Use `fetch()` API with proper error handling
- **User Feedback**: Show loading states and error messages to users

### Docker

- **Base Image**: Use `python:3.11-slim` for efficiency
- **Port**: Application runs on port 80
- **Health Check**: Include HEALTHCHECK directive for container orchestration
- **Optimization**: Copy requirements.txt first for better layer caching

## Workflow and Development Guidelines

### Making Changes

1. **Minimal Changes**: Make the smallest possible changes to achieve the goal
2. **Test Locally**: Always test changes locally before committing
   ```bash
   cd src
   pip install -r requirements.txt
   python app.py
   ```
3. **Docker Testing**: Build and test the container locally
   ```bash
   docker build -t ticket-tracker .
   docker run -p 80:80 ticket-tracker
   ```

### API Endpoints

When working with the API, remember these endpoints:

- `GET /api/tickets` - Get all tickets
- `GET /api/tickets/:id` - Get a specific ticket
- `POST /api/tickets` - Create a new ticket (requires: title, description, due_date)
- `PUT /api/tickets/:id` - Update a ticket (optional: title, description, due_date, status)
- `DELETE /api/tickets/:id` - Delete a ticket

### Data Model

Ticket structure:
```json
{
  "id": "uuid-string",
  "title": "string",
  "description": "string",
  "due_date": "YYYY-MM-DD",
  "status": "todo|in-progress|review|completed",
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp or null (set after first update)"
}
```

## Files You Should NOT Modify

- **`.github/agents/arch.agent.md`** - Custom architecture agent definition
- **`scripts/setup-azure.sh`** - Azure infrastructure setup (unless explicitly requested)
- **`.git/`** - Git internal files

## Auto-Healing Workflow

The `.github/workflows/deploy.yml` workflow includes auto-healing capabilities:

- **On Failure**: Automatically creates a GitHub issue with:
  - AI-generated summary using GitHub Copilot CLI
  - Root cause analysis
  - Suggested fixes
  - Full deployment logs
  - Assignment to @copilot for resolution

When working on deployment issues:
1. Read the auto-generated issue carefully
2. Analyze the provided logs
3. Make targeted fixes
4. Test locally before pushing
5. Close the issue once resolved

## Dependencies

### Python Dependencies
- **Flask 3.0.0**: Web framework for the API

To add new Python dependencies:
1. Add to `src/requirements.txt`
2. Update Dockerfile if needed (usually automatic via `pip install -r requirements.txt`)
3. Test locally before committing

## Azure Deployment

The application deploys to Azure Container Apps with these environment variables:
- `COMMIT_SHA`: Git commit SHA for tracking

Required GitHub Secrets:
- `AZURE_CONTAINER_REGISTRY`: ACR login server
- `REGISTRY_USERNAME`: ACR admin username
- `REGISTRY_PASSWORD`: ACR admin password
- `AZURE_RESOURCE_GROUP`: Resource group name
- `AZURE_CREDENTIALS`: Service principal JSON
- `GH_TOKEN`: GitHub token for issue creation
- `COPILOT_GITHUB_TOKEN`: Fine-grained PAT for Copilot access

## Testing Guidelines

Currently, this project does not have automated tests. When adding functionality:

1. **Manual Testing**: Test all changes manually
2. **API Testing**: Use curl or Postman to test API endpoints
3. **UI Testing**: Verify UI changes in a browser
4. **Docker Testing**: Always test container builds

## Common Tasks

### Adding a New API Endpoint
1. Add route decorator to `src/app.py`
2. Implement handler function with proper error handling
3. Return JSON with appropriate status code
4. Test with curl locally
5. Update README.md if it's a public-facing endpoint

### Modifying the Frontend
1. Edit `src/index.html` or `src/board.html`
2. Test in browser at `http://localhost:80`
3. Ensure mobile responsiveness if applicable
4. Check console for JavaScript errors

### Changing the Data Model
1. Update ticket structure in `src/app.py`
2. Consider data migration for existing `tickets_data.json`
3. Update API documentation in README.md
4. Test create/read/update operations

## Security Considerations

- **Input Validation**: Always validate user input
- **SQL Injection**: Not applicable (using JSON file storage)
- **XSS**: Sanitize any user-generated content displayed in HTML
- **Secrets**: Never commit secrets, use GitHub Secrets
- **Port 80**: Application runs as root in container on port 80

## Performance Considerations

- **File I/O**: JSON file storage is suitable for demo/small-scale use
- **Concurrency**: Flask development server is single-threaded (acceptable for demo)
- **Scalability**: For production, consider:
  - Database instead of JSON file
  - WSGI server (gunicorn, uWSGI)
  - Redis for caching
  - Multiple container replicas

## Documentation Standards

- **README.md**: Keep updated with any new features or deployment steps
- **Code Comments**: Add comments for complex logic only
- **Commit Messages**: Use clear, descriptive commit messages
- **API Documentation**: Update README.md for any API changes

## Need Help?

- Check the README.md for quick start and deployment instructions
- Review existing code in `src/app.py` for patterns
- Refer to Flask documentation: https://flask.palletsprojects.com/
- Check GitHub Actions logs for deployment issues

## Custom Agents

This repository includes specialized agents:

- **Architecture Agent** (`.github/agents/arch.agent.md`): Use for architectural design questions, creating diagrams, and NFR analysis. This agent does NOT generate code.
