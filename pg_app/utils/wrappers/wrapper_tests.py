from leetcode.leetcode_wrapper import LeetcodeWrapper

lcw = LeetcodeWrapper(is_async=False)
data = lcw.get_daily_question()

print(data)