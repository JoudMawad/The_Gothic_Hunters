import json
import os
import sys
import unittest
from collections import namedtuple
from typing import Optional

if len(sys.argv) < 2:
    print("Usage: python execute_tests.py <test_path>")
    sys.exit(1)

os.chdir(os.path.abspath(sys.argv[1]))

# Insert the test directory as module to find the tests
sys.path.insert(0, os.getcwd())
sys.path.append("src/")
sys.path.append("src/test")

# Definitions for the Exercise and ExerciseTest
Exercise = namedtuple("Exercise", ["name", "tests"])
ExerciseTest = namedtuple("ExerciseTest", ["test", "points", "is_master"])

is_master_env_name = "ENABLE_MASTER_TESTS"


def is_master_enabled() -> bool:
    """Parse the env attribute for enabling the tests for master students.

    This functions looks for the environment variable 'ENABLE_MASTER_TESTS'
    and determines if this attribute is flagged as True. It will return
    'True' if the flag and value can successful be parsed, otherwise 'False'.
    """
    master_env_attr = os.environ.get(is_master_env_name, "")
    master_env_attr = master_env_attr.lower()
    if master_env_attr == "true":
        return True

    try:
        with open("config.json", "r") as f:
            data = json.load(f)
            if "master" in data and data["master"]:
                return True
    except FileNotFoundError:
        pass

    return False


def print_score(reached_points: float, possible_points: float):
    """Print a points summary in stdout."""
    # Max length within the summary box
    content_length = 45

    reached_points_str = str(reached_points)
    reached_points_preamble = " reached Points: "

    possible_points_str = str(possible_points)
    possible_points_preamble = " possible Points: "

    # Print Box
    print("╔═════════════════════════════════════════════╗")
    print("║               \033[1mPoints Summary\033[0m                ║")
    print("╟─────────────────────────────────────────────╢")
    print(
        "║"
        + possible_points_preamble
        + possible_points_str
        + " "
        * (content_length - len(possible_points_str) - len(possible_points_preamble))
        + "║"
    )
    print(
        "║"
        + reached_points_preamble
        + reached_points_str
        + " "
        * (content_length - len(reached_points_str) - len(reached_points_preamble))
        + "║"
    )
    print("╚═════════════════════════════════════════════╝")


class JsonTestsImporter:
    """JSON importer for the tests."""

    def import_tests(self, json_list: tuple[dict]) -> Optional[tuple[ExerciseTest]]:
        """Import the tests from the given exercise JSON object/dict."""
        tests = []
        for test_entry in json_list:
            # Parse test
            test = test_entry.get("test", None)
            if not test:
                return None

            # Parse points
            points = test_entry.get("points", None)
            if not points:
                return None

            # Parse "is_master" attribute
            is_master = test_entry.get("is_master", False)

            exercise_test = ExerciseTest(test, points, is_master)
            tests.append(exercise_test)
        return tuple(tests)

    def import_exercise(self, json_obj: dict) -> Optional[Exercise]:
        """Import the tests through a exercise JSON object/dict."""
        tests = self.import_tests(json_obj["tests"])
        if not tests:
            return None

        name = json_obj.get("name", None)
        if not name:
            return None

        exercise = Exercise(name=name, tests=tests)
        return exercise

    def import_exercises(self, json_obj: dict) -> Optional[tuple[Exercise]]:
        """Import all the tests that are given in the diffrent exercise objects."""
        exercises = list()
        for exercise in json_obj:
            exercise_parsed = self.import_exercise(exercise)
            if not exercise:
                return None
            exercises.append(exercise_parsed)
        return tuple(exercises)

    def import_from_file(self, file_path: str) -> Optional[tuple[Exercise]]:
        """Import the tests from a JSON file with the given file path."""
        json_obj = None
        try:
            with open(file_path, "r") as file_obj:
                json_obj = json.load(file_obj)
        except json.decoder.JSONDecodeError:
            pass
        except FileNotFoundError:
            pass

        if not json_obj:
            return None
        return self.import_exercises(json_obj)


class TestExecutor:
    """An executor that executes the given Exercise objects."""

    def __init__(self):
        self.execute_master_tests = is_master_enabled()

    def execute_tests(self, exercises: tuple[Exercise]) -> bool:
        """Execute and collect the points through the tests."""
        test_loader = unittest.TestLoader()
        test_runner = unittest.TextTestRunner(
            stream=sys.stdout, buffer=True, verbosity=2
        )
        points = 0.0
        max_points = 0.0
        success_run = True

        results = dict()

        print(exercises)

        # Execute tests
        first_exercise = True
        for exercise in exercises:
            if first_exercise:
                first_exercise = False
            else:
                print("─" * 71)

            results[exercise.name] = dict()

            exercise_str = (
                f"\033[1mExecuting tests for exercise: {exercise.name}\033[0m"
            )
            print(exercise_str)
            for test in exercise.tests:
                # Skip the tests, if the exercise is for master and
                # execution for master tests are disabled
                if test.is_master and not self.execute_master_tests:
                    skipping_str = f"\033[33mSkipping test: {test.test}\033[0m"
                    print("-" * 71)
                    print(skipping_str)
                    print("-" * 71 + "\n")
                    results[exercise.name][test.test] = 0
                    continue

                suite = test_loader.loadTestsFromName(test.test)
                result = test_runner.run(suite)
                if result.wasSuccessful():
                    print(f"\033[92mTest passed ✓ - adding {test.points} points\033[0m")
                    points += test.points
                    results[exercise.name][test.test] = test.points
                else:
                    success_run = False
                    print("\033[91mTest not passed ✗ -  see errors above.\033[0m")
                    results[exercise.name][test.test] = 0
                max_points += test.points
                print("\n")
        print_score(points, max_points)

        with open("result.json", "w") as result_file:
            json.dump(results, result_file, indent=2)

        return success_run


json_importer = JsonTestsImporter()
points_file = "points.json"
points_path = os.path.join(os.getcwd(), points_file)
exercises = json_importer.import_from_file(points_file)
test_executor = TestExecutor()
result = test_executor.execute_tests(exercises)
# Set the exit code, depending on the successful execution of the tests
EXIT_CODE = 0
if not result:
    EXIT_CODE = 1
exit(EXIT_CODE)
