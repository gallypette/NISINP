from django_otp.forms import OTPAuthenticationForm
from django import forms
from .models import Question, QuestionCategory, RegulationType, Services, Sector, Impact, Answer
from django.utils.translation import gettext as _
from operator import is_not
from functools import partial
from datetime import datetime

from django.forms.widgets import ChoiceWidget

# TO DO: change the templates to custom one
class ServicesListCheckboxSelectMultiple(ChoiceWidget):
    allow_multiple_selected = True
    input_type = 'checkbox'
    template_name = 'django/forms/widgets/service_checkbox_select.html'
    option_template_name = 'django/forms/widgets/service_checkbox_option.html'

    def __init__(self, *args, **kwargs):
        super(ServicesListCheckboxSelectMultiple, self).__init__(*args, **kwargs)


# to add the other choice with input text when we are in  MULTI
# TO DO : improve layout
class OtherCheckboxSelectMultiple(ChoiceWidget):

    allow_multiple_selected = True
    input_type = 'checkbox'
    template_name = 'django/forms/widgets/other_checkbox_select.html'
    option_template_name = 'django/forms/widgets/other_checkbox_option.html'

    def __init__(self, *args, **kwargs):
        super(OtherCheckboxSelectMultiple, self).__init__(*args, **kwargs)
    
    #this is the standard optgroups function, just add a hook to add new input
    # and modify the CSS class
    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False
        
        for index, (option_value, option_label) in enumerate(self.choices):
            if option_value is None:
                option_value = ""
            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            other_choices = []
            for subvalue, sublabel in choices:
                selected = (not has_selected or self.allow_multiple_selected) and str(
                    subvalue
                ) in value
                has_selected |= selected
                attrs["class"] = attrs["class"]+" flex-checkbox"
                subgroup.append(
                    self.create_option(
                        name,
                        subvalue,
                        sublabel,
                        selected,
                        index,
                        subindex=subindex,
                        attrs=attrs,
                    )
                )
                if option_label.allowed_additional_answer:
                    other_choices.append(sublabel)
                if subindex is not None:
                    subindex += 1
            for other_choice in other_choices:
                subgroup.append(
                        self.add_other_choice(
                            name,
                            subvalue,
                            other_choice,
                            index,
                            subindex=subindex,
                            attrs=attrs,
                        )
                    )
                if subindex is not None:
                    subindex += 1
        return groups
    
    # function to add the input text
    def add_other_choice(
        self, name, value, label, index, subindex=None, attrs=None
    ):
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        option_attrs = (
            self.build_attrs(self.attrs, attrs) if self.option_inherits_attrs else {}
        )
        if "id" in option_attrs:
            option_attrs["id"] = self.id_for_label(option_attrs["id"], index)+'_answer'
        option_attrs["class"] = "flex-child "
        newValue = ''
        if hasattr(label, 'answer'):
            newValue=label.answer
        else:
            newValue = ''
        return {
            "name": str(value)+'_answer_input',
            "value": newValue,
            "label": label,
            "index": index,
            "attrs": option_attrs,
            "type": 'text',
            "template_name": 'django/forms/widgets/text.html',
            "wrap_label": True,
        }

    
class AuthenticationForm(OTPAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)

