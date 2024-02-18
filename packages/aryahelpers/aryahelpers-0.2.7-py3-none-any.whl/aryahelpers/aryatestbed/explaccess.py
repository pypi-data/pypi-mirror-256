"""Modules to access candidates explanations from DB"""
# -*- coding: utf-8 -*-
# @author Ratnadip Adhikari

import sys, os, json
BASE_PATH = os.path.abspath("./arya-helpers/Codes/src")
extendPaths = [p for p in (os.path.dirname(BASE_PATH), BASE_PATH) if p not in sys.path]
sys.path = extendPaths + sys.path
from copy import deepcopy
from aryautils.storageutils import MySQLManager
from aryahelpers.utils.mysqlutils import MySQLHelpers
from aryahelpers.appconfig import CONFIG, ALL_FEATURES, FACT_TOKENS, JOB_METADATA_COLS, CANDIDATE_TABLES
from aryahelpers.utils.genericutils import merge_dicts, flatten_iterable
from aryahelpers.utils.textclean import PreprocessText
import logging
LOGGER = logging.getLogger(__name__)


class AccessExplanations(object):
    """Access candidates explanations from DB"""
    def __init__(self, base_env: str, job_id: int, **kwargs):
        self._ALL_FEATURES = set(k.lower() for k in ALL_FEATURES)
        self.base_env, self.job_id = base_env, job_id
        [setattr(self, k, v) for k, v in kwargs.items()]  # num_candidates, candidate_name, candidate_guid
        self.db_key = 'database' if self.base_env == 'qa' else f'database.{self.base_env}'
        self.job_metadata, self.contds_metadata = {}, []
        self.explanations = {"JobInfo": [], "CandidatesInfo": []}
    
    def get_explanation_facts(self, candidate_details: dict):
        """Filter explanations, based on `explanation_type`"""
        explanation_type = self.explanation_type  # 'company', 'skill', 'role', 'occupation',
                                                  # 'industry', 'experience', 'facts'
        filtered_explanations = {}
        if explanation_type:
            if explanation_type != 'facts':
                filtered_explanations = candidate_details.get(
                    explanation_type, candidate_details.get(explanation_type.title(), {}))
            else:
                all_explkeys = list(candidate_details.keys())
                all_explkeys = {k: k if k.lower() != 'summary' else f'#{k}' for k in all_explkeys if isinstance(
                    candidate_details[k], dict) and (set(candidate_details[k].keys()) & FACT_TOKENS)}
                filtered_explanations["ExplanationFacts"] = {}
                for _explkey in all_explkeys:
                    for _fact_key in FACT_TOKENS:
                        get_facts = candidate_details.get(_explkey, {}).get(_fact_key, [])
                        if isinstance(get_facts, list):
                            get_facts = [_fact.get('Fact', '') + _fact.get('fact', '') if isinstance(
                                _fact, dict) else _fact for _fact in get_facts]
                        if get_facts:
                            filtered_explanations["ExplanationFacts"][all_explkeys[_explkey]] = get_facts
                            break
        else:
            return candidate_details
        return filtered_explanations
    
    def extract_analyzed_candidates(self, expl_tbl_key, job_id=None, expl_type=None):
        """Extract analyzed candidates details from the respective db"""
        cand_details = []
        db_name, table_name, jobid_key, guid_key, expl_key = tuple(
            CANDIDATE_TABLES["explanation"][expl_tbl_key].values())
        # Add the respective Score
        score_keys = ["CandidateScore"]
        if expl_type in self._ALL_FEATURES:
            score_keys += [] if expl_type in ['facts', 'summary'] else [
                "{}Score".format(expl_type.title())] if expl_type != 'role' else ['RoleLevelScore']
        else:
            score_keys += ['CompanyScore', 'RoleLevelScore', 'OccupationScore', 'EducationScore',
                            'ExperienceScore', 'IndustryScore', 'SkillScore']
        query_str = "SELECT {}, {}, {}, CONVERT_TZ(UpdatedDateTime,'+00:00','+05:30') \
            AS UpdatedDateTime, {} FROM {} WHERE {}={}".format(
                jobid_key, ", ".join(score_keys), guid_key, expl_key, table_name, jobid_key, job_id)
        cand_details = MySQLManager.execute_query(query_str, (), **CONFIG[self.db_key][db_name])
        cand_details = [{k: v for k, v in d.items() if v or (k not in score_keys)} for d in cand_details]
        for idx, d in enumerate(cand_details):
            cand_details[idx][expl_key] = deepcopy(json.loads(d[expl_key]))
            cand_details[idx][expl_key] = self.get_explanation_facts(cand_details[idx][expl_key])
        return cand_details
    
    def filter_candidates(self, contd_details: list, filter_keys: tuple):
        """Filter `contd_details` with respect to `filter_keys`"""
        filtered_details = contd_details.copy()
        num_candidates = self.num_candidates
        candidate_name = self.candidate_name
        candidate_guid = self.candidate_guid
        recommendation_status_id = self.recommendation_status_id  #[1, 2, 3]
        if num_candidates:
            filtered_details = [d for d in filtered_details[:num_candidates]]
        if candidate_name:
            filtered_details = [d for d in filtered_details if d[filter_keys[0]] == candidate_name]
        if candidate_guid:
            filtered_details = [d for d in filtered_details if d[filter_keys[1]] == candidate_guid]
        if recommendation_status_id:
            filtered_details = [d for d in filtered_details if d[filter_keys[2]] == recommendation_status_id]
        return filtered_details
    
    def collect_job_metadata(self):
        """Collect metadata info for the provided job"""
        try:
            exp_query = f"SELECT * FROM experience WHERE JobId={self.job_id};"
            job_exps = MySQLManager.execute_query(exp_query, (), **CONFIG[self.db_key]['intel'])
            job_exps = (job_exps[0]['min'], job_exps[0]['max'], job_exps[0]['source']) if job_exps else None
            job_details = MySQLHelpers.extract_arya_jobdetails(self.db_key, self.job_id)
            self.job_metadata = {k: v for k, v in job_details.items() if k in JOB_METADATA_COLS if k != 'JobDesc'}
            job_desc = PreprocessText().clean_html_tags(job_details['JobDesc'])
            self.job_metadata = merge_dicts(({"JobId": self.job_id}, self.job_metadata,
                                             {"JobExperience": job_exps}, {"JobDesc": job_desc}))
        except Exception as error:
            LOGGER.error(error)
            LOGGER.info("Error in extracting metadata info for the job: %s", self.job_id)
    
    def collect_contds_metadata(self):
        """Collect sourced contenders details for the given job"""
        try:
            job_id, base_env = self.job_id, self.base_env
            explanation_type = self.explanation_type

            # Access candidates explanations and other details
            filter_guids = []
            expl_tbl_key = 'copy' if base_env == 'new' else 'base'
            cand_details = self.extract_analyzed_candidates(expl_tbl_key, job_id, explanation_type)
            if not cand_details and base_env == 'new':
                expl_tbl_key = 'base'
                cand_details = self.extract_analyzed_candidates(expl_tbl_key, job_id, explanation_type)
            
            # Filter cand_guids
            guid_key = CANDIDATE_TABLES["explanation"][expl_tbl_key]['guid_key']
            jtr_candidates = MySQLHelpers().get_TopN_JTR(self.db_key, job_id)
            if jtr_candidates:
                filter_guids = [(d['candidate_name'], d['portal_candidate_id'],
                                d['recommendation_status_id'], d['rejected_reasons']) for d in jtr_candidates]
                filter_guids = self.filter_candidates(filter_guids, (0, 1, 2))
                # Access explanations
                for cand_info in filter_guids:
                    subset_cands = [d for d in cand_details if d[guid_key] == cand_info[1]]
                    if guid_key == 'portalGuid':
                        subset_cands = sorted(subset_cands, key=lambda d: d['UpdatedDateTime'], reverse=True)
                    if subset_cands:
                        extra_details = {"CandidateName": cand_info[0], "recommendation_status_id": cand_info[2],
                                        "rejected_reasons":  cand_info[3]} if cand_info[2] == 3 else \
                                            {"CandidateName": cand_info[0], "recommendation_status_id": cand_info[2]}
                        subset_cands = merge_dicts((extra_details, subset_cands[0]))
                        self.contds_metadata.append(subset_cands)
            else:
                # if jtr_candidates list is empty, e.g. manually entered info
                cand_details = [d for d in cand_details if d.get("CandidateScore", 0) >= 0]
                cand_details = sorted(cand_details, key=lambda x: x.get("CandidateScore", 0), reverse=True)
                cand_details = self.filter_candidates(cand_details, ('', guid_key, ''))
                self.contds_metadata.extend(cand_details)
            self.contds_metadata = flatten_iterable(self.contds_metadata)
        except Exception as error:
            LOGGER.error(error)
            LOGGER.info("Unexpected Error in extracting contds metadata info")
            
    def access_explanations(self):
        """Access explanations, based on specific filtering conditions"""
        try:
            self.collect_job_metadata()  # collect jobs metadata
            self.collect_contds_metadata()  # collect contds metadata
            self.explanations = {"JobInfo": self.job_metadata, "CandidatesInfo": self.contds_metadata}        
        except Exception as error:
            LOGGER.error(error)
            LOGGER.error("Unexpected Error in extracting candidates explanations !!")
            raise error
  

if __name__ == '__main__':
    print('python version:', sys.version)   
    print('cwd:', os.getcwd())
    # =================
    accessor = AccessExplanations(
        base_env='qa', job_id=359228, explanation_type='facts', num_candidates=10,
        candidate_name=None, candidate_guid=None, recommendation_status_id=None
    )
    accessor.access_explanations()
    cand_explanations = accessor.explanations
    print(json.dumps(cand_explanations, indent=4, default=str))
