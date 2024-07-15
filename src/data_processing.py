import io
import logging
import pandas as pd

def append_new_data(existing_file, new_files):
    """Appends new data to the existing file."""
    logging.info("Appending new data to the existing file.")
    existing_df = pd.read_csv(existing_file) if existing_file else pd.DataFrame()
    
    new_dfs = []
    for new_file in new_files:
        new_dfs.append(pd.read_csv(new_file))
    
    combined_df = pd.concat([existing_df] + new_dfs).drop_duplicates(keep='last')
    
    combined_content = io.BytesIO()
    combined_df.to_csv(combined_content, index=False)
    combined_content.seek(0)
    logging.info("Appended new data to the existing file.")
    return combined_content
