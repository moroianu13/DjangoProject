from django.shortcuts import render , redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Item, Category,  Review
from django.urls import reverse_lazy , reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ItemForm , ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import models




def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'myapp/register.html', {'form': form})


# View for the home page (My Shop)
class HomeView(TemplateView):
    template_name = 'myapp/home.html'

# View for listing all categories
class CategoryListView(ListView):
    model = Category
    template_name = 'myapp/category_list.html'

# View for showing items in a specific category
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'myapp/category_detail.html'

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve the current category object
        category = self.get_object()

        # Now add the items that belong to this category to the context
        context['items'] = Item.objects.filter(category=category)

        return context
    
    
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'myapp/category_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Category'
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'myapp/category_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Category'
        return context
    
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'myapp/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

# View for showing details of a specific item
class ItemDetailView(DetailView):
    model = Item
    template_name = 'myapp/item_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(item=self.object)
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        item = self.get_object()  # Retrieve the item being reviewed
        form = ReviewForm(request.POST)  # Handle the submitted form data
        if form.is_valid():
        # Check if the user already reviewed this item
            if Review.objects.filter(item=item, user=request.user).exists():
                messages.error(request, 'You have already reviewed this item.')
            else:
            # Save the new review
                review = form.save(commit=False)
                review.item = item
                review.user = request.user
                review.save()
                return redirect(reverse('item-detail', kwargs={'pk': item.pk}))

    # In case of errors, render the form with errors
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
    

# View for listing all items (you may want this for the admin section or general purpose)
class ItemListView(ListView):
    model = Item
    template_name = 'myapp/item_list.html'
    context_object_name = 'items'
    paginate_by = 10  # Optional pagination

    def get_queryset(self):
        queryset = Item.objects.all()
        search_query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=int(category_id))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        return context

# View for creating new items
class ItemCreateView(LoginRequiredMixin , CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'myapp/item_form.html'
    login_url = 'login'
    def get_initial(self):
        # If the category ID is in the URL (query parameters), pre-select that category in the form
        initial = super().get_initial()
        category_id = self.request.GET.get('category')
        if category_id:
            initial['category'] = category_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Item'
        return context



# View for updating items
class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'myapp/item_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Item'
        return context



# View for deleting items
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'myapp/item_confirm_delete.html'
    success_url = reverse_lazy('item-list')

# Function to create sample items (for testing)
def create_items(request):
    user1 = User.objects.create(username="user1")
    user2 = User.objects.create(username="user2")
    user3 = User.objects.create(username="user3")

    Item.objects.create(name="Item 1", user=user1)
    Item.objects.create(name="Item 2", user=user2)
    Item.objects.create(name="Item 3", user=user3)

    return HttpResponse('Items created!')


