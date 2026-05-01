---
name: quantitative-risk-assessment
description: Model and simulate cyber risks using Monte Carlo methods. Use when the user wants to conduct quantitative risk assessments, build risk models (Loss Event Frequency and Magnitude), and run simulations to find Mean Loss, P95, and other risk metrics.
---

# Quantitative Risk Assessment

This skill enables Gemini CLI to perform quantitative risk assessments using Monte Carlo simulations. It helps users move away from qualitative "Red/Amber/Green" scales to data-driven financial loss models.

## Workflow

1.  **Define Scenario**: Identify the risk (e.g., Data Breach, System Outage).
2.  **Estimate Frequency**: Determine how often the event occurs per year using a distribution (Constant, PERT, Poisson).
3.  **Estimate Magnitude**: Determine the financial loss if the event occurs using a distribution (Constant, PERT, Lognormal).
4.  **Run Simulation**: Use the `simulate.py` script to run 10,000+ iterations.
5.  **Interpret Results**: Analyze Mean Loss and P95 (Value at Risk).

## Distribution Types

*   **PERT**: Best for expert estimates. Requires `min`, `most_likely`, and `max`.
*   **Constant**: Use when a value is fixed. Requires `value`.
*   **Lognormal**: Good for long-tailed loss magnitudes. Requires `mean` and `std_dev`.
*   **Poisson**: Good for event counts. Requires `mean`.

## Examples

### Example 1: Ransomware Risk
User: "Model the risk of a ransomware attack. We expect it once every 5 years, with losses between $1M and $10M, most likely $3M."

Assistant: I will model this using a PERT distribution for both frequency (0.1, 0.2, 0.5 events/year) and magnitude ($1M, $3M, $10M).

### Running a Simulation

Use the bundled script:
```bash
python3 skills/quantitative-risk-assessment/scripts/simulate.py '<JSON_CONFIG>'
```

JSON Config Schema:
```json
{
  "name": "Ransomware",
  "frequency": { "type": "pert", "params": { "min": 0.1, "most_likely": 0.2, "max": 0.5 } },
  "magnitude": { "type": "pert", "params": { "min": 1000000, "most_likely": 3000000, "max": 10000000 } },
  "iterations": 10000
}
```

## Resources

### scripts/simulate.py
A Python script that performs the Monte Carlo simulation and returns summary statistics in JSON format.
