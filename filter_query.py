filtering_query = """
        MATCH (g:program)
        WITH COLLECT(g.program_acronym) AS all_programs
        MATCH (g:study)
        WITH COLLECT(g.study_acronym + ': ' + g.study_short_description)  AS all_studies, all_programs
        MATCH (g:study_subject)
        WITH COLLECT(g.disease_subtype)  AS all_diagnoses, all_studies, all_programs
        MATCH (g:stratification_factor)
        WITH COLLECT(g.grouped_recurrence_score) AS all_rc_scores, all_diagnoses, all_studies, all_programs
        MATCH (g:therapeutic_procedure)
        WITH COLLECT(g.chemotherapy_regimen) AS all_chemo_regimen, COLLECT(g.endocrine_therapy_type) AS all_endo_therapies, all_rc_scores, all_diagnoses, all_studies, all_programs
        MATCH (g:diagnosis)
        WITH COLLECT(g.tumor_size_group) AS all_tumor_sizes, COLLECT(g.tumor_grade) AS all_tumor_grades,
             COLLECT(g.er_status) AS all_er_status, COLLECT(g.pr_status) AS all_pr_status,
             all_chemo_regimen, all_endo_therapies, all_rc_scores, all_diagnoses, all_studies, all_programs
        MATCH (g:demographic_data)
        WITH COLLECT(g.menopause_status) AS all_meno_status, all_tumor_sizes, all_tumor_grades, all_er_status, all_pr_status,
             all_chemo_regimen, all_endo_therapies, all_rc_scores, all_diagnoses, all_studies, all_programs
        MATCH (ss)<-[:sf_of_study_subject]-(sf)
          WHERE sf.grouped_recurrence_score IN CASE $rc_scores WHEN [] THEN all_rc_scores ELSE $rc_scores END
        MATCH (ss)<-[:diagnosis_of_study_subject]-(d)<-[:tp_of_diagnosis]-(tp)
          WHERE d.tumor_size_group IN CASE $tumor_sizes WHEN [] THEN all_tumor_sizes ELSE $tumor_sizes END
            AND d.tumor_grade IN CASE $tumor_grades WHEN [] THEN all_tumor_grades ELSE $tumor_grades END
            AND d.er_status IN CASE $er_status WHEN [] THEN all_er_status ELSE $er_status END
            AND d.pr_status IN CASE $pr_status WHEN [] THEN all_pr_status ELSE $pr_status END
            AND tp.chemotherapy_regimen IN CASE $chemo_regimen WHEN [] THEN all_chemo_regimen ELSE $chemo_regimen END
            AND tp.endocrine_therapy_type IN CASE $endo_therapies WHEN [] THEN all_endo_therapies ELSE $endo_therapies END
        MATCH (ss:study_subject)-[:study_subject_of_study]->(s)-[:study_of_program]->(p)
          WHERE p.program_acronym IN CASE $programs WHEN [] THEN all_programs ELSE $programs END
            AND (s.study_acronym + ': ' + s.study_short_description) IN CASE $studies WHEN [] THEN all_studies ELSE $studies END
            AND ss.disease_subtype IN CASE $diagnoses WHEN [] THEN all_diagnoses ELSE $diagnoses END
        MATCH (ss)<-[:demographic_of_study_subject]-(demo)
          WHERE demo.menopause_status IN CASE $meno_status WHEN [] THEN all_meno_status ELSE $meno_status END
        WITH ss
        OPTIONAL MATCH (ss)<-[:sample_of_study_subject]-(sp)<-[:file_of_sample]-(f)-[:file_of_laboratory_procedure]->(lp)
        WITH ss, collect(DISTINCT sp.sample_id) AS samples, collect(DISTINCT lp.laboratory_procedure_id) AS lab_procedures, collect(DISTINCT f) AS files
        OPTIONAL MATCH (ss)-[:study_subject_of_study]->(s)-[:study_of_program]->(p)
        OPTIONAL MATCH (ss)<-[:sf_of_study_subject]-(sf)
        OPTIONAL MATCH (ss)<-[:diagnosis_of_study_subject]-(d)
        OPTIONAL MATCH (d)<-[:tp_of_diagnosis]-(tp)
        OPTIONAL MATCH (ss)<-[:demographic_of_study_subject]-(demo)
        WITH    p.program_acronym AS program,
                p.program_id AS program_id,
                s.study_acronym AS study_acronym,
                s.study_short_description AS study_short_description,
                s.study_acronym + ': ' + s.study_short_description AS study_info,
                ss.study_subject_id AS subject_id,
                ss.disease_subtype AS diagnosis,
                sf.grouped_recurrence_score AS recurrence_score,
                d.tumor_size_group AS tumor_size,
                d.tumor_grade AS tumor_grade,
                d.er_status AS er_status,
                d.pr_status AS pr_status,
                tp.chemotherapy_regimen AS chemotherapy,
                tp.endocrine_therapy_type AS endocrine_therapy,
                demo.menopause_status AS menopause_status,
                demo.age_at_index AS age_at_index,
                demo.survival_time AS survival_time,
                demo.survival_time_unit AS survival_time_unit,
                samples,
                files,
                lab_procedures
        UNWIND samples AS sample_id
        UNWIND lab_procedures AS lab_procedure_id
        UNWIND files AS file
        RETURN
                          """
filter_return = {
    "subjectIds":
    "COLLECT(DISTINCT subject_id) AS subjectIds",
    "num_programs":
    "COUNT(DISTINCT program) AS num_programs",
    "num_studies":
    "COUNT(DISTINCT study_acronym) AS num_studies",
    "num_subjects":
    "COUNT(DISTINCT subject_id) AS num_subjects",
    "num_lab_procedures":
    " COUNT(DISTINCT lab_procedure_id) AS num_lab_procedures",
    "num_samples":
    "COUNT(DISTINCT sample_id) AS num_samples",
    "num_files":
    "COUNT(DISTINCT file) AS num_files",
    "firstPage":
    """
   DISTINCT(subject_id) as `Case ID`,
program as `Program Code`,
program_id as `Program ID`,
study_acronym as `Arm`,
diagnosis as `Diagnosis`,
recurrence_score as `Recurrence Score`,
tumor_size as `Tumor Size (cm)`,
er_status as `ER Status`,
pr_status as `PR Status`,
age_at_index as `Age (years)`"""
}
