from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from .models import Photo, CustomUser
from .forms import PhotoForm,PhotoEditForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    model = Photo
    context_object_name = 'photos'

    def get_queryset(self):
        # Filtra as fotos pelo usuário
        username = self.kwargs.get('username')
        user = get_object_or_404(CustomUser, username=username)
        return Photo.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = get_object_or_404(CustomUser, username=username)
        context['userlogado'] = self.request.user
        context['user'] = user
        return context
    
    def follow(self, request, userlogado, user):
        userlogado.following += 1
        user.followers += 1

        # Adicionar o usuário à lista de "whos_following"
        whos_following_list = userlogado.get_whos_following_list()
        if user.username not in whos_following_list:
            whos_following_list.append(user.username)
            userlogado.whos_following = ','.join(whos_following_list)

        userlogado.save()
        user.save() 
        return HttpResponseRedirect(reverse('profile', args=[self.kwargs['username']]))

    def unfollow(self, request, userlogado, user):
        userlogado.following -= 1
        user.followers -= 1

        # Remover o usuário da lista de "whos_following"
        whos_following_list = userlogado.get_whos_following_list()
        if user.username in whos_following_list:
            whos_following_list.remove(user.username)
            userlogado.whos_following = ','.join(whos_following_list)

        userlogado.save()
        user.save()        
        return HttpResponseRedirect(reverse('profile', args=[self.kwargs['username']]))

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')  # Captura a ação a ser executada (follow ou unfollow)
        username = self.kwargs.get('username')
        user = get_object_or_404(CustomUser, username=username)
        userlogado = self.request.user

        if action == 'follow':
            return self.follow(request, userlogado, user)
        else:
            return self.unfollow(request, userlogado, user)

        return super().post(request, *args, **kwargs)




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
        context['userlogado'] = self.request.user
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
    
    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        if self.request.user != user:
            return redirect('permission-denied')  # Redirecionar para a página de permissão negada
        return super().dispatch(request, *args, **kwargs)

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
    
    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        if self.request.user != user:
            return redirect('permission-denied')  # Redirecionar para a página de permissão negada
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = CustomUser.objects.get(username=username)
        context['user'] = user
        context['userlogado'] = self.request.user
        return context
    
    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('profile', kwargs={'username': username})
    

class DeletePhoto(DeleteView):
    model = Photo
    context_object_name = "card"

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        if self.request.user != user:
            return redirect('permission-denied')  # Redirecionar para a página de permissão negada
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = CustomUser.objects.get(username=username)
        context['user'] = user
        context['userlogado'] = self.request.user
        return context
    
    def get_success_url(self):
        username = self.request.user
        return reverse_lazy('profile', kwargs={'username': username})

@method_decorator(login_required, name='dispatch')
class DesativarUsuarioView(View):
    def get(self,request):
        return render(request,'desativar.html')
        
    def post(self,request):
        user = request.user
        user.is_active = False
        user.save()
        return HttpResponseRedirect('index')
    