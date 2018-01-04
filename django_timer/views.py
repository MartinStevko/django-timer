
from django.views.generic import View
from django.http import JsonResponse, Http404

from django_timer.models import Timer, TimerResumeException

class TimerView(View):
    
    def get_json_response(self):
        if not hasattr(self, 'timer') or not self.timer:
            raise Http404
        return JsonResponse({
            'status': self.timer.status,
            'duration': self.timer.duration().total_seconds(),
            })

    def get_timer(self, pk):
        try:
            return Timer.objects.get(pk=pk)
        except Timer.DoesNotExist:
            pass
    
    def post(self, request, pk=None):
        self.timer = self.get_timer(pk)
        self.action(request, pk)
        return self.get_json_response()

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user

    def action(self, request, pk):
        raise NotImplementedError('{} has to define an action method.'.format(self.__class__))

class Start(TimerView):

    def action(self, request, pk):
        self.timer.start()
    
class Pause(TimerView):

    def action(self, request, pk):
        self.timer.pause()
            
class Resume(TimerView):

    def action(self, request, pk):
        try:
            self.timer.resume()
        except TimerResumeException:
            pass
        
class Stop(TimerView):

    def action(self, request, pk):
        self.timer.stop()