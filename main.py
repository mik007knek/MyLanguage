import re

params = {}
commands = ['in', 'out', 'init', 'set', 'math']


def init(param, znach=None):
    params[param] = znach


def math(param1, mark, param2):
    try:
        ev = eval(f"{param1}{mark}{param2}")
    except SyntaxError:
        print(f"MathError: no such math operator: {mark}")
        return
    else:
        return ev


def _in():
    return input()


def main():
    with open('new.txt', 'rt') as file:
        file = file.readlines()
        for j in range(len(file)):
            string = file[j].lstrip("\n").split()
            if string[0] not in commands:
                print(f"CommandError: no such command \'{string[0]}\'")
                return
            else:
                continue
        for j in range(len(file)):
            string = file[j].lstrip("\n").split()
            if string[0] == 'out':
                if len(string) > 4:
                    print("OutError: can't write more then 3 values")
                    return
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
                                    print(f"VarError: no such variable called '{i}'")
                                    return
                                else:
                                    to_print += str(i)
                        else:
                            to_print += str(p)
                        to_print += " "
                    print(to_print)
            elif string[0] == 'init':
                if len(string[1:]) > 3:
                    print(f'NewParamError: cannot process \'{string[1:]}\' expression\nwhile initialization')
                    return
                elif len(string[1:]) == 1:
                    init(string[1])
                elif string[2] != '~':
                    print("ExpressionError")
                    return
                else:
                    if re.match(r'\'.+\'', string[3]):
                        init(string[1], string[3])
                    elif string[3] == 'in':
                        init(string[1], _in())
                    else:
                        try:
                            p = int(string[3])
                        except ValueError:
                            print(f"ValueError: {string[3]} is not a number, string or param")
                            return
                        else:
                            init(string[1], p)
            elif string[0] == "set":
                if len(string[1:]) > 3:
                    print(f'NewParamError: cannot process \'{string[1:]}\' expression\nwhile initialization')
                    return
                elif len(string[1:]) < 3 or string[2] != '~':
                    print("ExpressionError")
                    return
                else:
                    try:
                        _ = params[string[1]]
                    except KeyError:
                        print(f"VarError: no such variable called '{string[1]}'")
                        return
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
                                    print(f"VarError: no such variable called '{string[3]}'")
                                    return
                                else:
                                    params[string[1]] = p
                            else:
                                init(string[1], params[string[3]])
            elif string[0] == 'math':
                if string[2] != '~':
                    print('ExpressionError')
                    return
                else:
                    try:
                        _ = params[string[1]]
                    except KeyError:
                        print(f"VarError: no such variable called '{string[1]}'")
                        return
                    else:
                        if len(string[3:]) > 3:
                            print("MathError: can process only one expression using \'math\' command")
                            return
                        else:
                            for i in range(len(string[3:])):
                                try:
                                    _ = params[string[3+i]]
                                except KeyError:
                                    continue
                                else:
                                    string[3+i] = params[string[3+i]]
                            init(string[1], math(string[3], string[4], string[5]))


if __name__ == '__main__':
    main()
