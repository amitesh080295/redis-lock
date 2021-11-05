class SampleService:

    def __init__(self):
        self.message = 'Success'

    def sample_method(self):
        return dict(message=self.message)
