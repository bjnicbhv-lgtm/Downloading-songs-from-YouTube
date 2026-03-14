import streamlit as st
import yt_dlp
import os

# הגדרות האתר
st.set_page_config(page_title="YouTube Music Downloader", page_icon="🎵")

st.title("YouTube Music Downloader")
st.write("הדבק קישור, בחר פורמט והורד את השיר ישירות.")

url = st.text_input("הכנס קישור כאן:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("בחר פורמט:", ["MP3", "MP4"], horizontal=True)

if url:
    if st.button("התחל הורדה"):
        with st.spinner("מעבד... נא להמתין."):
            try:
                # בדיקה וטעינה של עוגיות מהסודות
                if "YT_COOKIES" not in st.secrets:
                    st.error("שגיאה: חסר YT_COOKIES ב-Secrets של Streamlit.")
                    st.stop()
                
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])

                # הגדרות הורדה
                ydl_opts = {
                    'format': 'bestaudio/best' if format_choice == "MP3" else 'best',
                    'cookiefile': 'cookies.txt',
                    'outtmpl': 'downloaded_file.%(ext)s',
                    'noplaylist': True,
                }

                if format_choice == "MP3":
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if format_choice == "MP3" and not filename.endswith(".mp3"):
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                # כפתור הורדה
                if os.path.exists(filename):
                    with open(filename, "rb") as file:
                        st.success(f"✅ '{info.get('title')}' מוכן!")
                        st.download_button(
                            label="📥 לחץ כאן להורדה",
                            data=file,
                            file_name=f"{info.get('title')}.{'mp3' if format_choice == 'MP3' else 'mp4'}",
                            mime="audio/mpeg" if format_choice == "MP3" else "video/mp4"
                        )
                    os.remove(filename)
                
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")

            except Exception as e:
                st.error(f"חלה שגיאה: {str(e)}")