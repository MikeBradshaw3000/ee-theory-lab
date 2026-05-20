"""Apply outcome name extraction fix to tier3_regression.py.

The YAML's outcome field is a structured dict (name, construction, ETA, notes), not
a string. Current code uses spec['outcome'] directly, which renders as a dict in the
formula string and fails the eta_floor conditional (string == dict is always False).

Extract spec['outcome']['name'] as the actual column name. Use it in the conditional
and the formula construction.
"""
import pathlib

script_path = pathlib.Path(r"C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\phase_4b\scripts\tier3_regression.py")
content = script_path.read_text(encoding="utf-8")

# Edit 1: eta_floor conditional
old_eta_check = "    if spec['outcome'] == 'logit_p_base':\n        df['logit_p_base'], boundary_count = eta_floor_inversion(df['p_act'])"
new_eta_check = "    outcome_name = spec['outcome']['name'] if isinstance(spec['outcome'], dict) else spec['outcome']\n    if outcome_name == 'logit_p_base':\n        df['logit_p_base'], boundary_count = eta_floor_inversion(df['p_act'])"

content_1 = content.replace(old_eta_check, new_eta_check)

# Edit 2: formula string construction
old_formula = "    formula_str = f\"{spec['outcome']} ~ \" + \" + \".join(formula_parts)"
new_formula = "    formula_str = f\"{outcome_name} ~ \" + \" + \".join(formula_parts)"

content_2 = content_1.replace(old_formula, new_formula)

# Edit 3: also fix the report-writing reference to outcome
old_report_outcome = "        if spec['outcome'] == 'logit_p_base':"
new_report_outcome = "        if outcome_name == 'logit_p_base':"

content_3 = content_2.replace(old_report_outcome, new_report_outcome)

# Verify all three edits applied
edit_1 = content_1 != content
edit_2 = content_2 != content_1
edit_3 = content_3 != content_2

script_path.write_text(content_3, encoding="utf-8")
print(f"Edit 1 (eta_floor check):    {'APPLIED' if edit_1 else 'NOT APPLIED'}")
print(f"Edit 2 (formula string):     {'APPLIED' if edit_2 else 'NOT APPLIED'}")
print(f"Edit 3 (report outcome ref): {'APPLIED' if edit_3 else 'NOT APPLIED'}")
print(f"All edits successful: {edit_1 and edit_2 and edit_3}")
