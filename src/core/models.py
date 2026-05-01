from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class DistributionType(str, Enum):
    PERT = "pert"
    LOGNORMAL = "lognormal"
    POISSON = "poisson"
    CONSTANT = "constant"

class DistributionParams(BaseModel):
    min_val: Optional[float] = Field(None, alias="min")
    most_likely: Optional[float] = Field(None, alias="most_likely")
    max_val: Optional[float] = Field(None, alias="max")
    mean: Optional[float] = None
    std_dev: Optional[float] = None
    value: Optional[float] = None

class DistributionModel(BaseModel):
    type: DistributionType
    params: DistributionParams

class RiskScenario(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: DistributionModel
    magnitude: DistributionModel
    iterations: int = 10000

class SimulationResult(BaseModel):
    scenario_name: str
    iterations: int
    mean_loss: float
    median_loss: float
    p95_loss: float
    p99_loss: float
    losses: List[float] = Field(default_factory=list)
