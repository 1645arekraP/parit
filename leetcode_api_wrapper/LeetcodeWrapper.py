import requests
import json
import datetime
from queries import RECENT_AC_SUBMISSIONS, DAILY_QUESTION

class LeetcodeAc:
    def __init__(self):
        self.__id = None
        self.__title = None
        self.__timestamp = None
    
    def __init__(self, id: int, title: str, timestamp: int):
        # TODO: Raise errors

        self.__id = id
        self.__title = title
        self.__timestamp = datetime.datetime.fromtimestamp(int(timestamp), tz=datetime.timezone.utc)
    
    def __str__(self):
        return f"Solved {self.__title} at {self.__timestamp}"

class LeetcodeWrapper:
    def __init__(self):
        self.url = 'https://leetcode.com/graphql/'
        self.session = requests.session()

    # Helper methods for making requests
    def __makeAcRequest(self, username: str, limit: int = 15) -> json:
        """
        Helper method for creating a request. 
        """

        body = {
            "operationName": "recentAcSubmissions",
            "query": RECENT_AC_SUBMISSIONS,
            "variables": {
                "limit": limit,
                "username": username
            }
        }
        response = self.session.get(self.url, json=body)
        
        return response.json()
    
    def __makeDailyQuestionRequest(self):
        """
        """

        body = {
            "operationName": "questionOfToday",
            "query": DAILY_QUESTION,
            "variables": {}
        }
        response = self.session.get(self.url, json=body)

        return response.json()

    def __createAcObject(self, data: json) -> LeetcodeAc:
        """
        Helper method for creating an Accepted Solution object. Takes in json data that is from a leetcode request.
        """
        id = int(data['id'])
        title = data['title']
        timestamp = int(data['timestamp'])
        
        ac_object = LeetcodeAc(id, title, timestamp)
        return ac_object

    def getAcceptedSolutions(self, username: str, limit: int = 15) -> list[LeetcodeAc]:
        """
        Public getter for getting all recent accepted solutions from a user.
        """
        accepted_submissions = []

        data = self.__makeAcRequest(username, limit)
        for ac in data['data']['recentAcSubmissionList']:
            ac_object = self.__createAcObject(ac)
            accepted_submissions.append(ac_object)
        
        return accepted_submissions
    
    def getDailyQuestion(self):
        """
        This is a WIP till I figure out what data I want to display on the webpage
        """
        pass