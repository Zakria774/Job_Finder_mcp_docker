# Job Finder MCP Server

A Model Context Protocol (MCP) server built with Python that allows Claude Desktop to search for remote job listings using Playwright browser automation. The project is fully containerized with Docker for easy deployment and portability.

---

## Features

- Search remote jobs using Playwright
- MCP server compatible with Claude Desktop
- Dockerized for easy deployment
- Uses Groq API for intelligent processing
- Supports environment variables for secure API key management

---

## Tech Stack

- Python 3.12
- Model Context Protocol (MCP)
- Playwright
- Docker
- Claude Desktop
- Groq API

---

## Project Structure

```
Job_Finder_mcp_docker/
│
├── mcp_job.py          # MCP server implementation
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Zakria774/Job_Finder_mcp_docker.git
cd Job_Finder_mcp_docker
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Create a .env file

Create a file named `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

> **Do not upload your `.env` file to GitHub.**

---

## Running Locally

Start the MCP server:

```bash
python mcp_job.py
```

The server will wait for requests from an MCP client such as Claude Desktop.

---

## Running with Docker

Build the Docker image:

```bash
docker build -t job_finder .
```

Run the Docker container:

```bash
docker run -i --rm job_finder
```

---

## Claude Desktop Configuration

Add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "job_finder": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "job_finder"
      ]
    }
  }
}
```

Restart Claude Desktop after saving the configuration.

---

## Example Prompt

```
Find me remote Python jobs using my job finder tool.
```

Claude Desktop will invoke the MCP server and return job listings.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| GROQ_API_KEY | Your Groq API key |

---

## Security

Ensure your `.gitignore` includes:

```
.env
.venv/
__pycache__/
*.pyc
```

Never commit API keys or secrets to GitHub.

---

## Author

**Muhammad Zakria**

GitHub: https://github.com/Zakria774

---

## License

This project is open source and available under the MIT License.
