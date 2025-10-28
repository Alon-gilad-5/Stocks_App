from django.urls import path
from Stocks_App import views

urlpatterns = [
    path('', views.index, name='index.html'),
    path('index', views.index, name='index.html'),
    path('Query_answers', views.Query_answers, name='Query_Answers.html'),
    path('Add_transaction/', views.Add_transaction, name='Add_transaction'),
    path('last_date/', views.last_date, name='last_date'),
    path('Buy_stocks', views.Buy_stocks, name='Buy_stocks'),

]



