import streamlit as st
import yt_dlp
import os

# הגדרות דף ועיצוב
st.set_page_config(page_title="Ultimate Downloader", page_icon="📥")
st.title("YouTube Downloader")
st.write("הורדת שירים וסרטונים בצורה בטוחה. העתק קישור ובחר פורמט.")

# קלט מהמשתמש
url = st.text_input("הדבק כאן את הקישור מיוטיוב:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("מה תרצה להוריד?", ["MP3 (רק מוזיקה)", "MP4 (סרטון מלא)"], horizontal=True)

if url and st.button("התחל הורדה"):
    with st.spinner("מעבד את הבקשה... נא להמתין"):
        try:
            # הגדרת נתיב עוגיות מה-Secrets (למניעת חסימות)
            cookie_path = None
            if "YT_COOKIES" in st.secrets:
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])
                cookie_path = "cookies.txt"

            # הגדרות הורדה חכמות לעקיפת הגבלות
            ydl_opts = {
                'cookiefile': cookie_path,
                'outtmpl': 'download_file.%(ext)s',
                'nocheckcertificate': True,
                # הגדרה קריטית: הורדת שיר בודד בלבד גם אם הקישור הוא לפלייליסט/מיקס
                'noplaylist': True,
                # התחזות לדפדפן רגיל כדי לעקוף "Signature solving failed"
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
