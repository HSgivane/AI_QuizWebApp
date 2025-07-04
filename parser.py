import re

def parse_test(text):
    questions = []
    blocks = re.split(r'(?:\n\s*|\A)\d+\.\s+', text.strip())[1:]
    for block in blocks:
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        if not lines:
            continue
        question = lines[0]
        options = {}
        answer = None

        for line in lines[1:]:
            opt_match = re.match(r'^([a-d])\)\s+(.*)', line)
            if opt_match:
                options[opt_match.group(1)] = opt_match.group(2)
            elif line.startswith("Ответ:"):
                ans_match = re.search(r'Ответ:\s+([a-d])\)', line)
                if ans_match:
                    answer = ans_match.group(1)

        if question and options and answer:
            questions.append({
                "question": question,
                "options": options,
                "correct": answer
            })

    return questions
