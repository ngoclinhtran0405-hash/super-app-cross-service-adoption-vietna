# Data availability

The raw survey responses (n = 300) are **not published** in this repository to protect respondent privacy.

- Aggregated model outputs are in [`../results/`](../results/).
- To re-run `analysis/seminr_model.R`, place an anonymised file named `survey_anonymised.csv` here.
  Columns must be the item codes (e.g. `CL1`, `CSA1`, …, `VSS3`) on a 1–7 scale; no names, emails, phone numbers or free-text fields.
- `.gitignore` excludes `data/*.csv` and SmartPLS project files (`*.splsm`) so they cannot be committed by accident.
