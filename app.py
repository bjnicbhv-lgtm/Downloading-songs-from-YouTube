import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Ultimate Downloader", page_icon="📥")
st.title("YouTube Downloader")

url = st.text_input("הדבק קישור כאן:")

if url and st.button("הורד"):
    with st.spinner("מבצע הורדה... נא להמתין"):
        try:
            # שימוש בעוגיות מה-Secrets אם קיימות
            cookie_path = None
            if "YT_COOKIES" in st.secrets:
                with open("cookies.txt", "w") as f:
                    f.write(st.secrets["YT_COOKIES"])
                cookie_path = "cookies.txt"

            ydl_opts = {
                # הגדרה הכי בטוחה: וידאו+סאונד משולב מראש ב-MP4
                'format': 'best[ext=mp4]/best',
                'cookiefile': cookie_path,
                'outtmpl': 'video_file.%(ext)s',
                # התחזות לדפדפן אמיתי כדי למנוע Signature solving failed
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'nocheckcertificate': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, "rb") as f:
                st.success("הקובץ מוכן!")
                st.download_button(
                    label="📥 לחץ כאן לשמירה",
                    data=f,
                    file_name=f"{info.get('title', 'video')}.mp4",
                    mime="video/mp4"
                )
            
            os.remove(filename)
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")

        except Exception as e:
            st.error(f"חלה שגיאה: {str(e)}")
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")
