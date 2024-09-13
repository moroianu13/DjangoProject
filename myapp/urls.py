from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to 'home' after logout
    path('register/', register_view, name='register'),
    
    # Home page with "My Shop" link
    path('', HomeView.as_view(), name='home'),  
    
    # List of all categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    
    # Detail view of a specific category (showing items in that category)
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    path('category/new/', CategoryCreateView.as_view(), name='category-create'),
    
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    # Detail view of a specific item
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    
    # List of all items (optional, might be more relevant to administrators)
    path('items/', ItemListView.as_view(), name='item-list'),
    
    # Create sample items for testing
    path('create-items/', create_items),
    
    # Create a new item
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    
    # Update an existing item
    path('item/<int:pk>/edit/', ItemUpdateView.as_view(), name='item-update'),
    
    # Delete an existing item
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
]
