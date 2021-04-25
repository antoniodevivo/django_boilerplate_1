from django.urls import path
from bp_app.api.users.views import (LoginView, 
                                        LogoutView, 
                                        CheckToken, 
                                        InfoUser,
                                        register_api
                                )

urlpatterns = [
    #CRUD Switch
    path('login/', 
            LoginView.as_view(), 
            name="login"),
            
    path('checkToken/', 
            CheckToken.as_view(), 
            name="checkToken"),

    path('infoUser/', 
            InfoUser.as_view(), 
            name="infoUser"),

    path('logout/', 
            LogoutView.as_view(), 
            name="logout"),

    path('register/', 
            register_api, 
            name="register"),

]