from . import views
from django.urls import path, include 
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
# router = routers.DefaultRouter()
# router.register(r'all-ideas', views.IdeaViewSet)
# router.register(r'cnwl', views.CNWLIdeaViewSet)


urlpatterns = [
    #url path for submitting idea
    path ('<slug:orgslug>/submit-idea/', views.SubmitIdea.as_view(), name='submit_idea'),
    path ('<slug:orgslug>/submit-idea-criteria/', views.idea_criteria_form, name='idea_criteria'),
    path('<slug:orgslug>/submit-idea-success/', views.submit_success, name='idea_submit_success'),

    #url path for viewing ideas, e.g. latest ideas, ideas within data department and ect.
    path ('<slug:slug>/view-ideas/', views.IdeaList.as_view(), name='view_ideas_default'),
    path ('<slug:slug>/view-ideas-health/', views.IdeaListHealth.as_view(), name='view_ideas'),
    path ('<slug:slug>/view-ideas-culture/', views.IdeaListCulture.as_view(), name='view_ideas'),
    path ('<slug:slug>/view-ideas-job-satisfaction/', views.IdeaListJobSatifiction.as_view(), name='view_ideas'),
    path ('<slug:slug>/view-ideas-relationships/', views.IdeaListRelationships.as_view(), name='view_ideas'),
    path ('<slug:slug>/view-ideas-leadership/', views.IdeaListLeadership.as_view(), name='view_ideas'),
    path ('<slug:slug>/view-ideas-data/', views.IdeaListData.as_view(), name='view_ideas'),
    path ('<slug:slug>/view-ideas-pridar/', views.IdeaListPridar.as_view(), name='view_ideas'),
    path ('<slug:slug>/view-ideas/<slug:month>/<int:int>', views.IdeaListMonth.as_view(), name='view_ideas'),
    # path ('<slug:slug>/view-idea/', views.view_idea, name='view_idea'),

    # path('<slug:slug>/idea-store/', views.IdeaStore.as_view(), name='bloghub'),
    # path('<slug:slug>/pridar/', views.IdeaStoreOrgSpecific.as_view(), name='bloghub_org_specific'),
    # path('<slug:slug>/health/', views.IdeaStoreHealth.as_view(), name='bloghub_health'),
    # path('<slug:slug>/culture/', views.IdeaStoreCulture.as_view(), name='bloghub_culture'),
    # path('<slug:slug>/job-satisfaction/', views.IdeaStoreJobSatisfaction.as_view(), name='bloghub_job_satisfaction'),
    # path('<slug:slug>/relationships/', views.IdeaStoreRelationships.as_view(), name='bloghub_relationships'),
    # path('<slug:slug>/<slug:month>/<int:int>', views.IdeaStoreMonth.as_view(), name='bloghub_month'),
    # path('<slug:slug>/leadership/', views.IdeaStoreLeadership.as_view(), name='bloghub_leadership'),
    # path('<slug:slug>/data/', views.IdeaStoreData.as_view(), name='bloghub_data'),
    # path('<slug:slug>/search-blog/', views.search_blog, name='search_blog'),
    # path('<slug:slug>/submit-challenge-form-1/', views.submit_challenge, name='submit_challenge'),
    # path('<slug:slug>/submit-challenge-successful/', views.submit_challenge_successful, name='submit_challenge_successful'),
    # # path('add-category/', views.add_category_view.as_view(), name='add_category'),
    # path('<slug:slug>/management-dashboard/', views.IdeaStore.as_view(), name='dashboard'),
    # path('<slug:slug>/completed-challenges/', views.IdeaStoreCompleted.as_view(), name='completed_challenges'),
    # path('<slug:slug>/pending-ideas/', views.PendingIdeasList.as_view(), name='pending_ideas'),
    # path('<slug:slug>/statistics/', views.Statistics.as_view(), name='stats'),

    # path('challenge-history/completed-challenges/', views.HistoryListCompleted.as_view(), name='history_completed'),
    # path('<slug:slug>/challenge-history/ideas/open/<int:pk>', views.IdeaListOpen.as_view(), name='open_ideas'),
    # path('<slug:slug>/challenge-history/ideas/under-review/<int:pk>', views.IdeaListReview.as_view(), name='in_review_ideas'),
    # path('<slug:slug>/challenge-history/ideas/accepted/<int:pk>', views.IdeaListAccepted.as_view(), name='accepted_ideas'),
    # path('<slug:slug>/challenge-history/ideas/in-development/<int:pk>', views.IdeaListInDev.as_view(), name='in_dev_ideas'),
    # path('<slug:slug>/challenge-history/ideas/delivered/<int:pk>', views.IdeaListDelivered.as_view(), name='delivered_ideas'),
    # path('<slug:slug>/challenge-history/', views.History.as_view(), name='challenge_history'),
    # path('<slug:slug>/challenge-history/lifecycle/<int:pk>', views.lifecycle, name='lifecycle'),
    # path('<slug:orgslug>/<int:pk>/<slug:slug>/manage-ideas/', views.IdeaManagementDetail.as_view(), name='idea_management_detail'),
    # path('<slug:orgslug>/<int:pk>/<slug:slug>/manage/approve', views.approve_idea, name='approve_idea'),
    # path('<slug:orgslug>/<int:pk>/manage/<slug:slug>/reject', views.reject_idea, name='reject_idea'),
    # path('router/', include(router.urls)),
    # path('selected-ideas/', views.IdeaViewSet, name='selected_ideas'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('search-selected-idea/', views.search_idea, name='search_selected_idea'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


