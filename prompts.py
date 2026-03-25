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

            "you will put all the identified inclusion criterias in a list called included like this: included = ['IC1', 'IC2']\n"
            "you will put all the identified exclusion criterias in a list called excluded like this: excluded = ['EC1', 'EC4']\n" 
            "analysing those 2 lists YOU created (included and excluded) you will determine the llm status, following these rules:\n"
            "- if the included list is NOT empty and the excluded list is empty, the llm status will be INCLUDED\n"
            "- if the excluded list is NOT empty and the included list is empty, the llm status will be EXCLUDED\n"
            "- Any other situation, meaning the llm status is NOT INCLUDED and NOT EXCLUDED, the llm status be marked as PENDING\n"

            "IMPORTANT:\n"
            "- If you are unsure about a criteria, DO NOT include its code in the output.\n"
            "- Do not try to infer details that are not suggested by the title/abstract.\n\n"

            "Now analyze this study:\n\n"
            f"TITLE: {title.strip()}\n"
            f"ABSTRACT: {abstract.strip()}\n"
        )