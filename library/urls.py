from django.urls import path
from . import views


urlpatterns = [
    # 🔹 Landing Page
    path('', views.landing_page, name='landing'),

    # 🔹 Admin URLs
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),

    # 🔹 User URLs
    path('user-login/', views.user_login, name='user_login'),
    path('user-home/', views.user_home, name='user_home'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/issue/<int:book_id>/', views.issue_book, name='issue_book'),
    path('book/issued/success/<int:book_id>/<str:username>/', views.issue_success, name='issue_success'),
    path('issue-success/<int:book_id>/<str:username>/', views.issue_success, name='issue_success'),
    path('pending-requests/', views.pending_requests, name='pending_requests'),
    path('approve-request/<int:transaction_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:transaction_id>/', views.reject_request, name='reject_request'),


    path('search/', views.search_books, name='search_books'),
    path('transactions/', views.transaction_list, name='transactions'),
    path("overdue-books/", views.overdue_books, name="overdue_books"),
    path("edit-member/<int:member_id>/", views.edit_member, name="edit_member"),
    path("book/approve/<int:transaction_id>/", views.approve_issue, name="approve_issue"),

    # 🔹 Membership Management
    path("renew-membership/", views.renew_membership, name="renew_membership"),

    # 🔹 Member Management
    path("manage-members/", views.member_list, name="manage_members"),
    path('add-member/', views.add_member, name='add_member'),
    path("edit-member/<int:member_id>/", views.edit_member, name="edit_member"),
    path("delete-member/<int:member_id>/", views.delete_member, name="delete_member"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("issued-books-history/", views.issued_books_history, name="issued_books_history"),

    # 🔹 Book Management
    path('books/', views.book_list, name='book_list'),
    path('books/search/', views.search_books, name='search_books'),
    path('book/request/<int:book_id>/', views.request_book, name='request_book'),
    path('book/approve/<int:transaction_id>/', views.approve_issue, name='approve_issue'),

    # 🔹 Transaction Management
    path('transactions/', views.transaction_list, name='transactions'),
    path('pending-requests/', views.pending_requests, name='pending_requests'),
    path('book/return/<int:transaction_id>/', views.return_book, name='return_book'),

    # 🔹 Reports & Analytics
    path('reports/', views.generate_reports, name='reports'),
    path("fine-history/", views.fine_history, name="fine_history"),

    # 🔹 Fine Management
    path('manage-fines/', views.manage_fines, name='manage_fines'),
    path('pay-fine/<int:fine_id>/', views.pay_fine, name='pay_fine'),
    path("overdue-books/", views.overdue_books, name="overdue_books"),

    # 🔹 Logout
    path('logout/', views.user_logout, name='logout'),
]
