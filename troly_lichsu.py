# troly_lichsu.py
import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="Trợ lý Lịch sử Việt Nam", layout="centered")

if "audio_unlocked" not in st.session_state:
    st.session_state["audio_unlocked"] = False

st.title("📚 Trợ lý Lịch sử Việt Nam")
st.write("Nhấn **BẬT ÂM THANH** 1 lần (chỉ cần 1 lần trong phiên). Sau đó hỏi — ứng dụng sẽ tự đọc trên PC & Android. (iPhone vẫn cần bấm ▶).")

# Nút bật âm thanh: khi người dùng nhấn, server sẽ render lại và chèn JS để unlock audio
if st.button("🔊 BẬT ÂM THANH (1 lần)"):
    js = """
    <script>
    (function() {
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        if (ctx.state === 'suspended') {
          ctx.resume();
        }
        const o = ctx.createOscillator();
        const g = ctx.createGain();
        o.connect(g); g.connect(ctx.destination);
        g.gain.value = 0; // silent
        o.start(0);
        setTimeout(()=>{ o.stop(); }, 80);
      } catch(e) {
        console.log('unlock audio error', e);
      }
    })();
    </script>
    """
    components.html(js, height=0)           # chạy JS trên trình duyệt ngay trong lần tương tác
    st.session_state["audio_unlocked"] = True
    st.success("✅ Âm thanh đã được bật cho phiên này (PC & Android).")

# Dữ liệu mẫu
lich_su_data = {
    "trưng trắc": "Hai Bà Trưng khởi nghĩa chống quân Hán năm 40 sau Công Nguyên.",
    "ngô quyền": "Ngô Quyền đánh bại quân Nam Hán trên sông Bạch Đằng năm 938.",
    "lý thái tổ": "Năm 1010, Lý Thái Tổ dời đô về Thăng Long.",
    "trần hưng đạo": "Trần Hưng Đạo chỉ huy quân dân Đại Việt ba lần đánh bại quân Nguyên - Mông."
}

cau_hoi = st.text_input("❓ Nhập câu hỏi lịch sử:")

def tra_loi_lich_su(q):
    if not q: 
        return ""
    q_low = q.lower()
    for k, v in lich_su_data.items():
        if k in q_low:
            return v
    return "Xin lỗi, tôi chưa có thông tin về câu hỏi này."

if st.button("📖 Trả lời"):
    tra_loi = tra_loi_lich_su(cau_hoi)
    st.write("🔍", tra_loi)

    # tạo mp3 trong bộ nhớ
    mp3_fp = BytesIO()
    try:
        gTTS(text=tra_loi, lang="vi").write_to_fp(mp3_fp)
    except Exception as e:
        st.error("Lỗi khi tạo giọng nói: " + str(e))
        mp3_fp = None

    if mp3_fp:
        mp3_fp.seek(0)
        audio_bytes = mp3_fp.read()
        b64 = base64.b64encode(audio_bytes).decode()

        if st.session_state.get("audio_unlocked", False):
            # Dùng HTML audio với autoplay (phải đã unlock trước đó)
            html = f'<audio autoplay playsinline><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            components.html(html, height=80)
            st.info("🔊 Đang phát (tự động trên PC & Android).")
        else:
            # Hiển thị control (người dùng bấm Play) — cần cho iPhone và trường hợp chưa unlock
            st.audio(audio_bytes, format="audio/mp3")
            st.warning("⚠️ Nếu đang dùng iPhone hoặc chưa bấm 'BẬT ÂM THANH', hãy nhấn nút ▶ để nghe.")
