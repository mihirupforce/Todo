# todo_list/todo_app/views.py
from django.forms import DateInput
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from todo_app.forms import DateSearch
from .models import ToDoItem, ToDoList
from django.db.models import Q

# category List View


class categoryListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"


# category Item List View
class categoryItemListView(ListView):
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


# category List Create
class categoryListCreate(CreateView):
    model = ToDoList
    fields = ["title"]


# category Item Create
class categoryItemCreate(CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "is_completed",
        "due_date",
    ]
    widgets = {
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


# category Item Update
class categoryItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "is_completed",
        "due_date",
    ]
    widgets = {
        'due_date': DateInput(),
    }

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

# category List Delete


class categoryListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")


# category Item Delete
class categoryItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
