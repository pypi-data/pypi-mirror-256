from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "checkov_custom_policies"
    debug: bool = False
