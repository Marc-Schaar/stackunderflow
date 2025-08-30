from rest_framework.throttling import UserRateThrottle

## Kann Wiederverwenbar gemacht werden und erzeugt einen eigen Sope

class QuestionThrottle(UserRateThrottle):
    scope = 'question'

    def allow_request(self, request, view):

        if request.method == "GET":
            return True
        
        new_scope = 'question-' + request.method.lower()
        if new_scope in self.THROTTLE_RATES:
            self.scope = new_scope
            self.rate = self.get_rate()
            self.num_requests, self.duration = self.parse_rate(self.rate)

        return super().allow_request(request, view)
    
## Macht die Views unübersichtlich 

class QuestionGetThrottle(UserRateThrottle):
    scope = 'question-get'

class QuestionPostThrottle(UserRateThrottle):
    scope = 'question-post'