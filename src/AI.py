import pandas as pd
import json
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================= Configuration =================

API_KEY = "#############"
BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"
INPUT_FILE = "sample.csv"
OUTPUT_FILE = "sample.csv"

MAX_WORKERS = 50  # Number of threads for parallel processing

# =================================================

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def analyze_single_review(data_tuple):
    """
    Wrapper for multithreading. The row index and text are passed together.
    data_tuple: (index, review_text)
    """
    index, review_text = data_tuple

    prompt = f"""
    Analyze the review to understand the "Evaluative Lenses" (Perspectives).
    Review: "{review_text}"
    Instructions:
    1. Identify the high-level perspective (e.g., "Consumer Value", "Technical Stability", "Narrative").
    2. Return JSON key 'angles' with a list of 1-3 short phrases.
    Example: {{"angles": ["Price Perspective", "Gameplay Loop"]}}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Output JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            timeout=30
        )

        content = response.choices[0].message.content
        clean_json = content.replace("```json", "").replace("```", "").strip()

        data = json.loads(clean_json)
        angles = data.get("angles", [])
        return index, ", ".join(angles)

    except Exception:
        return index, "API_Error"

def main():
    print(f"1. Reading file: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    df['review_text'] = df['review_text'].astype(str)

    # Prepare task list: pack (index, text) pairs for threading
    tasks = []

    target_df = df        # Run full dataset
    # target_df = df.head(50)  # Use this line for quick debug/testing

    for index, row in target_df.iterrows():
        tasks.append((index, row['review_text']))

    results_dict = {}  # Store results because multithreading returns in random order

    print(f"2. Starting {MAX_WORKERS} threads to process {len(tasks)} records...")

    # --- Core: multithreaded processing ---
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_review = {executor.submit(analyze_single_review, task): task for task in tasks}

        # Show progress bar with tqdm
        for future in tqdm(as_completed(future_to_review), total=len(tasks), desc="AI Processing"):
            idx, result_str = future.result()
            results_dict[idx] = result_str

    # 3. Reconstruct ordered results
    print("3. Reconstructing ordered results...")
    final_results = []
    for i in target_df.index:
        final_results.append(results_dict.get(i, "Error"))

    target_df = target_df.copy()
    target_df['Review_Angles'] = final_results

    print(f"4. Saving to: {OUTPUT_FILE}")
    target_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print("Done!")

if __name__ == "__main__":
    main()
