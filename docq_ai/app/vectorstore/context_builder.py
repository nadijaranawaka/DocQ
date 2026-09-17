def contextBuilder(result:dict) -> list:
    context = []

    documents = result["documents"]
    metadatas = result["metadatas"]

    for document,metadata in zip(documents,metadatas):
        context.append(
            {
                "page":metadata["page"],
                "source":metadata["source"],
                "text": document
            }
        )
    return context