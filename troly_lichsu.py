import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Trợ lý Lịch sử Việt Nam", layout="centered")

# ====== trạng thái ======
if "audio_unlocked" not in st.session_state:
    st.session_state["audio_unlocked"] = False

st.title("📚 Trợ lý Lịch sử Việt Nam")
st.write("👉 Nhấn **BẬT ÂM THANH** (chỉ cần 1 lần cho phiên). Sau đó nhập câu hỏi và bấm **Trả lời**.")
st.write("📱 LƯU Ý: iPhone/Safari thường yêu cầu bạn bấm nút ▶ để nghe (đó là chính sách trình duyệt).")

# ====== nút bật âm thanh (user gesture) ======
if st.button("🔊 BẬT ÂM THANH (1 lần)"):
    # JS này resume AudioContext và phát 1 âm thanh rất ngắn (silent) để unlock
    js_unlock = """
    <script>
      (function(){
        try {
          const ctx = new (window.AudioContext || window.webkitAudioContext)();
          if (ctx.state === 'suspended') { ctx.resume(); }
          const o = ctx.createOscillator();
          const g = ctx.createGain();
          o.connect(g); g.connect(ctx.destination);
          g.gain.value = 0;
          o.start(0);
          setTimeout(()=>{ o.stop(); }, 60);
        } catch(e) {
          console.log('unlock audio error', e);
        }
      })();
    </script>
    """
    components.html(js_unlock, height=0)
    st.session_state["audio_unlocked"] = True
    st.success("✅ Âm thanh đã được bật (PC & Android).")

# ====== dữ liệu lịch sử (ví dụ) ======
lich_su_data = {
    "trưng trắc": "Hai Bà Trưng khởi nghĩa chống quân Hán năm 40 sau Công Nguyên.",
    "ngô quyền": "Ngô Quyền đánh bại quân Nam Hán trên sông Bạch Đằng năm 938.",
    "lý thái tổ": "Năm 1010, Lý Thái Tổ dời đô về Thăng Long.",
    "trần hưng đạo": "Trần Hưng Đạo ba lần đánh bại quân Nguyên - Mông."
}

def tra_loi_lich_su(q):
    if not q:
        return ""
    ql = q.lower()
    for k, v in lich_su_data.items():
        if k in ql:
            return v
    return "Xin lỗi, tôi chưa có thông tin về câu hỏi này."

# ====== UI ======
cau_hoi = st.text_input("❓ Câu hỏi lịch sử:")

if st.button("📖 Trả lời"):
    tra_loi = tra_loi_lich_su(cau_hoi)
    if not tra_loi:
        st.warning("Vui lòng nhập câu hỏi.")
    else:
        st.success(tra_loi)

        # ----- tạo mp3 trong bộ nhớ (BytesIO) -----
        try:
            mp3_fp = BytesIO()
            gTTS(text=tra_loi, lang="vi").write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            audio_bytes = mp3_fp.read()
        except Exception as e:
            st.error(f"Lỗi khi tạo giọng nói: {e}")
            audio_bytes = None

        if audio_bytes:
            # chuyển sang base64 để nhúng <audio> qua components.html
            b64 = base64.b64encode(audio_bytes).decode()

            # html + js: nếu là iOS -> show controls (người dùng bấm Play)
            #             nếu không phải iOS và đã unlock -> autoplay
            # Note: autoplay vẫn có thể bị chặn nếu chưa unlock.
            unlocked = "true" if st.session_state.get("audio_unlocked", False) else "false"

            html = f"""
            <div id="audio_wrapper"></div>
            <script>
            (function(){{
                const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
                const unlocked = {unlocked};
                const container = document.getElementById("audio_wrapper");
                const audio = document.createElement('audio');
                audio.playsInline = true;
                audio.setAttribute('playsinline','');
                audio.style.width = '100%';
                audio.src = "data:audio/mp3;base64,{b64}";
                audio.controls = true;
                container.appendChild(audio);
                if (!isIOS && unlocked === true || unlocked === 'true') {{
                    // Try autoplay on non-iOS when unlocked
                    audio.autoplay = true;
                    audio.play().catch(function(err){{ console.log('Autoplay failed:', err); }});
                }}
            }})();
            </script>
            """
            components.html(html, height=120)

            # Thông báo phù hợp
            if st.session_state.get("audio_unlocked", False):
                st.info("🔊 Nếu thiết bị hỗ trợ, âm thanh đang phát tự động (PC & Android).")
            else:
                st.warning("⚠️ Nếu bạn dùng iPhone hoặc chưa bật âm thanh, hãy nhấn nút ▶ để nghe.")
