import json

notebook_path = '4_analysis.ipynb'
with open(notebook_path, 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if "h = r['history']" in line:
                # We want to replace the plotting part to be robust against missing history
                source[i] = "        if 'history' not in r:\n"
                source.insert(i+1, "            ax.text(0.5, 0.5, 'History not saved\\n(5-Fold CV)', ha='center', va='center', fontsize=10)\n")
                source.insert(i+2, "            ax.set_title(f\"{r['model']} / {r.get('feature','')}\\n{r.get('instrument','')}\", fontsize=9)\n")
                source.insert(i+3, "            continue\n")
                source.insert(i+4, "        h = r['history']\n")
                break

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=2)
print("Patched 4_analysis.ipynb")
