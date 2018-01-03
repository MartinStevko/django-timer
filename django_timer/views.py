
from django.views.generic import View
from django.shortcuts import redirect

from django_timer.models import Timer, TimerResumeException

class TimerView(View):
    
    def get_success_url(self):
        return '/'
    
    def post(self, request, pk=None):
        self.action(request, pk)
        return redirect(self.get_success_url())

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user

    def action(self, request, pk):
        raise NotImplementedError('{} has to define an action method.'.format(self.__class__))

class Start(TimerView):

    def action(self, request, pk):
        user = self.get_user(request)
        Timer.objects.get_or_start(user=user)
    
class Pause(TimerView):

    def action(self, request, pk):
        user = self.get_user(request)
        try:
            Timer.objects.get_for_user(user).pause()
        except Timer.DoesNotExist:
            pass
            
class Resume(TimerView):

    def action(self, request, pk):
        user = self.get_user(request)
        try:
            Timer.objects.get_for_user(user).resume()
        except (TimerResumeException, Timer.DoesNotExist):
            pass
        
class Stop(TimerView):

    def action(self, request, pk):
        user = self.get_user(request)
        try:
            Timer.objects.get_for_user(user).stop()
        except Timer.DoesNotExist:
            pass