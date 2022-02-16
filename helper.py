import json
import os


CODEPATH = os.getenv("CODE_PATH", "/code")
TOOLBOX_PATH = os.getenv("TOOLBOX_PATH", "/toolbox")
ISSUES = []
CURRENT_FILEPATH = ""


def get_current_filepath() -> str:
    return CURRENT_FILEPATH

def set_current_filepath(filepath: str) -> str:
    global CURRENT_FILEPATH
    CURRENT_FILEPATH = filepath


def prepare_result(issues):
    """Prepare the result for the DeepSource analyzer framework to publish."""
    return {
        "issues": issues,
        "metrics": [],
        "is_passed": True if issues else False,
        "errors": [],
        "extra_data": ""
    }


def publish_results(result):
    """Publish the analysis results."""
    # write results into a json file:
    print("Raising issues: ", result)
    with open(os.path.join(TOOLBOX_PATH, 'analysis_results.json'), "w") as fp:
        fp.write(json.dumps(result))


def get_vcs_filepath(filepath):
    """Remove the /code/ prefix."""
    if filepath.startswith("/code/"):
        filepath = filepath[6:]

    return filepath


def make_issue(issue_code, issue_txt, filepath, line, col):
    """Prepare issue structure for the given issue data."""
    filepath = get_vcs_filepath(filepath)
    return {
        "issue_code": issue_code,
        "issue_text": issue_txt,
        "location": {
            "path": filepath,
            "position": {
                "begin": {
                    "line": line,
                    "column": col
                },
                "end": {
                    "line": line,
                    "column": col
                }
            }
        }
    }


def get_files(base_dir):
    """Return a generator with filepaths in base_dir."""
    for subdir, _, filenames in os.walk(base_dir):
        for filename in filenames:
            filepath = os.path.join(subdir, filename)
            yield filepath
