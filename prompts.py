def build_prompt1(title: str, abstract: str) -> str:
        return (
            "You are assisting in a systematic literature review about service-oriented robotic systems.\n"
            "Your task is to return a list of checked inclusion criteria, a list of checked exclusion criteria and the llmStatus like this: included = [LIST OF INCLUDED CRITERIAS], excluded = [LIST OF EXCLUDED CRITERIAS], llmStatus = [LLMSTATUS]\n"

            "Inclusion criteria:\n"
            "IC1: The primary study proposes or reports on the design and development of a service-oriented robotic system.\n"
            "IC2: The primary study proposes or reports on a new technology for developing service-oriented robotic systems.\n"
            "IC3: The primary study proposes or reports on a process, method, technique, reference architecture or any software engineering guideline that supports either the design or the development of service-oriented robotic systems.\n\n"
            
            "Exclusion criteria:\n"
            "EC1: The primary study reports on the development of a robotic systems without using SOA.\n"
            "EC2: The primary study presents contributions in areas other than Robotics.\n"
            "EC3: The primary study does not report on the design or development of service-oriented robotic system.\n"
            "EC4: The study is a previous version of a more complete study about the same research.\n"
            "EC5: The primary study is a table of contents, short course description, tutorial, copyright form or summary of an event.\n\n"

            "you will put all the identified inclusion and exclusion criterias in a list called llmCriterias like this: llmCriterias = ['IC1', 'IC2', 'EC2']\n"
            "analysing this llmCriterias list YOU created you will determine the llm status, following these rules:\n"
            "- if the number of inclusion criterias is more than 0 and the number of exclusion criteria is 0, the llm status will be INCLUDED\n"
            "- if the number of inclusion criterias is 0 and the number of exclusion criteria is more than 0, the llm status will be EXCLUDED\n"
            "- Any other situation, meaning the number of inclusion and exclusion criterias is more than 0, the llm status be marked as PENDING\n"

            "IMPORTANT:\n"
            "- If you are unsure about a criteria, DO NOT include its code in the output.\n"
            "Return ONLY a JSON object containing the key-value pairs of the criterias found (put together the inclusino criterias and the exclusion criterias) and the llmstatus "
            "- Do not try to infer details that are not suggested by the title/abstract.\n\n"

            "Now analyze this study:\n\n"
            f"TITLE: {title.strip()}\n"
            f"ABSTRACT: {abstract.strip()}\n"
        )

def build_prompt2(title: str, abstract: str) -> str:
        return (
            "You are assisting in a systematic literature review about service-oriented robotic systems.\n"
            "Your task is to return as a JSON object the following key-value pairs:\n"
            "1- the key is llmCriterias and the value is a list of checked inclusion and exclusion criterias like this: llmCriterias = ['IC1', 'EC2', 'IC2']\n"
            "2- the key is llmStatus and the content is a string like this: llmStatus = [INCLUDED] or llmStatus = [EXCLUDED] or llmStatus = [PENDING] \n"

            "To define the llmCriterias, use this source below:\n"

            "Inclusion criteria:\n"
            "IC1: The primary study proposes or reports on the design and development of a service-oriented robotic system.\n"
            "IC2: The primary study proposes or reports on a new technology for developing service-oriented robotic systems.\n"
            "IC3: The primary study proposes or reports on a process, method, technique, reference architecture or any software engineering guideline that supports either the design or the development of service-oriented robotic systems.\n\n"
            
            "Exclusion criteria:\n"
            "EC1: The primary study reports on the development of a robotic systems without using SOA.\n"
            "EC2: The primary study presents contributions in areas other than Robotics.\n"
            "EC3: The primary study does not report on the design or development of service-oriented robotic system.\n"
            "EC4: The study is a previous version of a more complete study about the same research.\n"
            "EC5: The primary study is a table of contents, short course description, tutorial, copyright form or summary of an event.\n\n"

            "To define the llmStatus, analyse the llmCriterias list you created, following these rules:\n"
            "- if the number of inclusion criterias is more than 0 and the number of exclusion criteria is 0, the llm status will be INCLUDED, example: llmCriterias = ['IC1', 'IC2']\n"
            "- if the number of inclusion criterias is 0 and the number of exclusion criteria is more than 0, the llm status will be EXCLUDED, example: llmCriterias = ['EC2', 'EC4']\n"
            "- Any other situation, meaning the number of inclusion and exclusion criterias is more than 0, the llm status be marked as PENDING, example: llmCriterias = ['IC1', 'EC2', 'IC2']\n"

            "IMPORTANT:\n"
            "- If you are unsure about a criteria, just skip it.\n"
            "- Do not try to infer details that are not suggested by the title/abstract.\n\n"

            "Now analyze this study:\n\n"
            f"TITLE: {title.strip()}\n"
            f"ABSTRACT: {abstract.strip()}\n"
        )