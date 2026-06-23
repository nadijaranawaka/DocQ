def build_prompt(question, chunks):
    # Need more prompt engineering
    context = "\n\n".join(chunks)

    prompt = f"""
    Answer the following question using ONLY the provided context,

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    return prompt