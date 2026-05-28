import argparse
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import yaml
import joblib
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)['train']
        
    data = np.load(args.input)
    X_train = data['X_train']
    y_train = data['y_train']
    
    if params['model_type'] == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=params['n_estimators'], 
            max_depth=params['max_depth'], 
            random_state=params['random_state']
        )
    else:
        raise ValueError(f"Unsupported model type {params['model_type']}")
        
    model.fit(X_train, y_train)
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    joblib.dump(model, args.output)

if __name__ == '__main__':
    main()
