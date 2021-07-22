from query_register import registered_queries,registered_output_schemas

def queryBuilder(input_filter, base_query, output_schema, required_output):
    base_query = base_query + builderReturn(output_schema,
                                            required_output)
    for filterOption in input_filter:
        if input_filter[filterOption] == "":
            # replace
            #CASE $meno_status WHEN [] THEN all_meno_status #ELSE $meno_status END
            #to
            #all_meno_status
            base_query = base_query.replace(
                "ELSE $" + filterOption + " END", "").replace(
                    "CASE $" + filterOption + " WHEN [] THEN ", "")
        else:
            # replace
            #CASE $meno_status WHEN [] THEN all_meno_status ELSE $meno_status END
            #to
            #$meno_status's value
            base_query = base_query[:base_query.find(
                "CASE $" + filterOption
            )] + input_filter[filterOption] + base_query[base_query.find(
                " $" + filterOption + " END") + len(filterOption) + 6:]
    return base_query


def builderReturn(output_schema, required_output):
    query = ""
    #base on the input filter to find the query and append to the query
    for schema in output_schema:
        if schema in output_schema and required_output[schema]:
            query = query + output_schema[schema] + " ,"
    return query


# factory defines which query builder to use
def BentoQueryBuilderFactory(type, input_filter, required_output):
    query = registered_queries;
    outputSchema = registered_output_schemas;
    return queryBuilder(input_filter, query[type], outputSchema[type],required_output)

