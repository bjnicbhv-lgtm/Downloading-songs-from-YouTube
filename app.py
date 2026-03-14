import streamlit as st
import yt_dlp
import os

# הגדרות דף ועיצוב
st.set_page_config(page_title="YouTube Downloader", page_icon="📥")
st.title("YouTube Downloader")
st.write("הורדת שירים וסרטונים בצורה בטוחה.")

# קלט מהמשתמש
url = st.text_input("הדבק כאן את הקישור מיוטיוב:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("בחר פורמט:", ["MP3 (שיר)", "MP4 (סרטון)"], horizontal=True)

if url and st.button("התחל הורדה"):
    with st.spinner("מעבד... נא להמתין"):
        try:
            # טיפול בעוגיות מתוך ה-Secrets של Streamlit
            cookie_path = None
            if "YT_COOKIES" in st.secrets:
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])
                cookie_path = "cookies.txt"

            # הגדרות הורדה מעודכנות לעקיפת חסימות
            ydl_opts = {
                'cookiefile': cookie_path,
                'outtmpl': 'downloaded_file.%(ext)s',
                'nocheckcertificate': True,
                'noplaylist': True,  # מוריד רק שיר אחד גם אם הקישור הוא לפלייליסט
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'extractor_args': {'youtube': {'player_client': ['web']}},
            }

            # הגדרות ספציפיות לפי בחירת המשתמש
            if "MP3" in format_choice:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                ydl_opts['format'] = 'best[ext=mp4]/best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # חילוץ מידע והורדה
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # וידוא סיומת נכונה במידה ובוצעה המרה ל-MP3
                if "MP3" in format_choice and not filename.endswith(".mp3"):
                    potential_mp3 = filename.rsplit('.', 1)[0] + ".mp3"
                    if os.path.exists(potential_mp3):
                        filename = potential_mp3

            # יצירת כפתור הורדה למשתמש
            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    st.success(f"✅ '{info.get('title')}' מוכן!")
                    st.download_button(
                        label="📥 לחץ כאן לשמירה במכשיר",
                        data=f,
                        file_name=f"{info.get('title', 'download')}.{'mp3' if 'MP3' in format_choice else 'mp4'}",
                        mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                    )
                
                # ניקוי קבצים זמניים מהשרת
                os.remove(filename)
                if os.path.exists("cookies.txt"): os.remove("cookies.txt")

        except Exception as e:
            st.error(f"שגיאה: {str(e)}")
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")
