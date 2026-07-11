import streamlit as st
from schedule_generation import new_generate_schedule
import pandas as pd
from zipfile import ZipFile
from pathlib import Path
import tempfile
import base64
import calendar

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()


@st.dialog("📊 Generation Summary")
def show_summary(stats):
    st.success("Schedule generated successfully!")
    st.metric("Unique Outlets", f"{stats['stores']:,}")
    st.metric("Schedules Generated", f"{stats['rows']:,}")
    st.metric("Files Generated", f"{stats['files']:,}")

    st.write("### Output Files")
    for file in stats["filenames"]:
        st.write(f"• {file}")

    st.write("Click outside this window to close, and Dowload the Zip File(s)")

bg_img = get_base64("assets/hd1.jpg")

st.set_page_config(

    page_title="Project RCC",
    page_icon="🐍",      # Optional: emoji or image
    layout="centered",   # or "wide"
    initial_sidebar_state="auto"

)
st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpeg;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

.block-container {
    max-width: 850px;
    margin: 100px auto 0 auto;
    padding: 40px;
    backdrop-filter: blur(20px);
    background: rgba(20,20,20,.55);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0,0,0,.35);
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Download button */
div[data-testid="stDownloadButton"] > button {

    width: 100%;
    height: 70px;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;

}

/* Generate button */
div[data-testid="stButton"] > button {

    width: 100%;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;

}

</style>
""", unsafe_allow_html=True)

def create_zip(output_files: list[Path], zip_name: str) -> Path:

    zip_path = Path("Output") / zip_name

    with ZipFile(zip_path, "w") as zip_file:

        for file in output_files:
            zip_file.write(file, arcname=file.name)

    return zip_path

st.title("ProjectRCC")
st.write("🎉 Please upload (1) file at time, make sure that it is in correct format before Running the script!")

uploaded_file = st.file_uploader(
                "Upload Consolidated RSR Schedule Summary",
                type=["xlsx"],
                accept_multiple_files = False,
            )
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    st.write(f'Initial checking you have **{len(df)} ** number of outlets in your file:')
    st.dataframe(df.head())

with st.sidebar:

    st.header("📖 User Guide")

    st.markdown("""
        ### Before Uploading

        Please make sure your Excel file contains the following columns:

        - **Store_ID**
        - **Store_Name**
        - **CallDays**

        ### Upload file
        1. Please make your  all **CallyDays** are uniquely identify.
        2. Please follow (Mon/Tue/Wed/Thu/Fri/Sat) as CallDays Format.
        ---

        ### Steps

        1. Upload the Consolidated RSR Schedule Summary.
        2. Select the Month.
        3. Enter the Year.
        4. Enter the Start Day.
        5. Provide an output filename.
        6. Click **Generate Schedule**.
        7. Download the generated ZIP file.

        ---

        ### Notes

        - Only **.xlsx** files are supported.
        - Maximum upload size: **200 MB**
        - Files are processed temporarily and are **not stored**.
        - Large outputs are automatically split into multiple CSV files.
        - Maximum of 99,998 Rows per Excel File.

        ---

        ### Need Help?

        Contact Japs, Need niya ng Sting.
        """)

month = st.selectbox(
                "Month",
                range(1,13),
                index=0      # July
            )

year = st.number_input(
    "Year",
    min_value=2025,
    max_value=2050,
    value=2026
)
last_day_of_month =calendar.monthrange(year,month)[1]
st.caption(f"Last day of {calendar.month_name[month]} {year}: **{last_day_of_month}**")

start_day = st.selectbox(
    "Start Day",
    options=list(range(1, last_day_of_month + 1)),
    index = 0,
    help  = f"Select a day between 1 and {last_day_of_month}."

)

output_name = st.text_input(
"Output filename",
"Your_File_Name.csv"
)       

if uploaded_file:
    

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    if st.button("🚀 Generate Schedule"):
    
            with st.spinner('Generating Now.. Please wait.'):
                output_files = new_generate_schedule(tempfile=temp_path,
                month=month,
                year=year,
                start_day=start_day,
                output_file=output_name,
                )
                       
            stats = {
                "stores": output_files["unique_store_count" ],
                "rows": output_files["total_schedule_rows"],
                "files": len(output_files["output_files"]),
                "filenames": [p.name for p in output_files["output_files"]],
            }
            show_summary(stats)


            zip_file = create_zip(output_files["output_files"], "Generated_Schedule.zip")    

            st.success("Schedule generated successfully!")
            st.balloons()
            st.toast("✅ 🗂️Generation Complete! Download the ZIP File.")
            col1, col2, col3 = st.columns([1, 2, 5])

            with col3:
                with open(zip_file, "rb") as f:

                    st.download_button(
                        "📦 Download Schedule ZIP",
                        data=f,
                        file_name="Generated_Schedule.zip",
                        mime="application/zip",

                    )


