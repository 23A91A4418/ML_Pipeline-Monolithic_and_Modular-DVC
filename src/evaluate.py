import argparse
import numpy as np
import joblib
import json
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--data', required=True)
    parser.add_argument('--metrics', required=True)
    args = parser.parse_args()
    
    model = joblib.load(args.model)
    data = np.load(args.data)
    X_test = data['X_test']
    y_test = data['y_test']
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if len(np.unique(y_test)) > 1 else np.zeros(len(y_test))
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'auc': float(roc_auc_score(y_test, y_pred_proba)),
        'f1_macro': float(f1_score(y_test, y_pred, average='macro'))
    }
    
    os.makedirs(os.path.dirname(args.metrics), exist_ok=True)
    with open(args.metrics, 'w') as f:
        json.dump(metrics, f)

if __name__ == '__main__':
    main()
