from openai import OpenAI
import os
import json
from prompt_template import ContextualRelevancyTemplate


class ContextualRelevancyTest:
    def __init__(
        self,
        question,
        retrieval_context,
        include_reason=True,
        model="gpt-3.5-turbo",
        threshold=0.5,
        temperature=0,
    ):
        self.question = question
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
        verdict_prompt = ContextualRelevancyTemplate.generate_verdicts(
            self.question, self.retrieval_context
        )
        verdict_response = self.model(verdict_prompt)
        verdicts = json.loads(self.trim_to_json(verdict_response))["verdicts"]
        return verdicts

    def generate_score(self, verdicts_list):
        irrelevant_sentences = sum(
            1 for verdict in verdicts_list if verdict["verdict"].lower() == "no"
        )
        total_sentence_count = len(verdicts_list)

        if total_sentence_count == 0:
            return 0

        return (total_sentence_count - irrelevant_sentences) / total_sentence_count

    def generate_reason(self):
        if self.include_reason:
            irrelevant_sentences = []
            for index, verdict in enumerate(self.verdicts):
                if verdict["verdict"].strip().lower() == "no":
                    data = {"Node": index + 1, "Sentence": verdict["sentence"]}
                    irrelevant_sentences.append(data)

            prompt = ContextualRelevancyTemplate.generate_reason(
                input=self.question,
                irrelevant_sentences=irrelevant_sentences,
                score=format(self.score, ".2f"),
            )

            res = self.model(prompt)
            reason = self.trim_to_json(res)
            return reason

    def run_test(self):
        self.verdicts = self.generate_verdicts()
        self.score = self.generate_score(self.verdicts)

        result = {
            "prompt": self.question,
            "context": self.retrieval_context,
            "score": self.score,
            "threshold": self.threshold,
            "is_passed": self.score >= self.threshold,
            "evaluated_with": {
                "model": self.model_name,
                "include_reason": self.include_reason,
            },
        }

        if self.include_reason:
            reason = self.generate_reason()
            result["reason"] = reason

        return result


if __name__ == "__main__":
    prompt = "What is the capital of France?"
    context = ["Paris is the capital of France.", "london is a city"]
    test_instance = ContextualRelevancyTest(prompt, context)
    result = test_instance.run_test()
    print(result)
