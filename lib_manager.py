import streamlit as st
import json
import os

data_file = 'lib.txt'

# ---------- Core Functions ----------
def load_lib():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_lib(lib):
    with open(data_file, 'w') as file:
        json.dump(lib, file, indent=4)

def add_book(lib, title, author, year, genre, read):
    new_book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    }
    lib.append(new_book)
    save_lib(lib)

def remove_book(lib, title_to_remove):
    updated = [book for book in lib if book['title'].lower() != title_to_remove.lower()]
    if len(updated) < len(lib):
        save_lib(updated)
        return updated, True
    return lib, False

def search_books(lib, field, term):
    return [book for book in lib if term.lower() in book[field].lower()]

def get_statistics(lib):
    total = len(lib)
    read = len([book for book in lib if book['read']])
    percent = (read / total) * 100 if total > 0 else 0
    return total, read, percent


st.set_page_config(page_title="📚 Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

lib = load_lib()


with st.expander("➕ Add New Book"):
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Year")
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        submitted = st.form_submit_button("Add Book")
        if submitted and title and author:
            add_book(lib, title, author, year, genre, read)
            st.success(f'"{title}" added to your library!')
            st.rerun()


with st.expander("🔍 Search Books"):
    search_by = st.selectbox("Search by", ["title", "author", "genre"])
    search_term = st.text_input(f"Enter {search_by}")
    if search_term:
        results = search_books(lib, search_by, search_term)
        if results:
            st.write(f"Found {len(results)} result(s):")
            for book in results:
                st.markdown(f"- **{book['title']}** by *{book['author']}* ({book['year']}) — {book['genre']} [{'✅' if book['read'] else '❌'}]")
        else:
            st.warning("No books matched your search.")


st.subheader("📖 All Books in Library")
if lib:
    for book in lib:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**{book['title']}** by *{book['author']}* ({book['year']}) — {book['genre']} [{'✅' if book['read'] else '❌'}]")
        with col2:
            if st.button("❌ Delete", key=book['title']):
                lib, removed = remove_book(lib, book['title'])
                if removed:
                    st.success(f'"{book["title"]}" removed.')
                    st.rerun()
else:
    st.info("Your library is empty. Start by adding a book!")


st.subheader("📊 Library Statistics")
total, read_count, percent = get_statistics(lib)
st.write(f"**Total books:** {total}")
st.write(f"**Books read:** {read_count}")
st.write(f"**Read percentage:** {percent:.2f}%")
