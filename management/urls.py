from . import views
from django.urls import path, include

urlpatterns = [
    path('<slug:slug>/management-dashboard/', views.PostList.as_view(), name='dashboard'),
    path('<slug:slug>/completed-challenges/', views.PostListCompleted.as_view(), name='completed_challenges'),
    path('<slug:slug>/pending-ideas/', views.PendingIdeasList.as_view(), name='pending_ideas'),
    path('<slug:slug>/approved-ideas/', views.ApprovedIdeaList.as_view(), name='approved_ideas'),

    path('<slug:orgslug>/<int:pk>/<slug:slug>/manage-challenges/', views.PostManagementDetail.as_view(), name='post_management_detail'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/manage-ideas/', views.IdeaManagementDetail.as_view(), name='idea_management_detail'),

    path('<slug:orgslug>/<int:pk>/<slug:slug>/manage/approve', views.approve_idea, name='approve_idea'),
    path('<slug:orgslug>/<int:pk>/manage/<slug:slug>/reject', views.reject_idea, name='reject_idea'),

]