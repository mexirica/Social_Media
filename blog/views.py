from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Photo, CustomUser
from .forms import PhotoForm,PhotoEditForm


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    model = Photo
    context_object_name = 'photos'

    def get_queryset(self):
        # Filtra as fotos pelo usuário
        username = self.kwargs.get('username')
        user = CustomUser.objects.get(username=username)
        return Photo.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = CustomUser.objects.get(username=username)
        context['userlogado'] = self.request.user
        context['user'] = user
        return context
    

class BuscarView(ListView):
    model = Photo
    template_name = 'buscar.html'
    context_object_name = 'cards'
    paginate_by = 40
    ordering = ['data']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('buscar')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query))
            
        return queryset
    

class IndexView(ListView):
    model = Photo
    template_name = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('?')

class AddView(CreateView):
    model = Photo
    template_name = 'add'
    form_class = PhotoForm

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('profile', kwargs={'username': username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = CustomUser.objects.get(username=username)
        context['user'] = user
        context['userlogado'] = self.request.user
        return context

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()
        return super().form_valid(form)
    

class DetalharFoto(DetailView):
    model=Photo
    template_name="detail"
    form_class=PhotoForm
    context_object_name = "card"


class Update(UpdateView):
    model=Photo
    context_object_name = "card"
    form_class=PhotoEditForm
    

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('profile', kwargs={'username': username})
    

class DeletePhoto(DeleteView):
    model = Photo
    context_object_name = "card"

    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('profile', kwargs={'username': username})
