DATA = """
Plugin Compilation Tester
(No further details provided in the original data.)
"""


def load():
    code: str
    with open("C:\\Users\\user\\Documents\\UnrealTools\\PluginBatch\\CompilePlugin.bat") as f:
        code = f.read()
    return f"""
{DATA}

Code.bat: \n{code}

"""