# 📅 Project RCC

Project RCC is a Streamlit-based web application that automates the generation of EDS Schedule Upload Files from the Consolidated RSR Schedule Summary.

The application allows users to upload an Excel file, generate schedules based on service days, and download the generated CSV files as a ZIP archive.

---

## ✨ Features

- 📁 Upload Consolidated RSR Schedule Summary (.xlsx)
- 👀 Preview uploaded data
- 📊 Display generation statistics
- 🚀 Generate schedule automatically
- 📦 Export multiple CSV files if export limit is exceeded
- 🗜 Automatically compress generated files into a ZIP archive
- 🎉 Success notification after generation
- 📈 Summary dialog showing generation metrics
- 🎨 Modern Streamlit UI with custom background

---

## 🖥️ Screenshots

> *(Add screenshots here after deployment.)*

---

## 📂 Project Structure

```
ProjectRCC/
│
├── app.py                     # Streamlit application
├── schedule_generation.py     # Schedule generation logic
├── assets/
│   ├── bg.jpg
│   └── logo.png
├── Output/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ProjectRCC.git
```

Go to the project directory

```bash
cd ProjectRCC
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📥 Input File Requirements

The uploaded Excel file must contain the following columns:

| Column | Description |
|---------|-------------|
| STORE_ID | Unique Outlet ID |
| STORE_NAME | Outlet Name |
| CALL_DAYS | Service Days (Example: Mon/Wed/Fri) |

Example

| STORE_ID | STORE_NAME | CALL_DAYS |
|----------|------------|-----------|
| 709942161428 | 271 EATERY | Mon/Wed/Fri |

---

## 🚀 How to Use

1. Open the application.
2. Upload the Consolidated RSR Schedule Summary.
3. Verify the uploaded data.
4. Select:
   - Month
   - Year
   - Start Day
5. Enter the output filename.
6. Click **Generate Schedule**.
7. Wait for the generation process to complete.
8. Review the generation summary.
9. Download the generated ZIP file.

---

## 📊 Generation Summary

After every successful generation, the application displays:

- Unique Outlets
- Total Schedules Generated
- Number of CSV Files Generated

---

## 📦 Export Logic

If the generated schedule exceeds the configured export limit, the application automatically splits the output into multiple CSV files.

Example:

```
Schedule.csv
```

or

```
Schedule_part_1.csv
Schedule_part_2.csv
Schedule_part_3.csv
```

All generated files are automatically compressed into a ZIP archive.

---

## 🛠️ Built With

- Python 3.13
- Streamlit
- Pandas
- OpenPyXL

---

## 📌 Version

Current Version: **1.0.0**

---

## 👨‍💻 Developer

Developed by **Z**

Project RCC was created to simplify and automate the generation of EDS Schedule Upload Files for internal operational use.

---

## 📄 License

This project is intended for internal use.

Unauthorized distribution or modification without permission is prohibited.
