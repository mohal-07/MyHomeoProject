# core/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Case, PastIllness
import re # For basic validation checks if needed

# Widgets
textarea_widget = forms.Textarea(attrs={'rows': 3, 'class': 'formbold-form-input'})
input_widget = forms.TextInput(attrs={'class': 'formbold-form-input'})
number_widget = forms.NumberInput(attrs={'class': 'formbold-form-input'})
date_widget = forms.DateInput(attrs={'class': 'formbold-form-input', 'type': 'date'})
select_widget = forms.Select(attrs={'class': 'formbold-form-input'})


class CaseForm(forms.ModelForm):
    # --- Fields corresponding to structured JSON data in the model ---
    personal_thermal_state = forms.CharField(required=False, widget=input_widget, label="Thermal State")
    personal_perspiration = forms.CharField(required=False, widget=input_widget, label="Perspiration")
    personal_appetite = forms.CharField(required=False, widget=input_widget, label="Appetite")
    personal_diet = forms.CharField(required=False, widget=input_widget, label="Diet")
    personal_desire = forms.CharField(required=False, widget=input_widget, label="Desire")
    personal_aversion = forms.CharField(required=False, widget=input_widget, label="Aversion")
    personal_thirst = forms.CharField(required=False, widget=input_widget, label="Thirst")
    personal_urine = forms.CharField(required=False, widget=input_widget, label="Urine")
    personal_bowels = forms.CharField(required=False, widget=input_widget, label="Bowels")
    personal_habits_addiction = forms.CharField(required=False, widget=input_widget, label="Habits/Addiction")
    personal_sleep = forms.CharField(required=False, widget=input_widget, label="Sleep")
    personal_dreams = forms.CharField(required=False, widget=textarea_widget, label="Dreams")
    personal_other = forms.CharField(required=False, widget=textarea_widget, label="Other Personal History Notes") # <-- ADDED

    menstrual_age_of_puberty = forms.CharField(required=False, widget=input_widget, label="Age of Puberty")
    menstrual_menses = forms.CharField(required=False, widget=input_widget, label="Menses (Cycle/Duration/Flow)")
    menstrual_menses_complaints = forms.CharField(required=False, widget=textarea_widget, label="Complaints During Menses")
    menstrual_age_at_marriage = forms.CharField(required=False, widget=input_widget, label="Age at Marriage")
    menstrual_lmp = forms.CharField(required=False, widget=input_widget, label="LMP (Last Menstrual Period)")
    menstrual_menses_triggers = forms.CharField(required=False, widget=input_widget, label="Menses Triggers")
    menstrual_leucorrhea = forms.CharField(required=False, widget=input_widget, label="Leucorrhea Details")
    menstrual_pregnancy = forms.CharField(required=False, widget=textarea_widget, label="Pregnancy History (G/P/L/A)")
    menstrual_menopause_age = forms.CharField(required=False, widget=input_widget, label="Menopause Age")
    menstrual_menopause_complaints = forms.CharField(required=False, widget=textarea_widget, label="Menopause Complaints")

    physical_built = forms.CharField(required=False, widget=input_widget, label="Built")
    physical_head = forms.CharField(required=False, widget=input_widget, label="Head")
    physical_throat = forms.CharField(required=False, widget=input_widget, label="Throat")
    physical_hair = forms.CharField(required=False, widget=input_widget, label="Hair")
    physical_mouth = forms.CharField(required=False, widget=input_widget, label="Mouth")
    physical_ear = forms.CharField(required=False, widget=input_widget, label="Ear")
    physical_nails = forms.CharField(required=False, widget=input_widget, label="Nails")
    physical_tongue = forms.CharField(required=False, widget=input_widget, label="Tongue")
    physical_eyes = forms.CharField(required=False, widget=input_widget, label="Eyes")
    physical_extremities = forms.CharField(required=False, widget=input_widget, label="Extremities")
    physical_teeth = forms.CharField(required=False, widget=input_widget, label="Teeth")
    physical_skin = forms.CharField(required=False, widget=input_widget, label="Skin")
    physical_lymph_glands = forms.CharField(required=False, widget=input_widget, label="Lymph Glands")
    physical_gums = forms.CharField(required=False, widget=input_widget, label="Gums")
    physical_nose = forms.CharField(required=False, widget=input_widget, label="Nose")
    physical_bp = forms.CharField(required=False, widget=input_widget, label="BP")
    physical_temperature = forms.CharField(required=False, widget=input_widget, label="Temperature")
    physical_pulse = forms.CharField(required=False, widget=input_widget, label="Pulse")
    physical_rr = forms.CharField(required=False, widget=input_widget, label="RR (Respiratory Rate)")
    physical_spo2 = forms.CharField(required=False, widget=input_widget, label="SpO2")
    physical_other = forms.CharField(required=False, widget=textarea_widget, label="Other Physical Examination Notes") # <-- ADDED

    class Meta:
        model = Case
        # These are the direct fields saved to the Case model (excluding JSON fields)
        fields = [
            'date', 'opd_no', 'patient_name', 'patient_age', 'patient_sex',
            'patient_occupation', 'patient_address', 'patient_phone',
            'presenting_complaints', 'history_of_present_illness',
            'past_history_vaccination', 'family_history',
            'patient_as_person', 'systemic_examination',
        ]
        widgets = { # Assign widgets for direct model fields
            'date': date_widget,
            'opd_no': input_widget,
            'patient_name': input_widget,
            'patient_age': input_widget,
            'patient_sex': select_widget,
            'patient_occupation': input_widget,
            'patient_address': textarea_widget,
            'patient_phone': input_widget,
            'presenting_complaints': textarea_widget,
            'history_of_present_illness': textarea_widget,
            'past_history_vaccination': textarea_widget,
            'family_history': textarea_widget,
            'patient_as_person': textarea_widget,
            'systemic_examination': textarea_widget,
        }
        labels = {
            'patient_name': 'Patient Name *',
            'presenting_complaints': 'Presenting Complaints *',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make patient_name and presenting_complaints required in the form display
        self.fields['patient_name'].required = True
        self.fields['presenting_complaints'].required = True
        # Ensure all other fields are NOT required
        for field_name, field in self.fields.items():
            if field_name not in ['patient_name', 'presenting_complaints']:
                field.required = False


    def clean_opd_no(self):
        opd_no = self.cleaned_data.get('opd_no')
        return opd_no


class PastIllnessForm(forms.ModelForm):
    class Meta:
        model = PastIllness
        fields = ['disease', 'approximate_age', 'duration', 'treatment', 'completely_recovered']
        widgets = { # Assign widgets as before
             'disease': input_widget,
             'approximate_age': input_widget,
             'duration': input_widget,
             'treatment': textarea_widget,
             'completely_recovered': input_widget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional in the formset rows
        for field in self.fields.values():
            field.required = False


PastIllnessFormSet = inlineformset_factory(
    Case,
    PastIllness,
    form=PastIllnessForm,
    extra=1, # Start with one empty form
    can_delete=True # Allow deletion
)