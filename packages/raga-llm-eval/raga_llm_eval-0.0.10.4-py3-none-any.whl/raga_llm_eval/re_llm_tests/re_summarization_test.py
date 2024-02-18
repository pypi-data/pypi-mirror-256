from openai import OpenAI
import os
import json
from prompt_template import SummarizationTemplate


class SummarizationTest:
    def __init__(
        self,
        source_document,
        summary,
        n=3,  # no of questions to generate
        model="gpt-3.5-turbo",
        threshold=0.5,
        temperature=0,
    ):
        self.source_document = source_document
        self.summary = summary
        self.n = n
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

    def generate_questions(self, score_type):
        if score_type == "alignment":
            prompt = SummarizationTemplate.closed_end_questions_template(
                n=self.n, text=self.summary
            )
        elif score_type == "inclusion":
            prompt = SummarizationTemplate.closed_end_questions_template(
                n=self.n, text=self.source_document
            )

        res = self.model(prompt)
        json_output = self.trim_to_json(res)
        data = json.loads(json_output)
        return data["questions"]

    def get_answer(self, question, text):
        prompt = SummarizationTemplate.closed_end_answers_template(
            question=question, text=text
        )
        res = self.model(prompt)
        reason = self.trim_to_json(res)
        return reason

    def get_score(self, score_type):
        questions = []
        if score_type == "alignment":
            questions = self.generate_questions(score_type)
        elif score_type == "inclusion":
            questions = self.generate_questions(score_type)

        score = 0
        interval = 1 / len(questions)
        for question in questions:
            source_answer = self.get_answer(question, self.source_document)
            summary_answer = self.get_answer(question, self.summary)

            if source_answer.strip().lower() == summary_answer.strip().lower():
                score += interval
        return score

    def run_test(self):
        alignment_score = self.get_score("alignment")
        inclusion_score = self.get_score("inclusion")
        summarization_score = min(alignment_score, inclusion_score)

        result = {
            "prompt": self.source_document,
            "response": self.summary,
            "score": summarization_score,
            "threshold": self.threshold,
            "is_passed": summarization_score >= self.threshold,
            "evaluated_with": {
                "model": self.model_name,
                "n": self.n,
            },
        }

        return result


if __name__ == "__main__":
    prompt = """
The 'inclusion score' is calculated as the percentage of assessment questions
for which both the summary and the original document provide a 'yes' answer. This
method ensures that the summary not only includes key information from the original
text but also accurately represents it. A higher inclusion score indicates a
more comprehensive and faithful summary, signifying that the summary effectively
encapsulates the crucial points and details from the original content.
"""
    response = """
The inclusion score quantifies how well a summary captures and
accurately represents key information from the original text,
with a higher score indicating greater comprehensiveness.
"""
    test_instance = SummarizationTest(prompt, response, n=3)
    result = test_instance.run_test()
    print(result)
