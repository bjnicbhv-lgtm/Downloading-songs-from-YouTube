import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="📥")
st.title("YouTube Downloader")

url = st.text_input("הדבק כאן את הקישור מיוטיוב:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("בחר פורמט:", ["MP3 (שיר)", "MP4 (סרטון)"], horizontal=True)

if url and st.button("התחל הורדה"):
    with st.spinner("מוריד... זה עשוי לקחת דקה"):
        try:
            cookie_path = None
            if "YT_COOKIES" in st.secrets:
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])
                cookie_path = "cookies.txt"

            ydl_opts = {
                'cookiefile': cookie_path,
                'outtmpl': 'download_file.%(ext)s',
                'nocheckcertificate': True,
                'noplaylist': True,
                'quiet': True,
                # שימוש בלקוח אינטרנט רגיל בלבד כדי למנוע דרישת PO Token של אנדרואיד
                'extractor_args': {'youtube': {'player_client': ['web']}},
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }

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
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if "MP3" in format_choice and not filename.endswith(".mp3"):
                    potential = filename.rsplit('.', 1)[0] + ".mp3"
                    if os.path.exists(potential):
                        filename = potential

            with open(filename, "rb") as f:
                st.success("✅ הצלחנו!")
                st.download_button(
                    label="📥 שמור במכשיר",
                    data=f,
                    file_name=f"{info.get('title', 'download')}.{'mp3' if 'MP3' in format_choice else 'mp4'}",
                    mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                )
            
            os.remove(filename)
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")

        except Exception as e:
            st.error(f"שגיאה: {str(e)}")
            if "403" in str(e):
                st.warning("נראה שיוטיוב חסמה את הגישה. נסה להוציא עוגיות (Cookies) חדשות מהדפדפן ולעדכן ב-Secrets.")
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")
