from . import views
from django.urls import path, include 
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
router = routers.DefaultRouter()
router.register(r'all-ideas', views.IdeaViewSet)
router.register(r'cnwl', views.CNWLIdeaViewSet)


urlpatterns = [
    path('<slug:slug>/submit-challenge-form-1/', views.submit_challenge, name='submit_challenge'),
    path('<slug:slug>/submit-challenge-successful/', views.submit_challenge_successful, name='submit_challenge_successful'),
    # path('add-category/', views.add_category_view.as_view(), name='add_category'),
    path('<slug:slug>/statistics/', views.Statistics.as_view(), name='stats'),

    path('challenge-history/completed-challenges/', views.HistoryListCompleted.as_view(), name='history_completed'),
    path('<slug:slug>/challenge-history/ideas/open/<int:pk>', views.IdeaListOpen.as_view(), name='open_ideas'),
    path('<slug:slug>/challenge-history/ideas/under-review/<int:pk>', views.IdeaListReview.as_view(), name='in_review_ideas'),
    path('<slug:slug>/challenge-history/ideas/accepted/<int:pk>', views.IdeaListAccepted.as_view(), name='accepted_ideas'),
    path('<slug:slug>/challenge-history/ideas/in-development/<int:pk>', views.IdeaListInDev.as_view(), name='in_dev_ideas'),
    path('<slug:slug>/challenge-history/ideas/delivered/<int:pk>', views.IdeaListDelivered.as_view(), name='delivered_ideas'),
    path('<slug:slug>/challenge-history/', views.History.as_view(), name='challenge_history'),
    path('<slug:slug>/challenge-history/lifecycle/<int:pk>', views.lifecycle, name='lifecycle'),
    path('router/', include(router.urls)),
    path('selected-ideas/', views.IdeaViewSet, name='selected_ideas'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('search-selected-idea/', views.search_idea, name='search_selected_idea'),
    path('<slug:slug>/ideas/<slug:stage>', views.trustnet_api),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


