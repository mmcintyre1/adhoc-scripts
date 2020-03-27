"""Brute force implementation of a hired.com assessment for programming.  
The goal is to make sure all brackets are opened and closed properly on the
left and right of the supplied string, respectively. """

def solution(brackets):
    open_bracket = 0
    close_bracket = 0

    for bracket in brackets:

        if bracket == "<":
            close_bracket += 1

        elif bracket == ">":
            if close_bracket:
                close_bracket -= 1
            else:
                open_bracket += 1


    return f"{'<' * open_bracket}{brackets}{'>' * close_bracket}"
