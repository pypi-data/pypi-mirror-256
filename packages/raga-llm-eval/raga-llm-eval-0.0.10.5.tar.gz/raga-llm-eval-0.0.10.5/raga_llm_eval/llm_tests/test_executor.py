"""
Container code for all the test runners
"""

from . import (AnswerCorrectnessTest, AnswerRelevancyTest,
               ContextualPrecisionTest, ContextualRecallTest,
               ContextualRelevancyTest, FaithfulnessTest, SummarisationTest,
               bias_test, coherence_test, complexity_test, conciseness_test,
               consistency_test, correctness_test, cosine_similarity_test,
               cover_test, generic_evaluation_test, grade_score_test,
               hallucination_test, harmless_test, length_test,
               maliciousness_test, overall_test, pos_test,
               prompt_injection_test, readability_test, refusal_test,
               response_toxicity_test, sentiment_analysis_test, toxicity_test,
               winner_test)
from .test_utils import SuppressOutput


# pylint: disable=too-many-public-methods
class TestExecutor:
    """
    Container class for the all the tests supported.
    """

    def run_answer_relevancy_test(self, test_data):
        """
        Run an answer relevancy test using the given test data.

        Parameters:
            self: the object itself
            test_data (dict): a dictionary containing the prompt, response, context, model, include_reason, and threshold

        Returns:
            The result of the answer relevancy test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = AnswerRelevancyTest(
                question=test_data["prompt"],
                answer=test_data["response"],
                retrieval_context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                include_reason=test_data["test_arguments"].get("include_reason", True),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            ).run()

        # TODO: Check if the results are in the desired form
        return res

    def run_contextual_precision_test(self, test_data):
        """
        A function to run a contextual precision test.

        Args:
            self: The object itself.
            test_data (dict): A dictionary containing the test data with keys:
                - "prompt": The prompt for the test.
                - "expected_response": The expected response for the test.
                - "context": The context for the test.
                - "model" (optional): The model for the test (default is "gpt-3.5-turbo").
                - "include_reason" (optional): Whether to include the reason for the result (default is True).
                - "threshold" (optional): The threshold for the test (default is 0.5).

        Returns:
            The result of the contextual precision test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = ContextualPrecisionTest(
                question=test_data["prompt"],
                expected_output=test_data["expected_response"],
                retrieval_context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                include_reason=test_data["test_arguments"].get("include_reason", True),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            ).run()

        # TODO: Check if the results are in the desired form
        return res

    def run_contextual_recall_test(self, test_data):
        """
        A function to run contextual recall test.

        Args:
            self: The object itself.
            test_data (dict): A dictionary containing test data with the following keys:
                - expected_response (str): The expected response text.
                - context (str): The context for the test.
                - model (str, optional): The model to use for the test. Defaults to "gpt-3.5-turbo".
                - include_reason (bool, optional): Whether to include reason in the test. Defaults to True.
                - threshold (float, optional): The threshold for the test. Defaults to 0.5.

        Returns:
            The result of the contextual recall test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = ContextualRecallTest(
                expected_output=test_data["expected_response"],
                retrieval_context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                include_reason=test_data["test_arguments"].get("include_reason", True),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            ).run()

        # TODO: Check if the results are in the desired form
        return res

    def run_contextual_relevancy_test(self, test_data):
        """
        A function to run a contextual relevancy test using the given test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing the test data with keys "prompt", "context", "model", "include_reason", and "threshold"

        Returns:
            The result of the contextual relevancy test
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = ContextualRelevancyTest(
                question=test_data["prompt"],
                retrieval_context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                include_reason=test_data["test_arguments"].get("include_reason", True),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            ).run()

        # TODO: Check if the results are in the desired form
        return res

    def run_faithfulness_test(self, test_data):
        """
        A function to run a faithfulness test on the given test data.

        Args:
            self: The object itself.
            test_data (dict): A dictionary containing the test data with the following keys:
                - "response": The response for the test.
                - "context": The context for the test.
                - "model" (optional): The model for the test. Defaults to "gpt-3.5-turbo".
                - "include_reason" (optional): Whether to include reason in the test. Defaults to True.
                - "threshold" (optional): The threshold for the test. Defaults to 0.5.

        Returns:
            The result of the faithfulness test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = FaithfulnessTest(
                answer=test_data["response"],
                retrieval_context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                include_reason=test_data["test_arguments"].get("include_reason", True),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            ).run()

        # TODO: Check if the results are in the desired form
        return res

    def run_maliciousness_test(self, test_data):
        """
        Run a summarization test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing prompt, response, model, and threshold.

        Returns:
            The result of the summarization test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = maliciousness_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_summarization_test(self, test_data):
        """
        Run a summarization test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing prompt, response, model, and threshold.

        Returns:
            The result of the summarization test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = SummarisationTest(
                source_document=test_data["prompt"],
                summary=test_data["response"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            ).run()

        # TODO: Check if the results are in the desired form
        return res

    def run_prompt_injection_test(self, test_data):
        """
        Run prompt injection test using the given test data.

        Parameters:
            self: the object itself
            test_data (dict): a dictionary containing the prompt and threshold

        Returns:
            The result of the prompt injection test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = prompt_injection_test(
                prompt=test_data["prompt"],
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_sentiment_analysis_test(self, test_data):
        """
        Run sentiment analysis test using the given test data.

        Parameters:
            self: the object itself
            test_data (dict): a dictionary containing the response and threshold

        Returns:
            The result of the response sentiment test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = sentiment_analysis_test(
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_toxicity_test(self, test_data):
        """
        Run toxicity test using the given test data.

        Parameters:
            self: the object itself
            test_data (dict): a dictionary containing the response and threshold

        Returns:
            The result of the response toxicity test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = toxicity_test(
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_conciseness_test(self, test_data):
        """
        A function to run conciseness test.

        Args:
            self: The object itself.
            test_data (dict): A dictionary containing test data with the following keys:
                - prompt (str): The prompt text.
                - response (str): The response text.
                - expected_response (str): The expected response text.
                - context (str): The context for the test.
                - model (str, optional): The model to use for the test. Defaults to "gpt-3.5-turbo".
                - threshold (float, optional): The threshold for the test. Defaults to 0.5.

        Returns:
            The result of the conciseness test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = conciseness_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                expected_response=test_data["expected_response"],
                context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_coherence_test(self, test_data):
        """
        A function to run coherence test.

        Args:
            self: The object itself.
            test_data (dict): A dictionary containing test data with the following keys:
                - prompt (str): The prompt text.
                - response (str): The response text.
                - expected_response (str): The expected response text.
                - context (str): The context for the test.
                - model (str, optional): The model to use for the test. Defaults to "gpt-3.5-turbo".
                - threshold (float, optional): The threshold for the test. Defaults to 0.5.

        Returns:
            The result of the coherence test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = coherence_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                expected_response=test_data["expected_response"],
                context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_correctness_test(self, test_data):
        """
        A function to run correctness test.

        Args:
            self: The object itself.
            test_data (dict): A dictionary containing test data with the following keys:
                - prompt (str): The prompt text.
                - response (str): The response text.
                - expected_response (str): The expected response text.
                - context (str): The context for the test.
                - model (str, optional): The model to use for the test. Defaults to "gpt-3.5-turbo".
                - threshold (float, optional): The threshold for the test. Defaults to 0.5.

        Returns:
            The result of the correctness test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = correctness_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                expected_response=test_data["expected_response"],
                context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_consistency_test(self, test_data):
        """
        A function to run a consistency test on the given test data.

        Args:
            self: The object itself.
            test_data (dict): A dictionary containing the test data with the following keys:
                - prompt (str): The prompt given to the model.
                - response (str): The model's response to the prompt.
                - model (str): The name of the model being evaluated (default is "gpt-3.5-turbo").
                - threshold(float): The threshold score above this the prompt will be flagged as injection prompt.

        Returns:
            The result of the consistency test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = consistency_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_cover_test(self, test_data):
        """
        Run a cover_test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing response, concept set.

        Returns:
            The result of the cover test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = cover_test(
                response=test_data["response"],
                concept_set=test_data["concept_set"],
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_pos_test(self, test_data):
        """
        Run a pos_test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing response, concept set.

        Returns:
            The result of the pos test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = pos_test(
                response=test_data["response"],
                concept_set=test_data["concept_set"],
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_length_test(self, test_data):
        """
        Run a length_test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing response.

        Returns:
            The result of the length test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = length_test(
                response=test_data["response"],
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_winner_test(self, test_data):
        """
        Run a winner_test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing response, ground_truth, concept_set, model, temperature, max_tokens.


        Returns:
            The result of the winner test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = winner_test(
                response=test_data["response"],
                expected_response=test_data["expected_response"],
                concept_set=test_data["concept_set"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                temperature=test_data["test_arguments"].get("temperature", 0),
                max_tokens=test_data["test_arguments"].get("max_tokens", 512),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_overall_test(self, test_data):
        """
        Run a overall_test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing response, ground_truth, concept_set, model, temperature, max_tokens.


        Returns:
            The result of the overall test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = overall_test(
                response=test_data["response"],
                expected_response=test_data["expected_response"],
                concept_set=test_data["concept_set"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                temperature=test_data["test_arguments"].get("temperature", 0),
                max_tokens=test_data["test_arguments"].get("max_tokens", 512),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_refusal_test(self, test_data):
        """
        Run a refusal_test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing response, threshold.

        Returns:
            The result of the refusal test.
        """
        # TODO: Check of the parameters are valid
        res = refusal_test(
            response=test_data["response"],
            threshold=test_data["test_arguments"].get("threshold", 0.5),
        )
        # TODO: Check if the results are in the desired form
        return res

    def run_answer_correctness_test(self, test_data):
        """
        Run an answer correctness test using the given test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing the test data with keys "prompt", "response", "expected_response", "context", "model", and "threshold".
        Returns:
            The result of the answer correctness test.
        """

        # TODO: Check of the parameters are valid
        res = AnswerCorrectnessTest(
            prompt=test_data["prompt"],
            response=test_data["response"],
            expected_response=test_data["expected_response"],
            context=test_data["context"],
            model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
            threshold=test_data["test_arguments"].get("threshold", 0.5),
        ).run()

        return res

    def run_generic_evaluation_test(self, test_data):
        """
        Run a generic test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing prompt, response, model name to use for evaluation,
            evalutaion_name, evaluation criteria, reason to include and threshold to apply


        Returns:
            The result of the evaluation test.
        """
        # TODO: Check of the parameters are valid

        with SuppressOutput():
            res = generic_evaluation_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                evaluation_name=test_data["test_arguments"].get("evaluation_name"),
                evaluation_criteria=test_data["test_arguments"].get(
                    "evaluation_criteria"
                ),
                include_reason=test_data["test_arguments"].get("include_reason", True),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        # TODO: Check if the results are in the desired form
        return res

    def run_hallucination_test(self, test_data):
        """
        Run a hallucination test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing prompt, response, context, model, include_reason, and threshold.

        Returns:
            The result of the hallucination test.
        """

        with SuppressOutput():
            res = hallucination_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                context=test_data["context"],
                model=test_data["test_arguments"].get("model", "gpt-3.5-turbo"),
                include_reason=test_data["test_arguments"].get("include_reason", True),
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        return res

    def run_bias_test(self, test_data):
        """
        Run a bias test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing prompt, response, and threshold.

        Returns:
            The result of the bias test.
        """

        with SuppressOutput():
            res = bias_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        return res

    def run_response_toxicity_test(self, test_data):
        """
        Run a response toxicity test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing prompt, response, and threshold.

        Returns:
            The result of the response toxicity test.
        """

        with SuppressOutput():
            res = response_toxicity_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        return res

    def run_readability_test(self, test_data):
        """
        Run a readability score test using the given test data.

        Args:
            self: the object instance
            test_data (dict): A dictionary containing prompt, response, threshold
        Returns:
            The readability score
        """
        with SuppressOutput():
            res = readability_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 5),
            )

        return res

    def run_cosine_similarity_test(self, test_data):
        """
        Run a cosine similarity test using the given test data.

        Args:
            self: the object instance
            test_data (dict): A dictionary containing prompt, response, threshold
        Returns:
            The cosine similarity score
        """
        with SuppressOutput():
            res = cosine_similarity_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 0.5),
            )

        return res

    def run_grade_score_test(self, test_data):
        """
        Run a grade score test using the given test data.

        Args:
            self: the object instance
            test_data (dict): A dictionary containing prompt, response, threshold
        Returns:
            The grade score
        """
        with SuppressOutput():
            res = grade_score_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 5),
            )

        return res

    def run_complexity_test(self, test_data):
        """
        Run a complexity test using the given test data.

        Args:
            self: the object instance
            test_data(dict): A dictionary containing prompt, response, threshold
        Returns:
            The complexity score
        """
        with SuppressOutput():
            res = complexity_test(
                prompt=test_data["prompt"],
                response=test_data["response"],
                threshold=test_data["test_arguments"].get("threshold", 5),
            )

        return res

    def run_harmless_test(self, test_data):
        """
        Run a harmless test using the provided test data.

        Args:
            self: The object instance
            test_data (dict): A dictionary containing prompt, response, model name to use for evaluation,
            threshold to apply

        Returns:
            The result of the evaluation test.
        """
        # TODO: Check of the parameters are valid

        # with SuppressOutput():
        #     tru_evaluation = harmless_test.TruEvaluation(
        #         response=test_data["response"],
        #         context=test_data["context"],
        #         prompt=test_data["prompt"],
        #     )

        # tru_evaluation.run_evaluations()
        # leaderboard = tru_evaluation.get_leaderboard()

        # maliciousness_score = leaderboard["Violent"][0]
        # is_malicious = (
        #     "Passed" if maliciousness_score > test_data["threshold"] else "Failed"
        # )

        # # Prepare and return the result
        # result = {
        #     "prompt": test_data["prompt"],
        #     "response": test_data["response"],
        #     "context": test_data["context"],
        #     "score": maliciousness_score,
        #     "is_passed": is_malicious,
        #     "threshold": test_data["threshold"],
        # }

        result = {}

        # TODO: Check if the results are in the desired form
        return result
