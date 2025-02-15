RECENT_AC_SUBMISSIONS = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    title
    titleSlug
    timestamp
    statusDisplay
    lang
    runtime
    memory
    time
  }
}
"""

RECENT_SUBMISSIONS = """
query getRecentSubmissions($username: String!, $limit: Int) {
  recentSubmissionList(username: $username, limit: $limit) {
    title
    titleSlug
    timestamp
    statusDisplay
    lang
    runtime
    memory
    time
    }
}"""

DAILY_QUESTION = """
query questionOfToday {
  activeDailyCodingChallengeQuestion {
    question {
      acRate
        title
        titleSlug
        content
        isPaidOnly
        difficulty
        exampleTestcases
        topicTags {
            name
            slug
        }
        hints
    }
  }
}
"""

GET_SELECTED_PROBLEM = """
query selectProblem($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        acRate
        title
        titleSlug
        content
        isPaidOnly
        difficulty
        exampleTestcases
        topicTags {
            name
            slug
        }
        hints
    }
}
"""

PROBLEM_QUESTION_LIST = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
        acRate
        title
        titleSlug
        content
        isPaidOnly
        difficulty
        exampleTestcases
        topicTags {
            name
            slug
        }
        hints
    }
  }
}
"""