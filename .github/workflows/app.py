import streamlit as st
import requests
import time

st.title("Downloading songs from YouTube")
st.write("הכנס קישור וההורדה תתחיל בשרת")

# תיבת קלט לקישור
url = st.text_input("הדבק כאן את הקישור מיוטיוב:")
format_choice = st.selectbox("בחר פורמט:", ["mp3", "mp4"])

if st.button("הורד שיר"):
    if url:
        # פקודה לגיטהאב להפעיל את ה-Action
        # כאן צריך להגדיר את פרטי המאגר שלך
        owner = "YOUR_GITHUB_USERNAME"
        repo = "YOUR_REPO_NAME"
        workflow_id = "download.yml"
        token = st.secrets["GH_TOKEN"] # מפתח אבטחה
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        data = {
            "ref": "main",
            "inputs": {
                "yt_urls": url,
                "format": format_choice
            }
        }
        
        response = requests.post(
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            headers=headers,
            json=data
        )
        
        if response.status_code == 204:
            st.success("הבקשה נשלחה! השיר יופיע ב-Releases בתוך דקה.")
            st.info("שלח לחברים קישור לדף ה-Releases שלך כדי שיורידו משם.")
        else:
            st.error("הייתה שגיאה בחיבור לגיטהאב.")
