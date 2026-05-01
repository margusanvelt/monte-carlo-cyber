import json
import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from ..core.models import RiskScenario, DistributionModel, DistributionType, DistributionParams
from ..core.simulation import run_simulation

app = typer.Typer(help="Quantitative Risk Assessment CLI")
console = Console()

@app.command()
def run(
    config: Path = typer.Argument(..., help="Path to the scenario JSON configuration file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Path to save simulation results")
):
    """
    Run a Monte Carlo simulation for a risk scenario.
    """
    if not config.exists():
        console.print(f"[red]Error: Configuration file {config} not found.[/red]")
        raise typer.Exit(code=1)
    
    try:
        with open(config, 'r') as f:
            data = json.load(f)
        
        scenario = RiskScenario(**data)
        console.print(f"Running simulation for: [bold blue]{scenario.name}[/bold blue]...")
        
        result = run_simulation(scenario)
        
        # Display results
        table = Table(title=f"Simulation Results: {scenario.name}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Iterations", f"{result.iterations:,}")
        table.add_row("Mean Loss", f"${result.mean_loss:,.2f}")
        table.add_row("Median Loss", f"${result.median_loss:,.2f}")
        table.add_row("95th Percentile (P95)", f"${result.p95_loss:,.2f}")
        table.add_row("99th Percentile (P99)", f"${result.p99_loss:,.2f}")
        
        console.print(table)
        
        if output:
            with open(output, 'w') as f:
                json.dump(result.model_dump(), f, indent=4)
            console.print(f"[green]Results saved to {output}[/green]")
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)

@app.command()
def template(
    path: Path = typer.Argument(Path("template.json"), help="Path to save the template file")
):
    """
    Generate a template scenario configuration file.
    """
    template_scenario = RiskScenario(
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
    
    with open(path, 'w') as f:
        json.dump(template_scenario.model_dump(by_alias=True), f, indent=4)
    
    console.print(f"[green]Template saved to {path}[/green]")

@app.command()
def wizard():
    """
    Interactive wizard to guide you through creating a risk scenario.
    """
    console.print("[bold blue]Welcome to the Risk Scenario Wizard![/bold blue]")
    console.print("This tool will help you define your risk in financial terms.\n")

    name = typer.prompt("1. Scenario Name (e.g., 'Ransomware Attack')")
    
    console.print("\n[bold]--- Frequency (How often does it happen?) ---[/bold]")
    console.print("We use the PERT distribution: think of the range over 1 year.")
    f_min = typer.prompt("   Min events/year (e.g., 0.05 for 1-in-20 years)", type=float)
    f_ml = typer.prompt("   Most Likely events/year (e.g., 0.1 for 1-in-10 years)", type=float)
    f_max = typer.prompt("   Max events/year (e.g., 0.5 for 1-in-2 years)", type=float)

    console.print("\n[bold]--- Magnitude (Financial impact per event) ---[/bold]")
    console.print("Include forensics, legal, fines, and lost productivity.")
    m_min = typer.prompt("   Min Loss ($)", type=float)
    m_ml = typer.prompt("   Most Likely Loss ($)", type=float)
    m_max = typer.prompt("   Max Loss ($)", type=float)

    iterations = typer.prompt("\nNumber of simulation iterations", default=10000, type=int)

    scenario = RiskScenario(
        name=name,
        frequency=DistributionModel(
            type=DistributionType.PERT,
            params=DistributionParams(min=f_min, most_likely=f_ml, max=f_max)
        ),
        magnitude=DistributionModel(
            type=DistributionType.PERT,
            params=DistributionParams(min=m_min, most_likely=m_ml, max=m_max)
        ),
        iterations=iterations
    )

    filename = f"{name.lower().replace(' ', '_')}_scenario.json"
    with open(filename, 'w') as f:
        json.dump(scenario.model_dump(by_alias=True), f, indent=4)
    
    console.print(f"\n[green]Success![/green] Scenario saved to [bold]{filename}[/bold]")
    if typer.confirm("Do you want to run the simulation now?"):
        run(Path(filename))

if __name__ == "__main__":
    app()
