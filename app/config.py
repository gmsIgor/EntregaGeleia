class Config:
    
    SECRET_KEY = 'super-secret-debug-key/not-for-production'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data-debug.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    JWT_SECRET_KEY = SECRET_KEY