import os

DATA = """Personal Webpage
(No further details provided in the original data - this is the portfolio site linked above.)
"""

def scan_dir(p) -> list[str]:
    entries = list[str]()

    with os.scandir(p) as ents:
        for e in ents:
            if e.is_dir():
                entries += scan_dir(e.path)
            else:
                entries.append(e.path)

    return entries



def load():

    rootPath = "C:\\Users\\user\\Documents\\WebPortfolio\\"
    path = "C:\\Users\\user\\Documents\\WebPortfolio\\webpage"

    list = scan_dir(os.path.join(path, "src"))

    all = dict[str, str]()

    for i in list:
        with open(i) as f:
            try:
                all[i[len(rootPath):]] = f.read()
            except UnicodeDecodeError as e:
                raise UnicodeDecodeError(e.encoding, e.object, e.start, e.end, e.reason + " At file: " + i)





    return f"""
{DATA}

Project:

{ "\n".join(f"File: {k}\nCode:{all[k]}" for k in all)}

"""
