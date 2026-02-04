import streamlit as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Ammo Calculator", layout="centered")

# RTL Support for Hebrew
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    div[data-baseweb="select"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    file_path = "C:\\code\\taz.csv"
    df = pd.read_csv(file_path)
    
    # Data Cleaning
    df["תחמושת"] = df["תחמושת"].astype(str).str.replace(r",", "", regex=True)
    df["תחמושת"] = pd.to_numeric(df["תחמושת"], errors='coerce').fillna(0)
    
    # Create a helper column for the selection box that combines Training and Name
    # Example: "אימון בוקר | ישראל ישראלי"
    df["display_name"] = df["אימון"].astype(str) + " | " + df["שם"].astype(str)
    return df

try:
    taz_file = load_data()

    st.title("מחשבון תחמושת ואימונים")

    # --- USER SELECTION ---
    st.subheader("בחירת נתונים")
    
    # The dropdown now shows the combined string
    options = taz_file["display_name"].tolist()
    selected_option = st.selectbox("בחר אימון ושם:", options)
    
    amount = st.number_input("בחר כמות:", min_value=1, value=1, step=1)

    # --- CALCULATION ---
    # Find the specific row where the combined string matches
    row_data = taz_file[taz_file["display_name"] == selected_option].iloc[0]
    
    ammo_per_unit = row_data["תחמושת"]
    training_type = row_data["אימון"]
    person_name = row_data["שם"]
    
    total_ammo = ammo_per_unit * amount

    # --- DISPLAY RESULTS ---
    st.divider()
    
    # Displaying details in a clean format
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="סה\"כ תחמושת נדרשת", value=f"{total_ammo:,.0f}")
    
    with col2:
        st.write(f"**אימון:** {training_type}")
        st.write(f"**שם:** {person_name}")
        st.write(f"**תחמושת ליחידה:** {ammo_per_unit}")

except FileNotFoundError:
    st.error("הקובץ לא נמצא בנתיב C:\\code\\taz.csv")
except Exception as e:
    st.error(f"שגיאה בעיבוד הנתונים: {e}")