search_query = """     
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
            AND ss.disease_subtype IN CASE $diagnoses WHEN [] THEN all_diagnoses ELSE $diagnoses END
        WITH ss, all_meno_status, all_tumor_sizes, all_tumor_grades, all_er_status, all_pr_status,
             all_chemo_regimen, all_endo_therapies, all_studies, all_programs
        MATCH (ss)<-[:diagnosis_of_study_subject]-(d)<-[:tp_of_diagnosis]-(tp)
          WHERE d.tumor_size_group IN CASE $tumor_sizes WHEN [] THEN all_tumor_sizes ELSE $tumor_sizes END
            AND d.tumor_grade IN CASE $tumor_grades WHEN [] THEN all_tumor_grades ELSE $tumor_grades END
            AND d.er_status IN CASE $er_status WHEN [] THEN all_er_status ELSE $er_status END
            AND d.pr_status IN CASE $pr_status WHEN [] THEN all_pr_status ELSE $pr_status END
            AND tp.chemotherapy_regimen IN CASE $chemo_regimen WHEN [] THEN all_chemo_regimen ELSE $chemo_regimen END
            AND tp.endocrine_therapy_type IN CASE $endo_therapies WHEN [] THEN all_endo_therapies ELSE $endo_therapies END
        WITH ss, all_meno_status, all_studies, all_programs
        MATCH (ss)-[:study_subject_of_study]->(s)-[:study_of_program]->(p)
          WHERE p.program_acronym IN CASE $programs WHEN [] THEN all_programs ELSE $programs END
            AND (s.study_acronym + ': ' + s.study_short_description) IN CASE $studies WHEN [] THEN all_studies ELSE $studies END
		WITH ss, all_meno_status, p, s
		MATCH (ss)<-[:demographic_of_study_subject]-(demo)
          WHERE demo.menopause_status IN CASE $meno_status WHEN [] THEN all_meno_status ELSE $meno_status END
        RETURN 
"""

search_return = {"study_subject_id": "DISTINCT ss.study_subject_id"}
