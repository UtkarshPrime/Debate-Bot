# LangGraph Debate System

A structured debate system between two AI agents (Scientist vs Philosopher) using LangGraph.

## Features
- **Structured Workflow**: Exactly 8 rounds of alternating turns.
- **Memory Management**: Agents receive relevant context.
- **Judge Node**: Declares a winner with reasoning.
- **Logging**: Full debate logs in JSON format.
- **Mock Mode**: Run without API keys for testing.

## Installation

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Copy `.env.example` to `.env` (if provided, or just set `GOOGLE_API_KEY`).
   - Or set `GOOGLE_API_KEY` in your shell.

## Usage

### Run Debate
```bash
python run_debate.py --topic "Should AI be regulated?"
```

### Options
- `--mock`: Run in mock mode (no API calls).
- `--topic`: Specify the debate topic.

### Generate DAG
```bash
python generate_dag.py
```
This will generate `dag.png` (requires internet for Mermaid service) or print Mermaid code.

## Project Structure
- `nodes/`: Contains LangGraph node definitions.
- `personas/`: Agent persona prompts.
- `utils/`: Helper functions (logging).
- `run_debate.py`: Main entry point.
- `config.py`: Configuration.

## Testing
Run unit tests:
```bash
python -m unittest discover tests
```
