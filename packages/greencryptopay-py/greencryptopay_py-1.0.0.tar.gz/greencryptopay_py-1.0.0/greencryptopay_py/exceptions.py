class GcpSdkRequestException(Exception):
    def __init__(self, message, code):
        super().__init__(message, code)
        self.code = code
        self.name = "GcpSdkRequestException"
