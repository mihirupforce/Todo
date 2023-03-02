# todo_list/todo_app/views.py
from django.forms import DateInput
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,FormView
from todo_app.forms import DateSearch, UserRegistrationForm
from .models import ToDoItem, ToDoList
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.widgets import HiddenInput


#  UserSignup
class UserSignup(FormView):
    template_name = 'todo_app/Signup.html'
    form_class = UserRegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignup, self).form_valid(form)


#  UserLoginView
class UserLoginView(LoginView):
    template_name = 'todo_app/signin.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    


# category List View
class categoryListView(LoginRequiredMixin,ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset  
    def form_valid(self, form):
            form.instance.owner = self.request.user
            return super().form_valid(form)

# category Item List View
class categoryItemListView(LoginRequiredMixin,ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        queryset = ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(due_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(Q(due_date__gte=start_date))
        elif end_date:
            queryset = queryset.filter(Q(due_date__lte=end_date))
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["form"] = DateSearch(self.request.GET)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# category List Create
class categoryListCreate(LoginRequiredMixin,CreateView):
    model = ToDoList
    fields = ["title"]

    def get_queryset(self):
        return super().get_queryset()
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# category Item Create
class categoryItemCreate(LoginRequiredMixin,CreateView):
    model = ToDoItem
    fields = (
        "todo_list",
        "title",
        "description",
        "is_completed",
        "due_date",
    )
    widgets = {
        'todo_list': HiddenInput(),
        'due_date': DateInput(),
    }
    
    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

    def due_date(date):
        pass
        
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# category Item Update
class categoryItemUpdate(LoginRequiredMixin,UpdateView):
    model = ToDoItem
    fields = (
        "todo_list",
        "title",
        "description",
        "is_completed",
        "due_date",
    )
    widgets = {
        'todo_list': HiddenInput(),
        'due_date': DateInput(),
    }

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# category List Delete

class categoryListDelete(LoginRequiredMixin,DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# category Item Delete
class categoryItemDelete(LoginRequiredMixin,DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
