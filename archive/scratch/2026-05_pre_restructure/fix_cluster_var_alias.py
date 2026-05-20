"""Apply cluster_variable name fix to tier3_regression.py.

YAML's uncertainty_method.cluster_variable is 'run_x_tick' (per Gemini routing).
Code's build_cluster_group function checks for 'cluster_run_tick'. Add 'run_x_tick'
as an accepted alias so the YAML and code align without modifying canonical YAML.
"""
import pathlib

script_path = pathlib.Path(r"C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\phase_4b\scripts\tier3_regression.py")
content = script_path.read_text(encoding="utf-8")

old_check = "    if cluster_var == 'cluster_run_tick':"
new_check = "    if cluster_var in ('cluster_run_tick', 'run_x_tick'):"

content_new = content.replace(old_check, new_check)
edit_applied = content_new != content
script_path.write_text(content_new, encoding="utf-8")
print(f"Cluster variable name fix: {'APPLIED' if edit_applied else 'NOT APPLIED'}")
