import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Pro Downloader", page_icon="📥")

st.title("YouTube Downloader")

url = st.text_input("הדבק קישור מיוטיוב:")
format_choice = st.radio("בחר פורמט:", ["MP3", "MP4"], horizontal=True)

if url and st.button("הורד"):
    with st.spinner("מבצע הורדה..."):
        try:
            # בדיקת עוגיות
            if "YT_COOKIES" not in st.secrets:
                st.error("שגיאה: חסר YT_COOKIES ב-Secrets!")
                st.stop()
            
            with open("cookies.txt", "w") as f:
                f.write(st.secrets["YT_COOKIES"])

            # הגדרות הורדה בסיסיות למניעת שגיאות פורמט
            ydl_opts = {
                'cookiefile': 'cookies.txt',
                'outtmpl': 'file_download.%(ext)s',
            }

            if format_choice == "MP3":
                ydl_opts['format'] = 'bestaudio/best'
                # מנסה להשתמש ב-FFmpeg אבל לא קורס אם הוא חסר
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                # הורדת וידאו MP4 פשוט
                ydl_opts['format'] = 'best[ext=mp4]/best'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # מוצא את שם הקובץ שנוצר בפועל
                filename = ydl.prepare_filename(info)
                if format_choice == "MP3" and not filename.endswith(".mp3"):
                    potential_mp3 = filename.rsplit('.', 1)[0] + ".mp3"
                    if os.path.exists(potential_mp3):
                        filename = potential_mp3

            # שליחת הקובץ למשתמש
            with open(filename, "rb") as f:
                st.success("הקובץ מוכן!")
                st.download_button(
                    label="לחץ כאן לשמירה",
                    data=f,
                    file_name=f"{info.get('title', 'download')}.{'mp3' if format_choice == 'MP3' else 'mp4'}"
                )
            
            os.remove(filename)
        except Exception as e:
            st.error(f"שגיאה: {str(e)}")
        finally:
            if os.path.exists("cookies.txt"): os.remove("cookies.txt")
