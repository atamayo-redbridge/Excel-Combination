import streamlit as st
import pandas as pd
from io import BytesIO

def combine_excel_files(uploaded_files):
    """Function to combine multiple Excel files into one while ensuring all columns are present."""
    combined_df = pd.DataFrame()
    
    for file in uploaded_files:
        df = pd.read_excel(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)
    
    return combined_df

def convert_df_to_excel(df):
    """Convert DataFrame to Excel format for download."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Combined Data')
    processed_data = output.getvalue()
    return processed_data

def main():
    st.title("Excel File Combiner")
    st.write("Upload multiple Excel files to combine them into a single file.")
    
    uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx'])
    
    if uploaded_files:
        st.write("Processing files...")
        combined_df = combine_excel_files(uploaded_files)
        
        st.write("### Combined Data Preview:")
        st.dataframe(combined_df.head(10))  # Show first 10 rows as a preview
        
        if st.checkbox("Drop columns?"):
            all_columns = list(combined_df.columns)
            columns_to_drop = st.multiselect("Select columns to drop", all_columns)
            if columns_to_drop:
                combined_df = combined_df.drop(columns=columns_to_drop)
                st.write("### Updated Data After Dropping Columns:")
                st.dataframe(combined_df.head(10))  # Show preview after dropping columns
        
        excel_data = convert_df_to_excel(combined_df)
        st.download_button(label="Download Combined Excel", data=excel_data, file_name="Combined_Data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()
