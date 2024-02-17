import keyboard as k
import os
import time
import colorama as c
import re
import threading as t
import re

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
LINE_UC = LINE_UP + LINE_CLEAR

def extractSub(test_str, sub1, sub2) -> str:

    # getting index of substrings
    idx1 = test_str.index(sub1)
    idx2 = test_str.index(sub2)

    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1), idx2):
        res = res + test_str[idx]

    return res

def extract(input_string: str, start_char: str, end_char: str) -> str:
    start_index = input_string.find(start_char)
    end_index = input_string.find(end_char)
    
    if start_index == -1 or end_index == -1:
        return None  # One or both of the characters not found
    
    # Adjusting start index to exclude the start_char
    start_index += 1
    
    if start_index >= end_index:
        return None  # end_char occurs before start_char or both indices are the same
    
    return input_string[start_index:end_index]

def _upAndClear() -> None:
    print(LINE_UP, end=LINE_CLEAR)

def _isFlot(test: any) -> bool:
	if test.find(".") == 1:
		split = str(test).split(".")
		if split[0].isnumeric() and split[1].isnumeric():
			return True

def _isNega(test: any) -> bool:
	if test.startswith("-"):
		if test.removeprefix("-").isnumeric() or _isFlot(test.removeprefix("-")):
			return True

def selPrompt(options: list, icons: list, intro: str) -> int:
    os.system("cls")
    print(intro)
    print("\nUse [↑] and [↓] to move cursor.\nUse [→] to select.\n")

    print("[" + icons[0] + "] " + str(options[0]))

    for i in range(len(options) - 1):
        print("[ ] " + str(options[i + 1]))

    temp = 0
    temp1 = 0

    while True:
        time.sleep(0.15)

        if temp1 != temp:
            for _ in range(len(options)):
                _upAndClear()
            for i in range(len(options)):
                if temp == i:
                    print("[" + icons[i] + "] " + str(options[i]))
                else:
                    print("[ ] " + str(options[i]))
                
            temp1 = temp

        if k.is_pressed("up"):
            if temp > 0:
                temp = temp - 1
                                    
        elif k.is_pressed("down"):
            if temp < len(options) - 1:
                temp = temp + 1

        elif k.is_pressed("right"):
            os.system("cls")
            return temp

