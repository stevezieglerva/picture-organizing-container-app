import glob
import json
import re
import sys
import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import HtmlTestRunner


def print_results(pattern):
    print("\n\n🗃  Test Results:")
    emojis = {"pass": "✅", "fail": "❗", "skip": "➖", "error": "❌"}
    test_count = 0
    for file in glob.glob(f"./reports/{pattern}"):
        with open(file, "r") as file:
            text = file.read()
            results = json.loads(text)

            for test_group in results["tests"]:
                test_class = test_group["class"]
                print(f"\n\n📋 {test_class}:")
                print(f"   Status  | Test")
                print("   ---------------------------------------------------")
                for test in test_group["tests"]:
                    test_name = test["test_name"]
                    status = test["status"]
                    emoji = emojis[status]
                    line = f"   {emoji} {status:<5} | {test_name:<80}"
                    print(line)
                    test_count = test_count + 1
    print(f"\n🗂  Total Tests: {test_count}\n")


def get_files_with_lots_of_tests_commented_out(start_dir):
    results = []
    path = f"{start_dir}**/test_*.py"
    print(f"❎ Checking for commented tests in {path}")
    files = glob.glob(path)
    for filename in files:
        with open(filename, "r") as file:
            file_lines = file.readlines()
            all_lines_count = len(file_lines)
            commented_lines = [l for l in file_lines if re.findall(r"#", l)]
            commented_lines_count = len(commented_lines)
            percent_commented = round(float(commented_lines_count / all_lines_count), 2)
            if percent_commented > 0.25:
                results.append((filename, percent_commented))
    return results


if __name__ == "__main__":
    start_dir = "tests/"
    pattern = "test_*.*"
    if len(sys.argv) > 1:
        for arg in sys.argv:
            print(arg)
        start_dir = sys.argv[1]
        pattern = sys.argv[2]

    print(f"\nstart_dir: {start_dir}")
    print(f"pattern: {pattern}\n")

    suite = unittest.defaultTestLoader.discover(start_dir, pattern=pattern)

    runner = HtmlTestRunner.HTMLTestRunner(
        template="report_template_json.txt",
        report_name="test_results.json",
        add_timestamp=False,
    )
    test_results = runner.run(suite)

    print_results(pattern)

    tests_with_lots_of_comments = get_files_with_lots_of_tests_commented_out(start_dir)
    if tests_with_lots_of_comments:
        print("\n🚨 Lots of commented tests")
        for f in tests_with_lots_of_comments:
            print(f"{f[0]:<60} {f[1]:.0%}")
    print()

    if test_results.wasSuccessful() == True:
        print("👍🎉 All tests passed!")
    else:
        print("😡 Some tests failed!")
        exit(1)
