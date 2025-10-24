from multi_query import MultiQuery

multi_query = MultiQuery()

queries = multi_query.generate_multiple_queries(
    "Can you tell me about Part 2 of the Developer's Guide to AI")

print(queries)
