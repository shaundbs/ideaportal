from . import views
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

# router = routers.DefaultRouter()
# router.register(r'all-ideas', views.IdeaViewSet)
# router.register(r'cnwl', views.CNWLIdeaViewSet)


urlpatterns = [
    # url path for submitting idea
    path("<slug:orgslug>/submit-idea/", views.SubmitIdea.as_view(), name="submit_idea"),
    path("<slug:orgslug>/submit-idea-criteria/", views.idea_criteria_form, name="idea_criteria"),
    path("<slug:orgslug>/submit-idea-success/", views.submit_success, name="idea_submit_success"),
    # url path for viewing ideas, e.g. latest ideas, ideas within data department and ect.
    path("<slug:slug>/view-ideas/", views.IdeaList.as_view(), name="view_ideas_default"),
    path("<slug:slug>/view-ideas-health/", views.IdeaListHealth.as_view(), name="view_ideas_health"),
    path("<slug:slug>/view-ideas-culture/", views.IdeaListCulture.as_view(), name="view_ideas_culture"),
    path("<slug:slug>/view-ideas-job-satisfaction/", views.IdeaListJobSatifiction.as_view(), name="view_ideas_job_sat"),
    path(
        "<slug:slug>/view-ideas-relationships/", views.IdeaListRelationships.as_view(), name="view_ideas_relationships"
    ),
    path("<slug:slug>/view-ideas-leadership/", views.IdeaListLeadership.as_view(), name="view_ideas_leadership"),
    path("<slug:slug>/view-ideas-data/", views.IdeaListData.as_view(), name="view_ideas_data"),
    path("<slug:slug>/view-ideas-pridar/", views.IdeaListPridar.as_view(), name="view_ideas_pridar"),
    path("<slug:slug>/view-ideas/<slug:month>/<int:int>", views.IdeaListMonth.as_view(), name="view_ideas_month"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
