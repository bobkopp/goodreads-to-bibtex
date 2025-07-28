# [[file:org/export.org::*Imports][Imports:1]]
import csv
import re
import sys
import unicodedata
# Imports:1 ends here

# [[file:org/export.org::*BibTex ID][BibTex ID:3]]
# Keep an index of all assigned IDs to avoid duplicates
# If an ID is duplicated, add one more meaningful word to the ID
assigned_ids = set()


def normalize_and_clean(text):
    # Normalize the Unicode string
    normalized_text = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII characters
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('ascii')
    # Remove special characters
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ ')
    new_text = ''.join(char for char in ascii_text if char in allowed_chars)
    return new_text
    
def clean_title(title):
    """Keep all letters from the titles, and convert everything to spaces. Keep
    one space between words only"""
    title = re.sub(r'\W+', ' ', title)
    title = re.sub(r'\s+', ' ', title)
    return title

def x_meaningful_words(title, x=1):
    """Return the `x` first words with more than three letters. Each word are
    concatenated without spaces in between them."""
    title = clean_title(title)
    words = title.split(' ')
    meaningful_words = []
    for word in words:
        if len(word) > 3:
            meaningful_words.append(word)
            if len(meaningful_words) == x:
                return "".join(meaningful_words)
    return "".join(meaningful_words)

def bibtex_id(author, year, title, x=1):
    """Generates a BibTeX ID"""
    global assigned_ids

    if(x > 5):
        id = author.split(', ')[0].lower() + year + '_' + "".join(clean_title(title).split(' ')).lower()
    else:
        id = author.split(', ')[0].lower() + year + '_' + x_meaningful_words(title, x).lower()
    id = re.sub(r'\W+', '', id)

    id = normalize_and_clean(id)
    if(x > 5):
        assigned_ids.add(id)
        return id

    if(id in assigned_ids):
        return bibtex_id(author, year, title, x+1)
    else:
        assigned_ids.add(id)
        return id
# BibTex ID:3 ends here

# [[file:org/export.org::*Export][Export:1]]
with open(sys.argv[1], newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    # Skip header
    next(reader)

    for row in reader:
        title = row[1]
        author = row[3]
        additional_authors = row[4]
        isbn = row[5]
        rating = row[7]
        publisher = row[9]
        binding = row[10]
        pages = row[11]
        year = row[12]
        date_read = row[14]
        date_added = row[15]
        bookshelf = row[16]
        exclshelf = row[18]

        note=""
        if date_read:
            note = str(note) + "Read: " + date_read + ". "
        if rating:
            note = str(note) + "Rating:  " + rating + ". "
        
        shelf=""
        if exclshelf:
            shelf = exclshelf
        if bookshelf:
            shelf = shelf + ", " + bookshelf


        print("@book{" + bibtex_id(author, year, title) + ",")
        print("    title = {" + title + "},")
        print("    author = {" + author + "},")
        if additional_authors:
            print("    additional_authors = {" + additional_authors + "},")
        if isbn:
            if isbn[2:-1]:
                print("    isbn = {" + isbn[2:-1] + "},")
        if publisher:
            print("    publisher = {" + publisher + "},")
        if pages:
            print("    pages = {" + pages + "},")
        if year:
            print("    year = {" + year + "},")
        if date_read:
            print("    date-read = {" + date_read + "},")
        if date_read:
            print("    date-modified = {" + date_read + "},")
        if date_added:
            print("    date-added = {" + date_added + "},")
        if rating:
            print("    rating = {" + rating + "},")
        if shelf:
            print("    keywords = {" + shelf + "},")           
        if note:
            print("    note = {" + note + "},")
        print("}\n")
# Export:1 ends here
