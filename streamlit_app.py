import streamlit as st
from utils import load_data, add_book, borrow_book, return_book
from datetime import date

st.set_page_config(page_title="Perpustakaan IMM Magelang")

# Session State
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.username = ""
    st.session_state.is_admin = False

def login_page():
    st.title("Login Perpustakaan IMM Magelang")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "immmagelang" and password == "superadmin":
            st.session_state.login = True
            st.session_state.username = username
            st.session_state.is_admin = True
        else:
            st.error("Login gagal!")

    if st.button("Masuk sebagai Tamu"):
        st.session_state.login = True
        st.session_state.is_admin = False
        st.session_state.username = "Tamu"

def main_page():
    st.title(f"Selamat Datang, {st.session_state.username}")

    data = load_data()

    st.subheader("📚 Daftar Buku")
    st.dataframe(
        [
            {
                "No": book["id"],
                "No. Inventaris": book["inventory_number"],
                "Judul": book["title"],
                "Penulis": book["author"],
                "Tersedia": "✅" if book["available"] else "❌",
                "Peminjam": book["borrower"],
                "Tanggal Pinjam": book["borrow_date"]
            }
            for book in data["books"]
        ]
    )

    if st.session_state.is_admin:
        st.subheader("➕ Tambah Buku")
        inv = st.text_input("Nomor Inventaris")
        title = st.text_input("Judul Buku")
        author = st.text_input("Penulis")
        if st.button("Tambah Buku"):
            if inv and title and author:
                add_book(inv, title, author)
                st.success("Buku berhasil ditambahkan!")

        st.subheader("📤 Peminjaman Buku")
        book_id = st.number_input("ID Buku", step=1, min_value=1)
        borrower = st.text_input("Nama Peminjam")
        tanggal = st.date_input("Tanggal Pinjam", value=date.today())
        if st.button("Pinjam Buku"):
            borrow_book(book_id, borrower, str(tanggal))
            st.success("Buku dipinjamkan!")

        st.subheader("📥 Pengembalian Buku")
        return_id = st.number_input("ID Buku untuk dikembalikan", step=1, min_value=1, key="return")
        if st.button("Kembalikan Buku"):
            return_book(return_id)
            st.success("Buku telah dikembalikan.")

    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.username = ""
        st.session_state.is_admin = False
        st.rerun()

# App Execution
if not st.session_state.login:
    login_page()
else:
    main_page()
