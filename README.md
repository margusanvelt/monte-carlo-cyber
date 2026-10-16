# Quantitative Cyber Risk Assessment Application

A comprehensive toolset for performing quantitative (cyber) risk assessments using Monte Carlo simulations. Move away from qualitative heatmaps and toward data-driven financial loss models.

---

## Table of Contents
1. [Overview & Why Quantitative?](#overview--why-quantitative)
2. [What is Monte Carlo Simulation?](#what-is-monte-carlo-simulation)
3. [How to Conduct an Assessment](#how-to-conduct-an-assessment)
4. [Example Case Study: Data Breach](#example-case-study-data-breach)
5. [Installation & Setup](#installation--setup)
6. [Usage Guide](#usage-guide)
    - [Web Interface (Interactive Dashboard)](#web-interface-interactive-dashboard)
    - [Command Line Interface (CLI)](#command-line-interface-cli)
    - [Agent Skills (Google Antigravity & Claude)](#agent-skills-google-antigravity--claude)
7. [Interpreting Simulation Results](#interpreting-simulation-results)
8. [Project Structure](#project-structure)

---

## Overview & Why Quantitative?

Most organizations use **Qualitative** methods (High/Medium/Low, Red/Amber/Green). While easy to start, they suffer from:
- **Subjectivity**: One person's "High" is another's "Medium."
- **Compressed Ranges**: A $100k risk and a $10M risk both end up as "Red."
- **Mathematical Invalidity**: You cannot average "High" and "Low."

**Quantitative** assessment (this tool) provides:
- **Financial Clarity**: Communicates risk in dollars, which boards and CFOs understand.
- **Probabilistic Insight**: Instead of saying "it might happen," we say "there is a 5% chance of losing more than $2.4M this year."
- **Prioritization**: Enables clear ROI analysis for security investments.

### Comparison Table

| Feature | Qualitative (Heatmaps) | Quantitative (Monte Carlo) |
| :--- | :--- | :--- |
| **Input** | Gut feel, "High/Medium/Low" | Ranges (Min, Max, Most Likely) |
| **Output** | 5x5 Matrix (Colors) | Loss Exceedance Curves & $ Values |
| **Decision Support** | Emotional/Vague | Data-driven / Financial ROI |
| **Aggregation** | Impossible (High + Low = ?) | Accurate (Sum of all distributions) |

---

## What is Monte Carlo Simulation?

**Monte Carlo simulations** are used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of random variables. It is a technique used to understand the impact of risk and uncertainty in prediction and forecasting models.

### How it works:
1.  **Define a Model**: We define risk as `Frequency * Magnitude`.
2.  **Assign Distributions**: Instead of single numbers, we use probability distributions (like PERT or Lognormal) to represent our uncertainty.
3.  **Run Iterations**: The computer runs the model thousands of times (e.g., 10,000). In each iteration, it randomly samples a value from the frequency distribution and a value from the magnitude distribution.
4.  **Aggregate Results**: By looking at the results of all 10,000 runs, we can see the range of possible outcomes and how likely they are to occur.

### Further Reading:
- [Wikipedia: Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- [IBM: What is Monte Carlo Simulation?](https://www.ibm.com/topics/monte-carlo-simulation)
- [Investopedia: Monte Carlo Simulation](https://www.investopedia.com/terms/m/montecarlosimulation.asp)

---

## How to Conduct an Assessment

### 1. Identify the Risk Scenario
Don't model "Cyber Risk" (too broad). Model a specific event:
*   *"Loss of confidentiality of customer PII via SQL Injection on the web portal."*

### 2. Estimate Frequency (Loss Event Frequency - LEF)
How many times per year do you expect this to happen? Use a range:
*   **Min**: 0.05 (Once every 20 years)
*   **Most Likely**: 0.1 (Once every 10 years)
*   **Max**: 0.5 (Once every 2 years)

### 3. Estimate Magnitude (Loss Magnitude - LM)
If it happens, what is the cost? Consider primary (forensics, fines) and secondary (reputation, lost sales) losses.
*   *Example Range: $500k (Min), $2M (Most Likely), $10M (Max).*

### 4. Run the Simulation
The engine performs the sampling to account for the overlapping uncertainties of frequency and impact.

### 5. Interpret Results
- **Mean Loss**: The expected "average" annual loss.
- **P95 (Value at Risk)**: The "worst-case" scenario (only a 5% chance of losing more than this).

---

## Example Case Study: Data Breach

**Scenario**: Unauthorized access to 100,000 records.

| Metric | Estimation (PERT) |
| :--- | :--- |
| **Frequency** | 0.1 (Min), 0.2 (ML), 0.5 (Max) |
| **Magnitude** | $1M (Min), $5M (ML), $25M (Max) |

**Simulated Result**:
- **Mean Annual Loss**: ~$1.8M
- **P95 (Worst Case)**: ~$6.2M

*Decision Support*: If a security control costs $500k/year and reduces the P95 by $3M, it has a clear, justifiable ROI.

---

## Installation & Setup

### 1. Prerequisites
- **Python 3.10+**
- `git`

> [!IMPORTANT]
> **Always use a Python virtual environment (`.venv`).**
> Never install dependencies into your system/global Python environment. All installations, web server launches, CLI runs, and simulations must strictly use an active virtual environment or target `.venv/bin/python` / `.venv/bin/pip` (or `.venv\Scripts\` on Windows). This prevents dependency conflicts and ensures reproducibility.

### 2. Local Environment Setup

Follow these steps to create an isolated environment and install the required dependencies:

#### macOS & Linux
```bash
# 1. Clone the repository and navigate to the project directory
git clone <repository-url>
cd monte-carlo-cyber

# 2. Create the virtual environment
python3 -m venv .venv

# 3. Activate the virtual environment
source .venv/bin/activate

# 4. Install dependencies inside the virtual environment
pip install -r requirements.txt
```

#### Windows (PowerShell or Command Prompt)
```powershell
# 1. Create the virtual environment
python -m venv .venv

# 2. Activate the virtual environment
# In PowerShell:
.venv\Scripts\Activate.ps1
# In Command Prompt (cmd.exe):
.venv\Scripts\activate.bat

# 3. Install dependencies inside the virtual environment
pip install -r requirements.txt
```

> [!TIP]
> Confirm that your virtual environment is active before running commands (`(.venv)` will appear at the start of your shell prompt). If you open a new terminal window, remember to reactivate it (`source .venv/bin/activate`).

---

## Usage Guide

### Web Interface (Interactive Dashboard)

The web interface is the easiest way to model cyber risks, adjust distribution parameters in real time, and visualize loss exceedance distributions.

#### 1. Start the Web Server
Make sure your virtual environment is activated, then run:

```bash
python3 -m uvicorn src.api.main:app --reload --port 8000
```

*(Alternatively, you can start the server directly using Python: `python3 -m src.api.main`)*

#### 2. Open the Dashboard
Open your web browser and navigate to:
```
http://localhost:8000
```
*(or `http://127.0.0.1:8000`)*

#### 3. Run a Simulation
1. **Scenario Definition**: Enter a name (e.g., *"Customer Database Breach"* or *"Cloud Ransomware"*) and select the iteration count (default: `10,000`).
2. **Frequency (Annual Event Likelihood)**: Input the PERT distribution bounds for expected events per year:
   - **Minimum**: e.g., `0.05` (once every 20 years)
   - **Most Likely**: e.g., `0.2` (once every 5 years)
   - **Maximum**: e.g., `0.5` (once every 2 years)
3. **Magnitude (Impact per Event)**: Input the estimated financial loss ($) per incident:
   - **Minimum ($)**: e.g., `50000`
   - **Most Likely ($)**: e.g., `250000`
   - **Maximum ($)**: e.g., `1500000`
4. Click **Run Monte Carlo Simulation**.
5. View the statistical outputs (**Mean Annual Loss**, **P95 Value at Risk**, **Median Loss**) and the interactive histogram of simulated outcomes.
6. When finished, stop the web server by pressing `Ctrl + C` in your terminal.

---

### Command Line Interface (CLI)

The CLI tool supports headless runs, automation scripts, and interactive wizards:

```bash
# Generate a sample scenario JSON file
python3 -m src.cli.main template my_risk.json

# Run a simulation from a JSON file and view formatted table results
python3 -m src.cli.main run my_risk.json

# Save simulation outputs to a JSON file
python3 -m src.cli.main run my_risk.json --output results.json

# Interactive CLI wizard that walks you through parameter definition
python3 -m src.cli.main wizard
```

#### JSON Input Schema
```json
{
  "name": "Data Breach",
  "iterations": 10000,
  "frequency": {
    "type": "pert",
    "params": { "min": 0.1, "most_likely": 0.5, "max": 2.0 }
  },
  "magnitude": {
    "type": "pert",
    "params": { "min": 10000, "most_likely": 50000, "max": 250000 }
  }
}
```

---

### Agent Skills (Google Antigravity & Claude)

This repository includes a skill conforming to the open [Agent Skills specification](https://agentskills.io) (`skills/quantitative-risk-assessment/SKILL.md`). This enables AI coding agents and LLMs to autonomously model cyber risks, invoke Monte Carlo simulations, and interpret financial loss metrics from plain-language user requests.

#### 1. Installing in Google Antigravity (IDE & CLI)

Antigravity natively indexes and activates skills using progressive disclosure:

- **Workspace / Project Scope (Recommended)**:
  Copy the skill folder into the `.agents/skills` directory in your workspace:
  ```bash
  mkdir -p .agents/skills
  cp -r skills/quantitative-risk-assessment .agents/skills/
  ```
  *(Antigravity automatically discovers skills inside `.agents/skills/` whenever this project is opened in the Antigravity IDE or CLI `agy`.)*

- **Global Scope (Available across all projects)**:
  Copy the skill folder into your user's global Antigravity config directory:
  ```bash
  mkdir -p ~/.gemini/config/skills
  cp -r skills/quantitative-risk-assessment ~/.gemini/config/skills/
  ```

#### 2. Installing in Claude (Claude Code & Claude.ai / Cowork)

- **Claude Code (Terminal CLI)**:
  - **Project Scope**:
    ```bash
    mkdir -p .claude/skills
    cp -r skills/quantitative-risk-assessment .claude/skills/
    ```
  - **Global Scope**:
    ```bash
    mkdir -p ~/.claude/skills
    cp -r skills/quantitative-risk-assessment ~/.claude/skills/
    ```

- **Claude.ai / Cowork / Claude Desktop (Web & App)**:
  1. Open Claude.ai or Claude Desktop.
  2. Navigate to your user settings or sidebar and click **Customize** (or the **Skills** tab).
  3. Click **+ Create skill** (or **Upload a skill**).
  4. Upload the packaged archive [`quantitative-risk-assessment.zip`](./quantitative-risk-assessment.zip) located in the root of this repository.
  *(Note: Ensure code execution/analysis is enabled in Claude's settings).*

#### 3. Legacy Gemini CLI (Optional)
If using the legacy Gemini CLI:
```bash
gemini skills install quantitative-risk-assessment.skill --scope workspace
```

#### Natural Language Usage Examples
Once installed in either Antigravity or Claude, simply prompt the AI assistant:
- *"Model a ransomware risk with frequency between 0.1 and 0.5 events/year and financial loss between $1M and $10M (most likely $3M)."*
- *"Simulate our exposure to a cloud provider outage with 10,000 iterations and show the P95 Value at Risk."*
- *"If a $250k security control cuts our breach frequency in half, calculate the expected annual financial ROI."*

---

## Interpreting Simulation Results

After running the simulation, you will receive several metrics. Here is how to use them for business decisions:

### 1. Mean Annual Loss (Average)
*   **What it is**: The mathematical average of all simulated years.
*   **Business Use**: Use this for **budgeting**. If your Mean Annual Loss for all risks is $1M, you should expect to lose roughly that much over a long period. It helps you decide if a security control is "worth it" based on how much it reduces this average.

### 2. P95 - Value at Risk (The "Worst Case")
*   **What it is**: There is only a **5% chance** that the actual loss will be *higher* than this number.
*   **Business Use**: Use this for **resilience and insurance**. This tells you how much capital you might need to "survive" a very bad year. If your P95 is $10M but you only have $2M in the bank, you have a critical solvency risk.

### 3. Median (P50)
*   **What it is**: The middle value. 50% of the simulated years were lower than this, and 50% were higher.
*   **Business Use**: If your distribution is "skewed" (a few very large losses), the Median will be much lower than the Mean. This tells you that in most years, the risk is actually quite manageable, but the rare "Black Swan" events are what drive the average up.

### 4. P99 (Extreme Case)
*   **What it is**: The "1-in-100 year" event. 
*   **Business Use**: Useful for high-compliance environments or critical infrastructure where even a 1% failure rate is unacceptable.

---

## Project Structure

- `src/core/`: Mathematical models, probability distributions (PERT, Lognormal, Poisson), and simulation logic.
- `src/cli/`: Typer-based command line interface and interactive wizard.
- `src/api/`: FastAPI backend with embedded web dashboard and Chart.js visualization.
- `skills/`: Agent skill definition conforming to the open Agent Skills standard.
- `quantitative-risk-assessment.zip`: Ready-to-upload skill package for Claude.ai / Cowork.
- `quantitative-risk-assessment.skill`: Packaged skill archive for Gemini CLI.
- `tests/`: Unit tests for the engine.

