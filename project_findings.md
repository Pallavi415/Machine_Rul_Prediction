# NASA C-MAPSS FD001 — Project Findings

**Author:** Pallavi Dahiya

---

## Project Goal

I built this project to predict the **Remaining Useful Life (RUL)** of turbofan engines using the NASA C-MAPSS FD001 dataset.

The main objective was not just to train a model, but to understand the data, identify useful patterns, test different modeling approaches, compare them fairly, and select the model that generalizes best to unseen engines.

---

## 1. Data Understanding

The dataset contains:

- Engine/unit ID
- Operating cycle
- 3 operational settings
- 21 sensor measurements
- Remaining Useful Life (RUL) as the prediction target

Each engine is observed over multiple operating cycles until failure.

The basic relationship we are trying to learn is:

**More operating cycles → Engine degradation → Less Remaining Useful Life**

This made the operating cycle an important feature throughout the project.

---

## 2. RUL Target Creation

For the training data, I created RUL using the maximum operating cycle of each engine.

**Formula:**

`RUL = Maximum cycle of the engine - Current cycle`

For example, if an engine fails at cycle 200:

- Current cycle = 50
- Maximum cycle = 200
- RUL = 200 - 50 = **150 cycles**

As the engine gets closer to failure, its RUL decreases.

---

## 3. Data Preprocessing

During preprocessing, I:

- Identified the structure of the dataset.
- Created the RUL target.
- Checked sensor behavior.
- Identified constant features.
- Removed constant features because they contain no useful variation.
- Created an engine-level training/validation split.

The validation split was done at the **engine level**, rather than randomly splitting individual rows.

This was important because multiple rows belong to the same engine. Randomly splitting rows could allow information from the same engine to appear in both training and validation data.

---

## 4. Important Data Findings

One of the most important findings from the analysis was the strong relationship between **operating cycle and RUL**.

The model coefficient analysis showed that `cycle` had the strongest contribution among the features:

| Feature | Coefficient |
|---|---:|
| cycle | -26.73 |
| sensor_11 | 6.56 |
| sensor_4 | 3.88 |
| sensor_7 | 3.84 |
| ... | ... |

The negative coefficient for `cycle` is consistent with the physical meaning of the problem:

**More operating cycles → Less remaining useful life**

Several sensor measurements also contributed useful information about the engine's degradation state.

The data therefore contained a strong overall degradation pattern rather than completely random relationships.

---

## 5. Why I Started With Linear Regression

I started with Linear Regression intentionally.

I did not choose it simply because it is the simplest model, and I did not assume that it would automatically be the best model.

I chose it as a baseline because the **data itself showed characteristics that made a linear approach reasonable**:

- RUL decreases as operating cycles increase.
- `cycle` showed a strong relationship with RUL.
- Several sensor measurements had meaningful relationships with RUL.
- The overall degradation pattern in FD001 was relatively smooth.
- RUL is a continuous target, so regression is appropriate.

The reasoning was:

**Data shows a strong overall degradation trend**  
↓  
**Linear Regression is a reasonable starting point**  
↓  
**Use it as a baseline**  
↓  
**Test whether more complex models can improve it**

This was a **data-driven starting point**, not a final assumption.

---

# Model Experiments

## 6. Linear Regression — Baseline

I started with Linear Regression because I wanted a simple and interpretable baseline before trying more complex models.

### Validation Result

| Metric | Result |
|---|---:|
| MAE | **25.16 cycles** |
| RMSE | **31.66 cycles** |
| R² | **0.768** |

I used this model as the benchmark for all later experiments.

---

## 7. Feature Selection

I tested whether using only the strongest features would improve the model.

### Finding

The reduced feature set performed slightly worse than the baseline.

### Decision

I kept the broader useful feature set.

### Lesson

A feature does not always need to be individually dominant to contribute useful information when combined with other features.

---

## 8. Ridge Regression

I tested Ridge Regression to determine whether regularization could improve the Linear Regression model.

### Finding

