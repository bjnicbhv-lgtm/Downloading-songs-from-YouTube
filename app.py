import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music Downloader", page_icon="🎵")

st.title("YouTube Music Downloader")
st.write("הדבק קישור למטה ולחץ על כפתור ההורדה.")

url = st.text_input("הכנס קישור כאן:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("הורד עכשיו"):
        with st.spinner("מעבד את השיר..."):
            try:
                # טעינת עוגיות מה-Secrets
                if "YT_COOKIES" not in st.secrets:
                    st.error("חסר YT_COOKIES ב-Secrets!")
                    st.stop()
                
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])

                # הגדרות הורדה הכי בטוחות שיש (מונע את שגיאת הפורמט)
                ydl_opts = {
                    'format': 'bestaudio/best', # לוקח את האודיו הכי טוב שזמין בלי להסתבך
                    'cookiefile': 'cookies.txt',
                    'outtmpl': 'song_file.%(ext)s',
                    'noplaylist': True,
                    'quiet': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    actual_filename = ydl.prepare_filename(info)

                # כפתור הורדה למשתמש
                with open(actual_filename, "rb") as file:
                    st.success(f"✅ השיר '{info['title']}' מוכן!")
                    st.download_button(
                        label="📥 לחץ כאן לשמירת השיר",
                        data=file,
                        file_name=f"{info['title']}.{actual_filename.split('.')[-1]}",
                        mime="audio/mpeg"
                    )
                
                # ניקוי
                os.remove(actual_filename)
                if os.path.exists("cookies.txt"): os.remove("cookies.txt")

            except Exception as e:
                st.error(f"חלה שגיאה: {e}")
