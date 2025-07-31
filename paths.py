import os


def getProjectPath() -> str:
    """得到项目路径"""
    project_path: str = os.path.join(
        os.path.dirname(__file__),
        '',
    )
    project_path = project_path.replace('\\', '/')
    return project_path
