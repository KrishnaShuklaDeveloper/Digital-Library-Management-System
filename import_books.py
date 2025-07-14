import csv
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library_Management.settings")
django.setup()

from library.models import Book, Category

def import_books_from_csv():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'books_dataset.csv')

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            category_name = row['category'].strip()

            # Get or create the Category object
            category, _ = Category.objects.get_or_create(name=category_name)

            # Create or update Book
            book, created = Book.objects.update_or_create(
                isbn=row['isbn'].strip(),  # use ISBN as unique field
                defaults={
                    'title': row['title'].strip(),
                    'author': row['author'].strip(),
                    'category': category,
                    'available_copies': int(row['available_copies']) if row['available_copies'] else 1
                }
            )
            count += 1
        print(f"✅ Successfully imported {count} books.")

if __name__ == "__main__":
    import_books_from_csv()
