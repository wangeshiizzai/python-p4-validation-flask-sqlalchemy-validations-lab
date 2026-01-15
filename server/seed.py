#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Author, Post

fake = Faker()

with app.app_context():

    # Clear existing data
    Author.query.delete()
    Post.query.delete()

    # -------------------- AUTHORS --------------------
    authors = []
    for _ in range(25):
        # Make sure phone number is exactly 10 digits
        phone = fake.random_number(digits=10, fix_len=True)
        author = Author(
            name=fake.unique.name(),
            phone_number=str(phone)
        )
        authors.append(author)

    db.session.add_all(authors)

    # -------------------- POSTS --------------------
    clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
    categories = ["Fiction", "Non-Fiction"]

    posts = []
    for _ in range(25):
        title = f"{rc(clickbait_phrases)} {fake.sentence(nb_words=5)}"
        content = " ".join(fake.paragraphs(nb=5))  # usually > 250 chars
        # Ensure content is at least 250 chars
        while len(content) < 250:
            content += " " + fake.paragraph()
        summary = fake.text(max_nb_chars=250)
        category = rc(categories)

        post = Post(
            title=title,
            content=content,
            summary=summary,
            category=category
        )
        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()

    print(f"Seeded {len(authors)} authors and {len(posts)} posts successfully!")
