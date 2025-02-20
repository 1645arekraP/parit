from pg_app.utils.wrappers.abstract_wrapper import AbstractRequestWrapper
from pg_app.utils.wrappers.leetcode.queries import RECENT_SUBMISSIONS, RECENT_AC_SUBMISSIONS, DAILY_QUESTION, PROBLEM_QUESTION_LIST, GET_SELECTED_PROBLEM
from pg_app.utils.wrappers.responses import QuestionResponse, QuestionListResponseList, ProfileResponse, SolutionResponse, SolutionResponseList
from typing import Dict
from datetime import datetime

class LeetcodeWrapper(AbstractRequestWrapper):
    """
    Concrete implementation of the RequestWrapper for LeetCode API interactions.

    This class provides methods to interact with the LeetCode GraphQL API, including
    retrieving questions, solutions, and profile information.

    Attributes
   ----------
    __platform_url : str
        The base URL for LeetCode's GraphQL API
    """
    def __init__(self):
        """
        Initialize the LeetCode wrapper with the GraphQL API endpoint.
        """
        super().__init__("https://leetcode.com/graphql/")

    def __create_question(self, data: Dict) -> QuestionResponse:
        """
        Create a QuestionResponse object from GraphQL response data.

        Args
        ----
        data : Dict
            GraphQL response data containing question information

        Returns
        -------
        QuestionResponse
            Parsed question data in QuestionResponse format

        Notes
        -----
        This is a private helper method used to standardize question data parsing.
        """
        return QuestionResponse(
            ac_rate=data['acRate'],
            content=data['content'],
            difficulty=data['difficulty'],
            example_test_cases=data['exampleTestcases'],
            hints=data['hints'],
            is_paid=data['isPaidOnly'],
            link=f'https://leetcode.com/problems/{data["titleSlug"]}',
            title=data['title'],
            title_slug=data['titleSlug'],
            topic_tags=[tag['name'] for tag in data['topicTags']]
        )

    def __create_solution(self, data: Dict) -> SolutionResponse:
        """
        Create a SolutionResponse object from GraphQL response data.

        Args
        ----
        data : Dict
            GraphQL response data containing solution information

        Returns
        -------
        SolutionResponse
            Parsed solution data in SolutionResponse format

        Notes
        -----
        This is a private helper method used to standardize solution data parsing.
        """
        return SolutionResponse(
            title=data['title'],
            title_slug=data['titleSlug'],
            timestamp=data['timestamp'],
            lang=data['lang'],
            runtime=data['runtime'],
            memory=data['memory'],
            status=data['statusDisplay']
        )

    async def _request(self, query: str, variables: Dict = {}, **kwargs) -> Dict:
        """
        Send a GraphQL query to the LeetCode API.

        Args
        ----
        query : str
            The GraphQL query string to execute
        variables : Dict, optional
            Variables to include in the GraphQL query (default: {})
        **kwargs
            Additional arguments for the underlying request method

        Returns
        -------
        Dict
            The JSON response from the LeetCode API

        Raises
        ------
        ValueError
            If no query is provided
        httpx.HTTPStatusError
            If the request was invalid

        Notes
        -----
        This method handles the low-level GraphQL API interaction, including
        proper request formatting and error handling.
        """
        if not query:
            raise ValueError("Must provide a query to make a request!")
        body = {
            "query": query,
            "variables": variables
        }
        return await self._make_request("", "POST", json=body, **kwargs)

    async def get_profile_stats(self, username: str) -> ProfileResponse:
        """
        Retrieve profile statistics for a LeetCode user.

        Args
        ----
        username : str
            The LeetCode username to retrieve statistics for

        Returns
        -------
        ProfileResponse
            Object containing the user's profile statistics

        Notes
        -----
        This method is currently a work in progress and will be implemented
        in a future version.
        """
        # TODO: LeetCode uses a bunch of different calls for getting data. I'll fill this in later.
        raise NotImplementedError("This method is still a WIP")

    async def get_accepted_solutions(self, username: str, limit: int = 15) -> SolutionResponseList:
        """
        Retrieve a list of accepted solutions for a LeetCode user.

        Args
        ----
        username : str
            The LeetCode username to retrieve solutions for
        limit : int, optional
            Maximum number of solutions to retrieve (default: 15)

        Returns
        -------
        SolutionResponseList
            List of accepted solutions with total count

        Notes
        -----
        This method uses the RECENT_AC_SUBMISSIONS GraphQL query to fetch
        accepted submissions.
        """
        query = RECENT_AC_SUBMISSIONS
        variables = {
            "limit": limit,
            "username": username
        }
        response = await self._request(query, variables)
        solutions = [self.__create_solution(data) for data in response["data"]["recentAcSubmissionList"]]
        return SolutionResponseList(
            total=len(solutions),
            solutions=solutions
        )

    async def get_recent_solutions(self, username: str, limit: int = 15) -> SolutionResponseList:
        """
        Retrieve a list of recent solutions for a LeetCode user.

        Args
        ----
        username : str
            The LeetCode username to retrieve solutions for
        limit : int, optional
            Maximum number of solutions to retrieve (default: 15)

        Returns
        -------
        SolutionResponseList
            List of recent solutions with total count

        Notes
        -----
        This method uses the RECENT_SUBMISSIONS GraphQL query to fetch
        all recent submissions, including both accepted and non-accepted ones.
        """
        query = RECENT_SUBMISSIONS
        variables = {
            "limit": limit,
            "username": username
        }
        response = await self._request(query, variables)
        solutions = [self.__create_solution(data) for data in response["data"]["recentSubmissionList"]]
        return SolutionResponseList(
            total=len(solutions),
            solutions=solutions
        )

    async def get_daily_question(self) -> QuestionResponse:
        """
        Retrieve the current daily coding challenge question.

        Returns
        -------
        QuestionResponse
            The current daily coding challenge question

        Notes
        -----
        This method uses the DAILY_QUESTION GraphQL query to fetch the
        active daily coding challenge.
        """
        response = await self._request(DAILY_QUESTION)
        data = response['data']['activeDailyCodingChallengeQuestion']['question']
        return self.__create_question(data)

    async def get_question(self, id: str) -> QuestionResponse:
        """
        Retrieve a specific LeetCode question by its title slug.

        Args
        ----
        id : str
            The title slug of the question to retrieve (e.g., "two-sum")

        Returns
        -------
        QuestionResponse
            The requested question data

        Notes
        -----
        This method uses the GET_SELECTED_PROBLEM GraphQL query to fetch
        detailed question information.
        """
        query = GET_SELECTED_PROBLEM
        variables = {
            "titleSlug": id
        }
        response = await self._request(query, variables)
        data = response['data']['question']
        return self.__create_question(data)

    async def get_questions(self, limit: int = 15) -> QuestionListResponseList:
        """
        Retrieve a list of LeetCode questions.

        Args
        ----
        limit : int, optional
            Maximum number of questions to retrieve (default: 15)

        Returns
        -------
        QuestionListResponseList
            List of questions with total count

        Notes
        -----
        This method uses the PROBLEM_QUESTION_LIST GraphQL query to fetch
        questions from the "all-code-essentials" category.
        """
        query = PROBLEM_QUESTION_LIST
        variables = {
            "categorySlug": "all-code-essentials",
            "filters": {},
            "limit": limit,
            "skip": 0
        }
        response = await self._request(query, variables)
        questions = [self.__create_question(data) for data in response['data']['problemsetQuestionList']['questions']]
        return QuestionListResponseList(
            total=len(questions),
            questions=questions
        )