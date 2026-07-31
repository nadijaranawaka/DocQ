def contextBuilder(result:dict) -> list:
    context = []

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]

    for document,metadata in zip(documents,metadatas):
        context.append(
            {
                "page":metadata["page"],
                "source":metadata["source"],
                "text": document
            }
        )
    return context