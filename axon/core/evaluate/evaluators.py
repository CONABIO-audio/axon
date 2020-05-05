"""A collection of useful evaluator classes."""
from .base import Evaluator


class BatchEvaluator(Evaluator):
    batch_size = 10

    def __init__(self, *args, batch_size=None, **kwargs):
        super().__init__(*args, **kwargs)

        if batch_size is not None:
            self.batch_size = batch_size

    def get_example_iterator(self, dataset):
        for id, example, target in dataset.batch(self.batch_size):
            yield id, example, target

    def evaluate(self):
        model = self.build_model(batch_size=self.batch_size)
        dataset = self.build_dataset()

        results = []
        example_iterator = self.get_example_iterator(dataset)
        for example_id_batch, example_batch, target_batch in example_iterator:
            prediction_batch = self.get_prediction(model, example_batch)

            subiterator = zip(
                example_id_batch,
                example_batch,
                target_batch,
                prediction_batch)
            for example_id, example, target, prediction in subiterator:
                evaluation_result = self.evaluate_single(prediction, target)

                # Get metric results info
                parsed_results = self.parse_metrics_results(evaluation_result)

                # Get additional metadata
                parsed_example_metadata = self.parse_examples(example)
                parsed_prediction_metadata = self.parse_predictions(prediction)
                parsed_target_metadata = self.parse_targets(target)

                data = {
                    'id': example_id,
                    **parsed_example_metadata,
                    **parsed_target_metadata,
                    **parsed_prediction_metadata,
                    **parsed_results
                }
                results.append(data)

        results = pd.DataFrame(results)
        self.log_results(results)
        self.save_results(results)
