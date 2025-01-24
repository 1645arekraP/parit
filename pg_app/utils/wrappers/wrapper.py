from abc import ABC, abstractmethod
import httpx

class RequestWrapper(ABC):
    def __init__(self, platform_url:str, is_async: bool):
        """
        Constructor to initialize the platform URL for each instance.
        :param platform_url: The base URL of the platform's API.
        :param is_async: A boolean representing the conext of the requests to be made.
        """
        if not platform_url:
            raise ValueError("You must provide a platform url!")
        self.__platform_url = platform_url
        self.__is_async = is_async
    
    async def __async_request(self, endpoint, method: str, **kwargs):
        """
        Make an asynchronous HTTP request to the platform's API.
        :param endpoint: The API endpoint (relative to `platform_url`).
        :param method: HTTP method (default: "GET").
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        :return: Response object.
        :raises httpx.HTTPStatusError: For non-200 status codes
        """
        # TODO: Switch to web sockets?
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, 
                f"{self.__platform_url}/{endpoint}", 
                **kwargs
                )
            response.raise_for_status()
        return response.json()
    
    def __sync_request(self, endpoint, method: str, **kwargs):
        """
        Make a synchronous HTTP request to the platform's API.
        :param endpoint: The API endpoint (relative to `platform_url`).
        :param method: HTTP method (default: "GET").
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        :return: Response object.
        :raises httpx.HTTPStatusError: For non-200 status codes
        """
        with httpx.Client() as client:
            response = client.request(
                method, 
                f"{self.__platform_url}/{endpoint}", 
                **kwargs
                )
            response.raise_for_status()
        return response.json() 
    
    def _make_request(self, endpoint, method: str = "GET", **kwargs):
        """
        Make an HTTP request to the platform's API.
        :param endpoint: The API endpoint (relative to `platform_url`).
        :param method: HTTP method (default: "GET").
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        :return: Response object.
        :raises httpx.HTTPStatusError: For non-200 status codes
        """
        if self.__is_async:
            return self.__async_request(endpoint, method, **kwargs)
        return self.__sync_request(endpoint, method, **kwargs)
    
    @abstractmethod
    def get_profile_stats(self, username: str, **kwrags):
        """
        Retrieve the user's profile statistics.
        :param username: The username of the profile.
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        """
        pass

    @abstractmethod
    def get_accepted_solutions(self, username: str, limit = 15, **kwrags):
        """
        Retrieve the user's accepted solutions.
        :param username: The username of the profile.
        :param limit: A limit of how many questions will be retrieved.
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        """
        pass

    @abstractmethod
    def get_all_solutions(self, username: str, limit: int = 15, **kwargs):
        """
        Retrieve the user's solutions.
        :param username: The username of the profile.
        :param limit: A limit of how many questions will be retrieved.
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        """
        pass

    @abstractmethod
    def get_daily_question(self, **kwargs):
        """
        Retrieve the platform's daily question.
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        """
        pass
    
    @abstractmethod
    def get_questions(self, limit:int = 15, **kwargs):
        """
        Retrieve the platform's questions.
        :param limit: A limit of how many questions will be retrieved.
        :param kwargs: Additional arguments for the HTTP request (e.g., params, headers, json).
        """
        pass