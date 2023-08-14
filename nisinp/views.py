from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django_otp.decorators import otp_required

from .forms import  ContactForm, QuestionForm, get_number_of_question, ImpactForFinalNotificationForm
from .models import Incident, Answer, Question, PredifinedAnswer

import datetime


from django.http import HttpResponseRedirect

from nisinp.settings import SITE_NAME

from formtools.wizard.views import SessionWizardView

@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        return redirect("admin:index")

def logout_view(request):
    logout(request)
    return redirect("login")


def terms(request):
    return render(request, "home/terms.html", context={"site_name": SITE_NAME})


def privacy(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})

def index(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})

def notifications(request):
    return render(request, "notification/index.html", context={"site_name": SITE_NAME})

# initialize data for the preliminary notification
def get_form_list(request, form_list=None):
    if form_list is None: 
        form_list = get_number_of_question()
    return FormWizardView.as_view(
        form_list,
        initial_dict={'0': ContactForm.prepare_initial_value(request=request)},
    )(request)

def get_final_notification_list(request, form_list=None, pk = None):
    if form_list is None: 
        form_list = get_number_of_question(is_preliminary = False)
    if pk is not None: 
        request.incident = pk        
    return FinalNotificationWizardView.as_view(
        form_list,
    )(request)



#get the list of incident
@login_required
def get_incident_list(request):
    user = request.user
    incidents = Incident.objects.all().order_by(
        'preliminary_notification_date').filter(contact_user=user)
    return render(
        request, 
        "notification/incident_list.html", 
        context={"site_name": SITE_NAME, "incidents": incidents}
    )

# Wizard to manage the preliminary form
class FormWizardView(SessionWizardView):
    template_name = "notification/declaration.html"

    def __init__(self, **kwargs):
        self.form_list = kwargs.pop('form_list')
        self.initial_dict = kwargs.pop('initial_dict')
        return super(FormWizardView, self).__init__(**kwargs)
        
    def get_form(self, step=None, data=None, files=None):
        if step is None:
            step = self.steps.current
        position = int(step)
        # when we have passed the fixed forms
        if position > 1:
            print(position)
            # create the form with the correct question/answers
            form = QuestionForm(data, position=position-2)

            return form
        else:
            form = super(FormWizardView, self).get_form(step, data, files)
        return form

    
    def done(self, form_list, **kwargs):
        data = [form.cleaned_data for form in form_list]
        print(data)
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        incident = Incident.objects.create(
            contact_lastname = data[0]['contact_lastname'],
            contact_firstname = data[0]['contact_firstname'],
            contact_title = data[0]['contact_title'],
            contact_email = data[0]['contact_email'],
            contact_telephone = data[0]['contact_telephone'],
            #technical contact
            technical_lastname = data[0]['technical_lastname'],
            technical_firstname = data[0]['technical_firstname'],
            technical_title = data[0]['technical_title'],
            technical_email = data[0]['technical_email'],
            technical_telephone = data[0]['technical_telephone'],
            
            incident_reference = data[0]['incident_reference'],
            complaint_reference = data[0]['complaint_reference'],
            contact_user = user
        )
        for regulation in data[1]['regulation']:
            incident.regulations.add(regulation)
        for service in data[1]['affected_services']:
            try:
                service = int(service)
                incident.affected_services.add(service)
            except:
                pass
        
        for d in range(2, len(data)):
            print('data d')
            print(data[d])
            for key, value in data[d].items():
                question_id = None
                try:
                    question_id = int(key)
                except:
                    pass
                if question_id is not None:
                    print('key')
                    print(key)
                    print('value')
                    print(value)
                    question = Question.objects.get(pk=key)
                    if question.question_type == 'FREETEXT':
                        answer = value
                        predifinedAnswer = None
                    elif question.question_type =='DATE':
                        answer = value.strftime('%m/%d/%Y')
                        predifinedAnswer
                    else : 
                        predifinedAnswers = []
                        for val in value:
                            predifinedAnswer = PredifinedAnswer.objects.get(pk=val)
                            predifinedAnswers.append(predifinedAnswer)
                        answer = None
                    answer_object = Answer.objects.create(
                        incident = incident,
                        question = question,
                        answer = answer,
                    )
                    answer_object.PredifinedAnswer.set(predifinedAnswers)

        return HttpResponseRedirect("incident_list")
    
# Wizard to manage the final notification form
class FinalNotificationWizardView(SessionWizardView):
    template_name = "notification/declaration.html"
    incident = None

    def __init__(self, **kwargs):
        self.form_list = kwargs.pop('form_list')
        return super(FinalNotificationWizardView, self).__init__(**kwargs)

    def get_form(self, step=None, data=None, files=None):
        #we get the incident
        print('self.request')
        print(self.request.incident)
        if self.request.incident:
            self.incident = Incident.objects.get(pk=self.request.incident)
        print(self.incident)
        if step is None:
            step = self.steps.current
        position = int(step)
        # when we have passed the fixed forms
        if position == 0:
            print(position)
            # create the form with the correct question/answers
            form = ImpactForFinalNotificationForm(data, incident=self.incident)

            return form
            # if not form.is_valid():
            #     print('form.errors')
            #     print(form.errors)
            #     print('form.is_bound')
            #     print(form.is_bound)
            

        else:
            form = super(FinalNotificationWizardView, self).get_form(step, data, files)
        return form

    
    def done(self, form_list, **kwargs):
        data = [form.cleaned_data for form in form_list]
        position = 0
        # for form in form_list:
        #     print(position)
        #     if position >1:
        #         for f in form.forms:
        #             data.append(f.cleaned_data)
        #     else:
        #         data.append(form.cleaned_data)
        #     position = position +1
        print(data)
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        incident = Incident.objects.create(
            contact_lastname = data[0]['contact_lastname'],
            contact_firstname = data[0]['contact_firstname'],
            contact_title = data[0]['contact_title'],
            contact_email = data[0]['contact_email'],
            contact_telephone = data[0]['contact_telephone'],
            #technical contact
            technical_lastname = data[0]['technical_lastname'],
            technical_firstname = data[0]['technical_firstname'],
            technical_title = data[0]['technical_title'],
            technical_email = data[0]['technical_email'],
            technical_telephone = data[0]['technical_telephone'],
            
            incident_reference = data[0]['incident_reference'],
            complaint_reference = data[0]['complaint_reference'],
            contact_user = user
        )
        for regulation in data[1]['regulation']:
            incident.regulations.add(regulation)
        for service in data[1]['affected_services']:
            try:
                service = int(service)
                incident.affected_services.add(service)
            except:
                pass
        
        for d in range(2, len(data)):
            print('data d')
            print(data[d])
            for key, value in data[d].items():
                question_id = None
                try:
                    question_id = int(key)
                except:
                    pass
                if question_id is not None:
                    print('key')
                    print(key)
                    print('value')
                    print(value)
                    question = Question.objects.get(pk=key)
                    if question.question_type == 'FREETEXT':
                        answer = value
                        predifinedAnswer = None
                    elif question.question_type =='DATE':
                        answer = value.strftime('%m/%d/%Y')
                        predifinedAnswer
                    else : 
                        predifinedAnswers = []
                        for val in value:
                            predifinedAnswer = PredifinedAnswer.objects.get(pk=val)
                            predifinedAnswers.append(predifinedAnswer)
                        answer = None
                    answer_object = Answer.objects.create(
                        incident = incident,
                        question = question,
                        answer = answer,
                    )
                    answer_object.PredifinedAnswer.set(predifinedAnswers)

        
        # return render(self.request, 'incident_list', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })
        return HttpResponseRedirect("incident_list")
    
    