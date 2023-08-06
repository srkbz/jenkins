from pydantic import BaseModel


class JenkinsConfig(BaseModel):
    version: str
    java_version: str
    plugin_manager_version: str
    plugins: dict[str, str]


class Config(BaseModel):
    jenkins: JenkinsConfig
