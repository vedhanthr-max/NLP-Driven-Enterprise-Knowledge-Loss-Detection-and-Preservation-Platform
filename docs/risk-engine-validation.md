# Risk Engine Mathematical Validation & Boundary Analysis

**Project:** NLP-Driven SaaS Platform for Enterprise Knowledge Loss Detection and Preservation  
**Classification:** Algorithmic & Mathematical Specification Verification  
**Evaluation Standard:** Zero-Fabrication Empirical Validation  

---

## 1. Mathematical Formulation

The risk calculation engine implements the exact 5-factor weighted linear composite model specified in `project-docs/ENHANCED_PROJECT_DOCUMENTATION.md` Section 17.

### 1.1 Core Formula
$$\text{Risk Score} = (C \times W_C) + (U \times W_U) + (D \times W_D) + (G \times W_G) + (A \times W_A)$$

### 1.2 Parameters, Weights, and Clamping Constraints

| Factor Symbol | Factor Description | Weight ($W$) | Source Code Constant | Input Range | Clamping Rule |
| :---: | :--- | :---: | :--- | :---: | :--- |
| $C$ | **Knowledge Criticality** | **0.30** (30%) | `settings.WEIGHT_CRITICALITY` | $0.0 - 100.0$ | $\max(0.0, \min(100.0, C))$ |
| $U$ | **Knowledge Uniqueness** | **0.25** (25%) | `settings.WEIGHT_UNIQUENESS` | $0.0 - 100.0$ | $\max(0.0, \min(100.0, U))$ |
| $D$ | **Organizational Dependency** | **0.20** (20%) | `settings.WEIGHT_DEPENDENCY` | $0.0 - 100.0$ | $\max(0.0, \min(100.0, D))$ |
| $G$ | **Documentation Gap** | **0.15** (15%) | `settings.WEIGHT_DOCUMENTATION_GAP` | $0.0 - 100.0$ | $\max(0.0, \min(100.0, G))$ |
| $A$ | **Expert Availability Risk** | **0.10** (10%) | `settings.WEIGHT_AVAILABILITY_RISK` | $0.0 - 100.0$ | $\max(0.0, \min(100.0, A))$ |
| $\Sigma$ | **Total Weight** | **1.00** (100%) | — | — | Sum of weights $\equiv 1.00$ |

---

## 2. Classification Thresholds

The resulting composite score (rounded to 2 decimal places) is categorized into four discrete operational risk tiers:

| Tier Name | Score Range | Documented Range | Implemented Rule | Automated Action Triggered |
| :--- | :---: | :---: | :--- | :--- |
| **LOW** | $0.00 - 30.00$ | $0 - 30$ | $\text{score} \le 30.0$ | Routine quarterly review |
| **MEDIUM** | $30.01 - 60.00$ | $31 - 60$ | $30.0 < \text{score} \le 60.0$ | Periodic cross-training |
| **HIGH** | $60.01 - 80.00$ | $61 - 80$ | $60.0 < \text{score} \le 80.0$ | Automated preservation action generated |
| **CRITICAL** | $80.01 - 100.00$ | $81 - 100$ | $\text{score} > 80.0$ | Immediate succession & transfer action generated |

---

## 3. Empirical Boundary Condition Testing

All boundary and threshold conditions were tested directly against the Python implementation (`app.risk.scoring:calculate_risk_score` and `classify_risk_level`):

| Test Vector ID | Inputs $(C, U, D, G, A)$ | Theoretical Score | Computed Score | Categorized Level | Expected Level | Match Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **B-01 (Zero Anchor)** | $(0, 0, 0, 0, 0)$ | 0.00 | **0.00** | `low` | `low` | **EXACT MATCH** |
| **B-02 (Low Ceiling)** | $(30, 30, 30, 30, 30)$ | 30.00 | **30.00** | `low` | `low` | **EXACT MATCH** |
| **B-03 (Medium Floor)** | $(31, 31, 31, 31, 31)$ | 31.00 | **31.00** | `medium` | `medium` | **EXACT MATCH** |
| **B-04 (Medium Ceiling)**| $(60, 60, 60, 60, 60)$ | 60.00 | **60.00** | `medium` | `medium` | **EXACT MATCH** |
| **B-05 (High Floor)** | $(61, 61, 61, 61, 61)$ | 61.00 | **61.00** | `high` | `high` | **EXACT MATCH** |
| **B-06 (High Ceiling)** | $(80, 80, 80, 80, 80)$ | 80.00 | **80.00** | `high` | `high` | **EXACT MATCH** |
| **B-07 (Critical Floor)**| $(81, 81, 81, 81, 81)$ | 81.00 | **81.00** | `critical` | `critical` | **EXACT MATCH** |
| **B-08 (Max Ceiling)** | $(100, 100, 100, 100, 100)$| 100.00 | **100.00** | `critical` | `critical` | **EXACT MATCH** |

---

## 4. Benchmark Scenario Verification

Testing against documented enterprise operational test vectors:

### Vector 1: Legacy Core Banking Settlement System
- **Inputs:** Criticality: 95.0, Uniqueness: 90.0, Dependency: 85.0, Doc Gap: 80.0, Availability Risk: 75.0
- **Calculation:** $(95 \times 0.30) + (90 \times 0.25) + (85 \times 0.20) + (80 \times 0.15) + (75 \times 0.10) = 28.50 + 22.50 + 17.00 + 12.00 + 7.50 = 87.50$
- **Result:** **87.50 (`critical`)** — Passed.

### Vector 2: Cloud Migration Runbook
- **Inputs:** Criticality: 70.0, Uniqueness: 60.0, Dependency: 75.0, Doc Gap: 65.0, Availability Risk: 50.0
- **Calculation:** $(70 \times 0.30) + (60 \times 0.25) + (75 \times 0.20) + (65 \times 0.15) + (50 \times 0.10) = 21.00 + 15.00 + 15.00 + 9.75 + 5.00 = 65.75$
- **Result:** **65.75 (`high`)** — Passed.

### Vector 3: Standard Onboarding Procedures
- **Inputs:** Criticality: 20.0, Uniqueness: 10.0, Dependency: 20.0, Doc Gap: 30.0, Availability Risk: 20.0
- **Calculation:** $(20 \times 0.30) + (10 \times 0.25) + (20 \times 0.20) + (30 \times 0.15) + (20 \times 0.10) = 6.00 + 2.50 + 4.00 + 4.50 + 2.00 = 19.00$
- **Result:** **19.00 (`low`)** — Passed.

---

## 5. Discrepancy & Alignment Audit

- **Formula Alignment:** 100% identical between `ENHANCED_PROJECT_DOCUMENTATION.md` and `app/risk/scoring.py`.
- **Weight Consistency:** $0.30 + 0.25 + 0.20 + 0.15 + 0.10 = 1.00$.
- **Boundary Semantics:** Implemented logic preserves strict discrete transitions across the Low/Medium/High/Critical boundaries with no overlapping states.
