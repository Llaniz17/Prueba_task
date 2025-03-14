from django import forms
from .models import Task
from django.utils.timezone import now  

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'city']

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')

        # Si due_date es None, no se valida pues se permite vacio
        if due_date and due_date < now().date():
            raise forms.ValidationError("La fecha de vencimiento debe ser despues o igual a la fecha actual (HOY)")
        
        return due_date
