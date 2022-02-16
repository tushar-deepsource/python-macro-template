import ast
import analyze
from helper import CODEPATH, ISSUES, get_files, prepare_result, publish_results, set_current_filepath


def run_analysis(filepath: str) -> None:
    with open(filepath) as file:
        source = file.read()

    if hasattr(analyze, "analyze") and callable(analyze.analyze):
        tree = ast.parse(source)
        analyze.analyze(tree)

    if hasattr(analyze, "analyze_source") and callable(analyze.analyze_source):
        analyze.analyze_source(source)


if __name__ == "__main__":
    for filepath in get_files(CODEPATH):
        if not filepath.endswith(".py"):
            continue

        set_current_filepath(filepath)
        run_analysis(filepath)

    result = prepare_result(ISSUES)
    publish_results(result)
