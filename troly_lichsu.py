import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

# ======================
# GIAO DIỆN ỨNG DỤNG
st.set_page_config(page_title="Trợ lý Lịch sử Việt Nam", layout="centered")

st.title("📚 Trợ lý Lịch sử Việt Nam")
st.write("Ứng dụng giúp trả lời các câu hỏi về lịch sử Việt Nam bằng giọng nói!")

# ======================
# BƯỚC 1: BẬT ÂM THANH
if "audio_unlocked" not in st.session_state:
    st.session_state["audio_unlocked"] = False

st.write("👉 **Nhấn nút bên dưới 1 lần để bật âm thanh (trước khi hỏi).**")

if st.button("🔊 Bắt đầu (Cho phép âm thanh)"):
    # JavaScript giúp trình duyệt cho phép phát âm thanh
    js_code = """
    <script>
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        if (ctx.state === 'suspended') {
          ctx.resume().then(() => console.log('Audio unlocked'));
        }
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        gain.gain.value = 0; // im lặng
        osc.start();
        setTimeout(() => osc.stop(), 100);
      } catch (e) {
        console.log('Unlock audio error', e);
      }
    </script>
    """
    st.components.v1.html(js_code, height=0)
    st.session_state["audio_unlocked"] = True
    st.success("✅ Âm thanh đã được bật! Bây giờ bạn có thể hỏi và ứng dụng sẽ tự đọc trả lời.")

# ======================
# DỮ LIỆU LỊCH SỬ (mẫu)
lich_su_data = {
    "Trưng Trắc": "Hai Bà Trưng khởi nghĩa chống quân Hán năm 40 sau Công Nguyên.",
    "Ngô Quyền": "Ngô Quyền đánh bại quân Nam Hán trên sông Bạch Đằng năm 938.",
    "Lý Thái Tổ": "Năm 1010, Lý Thái Tổ dời đô về Thăng Long, mở ra thời kỳ phát triển rực rỡ.",
    "Trần Hưng Đạo": "Trần Hưng Đạo chỉ huy quân dân Đại Việt ba lần đánh bại quân Nguyên - Mông.",
}

# ======================
# BƯỚC 2: NHẬP CÂU HỎI
cau_hoi = st.text_input("❓ Nhập câu hỏi lịch sử của bạn:")

def tra_loi_lich_su(cau_hoi):
    for nhan_vat, noi_dung in lich_su_data.items():
        if nhan_vat.lower() in cau_hoi.lower():
            return noi_dung
    return "Xin lỗi, tôi chưa có thông tin về câu hỏi này."

# ======================
# BƯỚC 3: TRẢ LỜI + TẠO GIỌNG NÓI
if st.button("📖 Trả lời"):
    tra_loi = tra_loi_lich_su(cau_hoi)
    st.success(tra_loi)

    # Tạo giọng nói (không lưu file)
    mp3_fp = BytesIO()
    gtts_obj = gTTS(text=tra_loi, lang="vi")
    gtts_obj.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    b64_audio = base64.b64encode(mp3_fp.read()).decode()

    # Nếu âm thanh đã được mở (Android/PC): phát tự động
    if st.session_state.get("audio_unlocked", False):
        st.markdown(f"""
        <audio autoplay playsinline>
          <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
        st.info("🔊 Đang phát giọng nói (tự động trên PC & Android).")
    else:
        st.markdown(f"""
        <audio controls playsinline>
          <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
        st.warning("⚠️ Trên iPhone, hãy bấm nút ▶ để nghe âm thanh.")
