from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    database_url: str = "postgresql+asyncpg://vop_user:vop_pass@localhost:5432/vop_db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Storage
    storage_backend: str = "local"
    local_storage_dir: str = "./artifacts"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket: str = ""
    azure_storage_connection_string: str = ""
    azure_container_name: str = ""

    # Renderer
    render_work_dir: str = "./tmp/renders"
    render_script_path: str = "./render.js"

    # Worker retry policy
    worker_max_jobs: int = 10
    worker_job_timeout_seconds: int = 600
    worker_max_tries: int = 3
    worker_retry_delay_seconds: int = 15

    # Signed URL
    signed_url_expires_seconds: int = 86400

    # App
    log_level: str = "INFO"
    environment: str = "development"
    api_key_secret: str = "changeme"


settings = Settings()
