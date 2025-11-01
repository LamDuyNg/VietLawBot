import os
import streamlit as st
import requests
import time
import threading

# phần api_url sẽ cần thay đổi mỗi khi chạy backend trên kaggle
def get_bot_response(message):
    try:
        api_url = "https://ee79be5af18d.ngrok-free.app/chat" # Thay đổi URL chỗ này, chỉ thay phần trước /chat
        response = requests.post(api_url, json={"message": message}, timeout=180)
        if response.status_code == 200:
            return response.json().get("answer", "⚠️ Không có phản hồi từ hệ thống.")
        else:
            return f"⚠️ Lỗi từ API: {response.status_code}"
    except Exception as e:
        return f"⚠️ Lỗi khi kết nối API: {str(e)}"
    
st.set_page_config(page_title="Chatbot Án lệ", layout="wide")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "history_titles" not in st.session_state:
    st.session_state.history_titles = []

# --- Sidebar ---
with st.sidebar:
    logo_path = "Logo-DH-Ton-Duc-Thang-TDT.webp"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
    else:
        st.sidebar.warning("⚠️ Không tìm thấy logo. Kiểm tra lại đường dẫn hoặc tên file.")

    st.title("Lịch sử Chat")

    if st.button("Tạo mới cuộc trò chuyện"):
        if st.session_state.messages:
            st.session_state.history.append(st.session_state.messages)
            st.session_state.history_titles.append(f"Cuộc trò chuyện {len(st.session_state.history)+1}")
        st.session_state.messages = []

    for idx, chat in enumerate(st.session_state.history):
        with st.expander(f"{st.session_state.history_titles[idx]}"):
            col1, col2 = st.columns([10, 1])
            with col2:
                menu = st.selectbox("⋯", ["", "Đổi tên", "Xóa"], key=f"menu_{idx}")
                if menu == "Đổi tên":
                    new_title = st.text_input("Nhập tên mới:", key=f"rename_{idx}")
                    if new_title:
                        st.session_state.history_titles[idx] = new_title
                elif menu == "Xóa":
                    st.session_state.history.pop(idx)
                    st.session_state.history_titles.pop(idx)
                    st.rerun()
            with col1:
                for msg in chat:
                    role = "🧑‍💻" if msg["role"] == "user" else "🤖"
                    st.markdown(f"{role}: {msg['content']}")

# --- Main Area ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2 style="color: #2c3e50;">Hệ thống hỗ trợ giải thích án lệ</h2>
    </div>
""", unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <h1 style="font-size: 54px; color: #444;">
            👋 Chào bạn, hệ thống sẽ giúp phân tích tình huống pháp lý mà bạn thắc mắc
        </h1>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="
            max-width: 60%;
            margin-left: auto;
            margin-right: 10px;
            padding: 0.5rem;
            background-color: #cceeff;
            color: #000000;
            border-radius: 10px;
            text-align: left;">
            <strong>You:</strong> {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            max-width: 60%;
            margin-right: auto;
            margin-left: 10px;
            padding: 0.5rem;
            background-color: #000000;
            color: #ffffff;
            border-radius: 10px;
            text-align: left;">
            <strong>System:</strong> {msg['content']}
        </div>
        """, unsafe_allow_html=True)


# --- Input box cố định dưới ---
st.markdown("""
    <div style="
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        z-index: 9999;
        background: white;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(0,0,0,0.1);
    ">
""", unsafe_allow_html=True)

user_input = st.chat_input("Nhập tình huống và câu hỏi của bạn tại đây...")

st.markdown("</div>", unsafe_allow_html=True)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Placeholder hiển thị loading
    placeholder = st.empty()
    start_time = time.time()
    result_container = {"reply": None}

    # Hàm gọi API chạy trong thread riêng
    def fetch_api():
        result_container["reply"] = get_bot_response(user_input)

    thread = threading.Thread(target=fetch_api)
    thread.start()

    # Update UI liên tục trong khi chờ API
    while thread.is_alive():
        elapsed = time.time() - start_time
        placeholder.markdown(f"🤖 Đang sinh câu trả lời... ⏱ {elapsed:.1f} giây")
        time.sleep(0.3)  # update mỗi 0.3s

    # Sau khi thread xong, lấy kết quả
    thread.join()
    bot_reply = result_container["reply"]

    placeholder.empty()
    total_elapsed = time.time() - start_time
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"{bot_reply}\n\n⏱Thời gian sinh: {total_elapsed:.2f} giây"
    })
    st.rerun()

# --- CSS bổ sung ---
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #23272b;
    padding-top: 0 !important;
}
.stSelectbox > div[data-baseweb="select"] {
    margin-top: -40px;
}
</style>
""", unsafe_allow_html=True)
# Người thuê nhà không trả tiền thuê trong 3 tháng thì chủ nhà có quyền đơn phương chấm dứt hợp đồng không?
