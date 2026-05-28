import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import yaml
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)['prepare']
        
    df = pd.read_csv(args.input)
    
    le = LabelEncoder()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)
            df[col] = le.fit_transform(df[col])
            
    X = df.drop('income', axis=1)
    y = df['income']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=params['test_size'], random_state=params['random_state']
    )
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    np.savez_compressed(args.output, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)

if __name__ == '__main__':
    main()
