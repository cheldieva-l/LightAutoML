from lightautoml.automl.presets.tabular_presets import TabularAutoML
from lightautoml.tasks import Task
from lightautoml.report import ReportDeco

class LamaFeatureSelector:
    def __init__(
            self,
            outcome,
            outcome_type,
            treatment,
            timeout,
            n_threads,
            n_folds,
            verbose,
            generate_report,
            report_dir,
            use_algos,
    ):
        self.outcome = outcome
        self.outcome_type = outcome_type
        self.treatment = treatment
        self.use_algos = use_algos
        self.timeout = timeout
        self.n_threads = n_threads
        self.n_folds = n_folds
        self.verbose = verbose
        self.generate_report = generate_report
        self.report_dir = report_dir

    def perform_selection(self, df):

        roles = {
            'target': self.outcome,
            'drop': [self.treatment],
        }

        if self.outcome_type == 'numeric':
            task_name = 'reg'
            loss = 'mse'
            metric = 'mse'
        elif self.outcome_type == 'binary':
            task_name = 'binary'
            loss = 'logloss'
            metric = 'logloss'
        else:
            task_name = 'multiclass'
            loss = 'crossentropy'
            metric = 'crossentropy'

        task = Task(
            name=task_name,
            loss=loss,
            metric=metric
        )

        automl = TabularAutoML(
            task=task,
            timeout=self.timeout,
            cpu_limit=self.n_threads,
            general_params={
                'use_algos': [self.use_algos]
            },
            reader_params={
                'n_jobs': self.n_threads,
                'cv': self.n_folds,
            }
        )

        if self.generate_report:
            report = ReportDeco(output_path=self.report_dir)
            automl = report(automl)

        _ = automl.fit_predict(df, roles=roles, verbose=self.verbose)

        return automl.model.get_feature_scores()