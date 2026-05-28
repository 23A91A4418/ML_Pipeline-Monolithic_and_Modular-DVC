import argparse
import pandas as pd
import numpy as np
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    df = pd.read_csv(args.input)
    df.replace(' ?', np.nan, inplace=True)
    df.dropna(inplace=True)
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False)

if __name__ == '__main__':
    main()
