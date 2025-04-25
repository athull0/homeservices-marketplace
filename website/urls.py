from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('home',homepage,name='home'),
    path('workerhome',workerhomepage,name='workerhome'),
    path('addcat/',addcategory,name='addcat'),
    path('dash',dashboard,name='dash'),
    path('users',manage_users,name='users'),
    path('workers',manage_workers,name='workers'),
    path('pendingworkers',pending_workers,name='pendingworkers'),
    path('pendingworkeraccept/<int:user_id>/',pending_workers_action_accept,name='pendingworkeraccept'),
    path('pendingworkerreject/<int:user_id>/',pending_workers_action_reject,name='pendingworkerreject'),
    path('reapply',worker_reapply,name='workerreapply'),
    path('userdelete/<int:user_id>',userdelete,name='userdelete'),
    path('wokerdelete/<int:user_id>',workerdelete,name='workerdelete'),
    path('get-categories/',get_categories,name='get_categories'),
    path('editcategory/<int:category_id>/',catupdate,name='editcategory'),
    path('catdel/<int:category_id>/',catdelete,name="catdel"),
    path('category/<int:category_id>',worker_list_by_category,name='workerslist'),
    path('workerdetails/<int:wid>',worker_detail,name='workerdetails'),
    path('hire/<int:worker_id>/',send_hire_request,name='send_hire_request'),
    path('wishlist',wishlist,name='wishlist'),
    path('addtowishlist/<int:wid>',add_to_wishlist,name='addtowishlist'),
    path('removefromwishlist/<int:wid>',delete_from_wishlist,name='removefromwishlist'),
    path('cancel-hire/<int:request_id>/', cancel_hire_request, name='cancel_hire_request'),
    path("mark-completed/<int:request_id>/", mark_completed, name="mark_completed"),
    path('worker-requests/', worker_requests, name='worker_requests'),
    path('respond-hire/<int:request_id>/', respond_hire_request, name='respond_hire_request'),
    path('hireresponse',user_hire_requests,name="hireresponse"),
    path('search/', search_workers, name='search_workers'),
    path('searchusers/',search_users,name='search_users'),
    path('searchworkers/',search_workers_admin,name='search_workers_a'),
    path('chat/<int:receiver_id>/',chat_page, name='chat_page'),
    path('send-message/',send_message, name='send_message'),
    
    path('get-messages/<int:receiver_id>/',get_new_messages, name='get_messages'),

    path('allmessages',allmessages_worker,name='allmessages')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)