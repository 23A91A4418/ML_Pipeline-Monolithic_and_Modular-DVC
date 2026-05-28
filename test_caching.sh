#!/bin/bash
dvc repro
sed -i 's/n_estimators: 100/n_estimators: 150/' params.yaml
dvc repro > repro_log.txt
