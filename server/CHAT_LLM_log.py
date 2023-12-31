import inspect

def LOG(message):
    caller_frame = inspect.currentframe().f_back
    filename = caller_frame.f_code.co_filename
    line_number = caller_frame.f_lineno
    print(f"LOG - - [{filename}, line {line_number}]")
    print(f"{message}")
