from allauth.account.adapter import DefaultAccountAdapter


class LmsAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        print("login reached here ")
        
        user = request.user

        # Replace 'role_field' with the actual field storing user role information
        # and adjust logic based on your specific requirements
        if user.role == 'admin':
            return '/admin/'
        
        elif user.role == "INSTRUCTOR":
            return '/course/create/'
        
        elif user.role == "STUDENT":
            return '/'
      
        else:
            return super().get_login_redirect_url(request)
