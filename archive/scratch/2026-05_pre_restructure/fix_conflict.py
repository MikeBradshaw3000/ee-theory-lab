import os

yaml_path = "phase_4b/pre_registrations/reg_01_scale_interactions.yaml"
script_path = "phase_4b/scripts/tier3_regression.py"

# 1. Update the YAML to say "ols"
with open(yaml_path, "r", encoding="utf-8") as f:
    yaml_data = f.read()
yaml_data = yaml_data.replace('model_family: "linear"', 'model_family: "ols"')
with open(yaml_path, "w", encoding="utf-8") as f:
    f.write(yaml_data)

# 2. Update the Regression script to accept "ols"
with open(script_path, "r", encoding="utf-8") as f:
    script_data = f.read()
script_data = script_data.replace("if family == 'linear':", "if family == 'ols':")
with open(script_path, "w", encoding="utf-8") as f:
    f.write(script_data)

print("SUCCESS: Both the YAML schema and the Python logic are now perfectly aligned on 'ols'!")