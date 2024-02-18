from openai import OpenAI
import os
import json
from prompt_template import FaithfulnessTemplate


class FaithfulnessTest:
    def __init__(
        self,
        answer,
        retrieval_context,
        include_reason=True,
        model="gpt-3.5-turbo",
        threshold=0.5,
        temperature=0,
    ):
        self.retrieval_context = retrieval_context
        self.answer = answer
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

    def generate_truths(self):
        prompt = FaithfulnessTemplate.generate_truths(self.retrieval_context)
        truths_response = self.model(prompt)
        truths = json.loads(self.trim_to_json(truths_response))
        return truths

    def generate_claims(self):
        prompt = FaithfulnessTemplate.generate_claims(self.answer)
        claims_response = self.model(prompt)
        claims = json.loads(self.trim_to_json(claims_response))
        return claims

    def generate_verdicts(self, claims, truths):
        prompt = FaithfulnessTemplate.generate_verdicts(
            claims=claims, retrieval_context=truths
        )
        verdict_response = self.model(prompt)
        verdicts = json.loads(self.trim_to_json(verdict_response))["verdicts"]
        return verdicts

    def generate_score(self, verdicts):
        if len(verdicts) == 0:
            return 0

        faithfulness_count = sum(
            1 for verdict in verdicts if verdict["verdict"].strip().lower() != "no"
        )
        return faithfulness_count / len(verdicts)

    def generate_reason(self, verdicts, score):
        contradictions = [
            verdict["reason"]
            for verdict in verdicts
            if verdict["verdict"].strip().lower() == "no"
        ]
        prompt = FaithfulnessTemplate.generate_reason(
            contradictions=contradictions, score=format(score, ".2f")
        )
        reason_response = self.model(prompt)
        reason = self.trim_to_json(reason_response)
        return reason

    def run_test(self):
        truths = self.generate_truths()
        claims = self.generate_claims()
        verdicts = self.generate_verdicts(claims, truths)
        score = self.generate_score(verdicts)

        result = {
            "response": self.answer,
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
            reason = self.generate_reason(verdicts, score)
            result["reason"] = reason

        return result


if __name__ == "__main__":
    response = "Paris, london"
    context = ["Paris is the capital of France.", "london is a city"]
    test_instance = FaithfulnessTest(response, context)
    result = test_instance.run_test()
    print(result)
