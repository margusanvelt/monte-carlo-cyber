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
    - [Command Line Interface (CLI)](#command-line-interface-cli)
    - [Web Interface](#web-interface)
    - [Gemini CLI Skill](#gemini-cli-skill)
7. [Project Structure](#project-structure)

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
-   Python 3.10+
-   [Gemini CLI](https://github.com/google/gemini-cli) (optional, for Skill usage)

### 2. Setup Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage Guide

### Command Line Interface (CLI)
```bash
# Generate a sample scenario file
python3 -m src.cli.main template my_risk.json

# Run the simulation and see results
python3 -m src.cli.main run my_risk.json
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

### Web Interface
Launch the interactive dashboard:
```bash
PYTHONPATH=. uvicorn src.api.main:app --port 8000
```
Then visit [http://localhost:8000](http://localhost:8000) in your browser.

### Gemini CLI Skill
Install the skill in your workspace:
```bash
gemini skills install quantitative-risk-assessment.skill --scope workspace
```
Once installed, use natural language: *"Model a ransomware risk with frequency 0.1-0.5 and magnitude $1M-$10M."*

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

-   `src/core/`: Mathematical models and simulation logic.
-   `src/cli/`: Typer-based command line interface.
-   `src/api/`: FastAPI backend and HTML/JS frontend.
-   `skills/`: Gemini CLI skill definition.
-   `tests/`: Unit tests for the engine.
