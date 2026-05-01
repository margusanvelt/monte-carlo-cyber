import numpy as np
from scipy.stats import beta
from .models import RiskScenario, SimulationResult, DistributionType

def sample_pert(min_val, most_likely, max_val, iterations, lambd=4):
    """
    Modified PERT distribution.
    """
    if min_val >= max_val:
        return np.full(iterations, min_val)
    
    # Calculate alpha and beta for the beta distribution
    alpha = 1 + lambd * (most_likely - min_val) / (max_val - min_val)
    beta_param = 1 + lambd * (max_val - most_likely) / (max_val - min_val)
    
    # Sample from beta and scale
    samples = beta.rvs(alpha, beta_param, size=iterations)
    return min_val + samples * (max_val - min_val)

def get_samples(dist_model, iterations):
    params = dist_model.params
    if dist_model.type == DistributionType.PERT:
        return sample_pert(params.min_val, params.most_likely, params.max_val, iterations)
    elif dist_model.type == DistributionType.LOGNORMAL:
        # Assuming params.mean and params.std_dev are provided
        return np.random.lognormal(params.mean, params.std_dev, iterations)
    elif dist_model.type == DistributionType.POISSON:
        return np.random.poisson(params.mean, iterations)
    elif dist_model.type == DistributionType.CONSTANT:
        return np.full(iterations, params.value)
    else:
        raise ValueError(f"Unsupported distribution type: {dist_model.type}")

def run_simulation(scenario: RiskScenario) -> SimulationResult:
    iterations = scenario.iterations
    
    # Sample frequency (events per year)
    frequencies = get_samples(scenario.frequency, iterations)
    
    # Sample magnitude (loss per event)
    magnitudes = get_samples(scenario.magnitude, iterations)
    
    # Calculate total loss for each iteration
    # Simplified: Frequency * Magnitude
    # In more complex models, frequency might be a count of events, 
    # and we'd sample magnitude for each event.
    losses = frequencies * magnitudes
    
    return SimulationResult(
        scenario_name=scenario.name,
        iterations=iterations,
        mean_loss=float(np.mean(losses)),
        median_loss=float(np.median(losses)),
        p95_loss=float(np.percentile(losses, 95)),
        p99_loss=float(np.percentile(losses, 99)),
        losses=losses.tolist()
    )
