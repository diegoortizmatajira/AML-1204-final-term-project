class MetaDataApiVersion:
    def __init__(self):
        self.major_version: str = 'v2'
        self.minor_version: str = '2018-11-08'


class Metadata:
    def __init__(self):
        self.apiversion: MetaDataApiVersion = MetaDataApiVersion()
