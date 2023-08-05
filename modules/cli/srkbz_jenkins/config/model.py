from pydantic import BaseModel


class JenkinsConfig(BaseModel):
    version: str
    java_version: str


class Config(BaseModel):
    jenkins: JenkinsConfig
