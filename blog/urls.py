from . import views
from django.urls import path, include
import challenges.views as cviews

urlpatterns = [
    path('<slug:slug>/live-polls/', views.PostList.as_view(), name='bloghub'),
    path('<slug:slug>/health/', views.PostListHealth.as_view(), name='bloghub_health'),
    path('<slug:slug>/culture/', views.PostListCulture.as_view(), name='bloghub_culture'),
    path('<slug:slug>/job-satisfaction/', views.PostListJobSatisfaction.as_view(), name='bloghub_job_satisfaction'),
    path('<slug:slug>/relationships/', views.PostListRelationships.as_view(), name='bloghub_relationships'),
    path('<slug:slug>/<slug:month>/<int:int>', views.PostListMonth.as_view(), name='bloghub_month'),
    path('<slug:slug>/pridar/', views.PostListOrgSpecific.as_view(), name='bloghub_org_specific'),


    path('<slug:slug>/leadership/', views.PostListLeadership.as_view(), name='bloghub_leadership'),
    path('<slug:slug>/data/', views.PostListData.as_view(), name='bloghub_data'),
    path('<slug:slug>/search-blog/', views.search_blog, name='search_blog'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/search-idea/', views.search_idea, name='search_idea'),
    path('<int:pk>/<slug:slug>/comments-list', views.PostCommentList.as_view(), name='bloghub_post_comments'),

    path('<slug:orgslug>/<int:pk>/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/<slug:slug>/', views.PostDetail.as_view(), name='post_detail_search'),

    path('<slug:orgslug>/<int:pk>/<slug:slug>/submit-idea-form-1/', cviews.ideaform.as_view(), name='ideaform'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/submit-idea-form-2/', cviews.idea_criteria_form, name='criteria'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/submit-idea-form-3/', cviews.submit_success, name='submit_success'),



    path('<slug:orgslug>/<int:pk>/<slug:slug>/manage-challenges/', views.PostManagementDetail.as_view(), name='post_management_detail'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/manage/approve', views.approve_challenge, name='approve_challenge'),
    path('<slug:orgslug>/<int:pk>/manage/<slug:slug>/reject', views.reject_challenge, name='reject_challenge'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/likes/', views.like_view, name='like_post'),

    
    path('<slug:orgslug>/<int:pk>/<slug:slug>/manage/approval-view/', views.approval_view, name='approval_view'),
    path('ideas/<slug:orgslug>/<int:pk>/<slug:slug>/', views.IdeaDetail.as_view(), name='idea_post'),
    path('ideas/selected-ideas/<int:pk>/<slug:slug>/', views.SelectedIdeaDetail.as_view(), name='chosen_idea_post'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/search-idea-main/', views.search_idea_page, name='search_idea_main'),


    path('ideas/<slug:orgslug>/likes/<int:pk>/<slug:slug>/', views.like_view_idea, name='like_idea'),
    path('ideas/<slug:orgslug>/<int:pk>/<slug:slug>/comment', views.idea_comment_view.as_view(), name='comment_idea'),
    path('<slug:orgslug>/<int:pk>/<slug:slug>/comment/', views.comment_view.as_view(), name='comment_post'),
    
]
