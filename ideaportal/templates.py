from organisations.models import Organisation
from django.views.generic import ListView
from django.db.models import Model
import logging

class ListViewTemplate(ListView):

    template_name: str = None
    model: Model = None
    paginate_by: int = None
    portal_choice: Organisation = None

    def _filter_queryset(self, queryset):
        """Override this method to filter the Model

        Note: The queryset is already filtered by Organisation. 
        Example of use: queryset.filter(xxx=x).order_by('xxx')
        """
        return queryset

    def get_queryset(self, *args, **kwargs):
        self.portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        queryset = self.model.objects.filter(org_tag=self.portal_choice)
        return self._filter_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['org'] = self.portal_choice
        context['orgslug'] = self.portal_choice.slug
        return context