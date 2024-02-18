from openai import OpenAI
import os
import json
from prompt_template import ContextualRecallTemplate


class ContextualRecallTest:
    def __init__(
        self,
        expected_output,
        retrieval_context,
        include_reason=True,
        model="gpt-3.5-turbo",
        threshold=0.5,
        temperature=0,
    ):
        self.expected_output = expected_output
        self.retrieval_context = retrieval_context
        self.include_reason = include_reason
        self.model_name = model
        self.threshold = threshold
        self.temperature = temperature

        # Key setup
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not defined. Please set it with your OpenAI API key."
            )
        self.client = OpenAI()

    def model(self, prompt):
        return self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=[{"role": "system", "content": prompt}],
        )

    def trim_to_json(self, response):
        message_content = response.choices[0].message.content
        data = json.dumps(message_content)
        return json.loads(data)

    def generate_verdicts(self):
        verdict_prompt = ContextualRecallTemplate.generate_verdicts(
            self.expected_output, self.retrieval_context
        )
        verdict_response = self.model(verdict_prompt)
        verdicts = json.loads(self.trim_to_json(verdict_response))["verdicts"]
        return verdicts

    def generate_score(self, verdicts):
        if len(verdicts) == 0:
            return 0

        justified_sentences = sum(
            1 for verdict in verdicts if verdict["verdict"].lower() == "yes"
        )
        return justified_sentences / len(verdicts)

    def generate_reason(self, supportive_reasons, unsupportive_reasons, score):
        prompt = ContextualRecallTemplate.generate_reason(
            expected_output=self.expected_output,
            supportive_reasons=supportive_reasons,
            unsupportive_reasons=unsupportive_reasons,
            score=score,
        )

        res = self.model(prompt)
        reason = self.trim_to_json(res)
        return reason

    def run_test(self):
        verdicts = self.generate_verdicts()
        score = self.generate_score(verdicts)

        supportive_reasons = [
            verdict["reason"]
            for verdict in verdicts
            if verdict["verdict"].lower() == "yes"
        ]
        unsupportive_reasons = [
            verdict["reason"]
            for verdict in verdicts
            if verdict["verdict"].lower() != "yes"
        ]

        result = {
            "expected_response": self.expected_output,
            "context": self.retrieval_context,
            "score": score,
            "threshold": self.threshold,
            "is_passed": score >= self.threshold,
            "evaluated_with": {
                "model": self.model_name,
                "include_reason": self.include_reason,
            },
        }

        if self.include_reason:
            reason = self.generate_reason(
                supportive_reasons, unsupportive_reasons, score
            )
            result["reason"] = reason

        return result


if __name__ == "__main__":
    expected_response = "Paris"
    context = ["Paris is the capital of France.", "london is a city"]
    test_instance = ContextualRecallTest(expected_response, context)
    result = test_instance.run_test()
    print(result)
