if IN_DOCKER: # type:ignore
    print("Running IN_DOCKER mode ...")
    assert MIDDLEWARE[:1] == [ # type:ignore
        'django.middleware.security.SecurityMiddleware'
    ]