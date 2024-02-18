from honeyhive.sdk.evaluations import HoneyHiveEvaluation
from honeyhive.sdk.tracer import HoneyHiveTracer
from honeyhive.sdk.utils import generate_random_string_extended
import concurrent.futures
import random

class eval(HoneyHiveEvaluation):
    def __init__(self, configs, dataset, name = "", project="test", metrics_to_compute=[]):
        if name == "":
            name = generate_random_string_extended()
            
        super().__init__(name=name, project=project, metrics_to_compute=metrics_to_compute)
        self.configs = configs
        self.dataset = dataset
        self.retry = []
        #instatiate search grid

    def _log_run(self, config, input, completion, metrics):
        super().log_run(config=config, input=input, completion=completion, metrics=metrics)

    def _finish(self):
        super().finish()

    def parallel_task(self, pipeline_a, config, datapoint):
        try:
            fresh_metrics = {} # {metric : "Nan" for metric in self.metrics_to_compute}
            fresh_tracer = HoneyHiveTracer(
                project=self.project,
                name=self.name,
                source=pipeline_a.__name__
            )
            
            tracer, metrics = pipeline_a(config, datapoint, fresh_tracer, fresh_metrics)

            metrics["session_id"] = tracer.session_id

            self._log_run(
                config=config,
                input=datapoint,
                completion=tracer.output,
                metrics=metrics  
            )
        except Exception as e:
            print(e)
            self.retry.append((pipeline_a, config, datapoint))

    def using(self, pipeline_a, parralelize=False, retry_max=3):

        if not parralelize:
            for config in self.configs:
                for datapoint in self.dataset:
                    self.parallel_task(pipeline_a, config, datapoint)

        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for config in self.configs:
                    for datapoint in self.dataset:
                        futures.append(executor.submit(self.parallel_task, config, datapoint))
                for future in concurrent.futures.as_completed(futures):
                    # Do any further processing if required on the results
                    pass

        retry_count = 0
        while len(self.retry) > 0 and retry_count < retry_max:
            pipeline_a, config, datapoint = self.retry.pop()
            print("retrying ", pipeline_a.__name__, config, datapoint)
            retry_count += 1
            self.parallel_task(pipeline_a, config, datapoint)

        self._finish()