def stringSelect(intro: str, default: str, numReq: bool, intReq: bool, fltReq: bool, posReq: bool, negReq: bool, maxChar: int, minChar: int, regexMatch: str) -> str:
    os.system("cls")
    print(intro)
    print("Use [←] to edit the text.\nOnce you have finished, use [→].")

    sel = default
    targets = 0
    isNum = False
    isInt = False
    isFlt = False
    isPos = False
    isNeg = False
    isMax = False
    isMin = False
    print(c.Fore.BLUE + sel + c.Style.RESET_ALL)
    
    if numReq:
        print(c.Fore.YELLOW + "[→] Must be a number." + c.Style.RESET_ALL)
        targets = targets + 1
    if intReq:
        print(c.Fore.YELLOW + "[→] Number must be whole." + c.Style.RESET_ALL)
        targets = targets + 1
    if fltReq:
        print(c.Fore.YELLOW + "[→] Number must have a decimal point." + c.Style.RESET_ALL)
        targets = targets + 1
    if posReq:
        print(c.Fore.YELLOW + "[→] Number must be positive." + c.Style.RESET_ALL)
        targets = targets + 1
    if negReq:
        print(c.Fore.YELLOW + "[→] Number must be negative." + c.Style.RESET_ALL)
        targets = targets + 1
    if maxChar != -1:
        print(c.Fore.YELLOW + "[→] Must be less than " + str(maxChar) + " characters." + c.Style.RESET_ALL)
        targets = targets + 1
    if minChar != -1:
        print(c.Fore.YELLOW + "[→] Must be at least " + str(minChar) + " characters." + c.Style.RESET_ALL)
        targets = targets + 1
    if regexMatch != "":
        print(c.Fore.YELLOW + "[→] Must match regular expression " + str(regexMatch) + c.Style.RESET_ALL)
        targets = targets + 1

    while True:
        time.sleep(0.15)
        
        for _ in range(targets):
           _upAndClear()

        if numReq and sel.isnumeric():
            print(c.Fore.GREEN + "[ ] Input is a number." + c.Style.RESET_ALL)
            isNum = True
        elif numReq and _isFlot(sel):
            print(c.Fore.GREEN + "[ ] Input is a number." + c.Style.RESET_ALL)
            isNum = True
        elif numReq and _isNega(sel):
            print(c.Fore.GREEN + "[ ] Input is a number." + c.Style.RESET_ALL)
            isNum = True
        elif numReq:
            print(c.Fore.YELLOW + "[→] Must be a number." + c.Style.RESET_ALL)
            isNum = False
        else:
            isNum = True
        
        if intReq and sel.find(".") == -1 and sel.isnumeric():
            print(c.Fore.GREEN + "[ ] Input is whole." + c.Style.RESET_ALL)
            isInt = True
        elif intReq:
            print(c.Fore.YELLOW + "[→] Number must be whole." + c.Style.RESET_ALL)
            isInt = False
        else:
            isInt = True

        if fltReq and _isFlot(sel):
            print(c.Fore.GREEN + "[ ] Input has a decimal point." + c.Style.RESET_ALL)
            isFlt = True
        elif fltReq:
            print(c.Fore.YELLOW + "[→] Number must have a decimal point." + c.Style.RESET_ALL)
            isFlt = False
        else:
            isFlt = True

        if posReq and sel.isnumeric() and float(sel) > -1:
            print(c.Fore.GREEN + "[ ] Input is positive." + c.Style.RESET_ALL)
            isPos = True
        elif posReq:
            print(c.Fore.YELLOW + "[→] Number must be positive." + c.Style.RESET_ALL)
            isPos = False
        else:
            isPos = True
        
        if negReq and _isNega(sel):
            print(c.Fore.GREEN + "[ ] Input is negative." + c.Style.RESET_ALL)
            isNeg = True
        elif negReq:
            print(c.Fore.YELLOW + "[→] Number must be negative." + c.Style.RESET_ALL)
            isNeg = False
        else:
            isNeg = True
        
        if maxChar != -1 and len(sel) <= maxChar:
            print(c.Fore.GREEN + "[ ] Input is less than " + str(maxChar) + " characters." + c.Style.RESET_ALL)
            isMax = True
        elif maxChar != -1:
            print(c.Fore.YELLOW + "[→] Must be less than " + str(maxChar) + " characters." + c.Style.RESET_ALL)
            isMax = False
        else:
            isMax = True
        
        if minChar != -1 and len(sel) >= minChar:
            print(c.Fore.GREEN + "[ ] Input is at least " + str(minChar) + " characters." + c.Style.RESET_ALL)
            isMin = True
        elif minChar != -1:
            print(c.Fore.YELLOW + "[→] Must be at least " + str(minChar) + " characters." + c.Style.RESET_ALL)
            isMin = False
        else:
            isMin = True
        
        if regexMatch != "" and re.search(regexMatch, sel):
            print(c.Fore.GREEN + "[ ] Matches regular expression " + str(regexMatch) + c.Style.RESET_ALL)
            isRe = True
        elif regexMatch != "":
            print(c.Fore.YELLOW + "[→] Must match regular expression " + str(regexMatch) + c.Style.RESET_ALL)
            isRe = False
        else:
            isRe = True
        
        if k.is_pressed("left"):
            os.system("cls")
            print("Old Input: " + sel)
            print(c.Fore.BLUE + "Hint: Use [↑] to retype the last input." + c.Style.RESET_ALL + "\nUse [→] to retype it one character at a time.\nUse [ENTER] when you are finished.")
            sel = input(c.Fore.CYAN + "New Input: ")
            print("", end=c.Style.RESET_ALL)
            os.system("cls")
            print(intro)
            print("Use [←] to edit the text.\nOnce you have finished, use [→].")
            print(c.Fore.BLUE + sel + c.Style.RESET_ALL)
            for _ in range(targets):
                print()
        
        if k.is_pressed("right"):
            if isNum and isInt and isFlt and isPos and isNeg and isMax and isMin and isRe:
                os.system("cls")
                return sel
            else:
                input(c.Fore.RED + "Check the requirements first!" + c.Style.RESET_ALL + "\nPress [ENTER] to continue...")
                _upAndClear()
                _upAndClear()

def fltList(listEdt: list, item: any) -> list:
    res = list(filter((item).__ne__, listEdt))
    return res

