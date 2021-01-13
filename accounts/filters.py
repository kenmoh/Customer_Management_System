import django_filters
from django_filters import DateFilter, CharFilter
from .models import Order
from django import forms


class OrderFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name='date_created', label='Date greater than', lookup_expr='gte', widget=forms.DateInput(
        attrs={
            'id': 'datepicker',
            'placeholder': '12/06/2020'
        }
    ))
    end_date = DateFilter(field_name='date_created', label='Date less than', lookup_expr='lte', widget=forms.DateInput(
        attrs={
            'class': 'datepicker',
            'placeholder': '12/06/2020'
        }
    ))
    description = CharFilter(field_name='description',label='Search by word', lookup_expr='icontains', widget=forms.DateInput(
        attrs={
            'class': '',
            'placeholder': 'Enter keywords'
        }
    ))

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']