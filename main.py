from flask import Flask
from Commons_Query import CommonsQueryBuilderFactory
from bento_query_service import BentoQueryBuilderFactory

app = Flask('app')


@app.route('/bento/search_query')
def bento_search_query():

    search_input_filter = {
        "rc_scores": "",
        "diagnoses": "",
        "tumor_sizes": "",
        "tumor_grades": "",
        "er_status": "",
        "pr_status": "",
        "chemo_regimen": "",
        "endo_therapies": "",
        "programs": "",
        "studies": "",
        "meno_status": "",
    }

    search_require_return = {"study_subject_id": True}

    search =BentoQueryBuilderFactory("search_query", search_input_filter, search_require_return)

    return "search_query:  " + search



@app.route('/')
def bento_filter_query():
    input_filter = {
        "rc_scores": "",
        "tumor_sizes": "",
        "tumor_grades": "",
        "er_status": "",
        "pr_status": "",
        "chemo_regimen": "",
        "endo_therapies": "",
        "programs": "",
        "studies": "",
        "diagnoses": "",
        "meno_status": "",
        "associations": "",
        "tissue_type": "",
        "tissue_composition": "",
        "arms": "",
        "menopause_status": "",
        "recurrence_score": "",
        "tumor_size_groups": "",
        "chemo_regimens": "",
        "endocrine_therapies": "",
        "file_types": "",
    }


    case_tab_return = {
        "subjectIds": False,
        "num_programs": False,
        "num_studies": False,
        "num_subjects": False,
        "num_lab_procedures": False,
        "num_samples": False,
        "num_files": False,
        "firstPage": True
    }

    file_tab_return = {
      "File ID": True,
      "File Name":True,
      "Association":True,
      "Description":True,
      "Format":True,
      "Size":True,
      "Program Code":True,
      "Arm":True,
      "Case ID":True,
      "Sample ID":True,
    }

    sample_tab_return ={
        "Sample ID": True,
        "Case ID": True,
        "Program Code": True,
        "Arm": True,
        "Diagnosis": True,
        "Tissue Type": True,
        "Tissue Composition": True,
        "Sample Anatomic Site": True,
        "Sample Procurement Method": True,
        "platform": True,
        "Tumor Size": True,
    }
    case_tab_data = BentoQueryBuilderFactory("case_tab_query", input_filter,case_tab_return)

    file_tab_data = BentoQueryBuilderFactory("file_tab_query", input_filter,file_tab_return)

    sample_tab_data = BentoQueryBuilderFactory("sample_tab_query", input_filter,sample_tab_return)


    
    return { 
              "case_tab_data. ": case_tab_data,
              "file_tab_data. ": file_tab_data,
              "sample_tab_data. ": sample_tab_data,
            }




@app.route('/ICDC')
def ICDC_CTDC_QUERY():
    icdc_filter = {
        "study_code": "",
        "study_type": "",
        "breed": "",
        "diagnosis": "",
        "disease_site": "",
        "stage_of_disease": "",
        "gender": "",
        "data_type": "",
        "file_formats": "",
    }

    icdc_output_schema = ["case_id", "study_code", "program", "study_type",
                   "breed", "diagnosis", "stage_of_disease", "disease_site", "age", "gender", "neutered_status",
                   "data_type", "file_formats", "files","number_of_files","number_of_sample","number_of_cases","number_of_study"]

    icdc_output_schema=["number_of_files","number_of_sample","number_of_cases","number_of_study"]


    ctdc_filter={
        "clinical_trial_code": "",
        "clinical_trial_id": "",
        "pubmed_id": "",
        "arm_id": "",
        "arm_drug": "",
        "disease": "",
        "gender": "",
        "race": "",
    }
    ctdc_output_schema=["case_id", "clinical_trial_code", "arm_id", "arm_drug", "pubmed_id", "disease", "gender", "race",
                   "ethnicity", "clinical_trial_id", "trial_arm", "file_types", "file_formats", "files","number_of_files","number_of_cases","number_of_trial"]
    ctdc_output_schema=["number_of_files","number_of_cases","number_of_trial"]
  

    return  " ".join(["icdc query: ",CommonsQueryBuilderFactory("icdc",icdc_filter,icdc_output_schema),"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ctdc query: ", CommonsQueryBuilderFactory("ctdc", ctdc_filter, ctdc_output_schema)])
    
  

app.run(host='0.0.0.0', port=8080)
