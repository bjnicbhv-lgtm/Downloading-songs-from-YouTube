import streamlit as st
import yt_dlp
import os

# הגדרות דף
st.set_page_config(page_title="YouTube Downloader Pro", page_icon="🎵")

st.title("YouTube Downloader")
st.write("הדבק קישור מיוטיוב, בחר פורמט והורד.")

# קלט מהמשתמש
url = st.text_input("הכנס קישור כאן:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("בחר פורמט:", ["MP3 (רק אודיו)", "MP4 (וידאו)"], horizontal=True)

if url:
    if st.button("התחל הורדה"):
        with st.spinner("מעבד... נא להמתין"):
            try:
                # טעינת עוגיות מה-Secrets (קריטי למניעת חסימות)
                if "YT_COOKIES" not in st.secrets:
                    st.error("שגיאה: חסר YT_COOKIES ב-Secrets של Streamlit.")
                    st.stop()
                
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])

                # הגדרות הורדה מעודכנות לעקיפת חסימות
                ydl_opts = {
                    'cookiefile': 'cookies.txt',
                    'outtmpl': 'downloaded_file.%(ext)s',
                    'nocheckcertificate': True,
                    'quiet': True,
                    'no_warnings': False,
                    # שימוש בלקוחות שונים כדי לעקוף Signature solving failed
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                }

                if "MP3" in format_choice:
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                else:
                    # הגדרה ל-MP4 איכותי שכולל וידאו וסאונד יחד
                    ydl_opts['format'] = 'best[ext=mp4]/best'

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # וידוא סיומת לקובץ MP3
                    if "MP3" in format_choice and not filename.endswith(".mp3"):
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                # יצירת כפתור הורדה למשתמש
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        st.success(f"✅ השיר '{info.get('title')}' מוכן!")
                        st.download_button(
                            label="📥 לחץ כאן להורדה",
                            data=file,
                            file_name=f"{info.get('title')}.{'mp3' if 'MP3' in format_choice else 'mp4'}",
                            mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                        )
                    os.remove(filename) # מחיקה לאחר הורדה לשמירה על מכסה בשרת
                
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")

            except Exception as e:
                st.error(f"חלה שגיאה: {str(e)}")
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")
