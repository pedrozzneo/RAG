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
            "2- the key is llmStatus and the content is a string like this: llmStatus = INCLUDED or llmStatus = EXCLUDED or llmStatus = PENDING \n"

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

def build_prompt3(title: str, abstract: str) -> str:
        return (
            "You are assisting in a systematic literature review about service-oriented robotic systems.\n"
            "Just to give you context, here are the Research Questions (RQs) that we are trying to answer:\n"
            "RQ1: How has service-orientation been applied to the development of robotic systems? This question aims to identify the abstraction level, such as sensors/actuators,actions or the whole robot, on which services have been developed?\n"
            "RQ2: What is the most common way of interaction among service-oriented robotic systems? The main objective of this question is to identify how services interact in the robotics domain. This interaction could be made, for example, between: sensorrobot, robotrobot, robotback-end or robotexternal services\n"
            "RQ3: What implementation technology has been mostly used to develop service-oriented robotic systems? The aim is to verify which implementation technology, such as SOAP and REST, is mostly used to develop service-oriented robotic systems;\n"
            "RQ4: What are the development environments and tools that support the development of service-oriented robotic systems? The objective is to identify development environments and tools used to develop robotic systems based on SOA\n"
            "RQ5: Is SOA applicable to all types of robots? This question aims at identifying if SOA is a viable solution for all robotic systems and their operational situation. Otherwise, in what area or context has SOA been mostly applied to robotic systems?\n"
            "RQ6: How has Software Engineering been applied to the development of service- oriented robotic systems? This question aims at identifying the software engineering knowledge, such as processes, activities, methods, and techniques used during the development of service-oriented robotic systems\n"

            "Your task is to return as a JSON object the following key-value pairs:\n"
            "1- the key is llmCriterias and the value is a list of checked inclusion and exclusion criterias like this: llmCriterias = ['IC1', 'EC2', 'IC2']\n"
            "2- the key is llmStatus and the content is a string like this: llmStatus = INCLUDED or llmStatus = EXCLUDED or llmStatus = PENDING \n"

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