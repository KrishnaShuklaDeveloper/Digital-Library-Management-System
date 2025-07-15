from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from .forms import IssueBookForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Fine, Member, Book, Transaction
from datetime import date, timedelta


# 🔹 Landing Page
def landing_page(request):
    return render(request, 'library/landing.html')


# 🔹 Authentication Views
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('user_home')
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, 'library/user_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, "Invalid admin credentials.")
    return render(request, 'library/admin_login.html')


def user_logout(request):
    logout(request)
    return redirect('landing')


# 🔹 Admin Dashboard
@login_required
def admin_home(request):
    context = {
        'total_books': Book.objects.count(),
        'total_members': Member.objects.exclude(user__is_superuser=True).count(),
        'issued_books': Transaction.objects.filter(is_returned=False).count(),
        'pending_returns': Transaction.objects.filter(is_returned=False, return_date__lt=now().date()).count()
    }
    return render(request, 'library/admin_home.html', context)


# 🔹 User Dashboard
@login_required
def user_home(request):
    member, _ = Member.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(member=member, is_returned=False)
    fines = Fine.objects.filter(member=member, is_paid=False)
    return render(request, 'library/user_home.html', {
        'member': member,
        'transactions': transactions,
        'fines': fines,
        'today': now().date()
    })


# 🔹 Book Views
@login_required
def book_list(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(category__icontains=query))
    paginator = Paginator(books, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'library/book_list.html', {'page_obj': page_obj, 'query': query})


@login_required
def add_book(request):
    if request.method == "POST":
        Book.objects.create(
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            total_copies=int(request.POST.get('total_copies', 1)),
            available_copies=int(request.POST.get('total_copies', 1))
        )
        messages.success(request, "Book added successfully!")
        return redirect('book_list')
    return render(request, 'library/add_book.html')


@login_required
def issue_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available_copies <= 0:
        messages.error(request, "No copies are currently available.")
        return redirect('book_list')

    if request.user.is_staff:
        if request.method == 'POST':
            form = IssueBookForm(request.POST)
            if form.is_valid():
                member = form.cleaned_data['member']
                issue_date = form.cleaned_data.get('issue_date') or now().date()
                due_date = form.cleaned_data.get('due_date') or (issue_date + timedelta(days=15))
                Transaction.objects.create(
                    member=member,
                    book=book,
                    issue_date=issue_date,
                    return_date=due_date,
                    is_returned=False
                )
                book.available_copies -= 1
                book.save()
                return redirect('issue_success', book_id=book.id, username=member.user.username)
        else:
            form = IssueBookForm()
        return render(request, 'issue_book.html', {'form': form, 'book': book})
    else:
        member, _ = Member.objects.get_or_create(user=request.user)
        Transaction.objects.create(
            member=member,
            book=book,
            issue_date=now().date(),
            return_date=now().date() + timedelta(days=15),
            is_returned=False
        )
        book.available_copies -= 1
        book.save()
        messages.success(request, f'Book "{book.title}" issued.')
        return redirect('book_list')


@login_required
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.is_returned = True
    transaction.save()
    transaction.book.available_copies += 1
    transaction.book.save()
    if transaction.return_date and now().date() > transaction.return_date:
        late_days = (now().date() - transaction.return_date).days
        Fine.objects.create(member=transaction.member, fine_amount=late_days * 10)
    messages.success(request, "Book returned successfully!")
    return redirect('user_home')


@login_required
def request_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    member, _ = Member.objects.get_or_create(user=request.user)
    if book.available_copies <= 0:
        messages.error(request, "No copies available!")
        return redirect('book_list')
    Transaction.objects.create(
        member=member,
        book=book,
        return_date=now().date() + timedelta(days=14),
        status="Pending"
    )
    messages.success(request, "Book request sent!")
    return redirect('book_list')


@login_required
def overdue_books(request):
    overdue_books_list = Transaction.objects.filter(return_date__lt=now().date(), is_returned=False)
    return render(request, "library/overdue_books.html", {"overdue_books": overdue_books_list})


# 🔹 Request Approval
@login_required
def approve_request(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.status = 'Approved'
    transaction.save()
    messages.success(request, f"Request approved for '{transaction.book.title}'.")
    return redirect('pending_requests')


@login_required
def reject_request(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.status = 'Rejected'
    transaction.save()
    messages.success(request, f"Request rejected for '{transaction.book.title}'.")
    return redirect('pending_requests')


@login_required
def pending_requests(request):
    pending_transactions = Transaction.objects.filter(status="Pending")
    return render(request, "library/pending_requests.html", {"pending_transactions": pending_transactions})


# 🔹 Transactions and Fines
@login_required
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'library/transactions.html', {'transactions': transactions})


@login_required
def issued_books_history(request):
    transactions = Transaction.objects.filter(member__user=request.user)
    return render(request, 'library/issued_books_history.html', {'transactions': transactions})


@login_required
def fine_history(request):
    fines = Fine.objects.filter(member__user=request.user)
    return render(request, "library/fine_history.html", {"fines": fines})


@login_required
def manage_fines(request):
    fines = Fine.objects.filter(is_paid=False)
    return render(request, 'library/manage_fines.html', {'fines': fines})


@login_required
def pay_fine(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    fine.is_paid = True
    fine.save()
    messages.success(request, "Fine paid successfully!")
    return redirect('user_home')


# 🔹 Reports
@login_required
def reports(request):
    context = {
        'total_books': Book.objects.count(),
        'total_members': Member.objects.count(),
        'total_issued_books': Transaction.objects.filter(status='Issued').count(),
        'total_pending_returns': Transaction.objects.filter(status='Issued', return_date__lt=now().date()).count(),
    }
    return render(request, 'library/reports.html', context)


# 🔹 Profile and Member Management
@login_required
def update_profile(request):
    member, _ = Member.objects.get_or_create(user=request.user)
    if request.method == "POST":
        request.user.email = request.POST.get('email')
        member.membership_type = request.POST.get('membership_type')
        if 'profile_image' in request.FILES:
            member.profile_image = request.FILES['profile_image']
        request.user.save()
        member.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_home')
    return render(request, 'library/update_profile.html', {'member': member})


@login_required
def member_list(request):
    members = Member.objects.exclude(user__is_superuser=True)
    return render(request, 'library/manage_members.html', {'members': members})


@login_required
def add_member(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or Email already exists!")
            return redirect('add_member')
        user = User.objects.create_user(username=username, email=email, password=password)
        Member.objects.create(user=user, membership_type=request.POST.get('membership_type', 'standard'))
        messages.success(request, "Member added successfully!")
        return redirect('manage_members')
    return render(request, 'library/add_member.html')


@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        member.user.email = request.POST.get('email')
        member.membership_type = request.POST.get('membership_type')
        member.user.save()
        member.save()
        messages.success(request, "Member updated successfully!")
        return redirect('manage_members')
    return render(request, 'library/edit_member.html', {'member': member})


@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.user.delete()
    member.delete()
    messages.success(request, "Member deleted successfully!")
    return redirect('manage_members')


# 🔹 Utility
@login_required
def issue_success(request, book_id, username):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'issue_success.html', {'book': book, 'username': username})


@login_required
def search_books(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(category__icontains=query)
    ) if query else Book.objects.all()
    paginator = Paginator(books, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'library/search_results.html', {'page_obj': page_obj, 'query': query})
