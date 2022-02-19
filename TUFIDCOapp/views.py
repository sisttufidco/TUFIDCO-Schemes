from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from .models import *
from .forms import EmailForm
from TUFIDCO.settings import EMAIL_HOST_USER


# Create your views here.
def home(request):
    data = tufidco_info.objects.all()
    gallery_photos = postphotogallery_slider.objects.all()
    form_slider_photos = postreformslider.objects.all()
    main_slider_photos = postmainslider.objects.all()
    total_projects = MasterSanctionForm.objects.count()
    project_cost = MasterSanctionForm.objects.aggregate(project_cost=Sum('ApprovedProjectCost'))
    knmt = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(knmt_share=Sum('SchemeShare'))
    ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(ulb_share=Sum('ULBShare'))
    dmp_total_projects = MasterSanctionForm.objects.filter(AgencyType__AgencyType='Municipality').count()
    dmp_project_cost = MasterSanctionForm.objects.filter(
        AgencyType__AgencyType='Municipality').aggregate(dmp_project_cost=Sum('ApprovedProjectCost'))
    dmp_knmt = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
        AgencyType__AgencyType='Municipality').aggregate(dmp_knmt=Sum('SchemeShare'))
    dmp_ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
        AgencyType__AgencyType='Municipality').aggregate(dmp_ulb_share=Sum('ULBShare'))
    ctp_total_projects = MasterSanctionForm.objects.filter(AgencyType__AgencyType='Town Panchayat').count()
    ctp_project_cost = MasterSanctionForm.objects.filter(
        AgencyType__AgencyType='Town Panchayat').aggregate(ctp_project_cost=Sum('ApprovedProjectCost'))
    ctp_knmt = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
        AgencyType__AgencyType='Town Panchayat').aggregate(ctp_knmt=Sum('SchemeShare'))
    ctp_ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
        AgencyType__AgencyType='Town Panchayat').aggregate(ctp_ulb_share=Sum('ULBShare'))

    context = {
        "tufidco_info": data,
        'gallery_photos': gallery_photos,
        'formSlider': form_slider_photos,
        'mainSlider': main_slider_photos,
        'total_projects': total_projects,
        'project_cost': project_cost,
        'knmt': knmt,
        'ulb_share': ulb_share,
        'dmp_total_projects': dmp_total_projects,
        'dmp_knmt': dmp_knmt,
        'dmp_project_cost': dmp_project_cost,
        'dmp_ulb_share': dmp_ulb_share,
        'ctp_total_projects': ctp_total_projects,
        'ctp_project_cost': ctp_project_cost,
        'ctp_knmt': ctp_knmt,
        'ctp_ulb_share': ctp_ulb_share
    }

    return render(request, 'pages/home.html', context)


def about(request):
    data = tufidco_info.objects.all()
    about_text = About.objects.all()

    context = {
        "tufidco_info": data,
        "about_text": about_text,
    }

    return render(request, 'pages/about.html', context)


def gallery(request):
    data = tufidco_info.objects.all()
    gallery_img = gallery_Images.objects.all()
    gallery_places = gallery_Images.objects.values_list('type', flat=True).order_by('type').distinct()

    context = {
        "tufidco_info": data,
        "gallery": gallery_img,
        "gallery_places": gallery_places,
    }

    return render(request, 'pages/gallery.html', context)


def contact(request):
    data = tufidco_info.objects.all()
    officer = Officer.objects.all()

    context = {
        "tufidco_info": data,
        "Officer": officer,
    }

    return render(request, 'pages/contact.html', context)


def FAQ(request):
    data = tufidco_info.objects.all()
    scheme_name = Scheme_Faq_Questions.objects.order_by('id').filter(name=1)
    scheme_name2 = Scheme_Faq_Questions.objects.order_by('id').filter(name=2)

    context = {
        "tufidco_info": data,
        "Scheme_name": scheme_name,
        "scheme_name2": scheme_name2,
    }

    return render(request, 'pages/faq.html', context)


def KNMT(request):
    data = tufidco_info.objects.all()

    context = {
        "tufidco_info": data,
    }

    return render(request, 'pages/knmtAtGlance.html', context)


def KNMT_AS(request):
    data = tufidco_info.objects.all()

    context = {
        "tufidco_info": data,
    }

    return render(request, 'pages/knmtAdministrativeSanction.html', context)


def S_Chennai(request):
    data = tufidco_info.objects.all()
    scheme = Scheme_Page.objects.filter(scheme=2)

    context = {
        "tufidco_info": data,
        "scheme": scheme
    }

    return render(request, 'pages/singaraChennai.html', context)


def S_Chennai_Guidelines(request):
    data = tufidco_info.objects.all()
    scheme = Scheme_Page.objects.filter(scheme=2)

    context = {
        "tufidco_info": data,
        "scheme": scheme
    }

    return render(request, 'pages/SingaraChennaiGuidelines.html', context)


def S_Chennai_AS(request):
    data = tufidco_info.objects.all()
    scheme = Scheme_Page.objects.filter(scheme=2)
    pdf = SchemeSanctionPdf.objects.filter(scheme=2)

    context = {
        "tufidco_info": data,
        "scheme": scheme,
        "pdf": pdf
    }

    return render(request, 'pages/SingaraChennaiAdministrativeSanction.html', context)


def KNMT_G(request):
    data = tufidco_info.objects.all()
    context = {
        "tufidco_info": data,
    }
    return render(request, 'pages/knmtGuideLines.html', context)


@method_decorator(login_required, name='dispatch')
class EmailAttachementView(View):
    form_class = EmailForm
    template_name = 'admin/contactULB.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            ULB = form.cleaned_data['ULB']
            ULB2 = form.cleaned_data['ULB2']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            user = User.objects.all()
            email = []
            for u in ULB:
                query = user.values_list('email', flat=True).filter(first_name=u)
                email.append(query[0])
            for u1 in ULB2:
                query = user.values_list('email', flat=True).filter(first_name=u1)
                email.append(query[0])
            files = request.FILES.getlist('attach')
            try:
                mail = EmailMessage(subject, message, EMAIL_HOST_USER, email)
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Email Sent Successfully'})
            except:
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name,
                      {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})
