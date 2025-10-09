import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

# ======================
# Dữ liệu lịch sử
lich_su_data = {
    "Trưng Trắc": "Hai Bà Trưng khởi nghĩa chống quân Hán năm 40 sau Công Nguyên.",
    "Ngô Quyền": "Ngô Quyền đánh bại quân Nam Hán trên sông Bạch Đằng năm 938.",
    "Lý Thái Tổ": "Năm 1010, Lý Thái Tổ dời đô về Thăng Long.",
    "Trần Hưng Đạo": "Trần Hưng Đạo ba lần đánh bại quân Nguyên - Mông."
}

def tra_loi_lich_su(cau_hoi):
    for tu_khoa, cau_tra_loi in lich_su_data.items():
        if tu_khoa.lower() in cau_hoi.lower():
            return cau_tra_loi
    return "Xin lỗi, tôi chưa có thông tin về câu hỏi này."

# ======================
# Giao diện Streamlit
st.title("📚 Trợ lý Lịch sử Việt Nam")
st.write("Nhập câu hỏi và bấm **Trả lời** để nghe kết quả (hoạt động tốt trên Android & iOS).")

# Ô nhập câu hỏi
cau_hoi = st.text_input("❓ Câu hỏi lịch sử:")

if st.button("Trả lời"):
    tra_loi = tra_loi_lich_su(cau_hoi)
    st.success(tra_loi)

    # 🔊 Tạo giọng nói tiếng Việt (không lưu file)
    mp3_fp = BytesIO()
    gtts_obj = gTTS(text=tra_loi, lang="vi")
    gtts_obj.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    b64 = base64.b64encode(mp3_fp.read()).decode()

    # Hiển thị âm thanh (iOS cần bấm Play)
    audio_html = f"""
    <audio controls playsinline>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    <p style="font-size:12px;color:gray">📱 Trên iPhone: hãy nhấn nút ▶ để nghe giọng đọc.</p>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
