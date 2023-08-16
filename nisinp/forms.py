from django_otp.forms import OTPAuthenticationForm
from django import forms
from .models import Question, QuestionCategory, RegulationType, Services, Sector, Impact
from django.utils.translation import gettext as _

class AuthenticationForm(OTPAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)

# create a form for each category and add fields which represent questions
class QuestionForm(forms.Form):

    label = forms.CharField(widget=forms.HiddenInput(), required=False)
    # for dynamicly add question to forms
    def create_question(self, question):
        if question.question_type == 'MULTI':
            choices = []
            for choice in question.predifined_answers.all():
                choices.append([choice.id, choice])
            self.fields[str(question.id)] = forms.MultipleChoiceField(
                required= question.is_mandatory,
                choices=choices,
                widget=forms.CheckboxSelectMultiple(
                    attrs={"class": "multiple-selection"}
                ),
                label=question.label,
            )
        elif question.question_type == 'DATE':
            self.fields[str(question.id)] = forms.DateField(
                widget=forms.SelectDateWidget(),
                required= question.is_mandatory,
            )
            self.fields[str(question.id)].label = question.label
        elif question.question_type == 'FREETEXT':
            self.fields[str(question.id)] = forms.CharField(required= question.is_mandatory)
            self.fields[str(question.id)].label = question.label

    def __init__(self, *args, **kwargs):
        questions = Question.objects.all().order_by('position')
        question = questions[1]
        position = -1
        if 'question' in kwargs:
            question = kwargs.pop("question") 
        if 'position' in kwargs:
            position = kwargs.pop("position")
        if 'is_preliminary' in kwargs:
            is_preliminary = kwargs.pop("is_preliminary")
        else:
            is_preliminary = True
        super(QuestionForm, self).__init__(*args, **kwargs)
        
        if position > -1:
            question = questions[position] 
            categories = QuestionCategory.objects.all().order_by(
            'position').filter(question__is_preliminary = is_preliminary).distinct()
            category = categories[position]
            questions = Question.objects.all().filter(category=category, is_preliminary= is_preliminary)
            for question in questions:
                self.create_question(question)
            

# the first question for preliminary notification
class ContactForm(forms.Form):   
    company_name = forms.CharField(label="Company name", max_length=100)

    contact_lastname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "contact_lastname"}
        ),
    )
    contact_firstname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "contact_firstname"}
        ),
    )
    contact_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "contact_title"}
        ),
    )
    contact_email = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "contact_email"}
        ),
    )
    contact_telephone = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "contact_telephone"}
        ),
    )

    is_technical_the_same = forms.BooleanField(
        required = False,
        widget=forms.CheckboxInput(
           attrs={"class": "required checkbox ",
                  'onclick': "if (checked==true) {"+
                    "document.getElementsByClassName('technical_lastname')[0].value="+
                        "document.getElementsByClassName('contact_lastname')[0].value; "+
                    "document.getElementsByClassName('technical_firstname')[0].value="+
                        "document.getElementsByClassName('contact_firstname')[0].value; "+
                    "document.getElementsByClassName('technical_title')[0].value="+
                        "document.getElementsByClassName('contact_title')[0].value; "+
                    "document.getElementsByClassName('technical_email')[0].value="+
                        "document.getElementsByClassName('contact_email')[0].value; "+
                    "document.getElementsByClassName('technical_telephone')[0].value="+
                        "document.getElementsByClassName('contact_telephone')[0].value;}"}
        ),
        initial = False
    )
    technical_lastname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "technical_lastname"}
        ),
    )
    technical_firstname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "technical_firstname"}
        ),
    )
    technical_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "technical_title"}
        ),
    )
    technical_email = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "technical_email"}
        ),
    )
    technical_telephone = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
           attrs={"class": "technical_telephone"}
        ),
    )

    incident_reference = forms.CharField(max_length=255)
    complaint_reference = forms.CharField(max_length=255)

    def prepare_initial_value(**kwargs):
        request = kwargs.pop("request") 
        if request.user.is_authenticated:
            return {
                    'contact_lastname' : request.user.last_name,
                    'contact_firstname' : request.user.first_name,
                    'contact_email' : request.user.email,
                    'contact_telephone' : request.user.phone_number,
                }
        return {}

# prepare an array of sector and services        
def construct_services_array(root_categories):
    choices_serv = []
    for root_category in root_categories:
        #keep integer for the services to avoid to register a false services
        choices_serv.append(['service'+ str(root_category.id), root_category])
        for service in Services.objects.all().filter(sector=root_category):
            choices_serv.append([service.id,service])
        if(len(Sector.objects.all().filter(parent=root_category))>0):
                choices_serv += construct_services_array(Sector.objects.all().filter(parent=root_category))

    return choices_serv

# the affected services with services load from services table
class ImpactedServicesForm(forms.Form):
   
    choices_serv = construct_services_array(
        Sector.objects.all().filter(parent=None),
    )
    choices_rt = []
    for choice in RegulationType.objects.all():
            choices_rt.append([choice.id, choice])

    regulation = forms.MultipleChoiceField(
        required = False,
        choices = choices_rt,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "multiple-selection"}
        ),
    )
    affected_services = forms.MultipleChoiceField(
        required = False,
        choices = choices_serv,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "multiple-selection"}
        ),
    )

class ImpactForFinalNotificationForm(forms.Form):
    # generic impact definitions
    generic_impact = forms.MultipleChoiceField(
        required= False,
        choices=[],
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "multiple-selection"}
        ),
        label='Generic impacts',
    )

    # create the questions for the impacted sectors
    def create_questions(self, affected_services):
        sectors = []
        for service in affected_services:
            sectors.append(service.sector)
            for sector in sectors:
                choices = [
                    (k.id, k.label)
                    for k in sector.specific_impact.all()
                ]
                self.fields[str(sector.id)] = forms.MultipleChoiceField(
                    required= False,
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple(
                        attrs={"class": "multiple-selection"}
                    ),
                    label=sector.name,
                )

    def __init__(self, *args, **kwargs):
        if 'incident' in kwargs:
            incident = kwargs.pop("incident") 
            super(ImpactForFinalNotificationForm, self).__init__(*args, **kwargs)
            affected_services = incident.affected_services.all()
            super(ImpactForFinalNotificationForm, self).__init__(*args, **kwargs)
            self.create_questions(affected_services)
        else:
            super(ImpactForFinalNotificationForm, self).__init__(*args, **kwargs)
        #init the generic choices
        self.fields['generic_impact'].choices = [
            (k.id, k.label)
            for k in Impact.objects.all().filter(is_generic_impact = True)
        ]
        

def get_number_of_question(is_preliminary = True):
    categories = QuestionCategory.objects.all().filter(question__is_preliminary = is_preliminary).distinct()
    
    if is_preliminary is True:
        category_tree = [ContactForm]
        category_tree.append(ImpactedServicesForm)
    else:
        category_tree = [ImpactForFinalNotificationForm]

    for category in categories:
        category_tree.append(QuestionForm)           
    
    return category_tree
