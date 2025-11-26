import pandas as pd

def sample_reviews(input_path, output_path, sample_size=1500):
    print(f"1. Reading file: {input_path} ...")
    
    try:
        # Read CSV file
        df = pd.read_csv(input_path, low_memory=False)
        print(f"   File loaded successfully. Total reviews: {len(df)}.")
    except Exception as e:
        print(f"   Failed to read file: {e}")
        return

    # Check whether data is sufficient
    if len(df) < sample_size:
        print(f" Warning: The file contains only {len(df)} rows, less than the requested {sample_size}.")
        print("  Exporting all rows instead.")
        sampled_df = df
    else:
        # --- Main step: random sampling ---
        print(f"2. Randomly sampling {sample_size} reviews...")
        # random_state=42 ensures reproducible sampling every run
        # If you want different results each time, remove random_state=42
        sampled_df = df.sample(n=sample_size, random_state=42)

    # Save output
    print(f"3. Saving sampled results to: {output_path}")
    sampled_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"Done! Successfully sampled {len(sampled_df)} rows from {len(df)} total.")

# ================= Configuration =================

# 1. Your source file (the CSV with ~200k English reviews)
input_file = "english_reviews_filtered_2077.csv"

# 2. Output file (the sampled CSV)
output_file = "random_1500_sample.csv"

# ==================================================

if __name__ == "__main__":
    sample_reviews(input_file, output_file)
