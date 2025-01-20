import requests
import json
import datetime
from pg_app.utils.queries import RECENT_AC_SUBMISSIONS, DAILY_QUESTION, PROBLEM_QUESTION_LIST

class LeetcodeAc():
    def __init__(self, id: int, title: str, timestamp: int):
        # TODO: Raise errors

        self.__id = id
        self.__title = title
        self.__timestamp = datetime.datetime.fromtimestamp(int(timestamp), tz=datetime.timezone.utc)

    def get_title(self):
        return self.__title
    
    def __str__(self):
        return f"Solved {self.__title} at {self.__timestamp}"

class LeetcodeQuestion():
    def __init__(self, ac_rate, content, difficulty, is_paid, link, title, title_slug, topic_tags):
        self.ac_rate = ac_rate
        self.content = content
        self.difficulty = difficulty
        self.is_paid = is_paid
        self.link = link
        self.title = title
        self.title_slug = title_slug
        self.topic_tags = topic_tags

    def __str__(self):
        return (
        f"Title: {self.title}\n"
        f"AC Rate: {self.ac_rate}\n"
        f"Difficulty: {self.difficulty}\n"
        f"Is Paid: {self.is_paid}\n"
        f"Link: {self.link}\n"
        f"Title Slug: {self.title_slug}\n"
        #f"Content: {self.content}\n"
        f"Topic Tags: {', '.join(self.topic_tags) if self.topic_tags else 'None'}"
    )


class LeetcodeWrapper():
    def __init__(self):
        self.url = 'https://leetcode.com/graphql/'
        self.session = requests.session()

    # Helper methods for making requests
    def __make_ac_request(self, username: str, limit: int = 15) -> json:
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
    
    def __make_daily_question_request(self):
        """
        """

        body = {
            "operationName": "questionOfToday",
            "query": DAILY_QUESTION,
            "variables": {}
        }
        response = self.session.get(self.url, json=body)

        return response.json()
    
    def __make_question_request_all(self, limit=20):
        body = {
            "query": PROBLEM_QUESTION_LIST,
            "variables": {
                "categorySlug": "all-code-essentials",
                "filters": {},
                "limit": limit,
                "skip": 0
            }
        }
        response = self.session.get(self.url, json=body)

        return response.json()

    def __create_ac_object(self, data: json) -> LeetcodeAc:
        """
        Helper method for creating an Accepted Solution object. Takes in json data that is from a leetcode request.
        """
        id = int(data['id'])
        title = data['title']
        timestamp = int(data['timestamp'])
        
        ac_object = LeetcodeAc(id, title, timestamp)
        return ac_object

    def get_accepted_solutions(self, username: str, limit: int = 15) -> list[LeetcodeAc]:
        """
        Public getter for getting all recent accepted solutions from a user.
        """
        accepted_submissions = []

        data = self.__make_ac_request(username, limit)
        for ac in data['data']['recentAcSubmissionList']:
            ac_object = self.__create_ac_object(ac)
            accepted_submissions.append(ac_object)
        
        return accepted_submissions
    
    
    def __create_question_object(self, data: json):
        """
        This is a WIP till I figure out what data I want to display on the webpage
        """
        topic_tags = []

        ac_rate = data["question"]["acRate"]
        content = data["question"]["content"]
        difficulty = data["question"]["difficulty"]
        is_paid = data["question"]["paidOnly"]
        link = data["link"]
        title = data["question"]["title"]
        title_slug = data["question"]["titleSlug"]

        for topic_tag in data["question"]["topicTags"]:
            topic_tags.append(topic_tag["slug"])
        
        question = LeetcodeQuestion(ac_rate, content, difficulty, is_paid, link, title, title_slug, topic_tags)
        return question
    
    def __create_all_question_object(self, data: json):
        """
        This is a WIP till I figure out what data I want to display on the webpage
        """
        topic_tags = []

        ac_rate = data["acRate"]
        content = data["content"]
        difficulty = data["difficulty"]
        is_paid = data["paidOnly"]
        link = f"https://leetcode.com/problems/{data['titleSlug']}"
        title = data["title"]
        title_slug = data["titleSlug"]

        for topic_tag in data["topicTags"]:
            topic_tags.append(topic_tag["slug"])
        
        question = LeetcodeQuestion(ac_rate, content, difficulty, is_paid, link, title, title_slug, topic_tags)
        return question
    
    def get_daily_question(self):
        """
        returns a Question
        """
        data = self.__make_daily_question_request()["data"]["activeDailyCodingChallengeQuestion"]
        question = self.__create_question_object(data)
        return question

    def get_problems(self, limit=20):
        questions = []
        data = self.__make_question_request_all(limit)["data"]["problemsetQuestionList"]
        for question in data["questions"]:
            question_obj = self.__create_all_question_object(question)
            questions.append(question_obj)
        return questions