The performance was essentially the same as the baseline.

### Decision

Ridge did not provide a meaningful improvement, so standard Linear Regression remained the benchmark.

---

## 9. Lasso Regression

I also tested Lasso Regression.

### Validation Result

- MAE: **25.15 cycles**
- RMSE: **31.66 cycles**
- R²: **0.767**

The MAE changed only slightly, while R² became slightly lower.

### Decision

I did not consider this a meaningful improvement.

---

## 10. RUL Capping Experiment

I tested whether limiting the maximum RUL to 125 cycles would make the prediction problem easier.

The original training data had a maximum RUL of **361 cycles**.

I created a capped target where:

**RUL > 125 → 125**

### Result

- MAE: **31.39 cycles**
- RMSE: **43.43 cycles**
- R²: **0.562**

The model became significantly worse.

### Decision

I rejected RUL capping.

### What I Learned

The higher RUL values contained useful information for the model. Removing that information damaged the overall relationship between the features and the target.

---

# Tree-Based Experiments

## 11. Random Forest

After testing linear models, I wanted to determine whether a nonlinear model could capture relationships that Linear Regression might miss.

I tested Random Forest because it combines many decision trees and can learn nonlinear relationships.

### Initial Result

- MAE: **28.00 cycles**
- RMSE: **39.46 cycles**
- R²: **0.698**

Random Forest performed worse than Linear Regression.

---

## 12. Random Forest Tuning

I did not reject Random Forest immediately.

I tested a few reasonable configurations to determine whether the model could improve with different parameters.

The best configuration tested was:

- `n_estimators = 300`
- `min_samples_leaf = 2`

### Best Result

- MAE: **27.87 cycles**
- RMSE: **39.34 cycles**
- R²: **0.700**

The tuning produced a small improvement.

However, it still remained behind Linear Regression.

### Decision

I stopped further Random Forest tuning because the improvement was too small to justify continuing.

---

## 13. Gradient Boosting

I then tested Gradient Boosting as another nonlinear tree-based approach.

Gradient Boosting builds trees sequentially, where later trees try to correct errors made by earlier trees.

### Result

- MAE: **27.76 cycles**
- RMSE: **38.91 cycles**
- R²: **0.707**

Gradient Boosting performed slightly better than Random Forest.

However, it still did not outperform Linear Regression.

---

# Model Comparison

| Model | MAE ↓ | RMSE ↓ | R² ↑ |
|---|---:|---:|---:|
| **Linear Regression** | **25.16** | **31.66** | **0.768** |
| Random Forest | 27.87 | 39.34 | 0.700 |
| Gradient Boosting | 27.76 | 38.91 | 0.707 |

---

## 14. Why Linear Regression Was Selected

Linear Regression was selected for **two reasons: the structure of the data and the validation results**.

### Data-Based Reason

The FD001 dataset showed a strong and relatively smooth degradation pattern.

The operating cycle had a strong relationship with RUL, and several sensor measurements also contained useful information about engine degradation.

This made a linear model a reasonable representation of the overall relationship.

The data suggested that we did not necessarily need a highly complex model to capture the main degradation trend.

### Experimental Reason

The validation experiments then confirmed that this assumption worked well.

The more complex tree-based models did not improve the validation performance.

Therefore:

**Data structure**  
↓  
**Linear model is reasonable**  
↓  
**Validation confirms the choice**  
↓  
**Linear Regression selected**

This is more meaningful than simply saying:

> "Linear Regression had the best score."

The model was first supported by the **patterns observed in the data**, and then its performance was verified through controlled experiments.

---

## 15. Why the Tree-Based Models Did Not Win

Random Forest and Gradient Boosting can learn nonlinear relationships, so I tested them to determine whether the sensor-to-RUL relationship required a more complex model.

However, both models performed worse than Linear Regression on the same validation engines.

One possible explanation is that the main degradation relationship in this FD001 setup is relatively smooth and strongly connected with operating cycle.

A tree model learns the data through rules and splits such as:

