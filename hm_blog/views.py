from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from hm_blog.models import Menu, Unique, Footer, FooterIcons, RowMenu, Verification, SocialSettings, \
    AddImages, ShotDetails, About, AboutTeam, Like, Follow, Comment, ContactUs, MyUser
from hm_blog.forms import RegisterForm, LoginForm, ShotDetailForm, SettingProfileForm, CommentForm, \
    ContactForm
import uuid
from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q


# Create your views here.

User = get_user_model()

def get_context():
    context = {}
    context['menu'] = Menu.objects.all()
    context['row_menu'] = RowMenu.objects.all()
    context['unique'] = Unique.objects.last()
    context['footer'] = Footer.objects.all()
    context['footer_icons'] = FooterIcons.objects.all()
    return context


# context['menu'] = Menu.objects.all()
# context['row_menu'] = RowMenu.objects.all()
# context['unique'] = Unique.objects.last()
# context['footer'] = Footer.objects.all()
# context['footer_icons'] = FooterIcons.objects.all()
# def base(request):
#     return render(request, 'base.html')

def home(request):
    context = get_context()
    context['menu'] = Menu.objects.all()
    context['row_menu'] = RowMenu.objects.all()
    context['unique'] = Unique.objects.last()
    context['footer'] = Footer.objects.all()
    context['footer_icons'] = FooterIcons.objects.all()
    context['login_form'] = LoginForm()
    # if not request.user.is_authenticated:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("profile")
            else:
                messages.error(request, "Istifadəçi adı və ya şifrə yanlışdır!!!")
                return redirect("home")
        else:
            return redirect("home")
    return render(request, "home.html", context)


def register(request):
    context = get_context()
    context['register_form'] = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('Password'))
            user.is_active = False
            user.save()
            messages.success(
                request, "Zəhmət olmasa email ünvanınızı təsdiq edin"
            )
            return redirect('home')
        else:
            messages.error(request, "Bu adda istifadəçi artıq mövcuddur!!!")
            context['form'] = form
            return redirect('home')

    return render(request, 'user-register.html', context)


def verify_view(request, token, user_id):
    verify = Verification.objects.filter(token=token, user_id=user_id, expire=False).last()
    if verify:
        verify.expire = True
        verify.save()
        verify.user.is_active = True
        verify.user.save()
        login(request, verify.user)
        messages.info(
            request, "Success"
        )
        return redirect('home')
    else:
        return redirect('home')


def logout_page(request):
    logout(request)
    return redirect("home")


# def explore(request):
#     context = get_context()
#     context['explore'] = ShotDetails.objects.all()
#     return render(request, 'explore-style3-cols3.html', context)


@login_required
def profile(request, id):
    context = get_context()
    user = User.objects.filter(id=id).last()
    context['profile'] = SettingProfileForm()
    context["profile_user"] = user
    page = Paginator(ShotDetails.objects.filter(user=user), 12)
    context['shot_detail_model'] = page.get_page(request.GET.get('page', 1))
    context['page_count'] = page.num_pages
    if request.is_ajax():
        return render(request, "explore.html", context)
    else:
        return render(request, 'user-profile.html', context)


@login_required
def add_shot(request):
    context = get_context()
    # context['meta_form'] = MetaDataForm()
    context['shot_detail'] = ShotDetailForm()
    context["image_data"] = str(uuid.uuid4())
    if request.method == "POST":
        form = ShotDetailForm(request.POST, request.FILES)
        # meta_form = MetaDataForm(request.POST)
        if form.is_valid():
            shot = form.save(commit=False)
            shot.Preview_image = request.FILES['Preview_image']
            shot.user = request.user
            shot.save()

            # news = form.save()
            image_data = request.POST.get("image_data")
            print("Imagedata =>", image_data)
            image_list = AddImages.objects.filter(image_token=image_data)
            print("Image list =>", image_list)
            if image_data:
                for image in image_list:
                    image.shotdetail = shot
                    image.save()
            return redirect("home")
        else:
            context["form"] = form
    return render(request, 'shot-add.html', context)


@login_required
def profile_settings(request):
    context = get_context()
    update = request.user
    if request.method == 'GET':
        if update:
            context['setting_profile'] = SettingProfileForm(instance=update, initial={
                "full_name": request.user.get_full_name()
            })
            return render(request, 'setting-profile.html', context)
    else:
        form = SettingProfileForm(request.POST, instance=update, initial={
            "full_name": request.user.get_full_name()
        })
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            context['form'] = form
            return render(request, 'user-profile.html', context)


@login_required
def social_settings(request):
    context = get_context()
    context['social_site'] = SocialSettings.objects.all()
    # print("-----------", SocialSettings.__getitem__)
    return render(request, 'setting-socials.html', context)


