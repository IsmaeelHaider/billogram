class Config:
    """
    Configs which will be common in all environments.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///billogram.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """
    Dev specific Configs.
    """
    pass


class ProdConfig(Config):
    """
    Production specific Configs.
    """
    pass
