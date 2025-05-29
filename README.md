# mcp-agent

A FastAPI-based backend project.

## Setup

### Clone the repo
```bash
git clone https://github.com/you/mcp-agent.git
cd mcp-agent
```

### Create a virtualenv and install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Install Playwright's browsers
```bash
playwright install
```

### Configure your environment
```bash
cp .env.example .env
# then edit .env and set MCP_API_KEY=your_secret_key
```

### Running the service
```bash
export MCP_API_KEY=your_secret_key
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will now be available at [http://localhost:8000](http://localhost:8000)
