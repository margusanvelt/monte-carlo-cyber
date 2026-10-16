from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from ..core.models import RiskScenario, SimulationResult, DistributionModel, DistributionType, DistributionParams
from ..core.simulation import run_simulation

app = FastAPI(title="Quantitative Risk Assessment API")

# Mount static files if needed, but for simplicity we can serve a single HTML
# or use StaticFiles for a more robust setup.
# app.mount("/static", StaticFiles(directory="src/api/static"), name="static")

@app.post("/simulate", response_model=SimulationResult)
async def simulate(scenario: RiskScenario):
    """
    Run a Monte Carlo simulation.
    """
    try:
        result = run_simulation(scenario)
        # We might want to truncate the losses list for the API response if it's too large,
        # or keep it for the frontend to plot.
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/template", response_model=RiskScenario)
async def get_template():
    """
    Get a template risk scenario.
    """
    return RiskScenario(
        name="Example Data Breach",
        description="Loss from a single data breach event",
        frequency=DistributionModel(
            type=DistributionType.PERT,
            params=DistributionParams(min=0.1, most_likely=0.5, max=2.0)
        ),
        magnitude=DistributionModel(
            type=DistributionType.PERT,
            params=DistributionParams(min=50000, most_likely=500000, max=5000000)
        ),
        iterations=10000
    )

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = Path(__file__).parent / "static" / "index.html"
    if index_path.exists():
        with open(index_path, "r") as f:
            return f.read()
    return "<h1>Quantitative Risk Assessment App</h1><p>Static index.html not found.</p>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)

