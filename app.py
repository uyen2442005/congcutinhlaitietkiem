import streamlit as st
st.image("logo.jpg")
# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM CỦA BẢO CHÂU")
st.write("Nhập thông tin tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

st.divider()


# ==============================
# PHẦN NHẬP THÔNG TIN
# ==============================
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )


col3, col4 = st.columns(2)

with col3:
    ky_han = st.selectbox(
        "📅 Kỳ hạn",
        options=[
            1,
            3,
            6,
            9,
            12,
            18,
            24,
            36
        ],
        format_func=lambda x: f"{x} tháng"
    )

with col4:
    hinh_thuc = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )


st.divider()


# ==============================
# NÚT TÍNH TOÁN
# ==============================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat <= 0:
        st.error("Vui lòng nhập lãi suất lớn hơn 0.")
        st.stop()

    # ---------------------------------
    # TÍNH TỔNG TIỀN LÃI
    # ---------------------------------

    # Công thức lãi đơn:
    # Tiền lãi = Tiền gửi × Lãi suất năm × Số tháng / 12

    tong_tien_lai = (
        so_tien_gui
        * (lai_suat / 100)
        * (ky_han / 12)
    )

    tong_tien_nhan = so_tien_gui + tong_tien_lai


    # ==============================
    # TÍNH LÃI THEO HÌNH THỨC NHẬN
    # ==============================

    if hinh_thuc == "Cuối kỳ":

        so_ky = 1
        lai_dinh_ky = tong_tien_lai

    elif hinh_thuc == "Hàng tháng":

        so_ky = ky_han
        lai_dinh_ky = tong_tien_lai / so_ky

    else:  # Hàng quý

        so_ky = ky_han // 3

        if so_ky == 0:
            st.error(
                "Kỳ hạn phải từ 3 tháng trở lên để chọn nhận lãi hàng quý."
            )
            st.stop()

        lai_dinh_ky = tong_tien_lai / so_ky


    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================

    st.subheader("📊 KẾT QUẢ TÍNH TOÁN")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    with col3:
        st.metric(
            "💰 Tổng tiền nhận",
            format_money(tong_tien_nhan)
        )


    st.divider()


    # ==============================
    # THÔNG TIN CHI TIẾT
    # ==============================

    st.subheader("📋 Thông tin khoản tiền gửi")

    thong_tin = {
        "Số tiền gửi": format_money(so_tien_gui),
        "Kỳ hạn": f"{ky_han} tháng",
        "Lãi suất": f"{lai_suat:.2f}%/năm",
        "Hình thức nhận lãi": hinh_thuc,
        "Tiền lãi định kỳ": format_money(lai_dinh_ky),
        "Tổng tiền lãi": format_money(tong_tien_lai),
        "Tổng gốc + lãi": format_money(tong_tien_nhan)
    }

    for key, value in thong_tin.items():
        col1, col2 = st.columns([1, 1])

        with col1:
            st.write(f"**{key}**")

        with col2:
            st.write(value)


    # ==============================
    # BẢNG CHI TIẾT CÁC KỲ NHẬN LÃI
    # ==============================

    st.subheader("📅 Lịch nhận lãi")

    if hinh_thuc == "Cuối kỳ":

        data = [
            {
                "Kỳ nhận": "Cuối kỳ",
                "Tiền lãi nhận": format_money(tong_tien_lai),
                "Tổng tiền nhận": format_money(tong_tien_nhan)
            }
        ]

    else:

        data = []

        if hinh_thuc == "Hàng tháng":
            don_vi = "Tháng"
            so_ky_nhan = ky_han

        else:
            don_vi = "Quý"
            so_ky_nhan = ky_han // 3

        for i in range(1, so_ky_nhan + 1):

            data.append(
                {
                    "Kỳ nhận": f"{don_vi} {i}",
                    "Tiền lãi nhận": format_money(lai_dinh_ky),
                    "Tổng tiền nhận": format_money(
                        lai_dinh_ky * i
                    )
                }
            )

    st.table(data)


# ==============================
# GHI CHÚ
# ==============================
st.divider()

st.caption(
    "📌 Công thức sử dụng: Tiền lãi = Tiền gửi × Lãi suất năm × Kỳ hạn / 12. "
    "Kết quả mang tính chất tham khảo và chưa tính các khoản thuế/phí nếu có."
)
