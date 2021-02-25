"""
Georgia Institute of Technology.
Tests for CS7637 Knowledge-Based Artificial Intelligence Raven's Progressive Matrix project
 I extracted the reading part from RavensProject.py's code.

 It should be set in the same directory as the Agent.py' one, or in a a tests subdirectory
    properly marking it as tests one.
 Set to False the global variable EXCEPTIONS_HANDLING if you wish to not globally capture
    exceptions and have more control of the debugging process.
"""
__credits__ = "Raven's Progressive Matrix CS7637 base code authors"
__author__ = "Breogan COSTA, CS7637 RavensProject.py base code authors"

import unittest
import os
import warnings

from Agent import Agent
from ProblemSet import ProblemSet


class TestAgent(unittest.TestCase):
    BASIC = 0
    CHALLENGE = 1
    milestone2_B = ["Basic Problems B",
                    "Challenge Problems B"]
    milestone3_C = ["Basic Problems C",
                    "Challenge Problems C"]
    milestone4_D = ["Basic Problems E",
                    "Challenge Problems E"]
    milestone4_E = ["Basic Problems E",
                    "Challenge Problems E"]

    def setUp(self) -> None:
        warnings.simplefilter("ignore")

    @staticmethod
    def get_next_line(r):
        """
        Based on Raven's Progressive Matrix CS7637 base code
        """
        return r.readline().rstrip()

    @staticmethod
    def solve_one(one_to_grade, restrict_to: int = -1):
        """
        Based on Raven's Progressive Matrix CS7637 base code
        """
        done = False
        problems = []

        r = open(os.path.join("Problems",
                              "ProblemSetList.txt"))
        while not done:
            line = TestAgent.get_next_line(r)
            if line == one_to_grade:
                problems.append(ProblemSet(line))
                done = True
        agent = Agent()
        answers = []
        r.close()

        for problem_set in problems:
            if restrict_to == -1:
                for problem in problem_set.problems:
                    answer = agent.Solve(problem)
                    answers.append(answer)
            else:
                problems_list = problem_set.problems
                answer = agent.Solve(problems_list[restrict_to])
                answers.append(answer)
        return answers

    @staticmethod
    def grade_one(one_to_grade, restrict_to: int = -1):
        """
        Based on Raven's Progressive Matrix CS7637 base code
        """
        answers_to_ret = []
        with open(os.path.join("Problems",
                               "ProblemSetList.txt")) as fd0:
            for line0 in fd0:
                if line0 == one_to_grade:
                    line0 = line0.rstrip()
                    with open(os.path.join("Problems",
                                           line0,
                                           "ProblemList.txt")) as fd1:
                        for line1 in fd1:
                            if restrict_to != -1:
                                if int(line1[-3:-1]) == restrict_to + 1:
                                    line1 = line1.rstrip()
                                    with open(os.path.join("Problems",
                                                           line0,
                                                           line1,
                                                           "ProblemAnswer.txt")) as fd2:
                                        ans = fd2.read().replace("\n", "")
                                        answers_to_ret.append(int(ans))
                            else:
                                line1 = line1.rstrip()
                                with open(os.path.join("Problems",
                                                       line0,
                                                       line1,
                                                       "ProblemAnswer.txt")) as fd2:
                                    ans = fd2.read().replace("\n", "")
                                    answers_to_ret.append(int(ans))
        return answers_to_ret

    @staticmethod
    def build_explanation(testcase, answers_proposed, answers_real):
        explanation = testcase \
                      + ":\n\t" \
                      + str(answers_real) \
                      + " expected vs.\n\t" \
                      + str(answers_proposed) \
                      + " received"
        return explanation

    @staticmethod
    def get_answers_and_solutions(problem_name, restrict_to: int):
        answers_proposed = TestAgent.solve_one(problem_name,
                                               restrict_to)
        answers_real = TestAgent.grade_one(problem_name + "\n",
                                           restrict_to)
        equals_counter = 0
        equals_pos = []
        if len(answers_proposed) == 0:
            equals_counter = 0
            answers_proposed = [0] * len(answers_real)
        else:
            for i in range(len(answers_real)):
                if answers_real[i] == answers_proposed[i]:
                    equals_counter += 1
                    equals_pos.append(i)

        equals_percent = equals_counter * 100 / len(answers_real)
        return answers_proposed, answers_real, equals_counter, equals_percent

    def problems_testcase_secure_run(self, testcase, restrict_to: int = -1):
        try:
            answers_agent, answers, equals_counter, equals_percent = self.get_answers_and_solutions(testcase,
                                                                                                    restrict_to)
        except Exception as ex:
            testcase += " - ERROR: " + str(ex)
            equals_percent = 0
            answers_agent = answers = "----- NOT EXECUTED -----"
        self.assertEqual("100.0%",
                         str(equals_percent) + "%",
                         TestAgent.build_explanation(testcase, answers_agent, answers))

    def problems_testcase_exceptions_not_captured(self, testcase, restrict_to: int = -1):
        answers_agent, answers, equals_counter, equals_percent = self.get_answers_and_solutions(testcase,
                                                                                                restrict_to)
        self.assertEqual("100.0%",
                         str(equals_percent) + "%",
                         TestAgent.build_explanation(testcase, answers_agent, answers))

    def problems_testcase(self, testcase, restrict_to: str = -1):
        if restrict_to != -1:
            restrict_to = int(restrict_to[-2:]) - 1
        if EXCEPTIONS_HANDLING:
            self.problems_testcase_secure_run(testcase, restrict_to)
        else:
            self.problems_testcase_exceptions_not_captured(testcase, restrict_to)

    def test_milestone2_basic_only_one(self):
        milestone_case = self.milestone2_B[0]
        test_to_run = "B-01"
        self.problems_testcase(milestone_case, restrict_to=milestone_case[:-3] + " " + test_to_run)

    def test_milestone2_basic(self):
        self.problems_testcase(self.milestone2_B[self.BASIC])

    def test_milestone2_challenge(self):
        self.problems_testcase(self.milestone2_B[self.CHALLENGE])

    def test_milestone3_basic(self):
        self.problems_testcase(self.milestone3_C[self.BASIC])

    def test_milestone3_challenge(self):
        self.problems_testcase(self.milestone3_C[self.CHALLENGE])

    def test_milestone4_basic(self):
        self.problems_testcase(self.milestone4_D[self.BASIC])

    def test_milestone4_challenge(self):
        self.problems_testcase(self.milestone4_D[self.CHALLENGE])

    def test_milestone4_basic(self):
        self.problems_testcase(self.milestone4_E[self.BASIC])

    def test_milestone4_challenge(self):
        self.problems_testcase(self.milestone4_E[self.CHALLENGE])


EXCEPTIONS_HANDLING = False
"""
EXCEPTIONS_HANDLING controls if exceptions must be capture when calling Agent.py
"""

if __name__ == '__main__':
    unittest.main()
