from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job,Comment,CaseInsensitiveFieldMixin
from django.db import models
from django.contrib.auth.decorators import login_required #@login_required(login_url ="user:login")

# Create your views here.
def jobs(request):
    keyword= request.GET.get("keyword")

    if keyword:
        jobs = Job.objects.filter(title__contains=keyword)
        return render(request,"jobs.html",{"jobs":jobs})
    jobs = Job.objects.all()

    return render(request,"jobs.html",{"jobs":jobs})
class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass
class CIEmailField(CaseInsensitiveFieldMixin, models.EmailField):
    pass

def index(request):
    keyword= request.GET.get("keyword")
    if keyword:
        jobs = Job.objects.filter(title__contains=keyword)
        return render(request,"jobs.html",{"jobs":jobs})
    jobs = Job.objects.all()
    return render(request,"index.html",{"jobs":jobs})

def help(request):
    return render(request,"help.html")
def about(request):
    return render(request,"about.html")
def contact(request):
    return render(request,"contact.html")
def contracted(request):
    return render(request,"contracted.html")
def contracted2(request):
    return render(request,"contracted2.html")
def contractedhelp(request):
    return render(request,"contractedhelp.html")
def mailbody(request):
    return render(request,"mailbody.html")
@login_required(login_url ="user:login")
def dashboard(request):
    jobs = Job.objects.filter(author=request.user)
    context = {

        "jobs":jobs
    }
    return render(request,"dashboard.html",context)



@login_required(login_url ="user:login")
def addJob(request):
    form = JobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)

        job.author=request.user

        job.save()
        messages.success(request,"İş başarıyla oluşturuldu")
        return redirect("jobs:dashboard")
    return render(request,"addjob.html",{"form":form})



def detail(request,id):
    #job = Job.objects.filter(id=id).first()
    job = get_object_or_404(Job,id=id)
    comments = job.comments.all()
    keyword= request.GET.get("keyword")
    if keyword:
        jobs = Job.objects.filter(title__contains=keyword)
        return render(request,"jobs.html",{"jobs":jobs})
    jobs = Job.objects.all()
    return render(request,"detail.html",{"job":job,"comments":comments,"jobs":jobs})


@login_required(login_url ="user:login")
def updateJob(request,id):
    job = get_object_or_404(Job,id=id)
    form=JobForm(request.POST or None, request.FILES or None,instance=job)
    if form.is_valid():
        job = form.save(commit=False)

        job.author=request.user

        job.save()
        messages.success(request,"İş başarıyla Güncellendi")
        return redirect("jobs:dashboard")


    return render(request,"update.html",{"form":form})
@login_required(login_url ="user:login")
def deleteJob(request,id):
    job = get_object_or_404(Job,id=id)

    job.delete()

    messages.success(request,"İş Başarıyla Silindi")
    return redirect("jobs:dashboard")

def addComment(request,id):
    job=get_object_or_404(Job,id=id)

    if request.method=="POST":
        comment_author = request.POST.get("comment_author")
        comment_content= request.POST.get("comment_content")
        rate= request.POST.get("rate")
        newComment =Comment(comment_author=comment_author,comment_content=comment_content,rate=rate)
        newComment.job=job
        newComment.save()
    return redirect(reverse("jobs:detail",kwargs={"id":id}))



