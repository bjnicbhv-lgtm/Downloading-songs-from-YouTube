import streamlit as st
import yt_dlp
import os

# הגדרת כותרת האתר ומראה כללי
st.set_page_config(page_title="YouTube Music Downloader", page_icon="🎵")

st.title("Downloading songs from YouTube with filtering")
st.write("הדבק קישור מיוטיוב, בחר פורמט ולחץ על הכפתור כדי להוריד.")

# תיבת קלט לקישור
url = st.text_input("הכנס קישור כאן:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("בחר פורמט הורדה:", ["MP3", "MP4"], horizontal=True)

if url:
    if st.button("התחל הורדה"):
        with st.spinner("מעבד את הבקשה... המתן לסיום"):
            try:
                # טעינת עוגיות מה-Secrets של Streamlit
                if "YT_COOKIES" not in st.secrets:
                    st.error("שגיאה: לא הוגדרו עוגיות (Cookies) ב-Secrets של האתר.")
                    st.stop()
                
                cookies_content = st.secrets["YT_COOKIES"]
                with open("cookies.txt", "w") as f:
                    f.write(cookies_content)

                # הגדרות הורדה חכמות - לוקח את הפורמט הכי טוב שזמין בלי להסתבך
                ydl_opts = {
                    'format': 'bestaudio/best' if format_choice == "MP3" else 'best/bestvideo+bestaudio',
                    'cookiefile': 'cookies.txt',
                    'outtmpl': 'downloaded_file.%(ext)s',
                    'writethumbnail': True,
                    'embedmetadata': True,
                    'quiet': True,
                    'no_warnings': True,
                }

                # הוספת המרה ל-MP3 אם נבחר
                if format_choice == "MP3":
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # חילוץ מידע והורדה
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # תיקון שם הקובץ במקרה של המרת אודיו
                    if format_choice == "MP3" and not filename.endswith(".mp3"):
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                # יצירת כפתור הורדה למשתמש
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        st.success(f"✅ השיר '{info.get('title', 'הקובץ')}' מוכן!")
                        st.download_button(
                            label="📥 לחץ כאן להורדה למכשיר",
                            data=file,
                            file_name=f"{info.get('title', 'download')}.{'mp3' if format_choice == 'MP3' else 'mp4'}",
                            mime="audio/mpeg" if format_choice == "MP3" else "video/mp4"
                        )
                    
                    # ניקוי קבצים מהשרת לאחר ההורדה
                    os.remove(filename)
                
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")

            except Exception as e:
                st.error(f"שגיאה בתהליך: {str(e)}")
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")
