import os
import django
from random import randint
from faker import Faker

# Setup Django environment before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_Management.settings')
django.setup()

from library.models import Book, Category  # ✅ Safe now after setup()

fake = Faker()

# Book categories and titles
books_data = {
    'Coding': [
        "Python Crash Course", "Fluent Python", "Eloquent JavaScript", "Clean Code", "Cracking the Coding Interview",
        "Automate the Boring Stuff", "You Don’t Know JS", "Effective Java", "Code Complete", "The Pragmatic Programmer",
        "Learn Python the Hard Way", "DSA Made Easy", "Head First Java", "HTML & CSS Design", "Django for Beginners"
    ],
    'Engineering': [
        "Strength of Materials", "Engineering Thermodynamics", "Digital Electronics", "Fluid Mechanics",
        "Control Systems", "Electrical Machines", "Mechanics of Solids", "Surveying", "Environmental Engineering",
        "Geotechnical Engineering", "Refrigeration and AC", "Machine Design", "Power Systems", "Signals & Systems",
        "Machine Drawing", "IC Engines", "Welding Technology", "Robotics Engineering", "Engineering Physics",
        "Network Theory", "Concrete Technology", "Metallurgy", "VLSI Design", "Instrumentation", "Highway Engineering",
        "Automobile Engineering", "Heat Transfer", "Structural Analysis", "Engineering Maths", "Engineering Chemistry"
    ],
    'UPSC': [
        "Indian Polity - Laxmikant", "Modern History - Bipin Chandra", "Geography NCERT", "Environment - Shankar IAS",
        "Indian Economy - Ramesh Singh", "CSAT Paper 2", "Ethics & Integrity", "Science & Tech", "Indian Society",
        "Governance & Constitution", "Essay Papers", "World History NCERT", "Art & Culture", "Economic Survey",
        "India Year Book", "Budget Highlights", "NCERT Class 6-12", "Prelims MCQs", "Mains GS Paper 2", "Geography - GC Leong"
    ],
    'Intermediate': [
        "Physics Part 1", "Physics Part 2", "Chemistry Part 1", "Chemistry Part 2", "Maths Part 1", "Maths Part 2",
        "Biology Vol 1", "Biology Vol 2", "English Literature", "Computer Science", "Statistics", "Accountancy",
        "Economics", "Business Studies", "Political Science", "History", "Hindi Vyakaran", "Sociology", "Geography", "Psychology"
    ]
}

# Load books
count = 0
for cat_name, titles in books_data.items():
    category_obj, _ = Category.objects.get_or_create(name=cat_name)
    for title in titles:
        Book.objects.create(
            title=title,
            author=fake.name(),
            category=category_obj,
            isbn=fake.isbn13(),
            available_copies=randint(3, 15)
        )
        count += 1

print(f"✅ {count} books loaded into the database successfully.")
