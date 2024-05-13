from backend.profiles.models import UserProfile

class OnlineStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # Update user's online status to True when logged in
            UserProfile.objects.filter(user=request.user).update(is_online=True)
        else:
            # Update user's online status to False when logged out
            UserProfile.objects.filter(user=request.user).update(is_online=False)
        return response
