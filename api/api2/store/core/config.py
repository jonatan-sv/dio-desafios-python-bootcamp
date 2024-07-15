from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):    
    DATABASE_URL: str # Presente no .env
    model_config = SettingsConfigDict(env_file='.env')
    
settings = Settings()