- Is `cycle` greater than a threshold?
- Is a sensor value greater than a threshold?
- Which side of the split gives lower prediction error?

This creates piecewise predictions.

For this dataset, the simpler linear relationship was better able to represent the overall degradation trend.

Therefore, increasing model complexity did not result in better validation performance.

---

## 16. Main Modeling Insight

One of the most important findings from this project was:

> **More complex models do not automatically produce better predictions.**

Random Forest and Gradient Boosting are more complex than Linear Regression, but they performed worse on our validation data.

This suggests that the main degradation relationship in this FD001 setup can be captured effectively by a simpler linear model.

The result also shows why model selection should be based on both:

- Understanding the data
- Evaluating the model objectively

---

# Final Model Evaluation

## 17. Training the Final Model

After completing model selection, I retrained the selected Linear Regression model using **all available training engines**.

The validation set was no longer needed for model selection because the final model had already been chosen.

The workflow became:

**All training engines**  
↓  
**Train selected Linear Regression**  
↓  
**Completely unseen test engines**

This allowed the final model to use all available training information.

---

## 18. Final Test Evaluation

I evaluated the final Linear Regression model on the completely unseen FD001 test engines.

The provided:

- `test_FD001.txt`
- `RUL_FD001.txt`

were used for the final evaluation.

The test data was kept separate from model selection to avoid test-data leakage.

The final test metrics are recorded in:

`notebooks/07_final_model_evaluation.ipynb`

The final test evaluation is the most important measure of how well the selected model generalizes to unseen engines.

---

# Final Project Workflow

```text
Problem Understanding
        ↓
Data Understanding
        ↓
EDA
        ↓
RUL Target Creation
        ↓
Data Preprocessing
        ↓
Identify Data Relationships
        ↓
Linear Regression Baseline
        ↓
Feature Selection
        ↓
Ridge / Lasso
        ↓
RUL Capping
        ↓
Random Forest
        ↓
Random Forest Tuning
        ↓
Gradient Boosting
        ↓
Model Comparison
        ↓
Linear Regression Selected
        ↓
Retrain Using All Training Data
        ↓
Evaluate on Unseen Test Engines

# Key Takeaways

1. **Operating cycle has a strong relationship with RUL.**
2. **Several sensor measurements provide useful information about engine degradation.**
3. **Constant features do not provide useful predictive information and were removed.**
4. **Engine-level validation was important because multiple observations belong to the same engine.**
5. **The data showed a relatively smooth degradation pattern, making Linear Regression a reasonable starting approach.**
6. **Linear Regression provided a strong and interpretable baseline.**
7. **Feature selection did not improve the baseline.**
8. **Ridge and Lasso did not provide meaningful improvements.**
9. **RUL capping significantly reduced performance.**
10. **Random Forest performed worse than Linear Regression.**
11. **Random Forest tuning produced only a small improvement.**
12. **Gradient Boosting performed slightly better than Random Forest but still worse than Linear Regression.**
13. **The simpler model was more effective for this particular data representation and validation setup.**
14. **The final model was evaluated separately on completely unseen test engines.**
15. **Model complexity was increased only when the data and validation results justified it.**

---

# Final Perspective

The main learning from this project was not simply which algorithm produced the lowest error.

The bigger lesson was the importance of **understanding the data before increasing model complexity**.

I started by studying the relationship between engine cycles, sensor measurements, and RUL.

The data showed a strong and relatively smooth degradation pattern, so Linear Regression was chosen as a reasonable baseline.

I then tested whether more complex approaches could improve that baseline.

Feature selection, Ridge, Lasso, RUL capping, Random Forest, Random Forest tuning, and Gradient Boosting were all evaluated using the same validation approach.

The experiments showed that the more complex models did not provide a meaningful improvement.

For this FD001 problem, the simpler Linear Regression model was able to capture the main degradation relationship effectively.

> **The best model is not necessarily the most complex model. It is the model that fits the structure of the data and performs reliably on unseen data.**
