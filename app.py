import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="file:///C:/Users/%D7%99%D7%9C%D7%93%D7%99%D7%9D/Downloads/00551.png")
st.title("YouTube Downloader")

url = st.text_input("הדבק כאן את הקישור מיוטיוב:", placeholder="https://www.youtube.com/watch?v=...")
format_choice = st.radio("בחר פורמט:", ["MP3 (שיר)", "MP4 (סרטון)"], horizontal=True)

if url and st.button("התחל הורדה"):
    with st.spinner("מעבד... נא להמתין"):
        try:
            # הגדרת עוגיות מה-Secrets
            cookie_path = None
            if "YT_COOKIES" in st.secrets:
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])
                cookie_path = "cookies.txt"

            ydl_opts = {
                'cookiefile': cookie_path,
                'outtmpl': 'file_download.%(ext)s',
                'nocheckcertificate': True,
                'noplaylist': True,
                'quiet': True,
                # הגדרה קריטית: שימוש בלקוח iOS שעוקף את ה-Signature solving
                'client_name': 'ios',
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios'],
                    }
                },
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            }

            if "MP3" in format_choice:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts['format'] = 'best[ext=mp4]/best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # תיקון סיומת ל-MP3
                if "MP3" in format_choice and not filename.endswith(".mp3"):
                    actual_filename = filename.rsplit('.', 1)[0] + ".mp3"
                    if os.path.exists(actual_filename):
                        filename = actual_filename

            with open(filename, "rb") as f:
                st.success(f"✅ הקובץ '{info.get('title')}' מוכן!")
                st.download_button(
                    label="📥 לחץ כאן לשמירה",
                    data=f,
                    file_name=f"{info.get('title', 'download')}.{'mp3' if 'MP3' in format_choice else 'mp4'}",
                    mime="audio/mpeg" if "MP3" in format_choice else "video/mp4"
                )
            
            # ניקוי
            os.remove(filename)
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")

        except Exception as e:
            st.error(f"שגיאה: {str(e)}")
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")
