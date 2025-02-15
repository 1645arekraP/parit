from pg_app.utils.wrappers.abstract_wrapper import AbstractRequestWrapper

class ProjectEulerWrapper(AbstractRequestWrapper):
    def __init__(self):
        super().__init__("https://projecteuler.net")

    def request(self, *args, **kwrags):
        pass
    
    def get_profile_stats(self, username, **kwrags):
        pass
    
    def get_questions(self, limit = 15, **kwargs):
        pass
    
    def get_daily_question(self, **kwargs):
        pass
    
    def get_accepted_solutions(self, username, limit=15, **kwrags):
        pass
    
    def get_all_solutions(self, username, limit = 15, **kwargs):
        pass