import streamlit as st
from schedule_generation import new_generate_schedule
import pandas as pd
from zipfile import ZipFile
from pathlib import Path
import tempfile
import base64
import calendar
from datetime import datetime


#----------------- LOGIN -----------------#
users = st.secrets["users"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "username" not in st.session_state:
    st.session_state.username = ""
    


#----------------- LOGIN END -----------------#

#----------------- FUNCTIONS -----------------#
def login():
    # Hardcoded credentials for demonstration purposes
    users = st.secrets["users"]
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if username in users and password == users[username]:
            st.session_state.logged_in = True
            st.session_state.username = username
                
            st.rerun()
        else:
            st.error("Invalid username or password.")
            
def sidebarlogin():
    with st.sidebar:
    
        st.write(f"👤 Logged in as **{st.session_state.username}**")
        if st.button("🚪 Logout", use_container_width = True):
            st.session_state.logged_in = False
            st.session_state.username = ''
            st.success("Logged out successfully!")
            st.rerun()


def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()


@st.dialog("📊 Generation Summary")
def show_summary(stats):
    st.success("Schedule generated successfully!")
    st.metric("Type", f"{stats['filetype']}")
    st.metric("Unique Outlets", f"{stats['stores']:,}")
    st.metric("Schedules Generated", f"{stats['rows']:,}")
    st.metric("Files Generated", f"{stats['files']:,}")
    st.metric("Date and Time", f"{stats['generation_date']}")
    

    st.write("### 📁 Output Files")
    max_show = 3

    if len(stats["filenames"]) <= max_show:
       files = stats["filenames"]
    else:
        files = stats["filenames"][:max_show]

    file_list = "\n".join(f"- `{file}`" for file in files)

    st.markdown(file_list)

    remaining = len(stats["filenames"]) - max_show
    st.caption(f"Showing the first {max_show} of {len(stats['filenames'])} generated files. "
            f"{remaining} additional file(s) are included in the ZIP download.")
    
    st.write("Click outside this window to close, and Dowload the Zip File(s)")

def main():
    sidebarlogin()

    bg_img = get_base64("assets/hd1.jpg")
    st.title(" RTM Command Center")
    st.header("📅 DMS Schedule Generator", divider = True )
    
    st.set_page_config(
    
        page_title="RCC - Schedule Generator",
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
        margin: 90px auto 0 auto;
        padding: 35px;
                
        background: rgba(48,92,222,.70);
        backdrop-filter: blur(35px);
        border:1px solid rgba(255,255,255,.35);
        box-shadow:0 10px 35px rgba(0,0,0,.25);
        border-radius:20px;
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
            ### About
            
            Project RCC automatically generates delivery schedules
            based on the uploaded RSR Schedule Summary
            while honoring each outlet's configured Call Days.  

            © 2026 ProjectRCC
            Version 1.0.0
            Build Date 2026.07
            ** Stricly for Internal Use Only**
            
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
            6. Please select the appropriate file type: Online, Offline, or Retailer.
            8. Click **Generate Schedule**.
            7. Download the generated ZIP file.
    
            ---
    
            ### Notes
    
            - Only **.xlsx** files are supported.
            - Maximum upload size: **200 MB**
            - Files are processed temporarily and are **not stored**.
            - Large outputs are automatically split into multiple CSV files.
            - Maximum of 99,998 Rows per Excel File.
            - Schedules are generated only for the outlet’s assigned call days.
            If the selected start date is not one of the configured call days (e.g., Sunday),
            generation will begin on the next valid call day.
            
            ---
            
            ### Need Help?
    
            Contact Japs, Need niya ng Sting.
            """)
    
    month = st.selectbox(
                    "Month",
                    range(1,13),
                    index=0,
                    format_func = lambda x : calendar.month_name[x] # July
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
    @st.dialog("Select File Upload types")
    def select_type_dialog():
        st.write(" What type of file are you uploading? ")
        f_file = st.selectbox('Types',
                     options = list(['Delivery Online','Delivery Offline','Retailer']),
                     index=0)
        if st.button('Submit', use_container_width = True):
            st.session_state["select_type"]  = f_file
            st.rerun()
    
    if "select_type" not in st.session_state:
        st.session_state["select_type"] = "Delivery Online"
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"""
            <div style="
                background:#1E2533;
                border-left:6px solid #4EA8FF;
                border-radius:10px;
                padding:18px;
                color:white;
                height:70px;
                display:flex;
                flex-direction:column;
                justify-content:center;
            ">
            <b>📂 File Type</b><span style="font-size:17px;color:#5CB8FF;">
            {st.session_state['select_type']}
            </span>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        if st.button("Change Type",use_container_width=True):
            select_type_dialog()
    
    
    output_name = st.text_input(
    "Output filename",
    "Your_File_Name.csv"
    )       
    
    if uploaded_file:
        
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name
    
        if st.button("🚀 Generate Schedule"):
                generated_zip_with_file_type = str(st.session_state["select_type"])+'_'+'Generated_Schedule.zip'
                with st.spinner('Generating Now.. Please wait.'):
                    output_files = new_generate_schedule(tempfile=temp_path,
                    month=month,
                    year=year,
                    start_day=start_day,
                    output_file= str(st.session_state["select_type"])+"_"+output_name,
                    )
                           
                stats = {
                    "stores": output_files["unique_store_count" ],
                    "rows": output_files["total_schedule_rows"],
                    "files": len(output_files["output_files"]),
                    "filenames": [p.name for p in output_files["output_files"]],
                    "filetype": st.session_state["select_type"],
                    "generation_date" : datetime.now().strftime("%B %d, %Y %I:%M %p")
                }
                show_summary(stats)
    
    
                zip_file = create_zip(output_files["output_files"], generated_zip_with_file_type)    
    
                st.success("Schedule generated successfully!")
                st.balloons()
                st.toast("✅ 🗂️Generation Complete! Download the ZIP File.")
                col1, col2, col3 = st.columns([1, 2, 5])
    
                with col3:
                    with open(zip_file, "rb") as f:
    
                        st.download_button(
                            "📦 Download Schedule ZIP",
                            data=f,
                            file_name = generated_zip_with_file_type,
                            mime = "application/zip",
    
                        )
if not st.session_state.logged_in:
    left, center, right = st.columns([1, 2, 1])
    st.markdown("""
                <style>

                /* Center column */
                div[data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"]{
                    background:#FFFFFF;
                    mix-blend-mode: normal;
                    margin: 10px auto;
                    border-radius:20px;
                    padding:10px;
                    box-shadow:0 15px
                }
                </style>
    """, unsafe_allow_html=True)
    
    with center:
    
        with st.container(border=True):
           
            st.markdown("""<style>
            .login-wrapper {
                background:white;
                border-radius: 10px;
                padding: 20px;
                border:none;
                box-shadow:0 15px 40px rgba(0,0,0,.18);
                
            }
            </style>""", unsafe_allow_html=True)
            st.markdown(
                """
                <div class="login-card">
                    <h1 style="text-align:center; margin-bottom:10px; font-size:34px; font-weight:700;
                    ">
                    🔐 ProjectRCC</h1>
                    <p style="text-align:center; margin-top:0px; margin-bottom:0px; font-size:12px; color:#E5E7EB;">
                    Please sign in to continue.</p>
                </div>
            
                <style>
                .login-card{
                    background-color: rgba(55, 55, 55, 0.9);
                    margin: 10px 10px 10px 10px;
                    padding: 20px 10px 20px 10px;
                    border-radius: 10px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    text-align: center;
                </style>   
                """,
                unsafe_allow_html=True
            )
            st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #1E40AF 0%, #2563EB 55%, #3B82F6 100%);
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            </style>
                        """,
                        unsafe_allow_html=True)
            st.markdown("""
            <style>

            /* Labels */
            .stTextInput label{
                color:#111827;
                font-weight:600;}
        
            .stTextInput input{
            color:#white;
            }
            .stTextInput input:focus{
                border:2px solid #2563EB;

            }
                       
            .stButton > button:hover{
            background:#2563EB;
            color:white;
            border:none;
            transform:translateY(-2px);
            box-shadow:0 8px 18px rgba(37,99,235,.35);
            cursor:pointer;
            }
            </style>
            """, unsafe_allow_html=True)
            login()
    st.stop()

main()

#------------------ APP FLOW -----------------#
# Developer: Japs
# Date: 2024-06-20  
#Dev note: The flow of the app is as follows:

            # Start App
            #       │
            #       ▼
            # Initialize Session State
            #       │
            #       ▼
            # Logged In?
            #    │        │
            #   No       Yes
            #    │        │
            # login()   main()
            #    │        │
            # st.stop() sidebar()
            #             │
            #             ▼
            #         Generate Module


#------------------ APP FLOW END -----------------#
