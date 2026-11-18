# Network Intrusion Detection Using Machine Learning

**Advanced Artificial Intelligence Final Project · Hunter Smith and John**

This project classifies network flows as **Benign** or **Suspicious** based on statistics such as flow duration and packet counts. The goal is to help security analysts prioritize flows for review while measuring the trade-off between missed intrusions and false alerts.

## Dataset

The notebook uses the [CIC-IDS2017 release on Kaggle](https://www.kaggle.com/datasets/dhoogla/cicids2017). The [Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html) documents the original dataset and its collection process. Each row represents a labeled network flow. The notebook maps the original benign label to `0` and all other traffic labels in this dataset to `1`. It retains the original labels for error analysis.

## Run in Google Colab

1. Download [Network_Intrusion_Detection_Colab.ipynb](Network_Intrusion_Detection_Colab.ipynb) from this repository and upload it to [Google Colab](https://colab.research.google.com/).
2. Connect to a CPU runtime and select **Runtime → Run all**. With `DATA_DIR = None`, the setup cell installs `kagglehub` and downloads the dataset.
3. If the automatic download fails, download and extract the Kaggle dataset manually. Place the extracted folder in the Colab runtime or mount Google Drive, then set `DATA_DIR` in Section 1 to the extracted folder path and rerun the notebook.
4. To keep your results, set `DOWNLOAD_OUTPUTS = True` in the optional cell at the end of Section 6 and run that cell to download `ids_outputs.zip`.

**Python dependencies:** `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `joblib`, `ipython`, and `pyarrow` for reading Parquet. The automatic Kaggle download also uses `kagglehub`.

The default configuration samples up to **20,000 rows per input file** and uses random seed **42**. Set `MAX_ROWS_PER_FILE = None` to process the full files if memory permits. Record the dataset release, sample cap, and package versions when reporting your results.

## Training and evaluation

The notebook audits missing values, infinite values, duplicates, and conflicting labels. It removes flow identifiers and capture metadata from the model inputs, then stratifies the cleaned data into **60% training, 20% validation, and 20% test** sets. Random Forest and linear SVM are compared against a majority-class baseline. The model pipelines fit imputation and constant-feature removal on the training split. The linear SVM pipeline also scales its inputs.

Validation F1 for the suspicious class determines the hyperparameters and which trained model is saved. The held-out test comparison reports confusion matrices, precision, recall, F1, average precision, false alerts per 1,000 benign flows, and missed intrusions. The notebook also breaks down missed detections by original traffic category.

## Prediction demo and outputs

Section 6 saves and reloads the trained pipeline, then predicts labels for an unlabeled sample of held-out flows. To try your own CSV, set `UPLOAD_CSV = True` in the optional cell and run it. Use `sample_flows.csv` as the template for the required numeric feature columns.

| Generated file | Contents |
| --- | --- |
| `network_ids.joblib` | Saved preprocessing pipeline, classifier, and expected feature columns |
| `test_metrics.csv` | Held-out comparison for all three models |
| `per_category_metrics.csv` | Selected model's missed detections and recall by traffic category |
| `tuning_results.csv` | Training and validation F1 for each parameter setting |
| `sample_flows.csv` | Unlabeled example inputs for the demo |
| `sample_predictions.csv` | Predictions for the example inputs |

Run the notebook from the first cell to reproduce the trained model and these files. The notebook collects them in `ids_outputs.zip`.

## Limitations and AI acknowledgment

The random split measures performance on held-out flows from the same benchmark. Related flows can still span splits, and per-file sampling can change the traffic mix. Testing on a separate capture would help assess how well the model transfers to another network. Use public benchmark inputs for the demo and avoid uploading private network data.

ChatGPT assisted with drafting and commenting the notebook and preparing this README.
