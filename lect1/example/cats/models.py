from django.db import models
from django.forms import ModelForm, ValidationError

class Cat( models.Model):
    name = models.CharField( max_length=72 )
    age = models.IntegerField( default=0 )

class CatForm( ModelForm ):
    class Meta:
        model = Cat
        fields = [ "name", "age" ]
    
    def clean_age(self):
        age = self.cleaned_data['age']
        if age > 30:
            raise ValidationError( "Cat's age more then 30 years." )
        return age


