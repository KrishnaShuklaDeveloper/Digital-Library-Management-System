import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now

# Function to set default membership end date (1 year from today)
def default_membership_end():
    return datetime.date.today() + datetime.timedelta(days=365)

# 📌 Member Management
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member")
    membership_type = models.CharField(
        max_length=50,
        choices=[('Standard', 'Standard'), ('Premium', 'Premium')],
        default='Standard'  # ✅ Fix: Added default value
    )
    membership_start = models.DateField(default=datetime.date.today)
    membership_end = models.DateField(default=default_membership_end)
    is_active = models.BooleanField(default=True)

    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} (Active: {self.is_active})"

# 📌 Book Categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# 📌 Book Management
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} - {self.author} ({self.available_copies} copies available)"

def get_due_date():
    return now().date() + timedelta(days=15)


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=now)
    due_date = models.DateField(default=get_due_date)  # <-- use named function here
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.member.user.username} - {self.book.title} (Returned: {self.is_returned})"


# 📌 Fine Management
class Fine(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine for {self.transaction.member.user.username}: {self.fine_amount} (Paid: {self.is_paid})"

# 📌 Reports & Analytics
class Report(models.Model):
    generated_on = models.DateTimeField(auto_now_add=True)
    total_books = models.PositiveIntegerField()
    total_members = models.PositiveIntegerField()
    issued_books = models.PositiveIntegerField()
    pending_returns = models.PositiveIntegerField()

    def __str__(self):
        return f"Report - {self.generated_on.strftime('%Y-%m-%d %H:%M:%S')}"

# 📌 Issued Book Tracking
class IssuedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"
