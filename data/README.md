# Data Documentation

This folder contains the datasets used and generated throughout the project.  
To ensure privacy and security, only **processed and anonymized datasets** are included in this repository.  
The **raw datasets with sensitive information are excluded** and ignored via `.gitignore`.

---

## 1. Raw Data (Not Included)

The original datasets are **NOT stored in this repository** because they contain sensitive user-generated content.

Raw files include:

- `cyberpunk2077_all_english_reviews.csv`
- `palworld_all_english_reviews.csv`
- `hammer_totoal_war.csv`

These files are stored locally under:

data/raw/


They are excluded from GitHub for privacy reasons.

---

## 2. Processing Pipeline

The data processing consists of **three main steps**, implemented in `src/process_reviews.py`.

### **Step 1 — Time Filtering**
Only reviews within a specific time range were retained.  
This helps ensure data consistency and relevance (e.g., post-release reviews).

### **Step 2 — Language Filtering (English Only)**
Non-English reviews were removed using a language detection pipeline.  
Only English-language reviews were kept for downstream analysis.

### **Step 3 — Removal of Low-Quality or Spam Comments**
We removed:
- empty reviews  
- extremely short comments  
- duplicate texts  
- reviews containing irrelevant or meaningless characters  
- detected spam or noise entries  

After these steps, each raw dataset was cleaned and standardized.

### **Output of 3-step cleaning:**
english_reviews_filtered_2077.csv # Example output file


Equivalent files exist for each game title (not included in this repo because they still contain textual content derived from the raw data).

---

## 3. Random Sampling (1500 Reviews)

From each cleaned dataset, we selected **1500 random reviews** for aspect extraction.  
This sampling process is implemented in:

src/random_selection.py


Sampling details:
- **Sample size:** 1500 reviews
- **Random seed:** 42 (ensures reproducibility)
- **Input:** e.g., `english_reviews_filtered_2077.csv`
- **Output:** `random_1500_sample.csv`

---

## 4. Aspect Extraction via LLMs

Using the sampled 1500 reviews, we applied multiple LLMs to extract **aspects** (topics/features mentioned by players).

Three models were used:

1. **xAI (xai)**
2. **DeepSeek**
3. **ChatGPT**

Each model produced structured outputs (aspects + sentiment or cluster metadata).  
We then clustered the extracted aspects and saved the results into final processed datasets.

Example of final output filenames:

palwrold_final_ai_clustered_deepseek.csv
palwrold_final_ai_clustered_gpt.csv
palwrold_final_ai_clustered_xai.csv

cyber_2077_final_ai_clustered_deepseek.csv
cyber_2077_final_ai_clustered_gpt.csv
cyber_2077_final_ai_clustered_xai.csv

hammer_final_ai_clustered_deepseek.csv
hammer_final_ai_clustered_gpt.csv
hammer_final_ai_clustered_xai.csv

These files contain **non-sensitive, aggregated, LLM-processed results**, and are therefore safe to include in this public repository.

---

## 5. Folder Structure Summary
```text
data/
│
├── raw/ # Not included in GitHub 
├── processed/ # Final public datasets 
│ ├── *_final_ai_clustered_deepseek.csv
│ ├── *_final_ai_clustered_gpt.csv
│ └── *_final_ai_clustered_xai.csv
│
└── README.md # (this file)

---

If you are using this dataset or pipeline, please ensure that the **raw data is stored securely** and