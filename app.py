import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Music & Video Downloader", page_icon="🎵")

st.title("YouTube Downloader")
st.write("הדבק קישור, בחר פורמט והורד בקלות.")

url = st.text_input("הכנס קישור כאן:", placeholder="https://www.youtube.com/watch?v=...")
# הוספת הבחירה מחדש
format_choice = st.radio("בחר פורמט הורדה:", ["MP3 (רק אודיו)", "MP4 (וידאו)"], horizontal=True)

if url:
    if st.button("התחל הורדה"):
        with st.spinner("מעבד... נא להמתין."):
            try:
                if "YT_COOKIES" not in st.secrets:
                    st.error("חסר YT_COOKIES ב-Secrets!")
                    st.stop()
                
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])

                # הגדרות הורדה גמישות למניעת השגיאה
                if "MP3" in format_choice:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'cookiefile': 'cookies.txt',
                        'outtmpl': 'downloaded_file.%(ext)s',
                    }
                else:
                    # הגדרות ל-MP4
                    ydl_opts = {
                        'format': 'best[ext=mp4]/best', # מבטיח הורדת MP4 שכולל גם סאונד וגם וידאו
                        'cookiefile': 'cookies.txt',
                        'outtmpl': 'downloaded_file.%(ext)s',
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # תיקון סיומת ל-MP3 אם עבר עיבוד
                    if "MP3" in format_choice and not filename.endswith(".mp3"):
                        filename = filename.rsplit('.', 1)[0] + ".mp3"

                with open(filename, "rb") as file:
                    st.success(f"✅ '{info.get('title')}' מוכן!")
                    st.download_button(
                        label="📥 לחץ כאן להורדה",
                        data=file,
                        file_name=f"{info.get('title')}.{'mp3' if 'MP3' in format_choice else 'mp4'}",
                        mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                    )
                
                os.remove(filename)
                if os.path.exists("cookies.txt"): os.remove("cookies.txt")

            except Exception as e:
                st.error(f"שגיאה: {str(e)}")
                if os.path.exists("cookies.txt"): os.remove("cookies.txt")
