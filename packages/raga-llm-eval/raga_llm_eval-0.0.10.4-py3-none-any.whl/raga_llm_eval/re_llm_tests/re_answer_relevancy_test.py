from openai import OpenAI
import os
import json
from prompt_template import AnswerRelevancyTemplate


class AnswerRelevancyTest:
    def __init__(
        self,
        question,
        answer,
        retrieval_context,
        include_reason=True,
        model="gpt-3.5-turbo",
        threshold=0.5,
        temperature=0,
    ):
        self.answer = answer
        self.retrieval_context = retrieval_context
        self.question = question
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

    def generate_key_points(self):
        key_points_prompt = AnswerRelevancyTemplate.generate_key_points(
            self.answer, self.retrieval_context
        )
        key_points_response = self.model(key_points_prompt)
        data = json.loads(self.trim_to_json(key_points_response))
        key_points = data["key_points"]
        return key_points

    def generate_verdicts(self, key_points):
        verdict_prompt = AnswerRelevancyTemplate.generate_verdicts(
            self.question, key_points
        )
        verdict_response = self.model(verdict_prompt)
        verdicts = json.loads(self.trim_to_json(verdict_response))["verdicts"]
        return verdicts

    def generate_score(self, verdicts):
        if len(verdicts) == 0:
            return 0

        relevant_count = sum(
            1 for verdict in verdicts if verdict["verdict"].strip().lower() != "no"
        )
        return relevant_count / len(verdicts)

    def generate_reason(self, verdicts, key_points, score):
        for i in range(len(verdicts)):
            verdicts[i]["key_point"] = key_points[i]

        irrelevant_points = [
            verdict["key_point"]
            for verdict in verdicts
            if verdict["verdict"].strip().lower() == "no"
        ]

        prompt = AnswerRelevancyTemplate.generate_reason(
            irrelevant_points=irrelevant_points,
            original_question=self.question,
            answer=self.answer,
            score=format(score, ".2f"),
        )

        res = self.model(prompt)
        reason = self.trim_to_json(res)
        return reason

    def run_test(self):
        key_points = self.generate_key_points()
        verdicts = self.generate_verdicts(key_points)
        score = self.generate_score(verdicts)

        result = {
            "prompt": self.question,
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
            reason = self.generate_reason(verdicts, key_points, score)
            result["reason"] = reason

        return result


if __name__ == "__main__":
    prompt = "What is the capital of France?"
    response = "paris, london"
    context = ["Paris is the capital of France.", "london is a city"]

    test_instance = AnswerRelevancyTest(prompt, response, context)
    result = test_instance.run_test()
    print(result)
