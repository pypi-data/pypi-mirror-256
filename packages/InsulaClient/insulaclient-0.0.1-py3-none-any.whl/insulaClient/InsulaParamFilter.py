from re import findall


class InsulaParamFilter(object):
    __result_pattern = '\\${(.*?)}'

    def __init__(self, value):
        super().__init__()
        self.__all_match = findall(self.__result_pattern, value)
        self.__has_match = len(self.__all_match) > 0

        self.__match = []
        if self.__has_match:
            self.__match = self.__all_match[0].split('.')

    def has_match(self) -> bool:
        return self.__has_match

    def get_step_id(self) -> str:
        return self.__match[0]

    def has_step_output(self) -> bool:
        return len(self.__match) == 2

    def get_step_output(self):
        if len(self.__match) == 2:
            return self.__match[1]

        return None


class Filter:
    __result_filter_pattern = '\\$\\[(.*?)]'

    def __init__(self, raw: str):
        self.__filters = findall(self.__result_filter_pattern, raw)

    def has_filters(self):
        return len(self.__filters) > 0

    def get_filters(self):
        return self.__filters

    def filter(self, filename):
        if self.has_filters():
            for filter_in in self.__filters:
                res = findall(filter_in, filename)
                if len(res) > 0:
                    return True
        return False


class BLaBla(object):

    @staticmethod
    def get_from_results(ipf: InsulaParamFilter, raw, results: dict):
        values = []
        ipf_filters = Filter(raw)
        if ipf.get_step_id() in results:
            for result in results[ipf.get_step_id()]['results']:

                if ipf.has_step_output() and result['output_id'] != ipf.get_step_output():
                    continue

                if ipf_filters.has_filters():
                    if ipf_filters.filter(result['uri']):
                        values.append(result)
                else:
                    values.append(result)
        return values
