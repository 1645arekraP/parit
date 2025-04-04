from abc import ABC, abstractmethod
from apps.questions.utils.wrappers.responses import QuestionResponse, QuestionListResponseList, ProfileResponse, SolutionResponse, SolutionResponseList
from typing import Self
import httpx

class AbstractRequestWrapper(ABC):
    """
    Abstract base class providing a standardized interface for making API requests to platforms.

    Attributes
   ----------
    __platform_url : str
        The base URL of the platform's API
    """

    def __init__(self, platform_url: str) -> None:
        """
        Initialize the RequestWrapper with a platform URL.

        Args
       ----
            platform_url : str
                The base URL of the platform's API

        Raises
       ------
            ValueError
                If platform_url is missing or empty
        """
        if not platform_url:
            raise ValueError("You must provide a platform url!")
        self.__platform_url = platform_url

    async def _make_request(self, endpoint: str, method: str = "GET", **kwargs) -> dict:
        """
        Make an asynchronous HTTP request to the platform's API.

        Args
       ----
            endpoint : str
                The API endpoint (relative to platform_url)
            method : str, optional
                HTTP method (default: "GET")
            **kwargs
                Additional arguments for the HTTP request (e.g., params, headers, json)

        Returns
       -------
            dict
                Response data from the API

        Raises
       ------
            httpx.HTTPStatusError
                If the request was invalid
        """
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.__platform_url}/{endpoint}",
                **kwargs
            )
            response.raise_for_status()
            return response.json()

    @abstractmethod
    async def _request(self, **kwargs) -> dict:
        """
        Platform-specific implementation of the request logic.

        Args
       ----
            **kwargs
                Additional parameters that vary by platform implementation

        Returns
       -------
            dict
                Response data from the API

        Notes
       -----
        Must be implemented by concrete subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def get_profile_stats(self, username: str, **kwargs) -> ProfileResponse:
        """
        Retrieve the user's profile statistics.

        Args
       ----
            username : str
                The username of the profile
            **kwargs
                Additional arguments for the HTTP request

        Returns
       -------
            ProfileResponse
                Object containing the profile statistics

        Notes
       -----
        Must be implemented by concrete subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def get_accepted_solutions(self, username: str, limit: int = 15, **kwargs) -> SolutionResponseList:
        """
        Retrieve the user's accepted solutions.

        Args
       ----
            username : str
                The username of the profile
            limit : int, optional
                Maximum number of solutions to retrieve (default: 15)
            **kwargs
                Additional arguments for the HTTP request

        Returns
       -------
            SolutionResponseList
                List of accepted solutions

        Notes
       -----
        Must be implemented by concrete subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def get_recent_solutions(self, username: str, limit: int = 15, **kwargs) -> SolutionResponseList:
        """
        Retrieve the user's recent solutions.

        Args
       ----
            username : str
                The username of the profile
            limit : int, optional
                Maximum number of solutions to retrieve (default: 15)
            **kwargs
                Additional arguments for the HTTP request

        Returns
       -------
            SolutionResponseList
                List of recent solutions

        Notes
       -----
        Must be implemented by concrete subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def get_daily_question(self, **kwargs) -> QuestionResponse:
        """
        Retrieve the platform's daily question.

        Args
       ----
            **kwargs
                Additional arguments for the HTTP request

        Returns
       -------
            QuestionResponse
                Object containing the daily question

        Notes
       -----
        Must be implemented by concrete subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def get_question(self, id: str, **kwargs) -> QuestionResponse:
        """
        Retrieve a specific question from the platform.

        Args
       ----
            id : str
                Identifier for the question to retrieve
            **kwargs
                Additional arguments for the HTTP request

        Returns
       -------
            QuestionResponse
                Object containing the requested question

        Notes
       -----
        Must be implemented by concrete subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def get_questions(self, limit: int = 15, **kwargs) -> QuestionListResponseList:
        """
        Retrieve a list of questions from the platform.

        Args
       ----
            limit : int, optional
                Maximum number of questions to retrieve (default: 15)
            **kwargs
                Additional arguments for the HTTP request

        Returns
       -------
            QuestionListResponseList
                List of questions

        Notes
       -----
        Must be implemented by concrete subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")