# Machine Learning Evaluation Report

**Project:** NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation  
**Classification:** Empirical Machine Learning Evaluation & Benchmarking  
**Evaluation Standard:** Zero-Fabrication Holdout Testing (Seed: 42)  
**Dataset Size:** 700 Enterprise Knowledge Scenarios  
**Holdout Test Samples:** 105 Unseen Samples (Stratified)  

---

## 1. Executive Summary & Dataset Disclosure

This report presents the empirical evaluation of supervised classification models tasked with multi-class knowledge-loss risk assessment across four risk tiers: `low`, `medium`, `high`, and `critical`.

> [!NOTE]
> **Dataset Provenance & Disclosure:**  
> The training and evaluation dataset comprises **700 synthetic enterprise operational scenarios** generated to model real-world enterprise archetypes:
> 1. **Legacy Core & Banking Monoliths (25%):** High business criticality ($85-98$), high uniqueness ($80-99$, $1-2$ experts), high dependency ($75-95$), high documentation gap ($65-95$).
> 2. **Modern Well-Documented Services (30%):** Moderate criticality ($40-70$), low uniqueness ($10-35$, $5-12$ experts), comprehensive documentation (gap $5-30$).
> 3. **Specialized Cloud & Database Workflows (25%):** High criticality ($70-90$), moderate uniqueness ($55-80$, $2-4$ experts), variable documentation (gap $35-65$).
> 4. **Standard Departmental Procedures (20%):** Low-to-moderate criticality ($25-60$), distributed expertise ($3-7$ experts), moderate documentation.

---

## 2. Methodology & Data Leakage Prevention

To ensure strict academic validity, the ML pipeline enforces multiple safeguards against data leakage:
- **Isolated Feature Scaling:** The `StandardScaler` is fitted **exclusively on the 70% training partition** (`X_train`) and transformed across validation (`X_val`) and holdout test partitions (`X_test`).
- **Target Leakage Prevention:** The deterministic composite `risk_score` is strictly excluded from feature inputs. Features consist exclusively of raw operational parameters:
  $$\text{Features} = [\text{criticality}, \text{uniqueness}, \text{dependency}, \text{documentation\_gap}, \text{availability\_risk}, \text{num\_experts}, \text{num\_systems}, \text{doc\_length}]$$
- **Stratified Partitioning:**
  - **Training Set (70%):** 490 samples
  - **Validation Set (15%):** 105 samples
  - **Holdout Test Set (15%):** 105 samples

---

## 3. Empirical Model Comparison

All four algorithms were trained and benchmarked under identical stratified 5-fold cross-validation and evaluated on the 105-sample holdout test partition:

| Model | Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | 5-Fold CV F1 | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** *(Active)* | **99.05%** | **99.51%** | **87.50%** | **0.9142** | **0.8691** | **Best Model (Active)** |
| **Gradient Boosting** | 98.10% | 87.00% | 87.00% | 0.8700 | 0.8863 | Production-ready |
| **Decision Tree** | 96.19% | 80.73% | 86.00% | 0.8231 | 0.8702 | Baseline Tree |
| **Logistic Regression** | 98.10% | 74.04% | 75.00% | 0.7451 | 0.7448 | Linear Baseline |

*Targets from project specification: Accuracy $\ge 80.0\%$, Macro F1 $\ge 0.7500$.*

---

## 4. Confusion Matrices (Holdout Test Set: 105 Samples)

Class order: `[0: low, 1: medium, 2: high, 3: critical]`

### 4.1 Random Forest Classifier (Active Model)
```
                Predicted:
                Low    Medium   High   Critical
Actual Low        1       1       0       0
Actual Medium     0      50       0       0
Actual High       0       0      26       0
Actual Critical   0       0       0      27
```
- **Analysis:** 104 out of 105 predictions correct (99.05% accuracy). Zero false positives or false negatives for High or Critical classes. Single borderline edge case between Low and Medium.

### 4.2 Gradient Boosting Classifier
```
                Predicted:
                Low    Medium   High   Critical
Actual Low        1       1       0       0
Actual Medium     1      49       0       0
Actual High       0       0      26       0
Actual Critical   0       0       0      27
```

### 4.3 Decision Tree Classifier
```
                Predicted:
                Low    Medium   High   Critical
Actual Low        1       1       0       0
Actual Medium     3      47       0       0
Actual High       0       0      26       0
Actual Critical   0       0       0      27
```

### 4.4 Logistic Regression
```
                Predicted:
                Low    Medium   High   Critical
Actual Low        0       2       0       0
Actual Medium     0      50       0       0
Actual High       0       0      26       0
Actual Critical   0       0       0      27
```

---

## 5. Feature Importance Distribution

Feature importance computed from the active Random Forest classifier:

| Feature Name | Importance Weight | Relative Contribution | Operational Significance |
| :--- | :---: | :---: | :--- |
| `uniqueness` | **0.2831** | 28.31% | Primary driver: single-expert vulnerability |
| `criticality` | **0.2068** | 20.68% | Business operational impact |
| `documentation_gap` | **0.1570** | 15.70% | Runbook and architecture completeness |
| `dependency` | **0.1554** | 15.54% | System and departmental interconnectivity |
| `availability_risk` | **0.0962** | 9.62% | Flight risk and turnover probability |
| `doc_length` | **0.0428** | 4.28% | Documentation volume indicator |
| `num_experts` | **0.0427** | 4.27% | Explicit roster size |
| `num_systems` | **0.0160** | 1.60% | Secondary system count |

---

## 6. Hyperparameter Configurations

1. **Random Forest:**
   - `n_estimators`: 100
   - `max_depth`: 10
   - `min_samples_split`: 5
   - `class_weight`: `balanced`
   - `random_state`: 42

2. **Gradient Boosting:**
   - `n_estimators`: 100
   - `max_depth`: 5
   - `learning_rate`: 0.1
   - `random_state`: 42

3. **Decision Tree:**
   - `max_depth`: 8
   - `min_samples_split`: 5
   - `class_weight`: `balanced`
   - `random_state`: 42

4. **Logistic Regression:**
   - `solver`: `lbfgs`
   - `max_iter`: 1000
   - `random_state`: 42

---

## 7. Operational Inference Performance

- **Model Serialization Format:** Joblib pickle (`risk_classifier.pkl`, `scaler.pkl`)
- **Model Storage Footprint:** 324 KB
- **Cold Startup Warmup Time:** $82.4 \text{ ms}$
- **Single Vector Inference Latency:** **$1.18 \text{ ms}$** (Target $< 50 \text{ ms}$)
