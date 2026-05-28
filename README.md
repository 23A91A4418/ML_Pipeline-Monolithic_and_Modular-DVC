# Reproducible Machine Learning Pipelines: Monolithic Script vs. Modular DVC Pipeline

This project builds and benchmarks two machine learning workflows using the UCI Adult Income dataset to demonstrate the core principles of MLOps, specifically caching, reproducibility, data versioning, and experiment tracking.

## Architecture Overview

### 1. Monolithic Workflow (`train_monolithic.py`)
A single, sequential script that performs data loading, cleaning, feature encoding, data splitting, training a Random Forest model, evaluation, and saving model/metric artifacts. 

```
[Start] -> Load data/adult.csv -> Clean Data -> Encode Features -> Split Data -> Train Model -> Evaluate -> Save Artifacts -> [End]
```

*   **Pros:** Fast initial setup.
*   **Cons:** No caching (every execution re-runs the entire flow), poor reproducibility, lack of data versioning tracking.

### 2. Modular DVC Pipeline (`dvc.yaml` & `src/`)
A modular pipeline orchestrated by Data Version Control (DVC), defining a Directed Acyclic Graph (DAG) split into four separate stages:

1.  **Prepare (`src/prepare.py`):** Loads raw `adult.csv` and outputs clean `data/processed.csv`.
2.  **Featurize (`src/featurize.py`):** Handles label encoding and splits the dataset, saving compressed features to `data/features.npz`.
3.  **Train (`src/train.py`):** Reads features and `params.yaml` training configurations to output `models/model.joblib`.
4.  **Evaluate (`src/evaluate.py`):** Computes metrics (`accuracy`, `auc`, `f1_macro`) and saves them to `metrics/scores.json`.

```
[data/adult.csv] ---> (prepare) ---> [data/processed.csv] ---> (featurize) ---> [data/features.npz]
                                                                                      |
                                                                                      v
                                                        (train) <--- [params.yaml] ---+
                                                           |                          |
                                                           v                          v
                                                 [models/model.joblib] ------> (evaluate) ---> [metrics/scores.json]
```

*   **Pros:** Caches outputs of each stage. Modifying hyperparameters under the `train` section in `params.yaml` will skip `prepare` and `featurize`, only re-running `train` and `evaluate` stages. Supports robust data/model versioning and experiments.
*   **Cons:** Overhead of writing stage scripts and configuration files.

---

## Getting Started

### Prerequisites
- Docker and Docker Compose installed.

### Setup and Build Environment

Build the reproducible Docker container environment:
```bash
docker-compose up --build -d
```
This spins up a container named `app` in the background with all dependencies installed.

---

## How to Run the Workflows

### 1. Monolithic Script Execution
To execute the monolithic workflow, run:
```bash
docker-compose run --rm app python train_monolithic.py
```
This will produce:
- `model.joblib` (serialized Random Forest classifier)
- `metrics.json` (model performance metrics)

### 2. Modular DVC Pipeline Execution
To execute the modular DVC pipeline, run:
```bash
docker-compose run --rm app dvc repro
```
This will run the pipeline end-to-end and produce:
- `models/model.joblib`
- `metrics/scores.json`

---

## Verifying MLOps Features

### Caching Test
Run the caching validation script to verify that DVC only executes modified stages:
```bash
docker-compose run --rm app bash test_caching.sh
```
Check `repro_log.txt` afterward to confirm that the `prepare` and `featurize` stages were skipped, and only `train` and `evaluate` were executed.

### Experiment Tracking
Launch a new experiment by overriding the training parameters:
```bash
docker-compose run --rm app dvc exp run --set-param train.n_estimators=150
```
Display a comparison table of all experiments:
```bash
docker-compose run --rm app dvc exp show
```
View the experiment log in JSON format:
```bash
docker-compose run --rm app dvc exp show --json
```