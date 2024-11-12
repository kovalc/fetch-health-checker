# HTTP Endpoint Health Checker

A Python application that monitors HTTP endpoints and tracks their availability percentage over time. Created as part of the Fetch Site Reliability Engineering take-home exercise.

## Overview

This program reads a YAML configuration file containing HTTP endpoints to monitor, checks their health status every 15 seconds, and reports the availability percentage for each domain. An endpoint is considered UP if it returns a 2xx status code and responds within 500ms.

## Requirements

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment (recommended):
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program by providing a YAML configuration file:
```bash
python health_checker.py endpoints.yaml
```

The program will:
- Check each endpoint every 15 seconds
- Calculate and display availability percentages per domain
- Continue running until interrupted with CTRL+C

### Example Output
```
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
```

## Configuration

The program accepts a YAML file listing endpoints to monitor. Each endpoint can have:

- `name` (required): Description of the endpoint
- `url` (required): The HTTP/HTTPS URL to check
- `method` (optional): HTTP method (defaults to GET)
- `headers` (optional): HTTP headers to include
- `body` (optional): Request body (JSON format)

Example configuration:
```yaml
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch index page
  url: https://fetch.com/
```

## Design Decisions

1. **In-Memory Storage**: Statistics are stored in memory as specified in requirements
2. **Error Handling**: All HTTP requests are wrapped in try-except blocks to handle timeouts and errors gracefully
3. **Domain Parsing**: Used urllib.parse for reliable domain extraction
4. **Graceful Shutdown**: Implemented signal handler for clean program termination

## Files In Repository

- `health_checker.py`: Main program file
- `endpoints.yaml`: Example configuration file
- `requirements.txt`: Python dependencies
- `README.md`: Documentation
- `.gitignore`: Git ignore rules

## Testing

To test the program, you can:
1. Use the provided `endpoints.yaml` file
2. Create your own YAML file with different endpoints
3. Modify existing endpoints to test different scenarios

## Notes
- The program uses no persistent storage (as per requirements)
- Statistics are calculated over the lifetime of the program
- The program can be safely terminated using CTRL+C

## Author
Connor Koval