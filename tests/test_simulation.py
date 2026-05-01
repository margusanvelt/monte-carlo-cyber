import pytest
from src.core.models import RiskScenario, DistributionModel, DistributionType, DistributionParams
from src.core.simulation import run_simulation

def test_basic_simulation():
    scenario = RiskScenario(
        name="Data Breach",
        frequency=DistributionModel(
            type=DistributionType.CONSTANT,
            params=DistributionParams(value=1.0)
        ),
        magnitude=DistributionModel(
            type=DistributionType.PERT,
            params=DistributionParams(min=10000, most_likely=50000, max=200000)
        ),
        iterations=1000
    )
    
    result = run_simulation(scenario)
    
    assert result.scenario_name == "Data Breach"
    assert result.iterations == 1000
    assert 10000 <= result.mean_loss <= 200000
    assert len(result.losses) == 1000

def test_pert_distribution_bounds():
    from src.core.simulation import sample_pert
    samples = sample_pert(10, 50, 100, 1000)
    assert all(10 <= s <= 100 for s in samples)
    # Most samples should be around the most likely value
    import numpy as np
    assert 40 <= np.mean(samples) <= 60
