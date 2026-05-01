import sys
import json
import numpy as np
from core.models import RiskScenario
from core.simulation import run_simulation

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 simulate.py '<json_scenario>'")
        sys.exit(1)
    
    try:
        scenario_data = json.loads(sys.argv[1])
        scenario = RiskScenario(**scenario_data)
        result = run_simulation(scenario)
        
        output = {
            "scenario_name": result.scenario_name,
            "iterations": result.iterations,
            "mean_loss": result.mean_loss,
            "median_loss": result.median_loss,
            "p95_loss": result.p95_loss,
            "p99_loss": result.p99_loss,
            "summary": f"Simulation for '{result.scenario_name}' completed. Mean: ${result.mean_loss:,.2f}, P95: ${result.p95_loss:,.2f}"
        }
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
