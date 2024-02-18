import yaml
from .InsulaApiConfig import InsulaApiConfig
from .InsulaWorkflowStep import InsulaWorkflowStep
from .InsulaJobStatus import InsulaJobStatus
from .InsulaFilesJobResult import InsulaFilesJobResult
from .InsulaWorkflowStepRunner import InsulaWorkflowStepRunner


class InsulaWorkflow(object):

    def __init__(self, insula_config: InsulaApiConfig, workflow):
        super().__init__()
        self.__insula_api_config = insula_config
        self.workflow = yaml.safe_load(workflow)
        self.__config = {}
        self.__results = {}

        self.__init_config()
        self.__init_workflow()

    def __init_config(self):

        # TODO: change with a class
        self.__config = {
            'continue_on_error': False,
            'max_parallel_jobs': 3,
            'delete_workflow_log': False
        }

        if 'configuration' in self.workflow:
            if 'continue_on_error' in self.workflow['configuration']:
                self.__config['continue_on_error'] = self.workflow['configuration']['continue_on_error']

        if 'max_parallel_jobs' in self.workflow['configuration']:
            self.__config['max_parallel_jobs'] = int(self.workflow['configuration']['max_parallel_jobs'])

        if 'delete_workflow_log' in self.workflow['configuration']:
            self.__config['delete_workflow_log'] = self.workflow['configuration']['delete_workflow_log']

    def __init_workflow(self):
        self.__name = self.workflow['name']
        self.__type = self.workflow['type']
        self.__requirements = []
        if 'requirements' in self.workflow and 'jobs' in self.workflow['requirements']:
            for job in self.workflow['requirements']['jobs']:
                self.__requirements.append(job)
        self.__steps = []

        for step in self.workflow['steps']:
            self.__steps.append(InsulaWorkflowStep(step))

        self.__init_job_requirements()

    def __init_job_requirements(self):
        for req in self.__requirements:
            run = {
                'name': req['name'],
                'service_id': req['id'],
                'results':
                    InsulaFilesJobResult(self.__insula_api_config).get_result_from_job(req['id'])
            }
            self.__results[run['name']] = run

    def run(self) -> None:

        print(f'configuration: {self.__config}')
        print('Running...')

        insula_job_status = InsulaJobStatus()
        insula_job_status.set_job_id("wf_" + self.__name)
        insula_job_status.set_properties(self.__results).save()
        try:
            for step in self.__steps:
                print(f'running... step: Step: {step}')
                _ = InsulaWorkflowStepRunner(
                    self.__insula_api_config,
                    step,
                    self.__results,
                    continue_on_error=self.__config['continue_on_error'],
                    max_parallel_jobs=self.__config['max_parallel_jobs']
                )
                results = _.run()
                for result in results['results']:
                    self.__results[result['step']['name']] = result['run']
                insula_job_status.set_properties(self.__results).save()

                if results['error']:
                    if not self.__config['continue_on_error']:
                        raise Exception('there is an error, check the pid file')

            if self.__config['delete_workflow_log']:
                insula_job_status.remove()

        except Exception as error:
            insula_job_status.set_job_error('ERROR', error).save()
            raise Exception(error)
