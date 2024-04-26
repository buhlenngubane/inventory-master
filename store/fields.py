from django.db import models
from six import with_metaclass

# Custom lowecase CharField

class UpperCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop('uppercase', False)
        super(UpperCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super(UpperCharField, self).get_prep_value(value)
        return value.upper()