"""Apply path-resolution fix to tier3_regression.py.

Adds get_paths to the import from _phase_4b_common, calls get_paths once before the
data-loading loop, and modifies the loop to resolve bare filenames against flight2_pq_dir.
"""
import pathlib

script_path = pathlib.Path(r"C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\phase_4b\scripts\tier3_regression.py")
content = script_path.read_text(encoding="utf-8")

# Edit 1: add get_paths to the import
old_import = "from _phase_4b_common import verify_environment, eta_floor_inversion"
new_import = "from _phase_4b_common import verify_environment, eta_floor_inversion, get_paths"
content_1 = content.replace(old_import, new_import)

# Edit 2: modify the data-loading loop to resolve bare filenames
old_loop = """    # Load files and R9: Shadow-copy / independent-run guard
    dfs = []
    file_stems = []
    file_sizes = set() # Lightweight heuristic to detect shadow copies
    
    for fpath in spec['data_files']:
        p = Path(fpath)
        file_stems.append(p.stem)
        
        # Track file sizes to heuristically detect byte-identical shadow copies
        if p.exists():
            file_sizes.add(os.path.getsize(p))
            
        df_part = pd.read_parquet(p)
        df_part['run_id'] = p.stem
        dfs.append(df_part)"""

new_loop = """    # Load files and R9: Shadow-copy / independent-run guard
    # Path resolution per Layer 2 review (2026-05-18): bare filenames resolve against
    # flight2_pq_dir from _phase_4b_common.get_paths(); absolute paths used as-is.
    _, flight2_pq_dir, _ = get_paths()
    dfs = []
    file_stems = []
    file_sizes = set() # Lightweight heuristic to detect shadow copies
    resolved_paths = []  # For report transparency
    
    for fpath in spec['data_files']:
        p = Path(fpath)
        # Bare filename (no parent directory) → resolve against canonical Flight 2 data dir
        if p.parent == Path('.') or not p.is_absolute() and len(p.parts) == 1:
            p = flight2_pq_dir / p
        if not p.exists():
            raise FileNotFoundError(
                f"T3 FAULT: data file not found after path resolution: {p}. "
                f"YAML listed: {fpath!r}. flight2_pq_dir resolved to: {flight2_pq_dir}"
            )
        resolved_paths.append(str(p))
        file_stems.append(p.stem)
        
        # Track file sizes to heuristically detect byte-identical shadow copies
        file_sizes.add(os.path.getsize(p))
            
        df_part = pd.read_parquet(p)
        df_part['run_id'] = p.stem
        dfs.append(df_part)"""

content_2 = content_1.replace(old_loop, new_loop)

# Verify both edits happened
edits_applied = (content_2 != content) and (content_2 != content_1) and ("get_paths" in content_2) and ("flight2_pq_dir" in content_2)

script_path.write_text(content_2, encoding="utf-8")
print(f"Edit 1 (import): {'APPLIED' if content_1 != content else 'NOT APPLIED'}")
print(f"Edit 2 (loop):   {'APPLIED' if content_2 != content_1 else 'NOT APPLIED'}")
print(f"Both edits successful: {edits_applied}")
