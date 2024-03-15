from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete-expense'),
    path('edit-expense/<int:id>/', views.edit_expense, name='edit-expense'),
    path("search-expenses/", csrf_exempt(views.search_expenses), name="search-expenses"),
    path("expense-category-summary/", views.expense_category_summary, name="expense-category-summary"),
    path("statistics/", views.stats_view, name="statistics")
]