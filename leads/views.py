from django.core.mail import send_mail
from django.shortcuts import render ,redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Lead , Agent
from .forms import LeadForm ,LeadModelForm , CustomUserCreationForm



class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect("dashboard")
    #     return super().dispatch(request, *args, **kwargs)

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


def landing_page(request):
    return render(request, "landing.html")



def lead_list(request):
    #return HttpResponse("Hello world!")
    leads = Lead.objects.all()
    context = {
        "leads":leads
        
        }

    return render(request,"leads/lead_list.html",context)

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"



def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context = {
          "lead":lead

    }
    return render(request,"leads/lead_detail.html",context)

class LeadCreateView(LoginRequiredMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class  =LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        # lead = form.save(commit=False)
        # lead.organisation = self.request.user.userprofile
        # lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        # messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)
    





def lead_create(request):
   form  =LeadModelForm()
   if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
   context = {
        "form": form
    }
   return render(request, "leads/lead_create.html", context)


class LeadUpdateView(LoginRequiredMixin ,generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class  = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)

class LeadDeleteView(LoginRequiredMixin ,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()
    

    def get_success_url(self):
        return reverse("leads:lead-list")



def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")



# def lead_create(request):
#    form  =LeadModelForm()
#    if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create( first_name=first_name, last_name=last_name,age = age, agent = agent)
#             return redirect("/leads")
#    context = {
#         "form": form
#     }
#    return render(request, "leads/lead_create.html", context)