@login_required
def explore(request):
    context = get_context()
    page = Paginator(ShotDetails.objects.all(), 8)
    context['explore'] = page.get_page(request.GET.get('page', 1))
    context['page_count'] = page.num_pages
    if request.method == "POST" and request.is_ajax():
        shot_id = request.POST.get('shot_id')
        shot = ShotDetails.objects.filter(id=shot_id).last()
        if shot:
            like = Like.objects.filter(detail=shot, user=request.user)
            if like:
                shot.like_count -= 1
                shot.save()
                like.delete()
                return JsonResponse({
                    'messages': f'{shot.Title} is like',
                    'like_count': shot.like_count,
                    'status': True
                })
            else:
                shot.like_count += 1
                shot.save()
                Like.objects.create(
                    user=request.user,
                    detail=shot
                )
                return JsonResponse({
                    'messages': f'{shot.Title} is dislike',
                    'like_count': shot.like_count,
                    'status': False
                })
    if 'q' in request.GET:
        query = request.GET.get('q')
        explore = ShotDetails.objects.filter(
            Q(tags__icontains=query) |
            Q(location__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
        page = Paginator(explore, 8)
        context['explore'] = page.get_page(request.GET.get('page', 1))

    if request.is_ajax():
        return render(request, "explore.html", context)
    else:
        return render(request, 'explore-style3-cols3.html', context)


def picture_add(request):
    if request.method == "POST" and request.is_ajax():
        img = AddImages.objects.create(
            image=request.FILES.get("file"),
            image_token=request.POST.get("image_data")
        )
        return JsonResponse({
            "pk": img.id,
            "uploaded": True
        })
    else:
        if not request.is_ajax():
            return redirect('home')
        return JsonResponse({
            "uploaded": False
        })


def picture_delete(request):
    if request.method == "POST" and request.is_ajax():
        pk = request.POST.get("remove_object")
        img = AddImages.objects.filter(id=pk).last()
        if img:
            img.delete()
            return JsonResponse({
                "deleted": True
            })
        else:
            return JsonResponse({
                "deleted": False
            })
    else:
        if not request.is_ajax():
            return redirect('home')
        return JsonResponse({
            "uploaded": False
        })


def about(request):
    context = get_context()
    context['about_us'] = About.objects.first()
    context['team'] = AboutTeam.objects.all()
    return render(request, 'page-about.html', context)


def into_shot(request, id):
    context = get_context()
    shot = ShotDetails.objects.filter(id=id).last()
    context["shot"] = shot
    context['comment'] = CommentForm()
    # context['comment_post'] = Comment.objects.all()
    post_comment = shot.comment_set.all()
    context['comment_post'] = post_comment
    if request.user not in shot.view.all():
        shot.view.add(request.user)
    if shot:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.shot = shot
                comment.save()
                # return JsonResponse({
                #     "status": 'OK'
                # })
                return redirect("explore")
            else:
                pass
                # return JsonResponse({
                #     "status": "False"
                # })

    return render(request, 'shot-gallery-for-modal.html', context)


class FollowView(generic.View):
    # template_name = 'user-followering.html'

    def post(self, request):
        user_id = request.POST.get('user_id')
        follow = Follow.objects.filter(
            from_user=request.user,
            to_user_id=user_id
        ).last()
        if not follow:
            follow = Follow.objects.create(
                from_user=request.user,
                to_user_id=user_id
            )
            return JsonResponse({
                'status': True
            })
        else:
            follow.delete()
            return JsonResponse({
                'status': False
            })

    # def get_context_data(self, **kwargs):
    #     context['following'] = [follow.to_user for follow in self.request.user.following.all()]
    #     context['user_list'] = User.objects.all().exclude(id=self.request.user.id)
    #     return context


# class FollowingView(generic.TemplateView):
#     template_name = 'user-followering.html'
#
#     def get_context_data(self, **kwargs):
#         context['following'] = [follow.to_user for follow in self.request.user.following.all()]
#         context['user_list'] = User.objects.all().exclude(id=self.request.user.id)
#         return context

def FollowingView(request, id):
    context = get_context()
    user = User.objects.filter(id=id).last()
    context["user_list"] = User.objects.all()
    context["user"] = user

    return render(request, 'user-followering.html', context)


def FollowersView(request, id):
    context = get_context()
    user = User.objects.filter(id=id).last()
    context["user_list"] = User.objects.all()
    context["user"] = user

    return render(request, 'user-followers.html', context)


# class CommentView(generic.FormView):
#     model = Comment
#     form_class = CommentForm
#     success_url = "/"
#
#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.user = self.request.user
#         comment.shot = ShotDetails.objects.filter(id=self.kwargs.get('id')).last()
#         comment.save()
#         return JsonResponse({
#             "status": "Ok"
#         })

# def CommentView(request, id):
#     shot = ShotDetails.objects.filter(id=id).last()
#     if shot:
#         if request.method == 'POST':
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.user = request.user
#                 comment.shot = shot
#                 comment.save()
#                 return JsonResponse({
#                     "status": "Ok"
#                 })
#             else:
#                 return JsonResponse({
#                     "status": "False"
#                 })
#         return render(request, 'shot-gallery-for-modal.html', context)

class ContactView(generic.TemplateView):
    template_name = 'page-contact.html'

    def get_context_data(self, **kwargs):
        # context['']
        context = get_context()
        return context


def ContactView(request):
    context = get_context()
    context['contact'] = ContactUs.objects.all()
    context['contact_form'] = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sizinle elaqe saxlanilacaq)')
            return redirect('contact')
            # return HttpResponse("if")
        else:
            messages.success(request, 'Melumatinizda yalnisliq var, zehmet olmasa formu yeniden doldurun(')
            context['contact_form'] = form
            return redirect('contact')
            # return HttpResponse('else')

    return render(request, 'page-contact.html', context)


def search(request):
    context = get_context()
    if 'q' in request.GET:
        query = request.GET.get('q')
        context['explore'] = ShotDetails.objects.filter(
            Q(tags__icontains=query) |
            Q(location__icontains=query) |
            Q(get_user_model=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) &
            Q(user__last_name__icontains=query)
        )


    return render(request, 'page-search.html', context)