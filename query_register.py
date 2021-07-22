from search_query import search_query,search_return
from filter_query import filtering_query,filter_return
from bento_file_tab_query import file_tab_query, file_tab_return
from bento_sample_tab_query import sample_tab_query,sample_tab_return


registered_queries = {
  "search_query": search_query, 
  "case_tab_query": filtering_query,
  "sample_tab_query":sample_tab_query,
  "file_tab_query":file_tab_query
}

registered_output_schemas = {
        "search_query": search_return,
        "case_tab_query": filter_return,
        "sample_tab_query":sample_tab_return,
        "file_tab_query":file_tab_return
}