from typing import Callable, List

import re

from parea.evals.utils import call_openai
from parea.schemas.log import Log


def percent_target_supported_by_context_factory(question_field: str = "question", context_fields: list[str] = ["context"]) -> Callable[[Log], float]:
    """Quantifies how many sentences in the target/ground truth are supported by the retrieved context."""

    def percent_target_supported_by_context(log: Log) -> float:
        """Quantifies how many sentences in the target/ground truth are supported by the retrieved context."""
        question = log.inputs[question_field]
        context = "\n".join(log.inputs[context_field] for context_field in context_fields)
        target = log.target

        classification = call_openai(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "user",
                    "content": f"""\
Given a context, and an answer, analyze each sentence in the answer and classify if the sentence can be attributed to the given context or not. Output json with reason.


question: What can you tell me about albert Albert Einstein?
context: Albert Einstein (14 March 1879 – 18 April 1955) was a German-born theoretical physicist,widely held to be one of the greatest and most influential scientists of all time. Best known for developing the theory of relativity, he also made important contributions to quantum mechanics, and was thus a central figure in the revolutionary reshaping of the scientific understanding of nature that modern physics accomplished in the first decades of the twentieth century. His mass–energy equivalence formula E = mc2, which arises from relativity theory, has been called "the world's most famous equation". He received the 1921 Nobel Prize in Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect", a pivotal step in the development of quantum theory. His work is also known for its influence on the philosophy of science. In a 1999 poll of 130 leading physicists worldwide by the British journal Physics World, Einstein was ranked the greatest physicist of all time. His intellectual achievements and originality have made Einstein synonymous with genius.
answer: Albert Einstein born in 14 March 1879 was  German-born theoretical physicist, widely held to be one of the greatest and most influential scientists of all time. He received the 1921 Nobel Prize in Physics "for his services to theoretical physics. He published 4 papers in 1905.  Einstein moved to Switzerland in 1895
classification:
[
    {{
        "statement_1":"Albert Einstein, born on 14 March 1879, was a German-born theoretical physicist, widely held to be one of the greatest and most influential scientists of all time.",
        "reason": "The date of birth of Einstein is mentioned clearly in the context.",
        "Attributed": "Yes"
    }},
    {{
        "statement_2":"He received the 1921 Nobel Prize in Physics 'for his services to theoretical physics.",
        "reason": "The exact sentence is present in the given context.",
        "Attributed": "Yes"
    }},
    {{
        "statement_3": "He published 4 papers in 1905.",
        "reason": "There is no mention about papers he wrote in the given context.",
        "Attributed": "No"
    }},
    {{
        "statement_4":"Einstein moved to Switzerland in 1895.",
        "reason": "There is no supporting evidence for this in the given context.",
        "Attributed": "No"
    }}
]

question: who won 2020 icc world cup?
context: Who won the 2022 ICC Men's T20 World Cup?
The 2022 ICC Men's T20 World Cup, held from October 16 to November 13, 2022, in Australia, was the eighth edition of the tournament. Originally scheduled for 2020, it was postponed due to the COVID-19 pandemic. England emerged victorious, defeating Pakistan by five wickets in the final to clinch their second ICC Men's T20 World Cup title.
answer: England
classification:
[
    {{
        "statement_1":"England won the 2022 ICC Men's T20 World Cup.",
        "reason": "From context it is clear that England defeated Pakistan to win the World Cup.",
         "Attributed": "Yes"
    }}
]

question: {question}
context: {context}
answer: {target}
classification:
""",
                }
            ],
            temperature=0.0,
        )
        pattern = r"\[\s*\{.*?\}(\s*,\s*\{.*?\})*\s*\]"
        match = re.search(pattern, classification.replace("\n", ""))
        if match:
            response = eval(classification)
            numerator = sum(item.get("Attributed").lower() == "yes" for item in response)
            return numerator / len(response)
        else:
            return 0.0

    return percent_target_supported_by_context
