import os

DATA = """CV Maker
(No further details provided in the original data - likely the tool used to help generate structured CVs like this one.)
"""


def load():
    code = dict[str, str]()
    root = os.path.join("C:\\Users","user","Documents","MyProjects", "CVMaker")
    
    with open(os.path.join(root, "build.js")) as f:
        code["build.js"] = f.read()

    with open(os.path.join(root, "templates", "cv.en.ejs")) as f:
        code["cv.ejs"] = f.read()

    with open(os.path.join(root, "styles", "style.css")) as f:
        code["style.css"] = f.read()

    return f"""
{DATA}

{ "\n".join(f"File: {k}\nCode:{code[k]}" for k in code)}

"""