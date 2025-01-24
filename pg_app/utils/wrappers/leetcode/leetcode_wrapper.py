from wrapper import RequestWrapper
from leetcode.queries import RECENT_SUBMISSIONS, RECENT_AC_SUBMISSIONS, DAILY_QUESTION, PROBLEM_QUESTION_LIST


class LeetcodeWrapper(RequestWrapper):
    def __init__(self, is_async: bool = True):
        super().__init__("https://leetcode.com/graphql/", is_async)
    
    def __make_query(self, query: str, variables: dict = {}, **kwargs):
        """
        General method to send GraphQL queries to the Leetcode API.
        :param query: The GraphQL query string.
        :param variables: Dictionary of variables to include in the query.
        :param kwargs: Additional arguments for the `_make_request` method.
        :return: The response from the API.
        """
        if not query:
            raise ValueError("Must provide a query to make a request!")

        body = {
            "query": query,
            "variables": variables
        }
        return self._make_request("", "POST", json=body, **kwargs)

    def get_profile_stats(self, username: str, **kwrags):
        # TODO: Leetcode uses a bunch of different calls for getting data. I'll fill this in later.
        pass

    def get_accepted_solutions(self, username: str, limit: int = 15, **kwrags):
        query = RECENT_AC_SUBMISSIONS
        variables = {
            "limit": limit,
            "username": username
        }
        response = self.__make_query(query, variables)
        return response

    def get_all_solutions(self, username: str, limit: int = 15, **kwargs):
        query = RECENT_SUBMISSIONS
        variables = {
            "limit": limit,
            "username": username
        }
        response = self.__make_query(query, variables)
        return response

    def get_daily_question(self, **kwargs):
        response = self.__make_query(DAILY_QUESTION)
        return response

    def get_questions(self, limit:int = 15, **kwargs):
        query = PROBLEM_QUESTION_LIST
        variables = {
            "categorySlug": "all-code-essentials",
            "filters": {},
            "limit": limit,
            "skip": 0
        }
        response = self.__make_query(query, variables)
        return response