class progressBar:
    def toggleDebug(self) -> None:
        if self.debug:
            self.debug = False
        else:
            self.debug = True

        self.forceRender()
    
    def toggleForceUpdate(self) -> None:
        if self.forceupd:
            self.forceupd = False
        else:
            self.forceupd = True
        
        self.forceRender()
    
    def updThreadFunc(self) -> t.Thread:
        stop_me = False
        while not stop_me:
            if self.forceupd:
                self.forceRender()
            time.sleep(0.25)
            if not self.isKallowed:
                stop_me = True

    def __init__(self, title: str, max: int, fad: str, ful: str, titclr: str) -> any:
        self.forceupd = False
        self.debug = False
        self.prg = 0
        self.title = title
        self.max = max
        self.fad = fad
        self.ful = ful
        self.titclr = titclr
        self.logmsg = []
        self.isKallowed = True

        self.oldprg = 0
        self.oldtitle = title
        self.oldfad = fad
        self.oldful = ful
        self.oldtitclr = titclr
        self.oldlogmsg = []

        self.f3 = k.add_hotkey("f3", self.toggleDebug)
        self.f2 = k.add_hotkey("f2", self.toggleForceUpdate)
        self.f1 = k.add_hotkey("f1", self.forceRender)

        self.updateThread = t.Thread(target=self.updThreadFunc)
        self.updateThread.start()
    
    def keyMode(self, enable: bool) -> None:
        self.isKallowed = enable
        
        if enable:
            self.f3 = k.add_hotkey("f3", self.toggleDebug)
            self.f2 = k.add_hotkey("f2", self.toggleForceUpdate)
            self.f1 = k.add_hotkey("f1", self.forceRender)
        else:
            k.remove_hotkey(self.f3)
            k.remove_hotkey(self.f2)
            k.remove_hotkey(self.f1)

    def increase(self, amount: int) -> None:
        self.prg += amount
    
    def decrease(self, amount: int) -> None:
        self.prg -= amount
    
    def setTitle(self, title: str) -> None:
        self.title = title
    
    def setColors(self, fad: str, ful: str, titclr: str) -> None:
        self.fad = fad
        self.ful = ful
        self.titclr = titclr
    
    def log(self, msg: str):
        self.logmsg.append(str(len(self.logmsg) + 1) + ": " + msg)
        self.forceRender()
    
    def render(self) -> None:
        if self.oldfad != self.fad or self.oldful != self.ful or self.oldprg != self.prg or self.oldtitclr != self.titclr or self.oldtitle != self.title or self.oldlogmsg != self.logmsg:
            self.forceRender()

    def forceRender(self) -> Warning:
        os.system("cls")
        print(self.titclr + self.title + c.Style.RESET_ALL)

        num = self.prg / (self.max / 10)
        dec_num = num * 10
        percent = round(dec_num, 2)

        print(self.ful + str(percent) + "%" + c.Style.RESET_ALL + " | ", end="")
        for _ in range(round(percent)):
            print(self.ful + "█", end=c.Style.RESET_ALL)
        for _ in range(100 - round(percent)):
            print(self.fad + "█", end=c.Style.RESET_ALL)
        print()
        
        if self.debug:
            print(c.Fore.CYAN + "gg8lib - Progress Bar" + c.Style.RESET_ALL)
            print(f"Progress: {str(self.prg)}/{str(self.max)}")
            print(f"Percent Calc: num = {str(num)}, dec_num = {str(dec_num)}")
            print(f"{str(percent)}%, ({str(round(percent))}/100)")

            if self.forceupd:
                print(c.Fore.CYAN + "Force Updating, Press [F2] to turn off" + c.Style.RESET_ALL)
            else:
                print(c.Fore.YELLOW + "Press [F2] to force update" + c.Style.RESET_ALL)
            
            for i in range(len(self.logmsg[-10:])):
                print(str(self.logmsg[-10:][i]))
        else:
            for i in range(len(self.logmsg[-15:])):
                print(str(self.logmsg[-15:][i]))

        self.oldprg = self.prg
        self.oldtitle = self.title
        self.oldfad = self.fad
        self.oldful = self.ful
        self.oldtitclr = self.titclr
        self.oldlogmsg = self.logmsg

def gitCommitBeautify(parsed: dict) -> str:
    out = ""
    i = int(parsed["ins"])
    f = int(parsed["cha"])
    d = int(parsed["del"])
    out = f"{out}{c.Fore.YELLOW}~{f}{c.Style.RESET_ALL} "
    out = f"{out}{c.Fore.GREEN}+{i}{c.Style.RESET_ALL} "
    out = f"{out}{c.Fore.RED}-{d}{c.Style.RESET_ALL} "
    out = f"{out}\n{c.Fore.YELLOW}{str(f)}{c.Style.RESET_ALL} changes"
    out = f"{out}\n{c.Fore.GREEN}{str(i)}{c.Style.RESET_ALL} additions"
    out = f"{out}\n{c.Fore.RED}{str(d)}{c.Style.RESET_ALL} deletions"
    return out

def gitCommitParse(output):
    """
    Extracts the number of files changed, insertions, and deletions from Git output.

    Args:
    - output: The Git pull or Git commit output string.

    Returns:
    - A tuple containing the number of files changed, insertions, and deletions.
    """
    file_pattern = r'(\d+) file(?:s)? changed'
    insertion_pattern = r'(\d+) insertion(?:s)?\(\+\)'
    deletion_pattern = r'(\d+) deletion(?:s)?\(-\)'

    files_changed = re.search(file_pattern, output)
    insertions = re.search(insertion_pattern, output)
    deletions = re.search(deletion_pattern, output)

    num_files_changed = int(files_changed.group(1)) if files_changed else 0
    num_insertions = int(insertions.group(1)) if insertions else 0
    num_deletions = int(deletions.group(1)) if deletions else 0

    return {
        "cha": num_files_changed,
        "del": num_deletions,
        "ins": num_insertions
    }

def gitStashParse(output):
    stashes = []
    lines = output.split('\n')
    for line in lines:
        if line.strip():
            parts = line.split(': ', 1)
            stash_hash = parts[0].split(' ')[0]
            comment = parts[1] if len(parts) > 1 else ''
            stashes.append({"hash": stash_hash, "comment": comment})
    return stashes