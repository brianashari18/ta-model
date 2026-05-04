# Ablation Study – Struktur Model & Feature Type

## Ringkasan

Notebook ablasi telah diperbarui untuk membandingkan:
- **5 Model Arsitektur**: RNN, GRU, LSTM, Bi-LSTM, Transformer
- **3 Jenis Ekstrasi Fitur**: MFCC, Chromagram, MFCC + Chroma
- **7 Skenario Instrumen**: Piano, Bass, Guitar, Vocals, Guitar+Piano, Guitar+Piano+Bass, No Vocals

## Struktur Notebook

### Notebook Baru (15 total)
```
ablation_<MODEL>_<FEATURE>.ipynb

Contoh:
- ablation_rnn_mfcc.ipynb
- ablation_lstm_chromagram.ipynb
- ablation_transformer_mfcc_chroma.ipynb
```

### Model & Feature Type Mapping
| Model | Key | Feature 1 | Feature 2 | Feature 3 |
|-------|-----|-----------|-----------|-----------|
| Vanilla RNN | `rnn` | MFCC | Chromagram | MFCC+Chroma |
| GRU | `gru` | MFCC | Chromagram | MFCC+Chroma |
| LSTM | `lstm` | MFCC | Chromagram | MFCC+Chroma |
| Bi-LSTM | `bilstm` | MFCC | Chromagram | MFCC+Chroma |
| Transformer | `transformer` | MFCC | Chromagram | MFCC+Chroma |

### Output Struktur
Setiap notebook menghasilkan:
```
ablation_outputs/
├── rnn_mfcc/
│   ├── best_piano.pt
│   ├── best_guitar.pt
│   ├── ...
│   └── summary_all_instruments.json
├── rnn_chromagram/
│   └── ...
├── lstm_mfcc/
├── lstm_chromagram/
├── lstm_mfcc_chroma/
└── ... (15 folder total)
```

## Cara Menggunakan

### 1. Menjalankan Single Notebook
Buka salah satu dari 15 notebook di Jupyter/Colab. Notebook akan:
1. Mount Google Drive (jika Colab)
2. Load file CSV feature extraction sesuai `FEATURE_TYPE`
3. Train model pada 7 instrumen
4. Simpan hasil ke `ablation_outputs/<model>_<feature>/`

**Catatan paths:**
- Notebook mengharapkan fitur CSV di: `/content/drive/My Drive/Kuliah/Tugas Akhir/Master Dataset/<instrument>/extracted_features_<feature_type>.csv`
- Output di: `/content/drive/My Drive/Kuliah/Tugas Akhir/ablation_outputs/<model>_<feature>/`

Sesuaikan `BASE_PATH` jika struktur folder berbeda.

### 2. Aggregation & Comparison
Setelah menjalankan semua 15 notebook (atau subset yang ingin dibandingkan), jalankan cell agregasi (Cell 10) untuk:

**Visualization 1: Model vs Feature Type** (agregasi semua instrumen)
- X-axis: Model (RNN, GRU, LSTM, Bi-LSTM, Transformer)
- Hue: Feature Type (MFCC, Chromagram, MFCC+Chroma)
- Y-axis: Rata-rata akurasi validasi

**Visualization 2: Feature Type per Instrumen** (fokus LSTM)
- X-axis: Instrumen
- Hue: Feature Type
- Y-axis: Akurasi validasi

Output tersimpan: `ablation_outputs/comparison_model_vs_feature.png` dan `comparison_feature_by_instrument_lstm.png`

## File Konfigurasi

### Elemen Kunci di Cell 1
```python
FEATURE_TYPE = 'mfcc'  # atau 'chromagram', 'mfcc_chroma'
FEATURE_FILENAME = f'extracted_features_{FEATURE_TYPE}.csv'
PKL_PATTERN = f'extracted_features_{FEATURE_TYPE}.pkl'
OUT_DIR = Path(...) / f'{MODEL_KEY}_{FEATURE_TYPE}'
```

### Summary JSON
Setiap notebook menghasilkan `summary_all_instruments.json`:
```json
[
  {
    "instrument": "piano",
    "model": "lstm",
    "feature_type": "mfcc",
    "best_val_acc": 0.8542,
    "checkpoint": "...best_piano.pt",
    "history": {...}
  },
  ...
]
```

## Data Requirements

### Input Files
Local folder structure (macOS/lokal):
```
/Users/brianashari18/Tugas Akhir/ta-model/
├── piano/
│   ├── extracted_features_mfcc.csv
│   ├── extracted_features_chromagram.csv
│   └── extracted_features_mfcc_chroma.csv
├── bass/
│   └── ...
└── ... (7 instrumen total)
```

Atau di Google Drive:
```
/content/drive/My Drive/Kuliah/Tugas Akhir/Master Dataset/
├── piano/
│   ├── extracted_features_mfcc.pkl + .csv
│   ├── extracted_features_chromagram.pkl + .csv
│   └── extracted_features_mfcc_chroma.pkl + .csv
└── ... (7 instrumen)
```

## Perubahan dari Versi Lama

### Sebelumnya
- 5 notebook (satu per model)
- Hardcoded feature: `CSV_FALLBACK = 'extracted_features_mfcc_chroma.csv'`
- Hanya bisa membandingkan model antar instrumen

### Sekarang
- **15 notebook** (5 model × 3 feature type)
- Feature type dapat dikonfigurasi per notebook
- **Automated comparison** model vs feature type
- Output terstruktur di folder per kombinasi
- Summary JSON include metadata feature type

## Tips & Tricks

### Quick Experiment
Jika hanya ingin test satu kombinasi:
1. Edit `_generate_ablation_notebooks.py` → line `feature_types = ['mfcc']`
2. Run: `python _generate_ablation_notebooks.py`
3. Jalankan `ablation_lstm_mfcc.ipynb`

### Batch Processing Lokal
Untuk machine dengan GPU lokal (bukan Colab):
1. Ubah `BASE_PATH` ke path lokal
2. Ubah output folder (remove `/content/drive/...`)
3. Jalankan notebook via `jupyter notebook` atau `jupyter lab`

### Comparing Only Subset
Cell agregasi otomatis hanya membaca folder yang ada:
- Jalankan hanya `ablation_lstm_*.ipynb` → agregasi hanya akan include LSTM
- Hasil accuracy akan agregasi dari 3 feature types

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError: extracted_features_mfcc.csv not found` | Pastikan CSV files ada di path. Sesuaikan `BASE_PATH` di Cell 1. |
| Memory error saat training | Kurangi `BATCH_SIZE` atau `MAX_LEN` di Cell 1. |
| Aggregation cells tidak menunjukkan grafik | Jalankan minimal 1 full notebook (7 instrumen) per kombinasi. |
| Module not found (torch, sklearn) | Install requirements: `pip install torch pytorch-cuda=11.8 scikit-learn pandas numpy matplotlib seaborn` |

## File Generator

Script `_generate_ablation_notebooks.py` dapat di-regenerate kapan saja:
```bash
python _generate_ablation_notebooks.py
```

Ini akan overwrite semua `ablation_*.ipynb` based on `MODEL_SPECS` dan `feature_types`.

## Next Steps

1. **Jalankan subset** notebook di Colab atau lokal (GPU recommended)
2. **Collect results** dari `ablation_outputs/`
3. **Run aggregation** cell untuk membandingkan model × feature type
4. **Analyze visualizations** untuk menentukan kombinasi terbaik

---

Last Updated: March 2026
