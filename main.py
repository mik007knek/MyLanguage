import re

params = {}
commands = ['in', 'out', 'init', 'set', 'math']
marks = ['+', '-', '*', '/', '%', '//']


def init(param, znach=None):
    params[param] = znach


def math(j, param1, mark, param2):
    if len(str(mark)) > 1:
        if mark != "//":
            print(f"Line {j + 1}\nMathError: no such math operator: {mark}")
            return -1
    try:
        ev = eval(f"{param1}{mark}{param2}")
    except SyntaxError:
        print(f"Line {j+1}\nMathError: no such math operator: {mark}")
        return -1
    else:
        return ev


def _in():
    return input()


def process(j, string):
    if string[0] == 'out':
        if len(string) > 4:
            print(f"Line {j+1}\nOutError: can't write more then 3 values")
            return -1
        else:
            to_print = ""
            for i in string[1:]:
                try:
                    p = params[i]
                except KeyError:
                    if re.match(r'\'.+\'', i) is not None:
                        to_print += str(i).strip("'")
                    else:
                        try:
                            i = int(i)
                        except ValueError:
                            print(f"Line {j+1}\nVarError: no such variable called '{i}'")
                            return -1
                        else:
                            to_print += str(i)
                else:
                    to_print += str(p)
                to_print += " "
            print(to_print)
    elif string[0] == 'init':
        if len(string[1:]) > 3:
            print(f'NewParamError: cannot process \'{string[1:]}\' expression\nwhile initialization')
            return -1
        elif len(string[1:]) == 1:
            init(string[1])
        elif string[2] != '~':
            print(f"Line {j+1}\nExpressionError")
            return -1
        else:
            if re.match(r'\'.+\'', string[3]):
                init(string[1], string[3])
            elif string[3] == 'in':
                init(string[1], _in())
            else:
                try:
                    p = int(string[3])
                except ValueError:
                    print(f"Line {j+1}\nValueError: {string[3]} is not a number, string or param")
                    return -1
                else:
                    init(string[1], p)
    elif string[0] == "set":
        if len(string[1:]) > 3:
            print(f'NewParamError: cannot process \'{string[1:]}\' expression\nwhile initialization')
            return -1
        elif len(string[1:]) < 3 or string[2] != '~':
            print(f"Line {j+1}\nExpressionError")
            return -1
        else:
            try:
                _ = params[string[1]]
            except KeyError:
                print(f"Line {j+1}\nVarError: no such variable called '{string[1]}'")
                return -1
            else:
                if re.match(r'\'.+\'', string[3]) is not None:
                    params[string[1]] = string[3]
                elif string[3] == 'in':
                    init(string[1], _in())
                else:
                    try:
                        _ = params[string[3]]
                    except KeyError:
                        try:
                            p = int(string[3])
                        except ValueError:
                            print(f"Line {j+1}\nVarError: no such variable called '{string[3]}'")
                            return -1
                        else:
                            params[string[1]] = p
                    else:
                        init(string[1], params[string[3]])
    elif string[0] == 'math':
        if string[2] != '~':
            print(f'Line {j+1}\nExpressionError')
            return -1
        else:
            try:
                _ = params[string[1]]
            except KeyError:
                print(f"Line {j+1}\nVarError: no such variable called '{string[1]}'")
                return -1
            else:
                if len(string[3:]) > 3:
                    print(f"Line {j+1}\nMathError: can process only one expression using \'math\' command")
                    return -1
                else:
                    for i in range(len(string[3:])):
                        try:
                            _ = params[string[3 + i]]
                        except KeyError:
                            continue
                        else:
                            string[3 + i] = params[string[3 + i]]
                    try:
                        init(string[1], math(j, string[3], string[4], string[5]))
                    except IndexError:
                        print(f"Line {j}\nExpressionError")