# create a form for each category and add fields which represent questions
class QuestionForm(forms.Form):
    label = forms.CharField(widget=forms.HiddenInput(), required=False)
    # for dynamicly add question to forms
    def create_question(self, question, incident = None):
        initial_data = []
        if question.question_type == 'MULTI' or question.question_type == 'MT':
            initial_answer = ''
            choices = []
            if incident is not None:
                initial_data = list(filter(partial(is_not, None),
                    Answer.objects.values_list(
                        'PredifinedAnswer', flat = True).filter(question=question, incident = incident)
                    )
                )
            for choice in question.predifined_answers.all():
                choices.append([choice.id, choice])
            self.fields[str(question.id)] = forms.MultipleChoiceField(
                required= question.is_mandatory,
                choices=choices,
                widget=forms.CheckboxSelectMultiple(
                    #attrs={"class": "multiple-selection"}
                ),
                label=question.label,
                initial = initial_data,
            )
            if question.question_type == 'MT':
                answer = Answer.objects.values_list(
                        'answer', flat = True).filter(question=question, incident = incident)
                if  answer[0] != '':
                    initial_answer = list(filter(partial(is_not, ''),
                        answer
                        )
                    )[0]
                self.fields[str(question.id)+'_answer'] = forms.CharField(
                    required = False,
                    widget=forms.TextInput(
                        attrs = {"class":"multichoice_input_freetext",
                                 "value":str(initial_answer)}
                    ),
                    label='Add precision'
                )
        elif question.question_type == 'DATE':
            initial_data = ''
            if incident is not None:
                answer = Answer.objects.values_list(
                            'answer', flat = True).filter(question=question, incident = incident)
                if len(answer) > 0:
                    initial_data = list(filter(partial(is_not, ''),answer))[0]
                    initial_data = datetime.strptime(initial_data, "%m/%d/%Y").date()
            self.fields[str(question.id)] = forms.DateField(
                widget=forms.SelectDateWidget(),
                required= question.is_mandatory,
                initial=initial_data,
            )
            self.fields[str(question.id)].label = question.label
        elif question.question_type == 'FREETEXT':
            initial_data = ''
            if incident is not None:
                answer = Answer.objects.values_list(
                        'answer', flat = True).filter(question=question, incident = incident)
                if  answer[0] != '':
                    initial_data = list(filter(partial(is_not, ''),
                        answer
                        )
                    )[0]
            self.fields[str(question.id)] = forms.CharField(
                required= question.is_mandatory,
                widget=forms.TextInput(
                    attrs={'value':str(initial_data)}    
                ),
                label = question.label
            )

    def __init__(self, *args, **kwargs):
        questions = Question.objects.all().order_by('position')
        question = questions[1]
        position = -1
        if 'question' in kwargs:
            question = kwargs.pop("question") 
        if 'position' in kwargs:
            position = kwargs.pop("position")
        if 'incident' in kwargs:
            incident = kwargs.pop("incident")
        else:
            incident = None
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
                self.create_question(question, incident)
   
    #get the strange raw data to put in the hidden field
    # def clean(self):
    #     answers = []
    #     for additional_answer in self.additional_answers:
    #         answers.append([additional_answer,self.data.get(additional_answer+'_input')])
    #     cleaned_data = super().clean()
    #     for index, value in answers:
    #         cleaned_data[index] = value
        
            

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
    categs = dict()
    services = Services.objects.all()

    final_categs = []
    for service in services:
        if not categs.get(service.sector):
            categs[service.sector] = [[service.id, service]]
        else:
            categs[service.sector].append([service.id, service])

    for sector, list_of_options in categs.items():
        name = sector.name
        while sector.parent is not None:
            name = sector.parent.name+' - '+name
            sector = sector.parent
        # [optgroup, [options]]
        final_categs.append([name, list_of_options])

    return final_categs

    # choices_serv = []
    # for root_category in root_categories:
    #     #keep integer for the services to avoid to register a false services
    #     choices_serv.append(['service'+ str(root_category.id), root_category])
    #     for service in Services.objects.all().filter(sector=root_category):
    #         choices_serv.append([service.id,service])
    #     if(len(Sector.objects.all().filter(parent=root_category))>0):
    #             choices_serv += construct_services_array(Sector.objects.all().filter(parent=root_category))

    # return choices_serv

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
        widget=ServicesListCheckboxSelectMultiple(
            attrs={"class": "multiple-selection"}
        ),
    )

class ImpactForFinalNotificationForm(forms.Form):
    #list of impact present in the incident table
    initial_data = []
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
    def create_questions(self, affected_services, initial_data = []):
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
                    initial = initial_data
                )

    def __init__(self, *args, **kwargs):
        if 'incident' in kwargs:
            incident = kwargs.pop("incident") 
            # get initial data if there are existing
            if incident is not None:
                initial_data = list(incident.impacts.values_list('id', flat=True))
            affected_services = incident.affected_services.all()
            super(ImpactForFinalNotificationForm, self).__init__(*args, **kwargs)
            self.create_questions(affected_services, initial_data)
        else:
            super(ImpactForFinalNotificationForm, self).__init__(*args, **kwargs)
        #init the generic choices
        self.fields['generic_impact'].choices = [
            (k.id, k.label)
            for k in Impact.objects.all().filter(is_generic_impact = True)
        ]
        self.fields['generic_impact'].initial = initial_data
        

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
