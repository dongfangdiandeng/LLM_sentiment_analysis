import pandas as pd
from langdetect import detect, DetectorFactory
from tqdm import tqdm

# Fix random seed to ensure stable language detection results
DetectorFactory.seed = 0

def process_large_csv(file_path, review_col, time_col, output_path):
    print(f"1. Reading CSV file: {file_path} ...")
    
    try:
        # Use read_csv with low_memory=False to prevent mixed-type warnings on large files
        # If you encounter UnicodeDecodeError, try setting encoding='utf-8' or 'gbk'
        df = pd.read_csv(file_path, low_memory=False)
        print(f"   Successfully loaded. Total rows: {len(df)}.")
    except Exception as e:
        print(f"   Failed to read file: {e}")
        print("   Tip: If you see an encoding error, try changing the encoding parameter (e.g., 'gbk').")
        return

    # Check if required columns exist
    if review_col not in df.columns or time_col not in df.columns:
        print(f"Error: Column names do not match.")
        print(f"Your CSV contains columns: {list(df.columns)}")
        print("Please verify your configured column names.")
        return

    # --- Step 1: Filter by timestamp (before June 30, 2025) ---
    print("2. Filtering by timestamp...")

    # Ensure timestamp column is numeric (handles dirty data)
    df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
    df = df.dropna(subset=[time_col])  # Remove invalid timestamp rows

    # Convert timestamp to readable datetime (unit='s' means seconds)
    df['datetime_readable'] = pd.to_datetime(df[time_col], unit='s')

    # Define cutoff date
    cutoff_date = pd.Timestamp("2025-06-30")

    # Filter rows
    df_filtered = df[df['datetime_readable'] < cutoff_date].copy()
    print(f"   After timestamp filtering: {len(df_filtered)} rows (removed {len(df) - len(df_filtered)} rows).")

    if len(df_filtered) == 0:
        print("Warning: No data left after date filtering. Please check your timestamp column.")
        return

    # --- Step 2: Prepare review text ---
    # Keep only the review column and drop empty values
    df_filtered = df_filtered[[review_col]].dropna()
    df_filtered[review_col] = df_filtered[review_col].astype(str)

    # --- Step 3: Language detection (keep English only) ---
    print(f"3. Detecting language for {len(df_filtered)} rows...")

    def is_english(text):
        try:
            if len(text) < 3:
                return False  # Ignore very short text
            return detect(text) == 'en'
        except:
            return False

    tqdm.pandas(desc="Language Detection Progress")
    mask = df_filtered[review_col].progress_apply(is_english)

    final_df = df_filtered[mask]

    print(f"4. Language detection completed! Final English reviews: {len(final_df)}.")

    # --- Step 4: Save output ---
    print(f"5. Saving output to: {output_path}")
    # encoding='utf-8-sig' makes CSV readable in Excel without BOM issues
    final_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print("Done!")

# ================= Configuration Section =================

# 1. Input CSV file (must end with .csv)
input_file = "cyberpunk2077_all_english_reviews.csv"

# 2. Column name that contains review text
review_column_name = "review_text"

# 3. Timestamp column name (as identified in your dataset)
time_column_name = "timestamp_created"

# 4. Output filename
output_file = "english_reviews_filtered_2077.csv"

# ========================================================

if __name__ == "__main__":
    process_large_csv(input_file, review_column_name, time_column_name, output_file)
