import streamlit as st
from gtts import gTTS
from io import BytesIO

# ======================
# Dữ liệu lịch sử
lich_su_data = {
    "Trưng Trắc": "Hai Bà Trưng khởi nghĩa chống quân Hán năm 40 sau Công Nguyên.",
    "Ngô Quyền": "Ngô Quyền đánh bại quân Nam Hán trên sông Bạch Đằng năm 938.",
    "Lý Thái Tổ": "Năm 1010, Lý Thái Tổ dời đô về Thăng Long.",
    "Trần Hưng Đạo": "Trần Hưng Đạo ba lần đánh bại quân Nguyên - Mông."
}

# ======================
# Hàm trả lời câu hỏi
def tra_loi_lich_su(cau_hoi):
    for tu_khoa, cau_tra_loi in lich_su_data.items():
        if tu_khoa.lower() in cau_hoi.lower():
            return cau_tra_loi
    return "Xin lỗi, tôi chưa có thông tin về câu hỏi này."

# ======================
# Giao diện Streamlit
st.title("📚 Trợ lý Lịch sử Việt Nam")
st.write("Nhập câu hỏi rồi bấm **Trả lời** để nghe kết quả.")

# Ô nhập câu hỏi
cau_hoi = st.text_input("❓ Câu hỏi lịch sử:")

# Nút bấm
if st.button("Trả lời"):
    tra_loi = tra_loi_lich_su(cau_hoi)
    st.success(tra_loi)

    # 🔊 Tạo giọng nói trực tiếp, không lưu file
    mp3_fp = BytesIO()
    gtts_obj = gTTS(text=tra_loi, lang="vi")
    gtts_obj.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Phát âm thanh
    st.audio(mp3_fp, format="audio/mp3", autoplay=True)
