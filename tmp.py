
icdc_schema=["study","studyType","Breed","Diagnosis",
    "Primary Disease Site","Stage of Disease","GENDER","Associated File Format","Associated File Type"]

class QueryBuilder(object):

    def factory(type,input):
        if type == "icdc":
            return icdcBuildQuery(input)
        if type == "ctdc":
            return ctdcBuildQuery(input)

def icdcBuildQuery(input)-> str:
    builder(input,icdc_schema)
    print("icdc builder")

def ctdcBuildQuery()-> str:
    print("ctdc builder")

def builder(input_data,input_schema):
    for schema in input_schema:
      if schema in input_data:
          print(input_data[schema])


if __name__ == "__main__":

    icdc_input_data = {
    "study":"COTC007B",
    "studyType":"Clinical Trial",
    "Breed":"Beagle",
    "Diagnosis":"Stage 3",
    "Primary Disease Site": "LYMPH NODE",
    "Stage of Disease": "IIIA",
    "GENDER":"Castrated male",
    "Associated File Format":'doc',
    "Associated File Type":'Pathology Report'
  }


    QueryBuilder("icdc",icdc_input_data)