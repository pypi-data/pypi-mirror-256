

class CorrectnessTemplate:
    @staticmethod
    def generate_correctness_prompt(question, answer, expected_response, context):
        return f"""Given the input with question, answer, expected_response, context and based on the instruction below create JSON similar to the examples for the input with keys `question`, `answer`, `expected_response`, `extracted_statements`: 
    Input:
    {{{{"question": 
    {question}
    "answer":
    {answer}
    "expected_response":
    {expected_response}
    "context":
    {context}
    }}}}
        

    Instruction:
    Extract following from input question, ground truth based on the context
    "extraced_statements":
        "TP": statements that are present in both the answer and the ground truth,
        "FP": statements present in the answer but not found in the ground truth,
        "FN": relevant statements found in the ground truth but omitted in the answer,
    

    Example: 
    {{
        "question": "What powers the sun and what is its primary function?",
        "answer": "The sun is powered by nuclear fission, similar to nuclear reactors on Earth, and its primary function is to provide light to the solar system.",
        "ground_truth": "The sun is actually powered by nuclear fusion, not fission. In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy. This energy is what lights up the sun and provides heat and light, essential for life on Earth. The sun's light also plays a critical role in Earth's climate system and helps to drive the weather and ocean currents.",
        "extracted_statements": {{
            "TP": ["The sun's primary function is to provide light"],
            "FP": [
                "The sun is powered by nuclear fission",
                "similar to nuclear reactors on Earth",
            ],
            "FN": [
                "The sun is powered by nuclear fusion, not fission",
                "In its core, hydrogen atoms fuse to form helium, releasing a tremendous amount of energy",
                "This energy provides heat and light, essential for life on Earth",
                "The sun's light plays a critical role in Earth's climate system",
                "The sun helps to drive the weather and ocean currents",
            ],
        }},
    }},
    {{
        "question": "What is the boiling point of water?",
        "answer": "The boiling point of water is 100 degrees Celsius at sea level.",
        "ground_truth": "The boiling point of water is 100 degrees Celsius (212 degrees Fahrenheit) at sea level, but it can change with altitude.",
        "extracted_statements": {{
            "TP": [
                "The boiling point of water is 100 degrees Celsius at sea level"
            ],
            "FP": [],
            "FN": [
                "The boiling point can change with altitude",
                "The boiling point of water is 212 degrees Fahrenheit at sea level",
            ],
        }},
    }}
    ===== END OF EXAMPLE ======
    The key extracted_statements in the JSON should stricly have multiple sentences separated by comma if any.
    """ 