def check(j, string):
    if string[0] == 'out':
        if len(string) > 4:
            print(f"Line {j+1}\nOutError: can't write more then 3 values")
            return -1
        else:
            to_print = ""
            for i in string[1:]:
                try:
                    p = params[i]
                except KeyError:
                    if re.match(r'\'.+\'', i) is not None:
                        to_print += str(i).strip("'")
                    else:
                        try:
                            i = int(i)
                        except ValueError:
                            print(f"Line {j+1}\nVarError: no such variable called '{i}'")
                            return -1
                        else:
                            to_print += str(i)
                else:
                    to_print += str(p)
                to_print += " "
            # print(to_print)
    elif string[0] == 'init':
        if len(string[1:]) > 3:
            print(f'NewParamError: cannot process \'{string[1:]}\' expression\nwhile initialization')
            return -1
        elif len(string[1:]) == 1:
            init(string[1])
        elif string[2] != '~':
            print(f"Line {j+1}\nExpressionError")
            return -1
        else:
            if re.match(r'\'.+\'', string[3]):
                init(string[1], string[3])
            elif string[3] == 'in':
                # init(string[1], _in())
                init(string[1], None)
            else:
                try:
                    p = int(string[3])
                except ValueError:
                    print(f"Line {j+1}\nValueError: {string[3]} is not a number, string or param")
                    return -1
                else:
                    init(string[1], p)
    elif string[0] == "set":
        if len(string[1:]) > 3:
            print(f'NewParamError: cannot process \'{string[1:]}\' expression\nwhile initialization')
            return -1
        elif len(string[1:]) < 3 or string[2] != '~':
            print(f"Line {j+1}\nExpressionError")
            return -1
        else:
            try:
                _ = params[string[1]]
            except KeyError:
                print(f"Line {j+1}\nVarError: no such variable called '{string[1]}'")
                return -1
            else:
                if re.match(r'\'.+\'', string[3]) is not None:
                    params[string[1]] = string[3]
                elif string[3] == 'in':
                    # init(string[1], _in())
                    init(string[1], None)
                else:
                    try:
                        _ = params[string[3]]
                    except KeyError:
                        try:
                            p = int(string[3])
                        except ValueError:
                            print(f"Line {j+1}\nVarError: no such variable called '{string[3]}'")
                            return -1
                        else:
                            init(string[1], p)
                    else:
                        init(string[1], params[string[3]])
    elif string[0] == 'math':
        if string[2] != '~':
            print(f'Line {j+1}\nExpressionError')
            return -1
        else:
            try:
                _ = params[string[1]]
            except KeyError:
                print(f"Line {j+1}\nVarError: no such variable called '{string[1]}'")
                return -1
            else:
                if len(string[3:]) > 3:
                    print(f"Line {j+1}\nMathError: can process only one expression using \'math\' command")
                    return -1
                else:
                    for i in range(len(string[3:])):
                        try:
                            _ = params[string[3 + i]]
                        except KeyError:
                            continue
                        else:
                            string[3 + i] = params[string[3 + i]]
                    try:
                        try:
                            init(string[1], math(j, string[3], string[4], string[5]))
                            i = math(j, string[3], string[4], string[5])
                        except IndexError:
                            print(f"Line {j+1}\nMathError: there is no math operator")
                            return -1
                        else:
                            if string[4] not in marks:
                                print(f"Line {j+1}\nMathError: no such math operator: {string[4]}")
                                return -1
                    except IndexError:
                        print(f"Line {j}\nExpressionError")
                        return -1
                    else:
                        if i == -1:
                            return -1


def main():
    global params
    with open('new.txt', 'rt') as file:
        file = file.readlines()
        for j in range(len(file)):
            string = file[j].lstrip("\n").split()
            if string[0] not in commands:
                print(f"Line {j+1}\nCommandError: no such command \'{string[0]}\'")
                return
            else:
                if check(j, string) == -1:
                    return
        params = {}
        for j in range(len(file)):
            string = file[j].lstrip("\n").split()
            if process(j, string) == -1:
                return


if __name__ == '__main__':
    main()
