from . import views
from django.urls import path, include 
   
urlpatterns = [
    path('<slug:slug>/submit-challenge-form-1/', views.submit_challenge, name='submit_challenge'),
    path('<slug:slug>/submit-challenge-successful/', views.submit_challenge_successful, name='submit_challenge_successful'),
    path('add-category/', views.add_category_view.as_view(), name='add_category'),
    path('<slug:slug>/management-dashboard/', views.PostList.as_view(), name='dashboard'),
    path('completed-challenges/', views.PostListCompleted.as_view(), name='completed_challenges'),
    path('challenge-history/', views.challenge_history, name='challenge_history'),
]


