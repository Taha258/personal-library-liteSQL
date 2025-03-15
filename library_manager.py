# library_manager.py

import streamlit as st
import sqlite3
import pandas as pd
import os

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Database connection function
def get_db_connection():
    try:
        conn = sqlite3.connect("personal_library.db")
        return conn
    except sqlite3.Error as e:
        st.error(f"❌ Error connecting to SQLite: {e}")
        return None

# Initialize database and table
def init_db():
    conn = get_db_connection()
    if conn is None:
        st.error("Database connection failed. Cannot initialize database.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                genre TEXT,
                read_status INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        st.write("✅ Database initialized successfully")
    except sqlite3.Error as e:
        st.error(f"❌ Error during database initialization: {e}")
    finally:
        cursor.close()
        conn.close()

# Add book to database
def add_book(title, author, year, genre, read_status):
    conn = get_db_connection()
    if conn:
        try:
            with conn:  # Auto-commit aur close
                cursor = conn.cursor()
                query = "INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)"
                values = (title, author, year, genre, int(read_status))
                cursor.execute(query, values)
                # Debugging: Check rows affected aur total count
                st.write(f"✅ Added book: {title}, Rows affected: {cursor.rowcount}")
                cursor.execute("SELECT COUNT(*) FROM books")
                total_books = cursor.fetchone()[0]
                st.write(f"📚 Total books in database: {total_books}")
            return True
        except sqlite3.Error as e:
            st.error(f"❌ Error adding book: {e}")
            return False
    return False

# Remove book from database
def remove_book(title):
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                query = "DELETE FROM books WHERE title = ?"
                cursor.execute(query, (title,))
                st.write(f"✅ Removed book: {title}")
            return True
        except sqlite3.Error as e:
            st.error(f"❌ Error removing book: {e}")
            return False
    return False

# Search books
def search_books(search_by, value):
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                if search_by == "Title":
                    query = "SELECT * FROM books WHERE title LIKE ?"
                else:
                    query = "SELECT * FROM books WHERE author LIKE ?"
                cursor.execute(query, (f"%{value}%",))
                results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            st.error(f"❌ Error searching books: {e}")
            return []
    return []

# Get all books
def get_all_books():
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM books")
                results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            st.error(f"❌ Error fetching books: {e}")
            return []
    return []

# Get statistics
def get_statistics():
    conn = get_db_connection()
    if conn:
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM books")
                total = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
                read = cursor.fetchone()[0]
            return total, read
        except sqlite3.Error as e:
            st.error(f"❌ Error fetching statistics: {e}")
            return 0, 0
    return 0, 0

# Function to add background image
def add_bg_from_local(image_file):
    if os.path.exists(image_file):
        try:
            st.write(f"Background image {image_file} loaded successfully")
        except Exception as e:
            st.warning(f"Could not load background image: {e}")
            st.markdown(
                """
                <style>
                .stApp {
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                }
                </style>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning(f"Background image '{image_file}' not found. Using default background.")
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# Streamlit UI
def main():
    # Database ko sirf ek baar initialize karo
    if 'db_initialized' not in st.session_state:
        with st.spinner("Initializing database..."):
            init_db()
        st.session_state.db_initialized = True

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background: rgba(255, 245, 230, 0.85);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #fffaf0;
            font-family: 'Arial', sans-serif;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        h2 {
            color: #f5e8c7;
            font-family: 'Arial', sans-serif;
        }
        .css-1d391kg {
            background-color: rgba(139, 69, 19, 0.9);
            border-right: 2px solid #d2a679;
        }
        .css-1v3fvcr p {
            color: #fffaf0;
            font-weight: bold;
        }
        .stRadio > label {
            color: #fffaf0;
            padding: 0.5rem;
            border-radius: 5px;
            margin: 0.2rem 0;
            background: rgba(210, 166, 121, 0.2);
        }
        .stRadio > label:hover {
            background: rgba(210, 166, 121, 0.4);
        }
        .stButton>button {
            background: linear-gradient(45deg, #d2a679, #f4c430);
            color: #1a1a2e;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 1.5rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(45deg, #f4c430, #d2a679);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(210, 166, 121, 0.4);
        }
        .stTextInput>div>input {
            background-color: rgba(255, 250, 240, 0.9);
            border: 2px solid #d2a679;
            border-radius: 10px;
            padding: 0.5rem;
            color: #1a1a2e;
        }
        .stDataFrame {
            border: 2px solid #d2a679;
            border-radius: 10px;
            background-color: rgba(255, 245, 230, 0.95);
        }
        .stMetric {
            background-color: rgba(139, 69, 19, 0.9);
            border: 2px solid #d2a679;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            color: #fffaf0;
        }
        .stMetric > div > div > div > div {
            color: #fffaf0;
        }
        .stMetric > div > div > div > div > div {
            color: #f5e8c7;
        }
        .stCheckbox>label {
            color: #fffaf0;
        }
        p, div {
            color: #fffaf0;
            font-family: 'Arial', sans-serif;
        }
        .stSuccess {
            background-color: rgba(144, 238, 144, 0.2);
            border: 1px solid #98fb98;
            border-radius: 5px;
            color: #fffaf0;
        }
        .stError {
            background-color: rgba(255, 182, 193, 0.2);
            border: 1px solid #ffb6c1;
            border-radius: 5px;
            color: #fffaf0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📚 Personal Library Manager")

    st.sidebar.header("Navigation")
    menu_options = ["Add Book", "Remove Book", "Search Books", "View Library", "Statistics"]
    choice = st.sidebar.radio("Select an option", menu_options, format_func=lambda x: f"✨ {x}")

    if choice == "Add Book":
        st.subheader("Add a New Book 📖")
        with st.form(key='add_form', clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title", placeholder="Enter book title")
                year_input = st.text_input("Publication Year", placeholder="Enter year (1900-2025)")
            with col2:
                author = st.text_input("Author", placeholder="Enter author name")
                genre = st.text_input("Genre", placeholder="Enter genre")
            read_status = st.checkbox("Mark as Read?")
            submit = st.form_submit_button("Add Book")
            
            if submit:
                try:
                    year = int(year_input)
                    if 1900 <= year <= 2025:
                        if title and author:
                            if add_book(title, author, year, genre, read_status):
                                st.success("Book added successfully! 🎉")
                            else:
                                st.error("Error adding book 😞")
                        else:
                            st.warning("Please fill in Title and Author fields")
                    else:
                        st.warning("Publication Year must be between 1900 and 2025")
                except ValueError:
                    st.warning("Please enter a valid Publication Year (e.g., 2021)")

    elif choice == "Remove Book":
        st.subheader("Remove a Book 🗑️")
        title = st.text_input("Enter book title to remove", placeholder="Book title")
        if st.button("Remove"):
            if title:
                if remove_book(title):
                    st.success("Book removed successfully! ✅")
                else:
                    st.error("Error removing book or book not found 😞")
            else:
                st.warning("Please enter a title")

    elif choice == "Search Books":
        st.subheader("Search Books 🔍")
        col1, col2 = st.columns([1, 2])
        with col1:
            search_by = st.radio("Search by", ["Title", "Author"])
        with col2:
            search_value = st.text_input(f"Enter {search_by}", placeholder=f"Search by {search_by.lower()}")
        if st.button("Search"):
            results = search_books(search_by, search_value)
            if results:
                df = pd.DataFrame(results, columns=['ID', 'Title', 'Author', 'Year', 'Genre', 'Read'])
                df['Year'] = df['Year'].astype(str)
                df['Read'] = df['Read'].map({1: 'Yes', 0: 'No'})
                st.dataframe(df.drop('ID', axis=1), use_container_width=True)
            else:
                st.info("No matching books found 📭")

    elif choice == "View Library":
        st.subheader("Your Library 📚")
        books = get_all_books()
        if books:
            df = pd.DataFrame(books, columns=['ID', 'Title', 'Author', 'Year', 'Genre', 'Read'])
            df['Year'] = df['Year'].astype(str)
            df['Read'] = df['Read'].map({1: 'Yes', 0: 'No'})
            st.dataframe(df.drop('ID', axis=1), use_container_width=True)
        else:
            st.info("Your library is empty 🌱")

    elif choice == "Statistics":
        st.subheader("Library Statistics 📊")
        total, read = get_statistics()
        if total > 0:
            percentage = (read / total) * 100
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Books", total, help="Total books in library")
            with col2:
                st.metric("Books Read", read, help="Books you've read")
            with col3:
                st.metric("Percentage Read", f"{percentage:.1f}%", help="Reading completion rate")
        else:
            st.info("No books in library yet 🌿")

if __name__ == "__main__":
    main()