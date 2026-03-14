import streamlit as st
import yt_dlp
import os

# הגדרת כותרת האתר
st.set_page_config(page_title="Music Downloader", page_icon="🎵")

st.title("Downloading songs from YouTube with filtering")
st.write("הדבק קישור מיוטיוב, המתן לעיבוד והורד את השיר ישירות למכשיר שלך.")

# תיבת קלט
url = st.text_input("הכנס קישור כאן:")
format_choice = st.radio("בחר פורמט:", ["MP3", "MP4"], horizontal=True)

if url:
    if st.button("התחל עיבוד"):
        with st.spinner("מוריד ומעבד... זה לוקח כדקה."):
            try:
                # טעינת עוגיות מה-Secrets של Streamlit
                cookies_content = st.secrets["YT_COOKIES"]
                with open("cookies.txt", "w") as f:
                    f.write(cookies_content)

                # הגדרות ההורדה
                ydl_opts = {
                    'format': 'bestaudio/best' if format_choice == "MP3" else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }] if format_choice == "MP3" else [],
                    'outtmpl': 'downloaded_file.%(ext)s',
                    'cookiefile': 'cookies.txt',
                    'writethumbnail': True,
                    'embedmetadata': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    actual_filename = ydl.prepare_filename(info)
                    
                    # תיקון סיומת אם בחרנו MP3
                    if format_choice == "MP3":
                        actual_filename = actual_filename.rsplit('.', 1)[0] + ".mp3"

                # הצגת כפתור הורדה
                with open(actual_filename, "rb") as file:
                    st.success(f"השיר '{info['title']}' מוכן להורדה!")
                    st.download_button(
                        label="🎵 לחץ כאן להורדת הקובץ",
                        data=file,
                        file_name=f"{info['title']}.{'mp3' if format_choice == 'MP3' else 'mp4'}",
                        mime="audio/mpeg" if format_choice == "MP3" else "video/mp4"
                    )
                
                # ניקוי קבצים זמניים
                os.remove(actual_filename)
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")

            except Exception as e:
                st.error(f"שגיאה: {e}")
