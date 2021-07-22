file_tab_query = """     
    MATCH (p:program) WITH 
        COLLECT(DISTINCT(p.program_acronym)) AS all_programs
    MATCH (s:study) WITH 
        COLLECT(DISTINCT(s.study_acronym + ': ' + s.study_short_description)) AS all_studies,
        all_programs
    MATCH (ss:study_subject) WITH 
        COLLECT(DISTINCT(ss.disease_subtype)) AS all_diagnoses,
        all_studies, all_programs
    MATCH (d:diagnosis) WITH 
        COLLECT(DISTINCT(d.recurrence_score)) AS all_recurrence_scores,
        COLLECT(DISTINCT(d.tumor_size_group)) AS all_size_groups,
        COLLECT(DISTINCT(d.tumor_grade)) AS all_grades,
        COLLECT(DISTINCT(d.er_status)) AS all_er_statuses,
        COLLECT(DISTINCT(d.pr_status)) AS all_pr_statuses,
        all_diagnoses, all_studies, all_programs
    MATCH (tp:therapeutic_procedure) WITH
        COLLECT(DISTINCT(tp.chemotherapy_regimen)) AS all_chemo_regimens,
        COLLECT(DISTINCT(tp.endocrine_therapy_type)) AS all_endo_therapies,
        all_recurrence_scores, all_size_groups, all_grades, all_er_statuses, all_pr_statuses, all_diagnoses, all_studies, all_programs
    MATCH (dd:demographic_data) WITH
        COLLECT(DISTINCT(dd.menopause_status)) AS all_menopause_statuses,
        all_chemo_regimens, all_endo_therapies, all_recurrence_scores, all_size_groups, all_grades, all_er_statuses, all_pr_statuses, all_diagnoses, all_studies, all_programs
    MATCH (samp:sample) WITH
        COLLECT(DISTINCT(samp.tissue_type)) AS all_tissue_types,
        COLLECT(DISTINCT(samp.composition)) AS all_tissue_compositions,
        all_menopause_statuses, all_chemo_regimens, all_endo_therapies, all_recurrence_scores, all_size_groups, all_grades, all_er_statuses, all_pr_statuses, all_diagnoses, all_studies, all_programs
    MATCH (f:file)
    MATCH (parent)<--(f) WITH
        COLLECT(DISTINCT(head(labels(parent)))) AS all_associations,
        COLLECT(DISTINCT(f.file_type)) AS all_file_types,
        all_tissue_types, all_tissue_compositions, all_menopause_statuses, all_chemo_regimens, all_endo_therapies, all_recurrence_scores, all_size_groups, all_grades, all_er_statuses, all_pr_statuses, all_diagnoses, all_studies, all_programs
    MATCH (f:file)
    MATCH (f)-->(parent)
        WHERE NOT (parent:laboratory_procedure)
        AND (head(labels(parent))) IN CASE $associations WHEN [] THEN all_associations ELSE $associations END
        AND f.file_type IN CASE $file_types WHEN [] THEN all_file_types ELSE $file_types END
    MATCH (f)-[:file_of_sample]->(samp)
        WHERE samp.tissue_type IN CASE $tissue_type WHEN [] THEN all_tissue_types ELSE $tissue_type END
        AND samp.composition IN CASE $tissue_composition WHEN [] THEN all_tissue_compositions ELSE $tissue_composition END
    MATCH (f)-[*..2]->(ss)-[:study_subject_of_study]->(s)-[:study_of_program]->(p)
        WHERE (s.study_acronym + ': ' + s.study_short_description) IN CASE $studies WHEN [] THEN all_studies ELSE $studies END
        AND p.program_acronym IN CASE $arms WHEN [] THEN all_programs ELSE $arms END
    MATCH (ss)<-[:demographic_of_study_subject]-(dd)
        WHERE dd.menopause_status IN CASE $menopause_status WHEN [] THEN all_menopause_statuses ELSE $menopause_status END
    MATCH (ss)<-[:diagnosis_of_study_subject]-(d)<-[:tp_of_diagnosis]-(tp)
        WHERE d.recurrence_score IN CASE $recurrence_score WHEN [] THEN all_recurrence_scores ELSE $recurrence_score END
        AND d.tumor_size_group IN CASE $tumor_size_groups WHEN [] THEN all_size_groups ELSE $tumor_size_groups END
        AND d.tumor_grade IN CASE $tumor_grades WHEN [] THEN all_grades ELSE $tumor_grades END
        AND d.er_status IN CASE $er_status WHEN [] THEN all_er_statuses ELSE $er_status END
        AND d.pr_status IN CASE $pr_status WHEN [] THEN all_pr_statuses ELSE $pr_status END
        AND tp.chemotherapy_regimen IN CASE $chemo_regimens WHEN [] THEN all_chemo_regimens ELSE $chemo_regimens END
        AND tp.endocrine_therapy_type IN CASE $endocrine_therapies WHEN [] THEN all_endo_therapies ELSE $endocrine_therapies END
        RETURN
"""


file_tab_return = {
  "File ID":"f.file_id AS `File ID`",
  "File Name":"f.file_name AS `File Name`",
  "Association":"head(labels(parent)) AS `Association`",
  "Description":"f.file_description AS `Description`",
  "Format":"f.file_format AS `Format`",
  "Size":"f.file_size AS `Size`",
  "Program Code":"p.program_acronym AS `Program Code`",
  "Arm":"s.study_acronym AS `Arm`",
  "Case ID":"ss.study_subject_id AS `Case ID`",
  "Sample ID":"samp.sample_id AS `Sample ID`"
}
