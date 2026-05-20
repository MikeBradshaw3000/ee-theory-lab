import pathlib
p = pathlib.Path(r'C:\Users\vkz244\EE_Theory_Lab\ee-theory-lab\phase_4b\scripts\tier3_regression.py')
t = p.read_text(encoding='utf-8')
broken = 'result_primary.summary().as_text() + "\\n\n```\\n")'
fixed = 'result_primary.summary().as_text() + "\\n```\\n")'
t2 = t.replace(broken, fixed)
p.write_text(t2, encoding='utf-8')
print('replaced:', t != t2)
