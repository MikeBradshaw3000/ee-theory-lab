import pandas as pd
from pathlib import Path

# Target directory
out_dir = Path("phase_4b/tier2_outputs")

# Find all individual files (excluding the master file if it exists)
files = [f for f in out_dir.glob("global_timeseries_*.csv") if f.name != "global_timeseries.csv"]

print(f"Found {len(files)} individual timeseries files. Merging and injecting run_id...")

dfs = []
for f in files:
    df = pd.read_csv(f)
    # Extract the run_id from the filename
    run_id = f.stem.replace("global_timeseries_", "")
    
    # Inject the run_id as a new column so Tier 3 can join on it
    df['run_id'] = run_id
    dfs.append(df)

# Combine and save
merged = pd.concat(dfs, ignore_index=True)
master_path = out_dir / "global_timeseries.csv"
merged.to_csv(master_path, index=False)

print(f"SUCCESS: Master file created at {master_path} with 'run_id' column injected.")