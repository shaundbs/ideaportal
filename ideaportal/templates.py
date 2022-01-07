from organisations.models import Organisation
from django.views.generic import ListView
from django.db.models import Model, QuerySet
import logging

class ListViewTemplate(ListView):

    template_name: str = None
    model: Model = None
    paginate_by: int = None
    portal_choice: Organisation = None

    def _filter_queryset(self, queryset):
        """Override this method to filter the Model

        e.g. self.model.objects.filter(xxx=x).order_by('xxx')
        """
        return queryset

    def get_queryset(self, *args, **kwargs):
        portal_choice = Organisation.objects.get(slug=self.kwargs['slug'])
        logging.error(portal_choice)
        self.portal_choice = portal_choice
        queryset = self.model.objects.filter(Organisation=self.portal_choice)
        return self._filter_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['org'] = self.portal_choice
        context['orgslug'] = self.portal_choice.slug
        return context