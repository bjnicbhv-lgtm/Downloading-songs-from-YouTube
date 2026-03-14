import streamlit as st
import yt_dlp
import os

# הגדרות עיצוב בסיסיות
st.set_page_config(page_title="YouTube Music & Video Downloader", page_icon="🎵")

st.title("YouTube Downloader")
st.write("הדבק קישור, בחר פורמט ולחץ על כפתור ההורדה.")

# קלט מהמשתמש
url = st.text_input("הכנס קישור כאן:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("בחר פורמט הורדה:", ["MP3 (אודיו בלבד)", "MP4 (וידאו)"], horizontal=True)

if url:
    if st.button("התחל הורדה"):
        with st.spinner("מעבד את הבקשה... המתן לסיום"):
            try:
                # טעינת עוגיות מה-Secrets של Streamlit
                if "YT_COOKIES" not in st.secrets:
                    st.error("שגיאה: חסר YT_COOKIES ב-Secrets של האתר.")
                    st.stop()
                
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])

                # הגדרות הורדה חכמות לעקיפת חסימות
                ydl_opts = {
                    'cookiefile': 'cookies.txt',
                    'outtmpl': 'downloaded_file.%(ext)s',
                    'nocheckcertificate': True,
                    'ignoreerrors': False,
                    'logtostderr': False,
                    'quiet': True,
                    'no_warnings': True,
                    # הגדרה קריטית לעקיפת בעיות Signature (Signature Solving)
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
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
                    # הורדת MP4 כולל וידאו וסאונד
                    ydl_opts['format'] = 'best[ext=mp4]/best'

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # שליפת מידע והורדה
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # תיקון שם הקובץ במידה ועבר המרה ל-MP3
                    if "MP3" in format_choice and not filename.endswith(".mp3"):
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                # יצירת כפתור הורדה למשתמש
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        st.success(f"✅ '{info.get('title', 'הקובץ')}' מוכן להורדה!")
                        st.download_button(
                            label="📥 לחץ כאן להורדה למכשיר",
                            data=file,
                            file_name=f"{info.get('title', 'downloaded_file')}.{'mp3' if 'MP3' in format_choice else 'mp4'}",
                            mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                        )
                    
                    # מחיקת הקובץ מהשרת לאחר שהועבר למשתמש
                    os.remove(filename)
                
                # מחיקת קובץ העוגיות הזמני
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")

            except Exception as e:
                st.error(f"חלה שגיאה בתהליך: {str(e)}")
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")
