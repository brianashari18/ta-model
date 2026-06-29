import json

notebook_path = '3_modeling.ipynb'
with open(notebook_path, 'r') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "def run_experiment(data_key, model_key):" in source:
            new_source = """def run_experiment(data_key, model_key):
    from sklearn.model_selection import KFold
    import numpy as np
    import collections
    
    entry = master_data[data_key]
    seqs = list(entry['sequences'])
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    fold_metrics = collections.defaultdict(list)
    n_feat = len(entry['feature_columns'])
    
    # Store history for each fold to compute average later
    all_folds_history = []
    
    for fold, (train_idx, val_idx) in enumerate(kf.split(seqs)):
        torch.manual_seed(RANDOM_SEED + fold)
        np.random.seed(RANDOM_SEED + fold)
        
        print(f'    --- Fold {fold+1}/5 ---')

        train_seqs = [seqs[i] for i in train_idx]
        val_seqs = [seqs[i] for i in val_idx]
        
        train_loader = DataLoader(ChordSeqDataset(train_seqs), batch_size=BATCH_SIZE,
                                  shuffle=True, collate_fn=collate_pad)
        val_loader = DataLoader(ChordSeqDataset(val_seqs), batch_size=BATCH_SIZE,
                                shuffle=False, collate_fn=collate_pad)
        
        model = build_model(model_key, n_feat, N_CLASSES)
        optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
        criterion = FocalLoss(gamma=2.0, ignore_index=-100)
        
        best_val_acc = -1.0
        fold_hist = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
        
        for ep in range(1, EPOCHS + 1):
            tl, ta = train_one_epoch(model, train_loader, optimizer, criterion)
            vl, va = evaluate(model, val_loader, criterion)
            
            fold_hist['train_loss'].append(tl)
            fold_hist['train_acc'].append(ta)
            fold_hist['val_loss'].append(vl)
            fold_hist['val_acc'].append(va)
            
            if va > best_val_acc:
                best_val_acc = va
            if ep % 10 == 0:
                print(f'        Ep {ep:3d}/{EPOCHS} │ TrL={tl:.4f} VaL={vl:.4f} VaA={va:.4f}')
        
        all_folds_history.append(fold_hist)
        mir_metrics = compute_mir_eval_metrics(model, val_seqs, CLASS_NAMES)
        fold_metrics['best_val_acc'].append(best_val_acc)
        for k, v in mir_metrics.items():
            fold_metrics[k].append(v)
            
    result = {'n_train': len(train_idx), 'n_val': len(val_idx), 'n_features': n_feat}
    print(f'    ── 5-Fold CV Results ──')
    for k, v in fold_metrics.items():
        mean_v = np.mean(v)
        std_v = np.std(v)
        result[k] = mean_v
        result[k + '_std'] = std_v
        print(f'    {k:15s} = {mean_v:.4f} ± {std_v:.4f}')
    
    # Compute average history across folds
    avg_hist = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    for ep in range(EPOCHS):
        avg_hist['train_loss'].append(float(np.mean([f['train_loss'][ep] for f in all_folds_history])))
        avg_hist['train_acc'].append(float(np.mean([f['train_acc'][ep] for f in all_folds_history])))
        avg_hist['val_loss'].append(float(np.mean([f['val_loss'][ep] for f in all_folds_history])))
        avg_hist['val_acc'].append(float(np.mean([f['val_acc'][ep] for f in all_folds_history])))
    
    result['history'] = avg_hist
    return result
"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')][:-1]

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=2)
print("Patched 3_modeling.ipynb to record and average history")
