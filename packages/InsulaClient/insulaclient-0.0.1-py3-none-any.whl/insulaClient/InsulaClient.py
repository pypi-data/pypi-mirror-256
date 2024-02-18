from .InsulaUtils import InsulaUtils
from .InsulaApiConfig import InsulaApiConfig
from .InsulaWorkflow import InsulaWorkflow


class InsulaClient(object):
    def __init__(self, insula_config: InsulaApiConfig):
        self.__insula_api_config = insula_config

    def run_from_file(self, filename):
        self.run(InsulaUtils.load_from_file(filename))

    def run(self, content: str):
        wf = InsulaWorkflow(self.__insula_api_config, content)
        wf.run()
