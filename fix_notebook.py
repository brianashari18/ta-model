import json

file_path = "/Users/brianashari18/Tugas Akhir/ta-model/4_analysis.ipynb"

with open(file_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = cell["source"]
        new_source = []
        for line in source:
            if "fig, axes = plt.subplots(1, n_exp, figsize=(5*n_exp, 4), squeeze=False)" in line:
                new_source.extend([
                    "    import math\n",
                    "    n_exp = len(full_results)\n",
                    "    n_cols = 2\n",
                    "    n_rows = math.ceil(n_exp / n_cols)\n",
                    "    fig, axes = plt.subplots(n_rows, n_cols, figsize=(10, 4*n_rows), squeeze=False)\n"
                ])
            elif "ax = axes[0][i]" in line:
                new_source.extend([
                    "        row = i // n_cols\n",
                    "        col = i % n_cols\n",
                    "        ax = axes[row][col]\n"
                ])
            else:
                new_source.append(line)
        cell["source"] = new_source

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Notebook updated successfully.")
