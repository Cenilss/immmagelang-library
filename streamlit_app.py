import streamlit as st
import db
from auth import check_login
from datetime import date

st.set_page_config("Perpustakaan IMM Magelang", layout="wide")
db.init_db()

if "page" not in st.session_state:
    st.session_state.page = "home"


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.is_admin = False

def homepage():
    st.image("https://upload.wikimedia.org/wikipedia/id/3/32/Logo_IMM.svg", width=80)
    st.title("📚 Perpustakaan IMM Magelang")

    col1, col2 = st.columns(2)
    with col1:
        st.write("Silakan login sebagai admin bila Anda merupakan administrator")
        if st.button("🔐 Login Admin"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        st.write("Silakan masuk sebagai tamu apabila hanya ingin melihat-lihat buku yang tersedia.")
        if st.button("👤 Masuk sebagai Tamu"):
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.page = "dashboard"
            st.rerun()

def login_page():
    st.image("https://upload.wikimedia.org/wikipedia/id/3/32/Logo_IMM.svg", width=50)
    st.title("📚 Login Admin Perpustakaan IMM")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Login gagal. Periksa kembali username dan password.")


def show_books():
    st.subheader("📚 Daftar Buku")

    search = st.text_input("🔍 Cari buku...")
    books = db.load_books()

    # Filter: bisa cari dari semua kolom teks
    if search:
        search = search.lower()
        books = [
            b for b in books if
            search in b["inventory_number"].lower()
            or search in b["title"].lower()
            or search in b["author"].lower()
        ]

    # Urutkan default berdasarkan Nomor Inventaris
    books_sorted = sorted(books, key=lambda b: b["inventory_number"])

    df = [
        {
            "No. Inventaris": b["inventory_number"],
            "Judul": b["title"],
            "Penulis": b["author"],
            "Tersedia": "Ya" if b["available"] else "Tidak",
            "Peminjam": b["borrower"],
            "Tanggal Pinjam": b["borrow_date"]
        } for b in books_sorted
    ]

    st.dataframe(df, use_container_width=True)


def tambah_buku():
    st.subheader("➕ Tambah Buku")
    inv = st.text_input("Nomor Inventaris")
    title = st.text_input("Judul Buku")
    author = st.text_input("Penulis")
    if st.button("Simpan Buku"):
        if inv and title and author:
            try:
                db.add_book(inv, title, author)
                st.success("✅ Buku ditambahkan!")
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {str(e)}")


def pinjam_buku():
    st.subheader("📤 Peminjaman Buku")
    inv_number = st.text_input("Nomor Inventaris Buku")
    borrower = st.text_input("Nama Peminjam")
    tgl = st.date_input("Tanggal Pinjam", value=date.today())

    if st.button("Pinjam"):
        book = db.find_by_inventory(inv_number)
        if book and book["available"]:
            db.borrow_book(book["id"], borrower, str(tgl))
            st.success(f"Buku '{book['title']}' berhasil dipinjam.")
            st.rerun()
        else:
            st.error("❌ Buku tidak ditemukan atau sedang dipinjam.")

def kembali_buku():
    st.subheader("📥 Pengembalian Buku")
    inv_number = st.text_input("Nomor Inventaris Buku yang Dikembalikan")

    if st.button("Kembalikan"):
        book = db.find_by_inventory(inv_number)
        if book and not book["available"]:
            db.return_book(book["id"])
            st.success(f"Buku '{book['title']}' telah dikembalikan.")
            st.rerun()
        else:
            st.error("❌ Buku tidak ditemukan atau sudah tersedia.")

def hapus_buku():
    st.subheader("🗑️ Hapus Buku")
    inv_number = st.text_input("Nomor Inventaris Buku yang Akan Dihapus")

    if st.button("Hapus"):
        book = db.find_by_inventory(inv_number)
        if book:
            db.delete_book(book["id"])
            st.success(f"Buku '{book['title']}' berhasil dihapus.")
            st.rerun()
        else:
            st.error("❌ Buku tidak ditemukan.")

def dashboard():
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/id/3/32/Logo_IMM.svg", width=120)
    st.sidebar.title("📖 Menu")

    # Susun menu secara dinamis
    menu_options = ["Lihat Buku"]

    if st.session_state.is_admin:
        menu_options += [
            "Tambah Buku",
            "Pinjam Buku",
            "Kembalikan Buku",
            "Hapus Buku"
        ]

    # Tampilkan menu
    menu = st.sidebar.radio("Navigasi", menu_options)

    st.sidebar.markdown("---")
    st.sidebar.caption("Login sebagai: **{}**".format("Admin" if st.session_state.is_admin else "Tamu"))

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.page = "home"  # jika pakai sistem page
        st.rerun()

    st.title("Perpustakaan IMM Magelang")

    # Aksi berdasarkan menu
    if menu == "Lihat Buku":
        show_books()
    elif menu == "Tambah Buku":
        tambah_buku()
    elif menu == "Pinjam Buku":
        pinjam_buku()
    elif menu == "Kembalikan Buku":
        kembali_buku()
    elif menu == "Hapus Buku":
        hapus_buku()

# Routing berdasarkan halaman
if st.session_state.page == "home":
    homepage()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard" and st.session_state.logged_in:
    dashboard()
else:
    # fallback jika akses dashboard tanpa login
    st.session_state.page = "home"
    st.rerun()
