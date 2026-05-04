## 📊 Ablation Study – Feature Type Comparison
### Status: ✅ COMPLETE & READY

---

## 🎯 What's New

### 15 Notebooks Generated ✓
Every notebook follows the pattern: `ablation_<MODEL>_<FEATURE>.ipynb`

**5 Models × 3 Feature Types = 15 Combinations**

---

## ✅ Apa yang Telah Dilakukan

### 1. Generator Script Updated ✓
File: `_generate_ablation_notebooks.py`
- Sebelumnya: Generate 5 notebook (1 per model)
- Sekarang: Generate **15 notebook** (5 model × 3 feature type)

### 2. New Notebooks Created ✓
Total **15 notebook baru** dengan naming convention:
```
ablation_<MODEL>_<FEATURE>.ipynb
```

**Model Keys:**
- `rnn` → Vanilla RNN
- `gru` → GRU  
- `lstm` → LSTM
- `bilstm` → Bi-LSTM
- `transformer` → Transformer

**Feature Type:**
- `mfcc` → MFCC
- `chromagram` → Chromagram
- `mfcc_chroma` → MFCC + Chroma

### 3. Updated Features ✓

#### Cell 1 (Konfigurasi)
```python
FEATURE_TYPE = 'mfcc'  # Configurable per notebook
FEATURE_FILENAME = f'extracted_features_{FEATURE_TYPE}.csv'
OUT_DIR = ... / f'{MODEL_KEY}_{FEATURE_TYPE}'
```

#### Cell 7 (Results Tracking)
```python
res['feature_type'] = FEATURE_TYPE  # Added tracking
```

#### Cell 10 (Aggregation & Visualization)
- **Visualization 1**: Bar chart Model vs Feature Type
  - Model di X-axis, Feature Type sebagai hue
  - Agregasi semua instrumen
  - Output: `comparison_model_vs_feature.png`

- **Visualization 2**: Feature Type per Instrument (LSTM focus)
  - Instrumen di X-axis, Feature Type sebagai hue
  - Output: `comparison_feature_by_instrument_lstm.png`

### 4. Output Organization ✓
```
ablation_outputs/
├── rnn_mfcc/
│   ├── best_piano.pt
│   ├── ...
│   └── summary_all_instruments.json
├── rnn_chromagram/
│   └── ...
├── rnn_mfcc_chroma/
│   └── ...
├── gru_mfcc/
│   └── ...
... (15 folder total)
```

## Struktur Perbandingan

### Dimensi Perbandingan
```
Model (5) × Feature Type (3) × Instrument (7) × Metrics (val_acc, history)
= 5 × 3 × 7 = 105 training runs per full execution
```

### Comparison Hierarchy
1. **Primary**: Model vs Feature Type (Cell 10 - Chart 1)
   - Mana kombinasi model+feature terbaik?
   - Aggregate semua instrumen

2. **Secondary**: Feature Type Effectiveness (Cell 10 - Chart 2)
   - Untuk LSTM, feature mana yang terbaik per instrumen?
   - Determine feature-specific performance

3. **Tertiary**: Per-Instrument Analysis (dari summary JSON)
   - Manual analysis: buka `ablation_outputs/<model>_<feature>/summary_all_instruments.json`

## Cara Menggunakan

### Option A: Run All 15 Notebooks (Recommended for full comparison)
```bash
# Di Colab, buka semua 15 notebook:
- ablation_rnn_mfcc.ipynb
- ablation_rnn_chromagram.ipynb
- ... (15 total)

# Run setiap notebook (estimate 30 min - 2 hours per notebook with GPU)
```

### Option B: Run Subset untuk Quick Comparison
**Contoh: Bandingkan hanya LSTM ke 3 feature types**
```bash
# Run hanya ketiga:
- ablation_lstm_mfcc.ipynb
- ablation_lstm_chromagram.ipynb
- ablation_lstm_mfcc_chroma.ipynb

# Cell 10 akan generate comparison otomatis
```

### Option C: Run Lokal (jika punya GPU)
```bash
# Sesuaikan paths di Cell 1:
BASE_PATH = Path('/path/to/master/dataset')
OUT_DIR = Path('/path/to/ablation_outputs')

# Jalankan via Jupyter
jupyter notebook ablation_lstm_mfcc.ipynb
```

## Key Improvements

| Aspek | Before | After |
|-------|--------|-------|
| **Notebooks** | 5 | **15** |
| **Feature Comparison** | Manual (1 hardcoded) | Automated (3 types) |
| **Dimensions** | Model × Instrument | **Model × Feature × Instrument** |
| **Visualization** | Single bar chart | **2 comparison charts** |
| **Scalability** | Hard to extend | Easy to add features/models |
| **Tracking** | No feature type info | Full metadata in JSON |

## File Locations

### Generated Notebooks (in workspace root)
```
/Users/brianashari18/Tugas Akhir/ta-model/
├── ablation_rnn_mfcc.ipynb ✓
├── ablation_rnn_chromagram.ipynb ✓
├── ablation_rnn_mfcc_chroma.ipynb ✓
├── ablation_gru_mfcc.ipynb ✓
├── ablation_gru_chromagram.ipynb ✓
├── ... (15 total)
└── ablation_transformer_mfcc_chroma.ipynb ✓
```

### Documentation
```
/Users/brianashari18/Tugas Akhir/ta-model/
├── README_ABLATION_STRUCTURE.md (Detailed guide)
├── ABLATION_QUICKSTART.md (This file)
└── _generate_ablation_notebooks.py (Generator script)
```

### Generator Script
```
/Users/brianashari18/Tugas Akhir/ta-model/_generate_ablation_notebooks.py
```
Run to regenerate any notebook if needed:
```bash
python _generate_ablation_notebooks.py
```

## Expected Results

After running all 15 notebooks, you'll have:

### Directory Structure
```
ablation_outputs/
├── rnn_mfcc/summary_all_instruments.json
├── rnn_chromagram/summary_all_instruments.json
├── rnn_mfcc_chroma/summary_all_instruments.json
├── ... (15 summary files)
├── comparison_model_vs_feature.png
└── comparison_feature_by_instrument_lstm.png
```

### Analysis Points
1. **Best Model-Feature Combo**: Which (model, feature) pair gives highest accuracy?
2. **Feature Robustness**: Does one feature type perform consistently across models?
3. **Model Sensitivity**: Which models are most sensitive to feature type changes?
4. **Instrument-Feature Interaction**: Do certain features work better for specific instruments?

## Next Steps

1. ✅ **Generator Updated** – 15 notebooks created
2. ⏳ **Run notebooks** – Execute on Colab/local GPU
3. ⏳ **Analyze results** – Compare `summary_*.json` files
4. ⏳ **Generate comparison charts** – Run Cell 10 in any notebook
5. ⏳ **Write findings** – Document feature-model interactions

## Troubleshooting

**Q: Can I regenerate specific notebooks only?**
A: Edit `_generate_ablation_notebooks.py`:
- Line ~870: Modify `feature_types` or `MODEL_SPECS`
- Run: `python _generate_ablation_notebooks.py`

**Q: How do I update BASE_PATH for Colab?**
A: Each notebook Cell 1 has `BASE_PATH` variable. Update if your Drive structure differs.

**Q: Can I run notebooks in parallel?**
A: Yes, on different GPU machines. Results will aggregate automatically if saved to same `ablation_outputs/`.

**Q: How long does one notebook take?**
A: ~30 minutes to 2 hours per notebook (depends on GPU, datasize, epochs).

---

**Status**: ✅ Complete – Ready for experimentation phase
**Created**: March 2026
