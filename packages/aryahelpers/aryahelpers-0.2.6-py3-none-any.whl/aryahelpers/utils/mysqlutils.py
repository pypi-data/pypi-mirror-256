"""MySQL utility modules to help Arya operations"""
# -*- coding: utf-8 -*-
# @author Ratnadip Adhikari

import json
import re
import pprint
import logging
import pandas as pd
from copy import deepcopy
from functools import reduce
from collections import Counter
from IPython.core.display import display
from aryahelpers.utils.genericutils import import_file, save_files, null_handler, merge_dicts, format_datetime
from aryautils.storageutils import WARNING_MESSAGE, mysqlcursor, MySQLManager
from aryahelpers.appconfig import CONFIG
LOGGER = logging.getLogger(__name__)


class MySQLHelpers(object):
    """MySQL utility class"""
    def __init__(self):
        pass  # initialized class with empty constructor
    
    @staticmethod
    @mysqlcursor
    def mysql_query_execute(query, args, **kw):
        """Execute MySQL standalone queries (DELETE/DROP/TRUNCATE etc.) but not SELECT type queries."""
        return_flag = True
        cursor = kw.get('cursor')
        if not cursor:
            raise UserWarning(WARNING_MESSAGE)
        try:
            cursor.execute(query, args)
        except Exception:
            return_flag = False
        return return_flag
    
    @staticmethod
    def copyinfo_for_dbtransaction(cands_path, copy_params=None, jobstats_key=None,
                                   to_stringify=True, to_print=True, save_path=False):
        """This function prepares the 'copy_info' list of dicts for performing transactions on db tables.

        Args:
            cands_path (str):
                Path of the json file of candidates analysis information.
            copy_params (dict, optional):
                A dict for copy params of the form:
                {'table_param_1': 'analysis_param_1',...,'table_param_n': 'analysis_param_n'}. \n
                For e.g.:
                    {'job_id': 'jobId',
                    'name': 'candidate_name',
                    'portal_candidate_id': 'candidate_guid'}
                If ``None``, then the function returns empty 'copy_info' list. 
            jobstats_key (str, optional):
                The particular job stats key for which the db transaction (COPY/DELETE/EXTRACT)is to be performed.
            to_stringify (bool, optional):
                Whether to stringify each key-value in 'copy_info'. this is required for certain db transactions.
            to_print (bool, optional):
                Whether to partially display (at most 10 elements) 'copy_info'.
            save_path (bool, optional):
                The path to save the 'copy_info' list of dicts. Defaults to ``False``.

        Returns:
            The derived 'copy_info' list of dicts.
        """
        # =================
        cands_details = import_file(cands_path)
        copy_info = []
        if not isinstance(copy_params, dict):
            if to_print:
                display(len(copy_info), copy_info[:10])
            return copy_info
        # +++++++++++++++++
        for idx, val in enumerate(cands_details):
            cands_dicts, getCands = [], []
            id_key = list(val.keys())[0]
            if isinstance(val[id_key], dict):
                candInfo = val[id_key]
                info_keys = list(candInfo.keys()) if jobstats_key is None else jobstats_key
                [getCands.extend(candInfo[key]) for key in info_keys];
            else:
                getCands.append(val)
            # +++++++++++++++++
            [cands_dicts.append({i[0]:str(val.get(i[1])) if to_stringify else val.get(
                i[1]) for i in copy_params.items()}) for val in getCands];
            copy_info += cands_dicts
        # +++++++++++++++++
        if to_print:
            display(len(copy_info), copy_info[:10])
        save_files(copy_info, save_path, 'copy_info', '.json', indent=4, default=str) # save 'copy_info' list
        return copy_info

    @staticmethod
    def get_TopN_JTR(db_key, jobid, topN=None):
        """Get JTR candidates"""
        query_str = "SELECT job_id, candidate_name,  format(candidate_score, 2) AS candidate_score, \
            portal_candidate_id, candidate_guid, recommendation_status_id FROM `arya`.`job_top_recommendations` jtr \
                JOIN `arya`.`job_recommendations_metadata` jrm ON jtr.recommendation_id = jrm.recommendation_id \
                    WHERE job_id = {} AND recommendation_status_id in (1, 2, 3) \
                        ORDER BY candidate_score DESC;".format(jobid)
        TopN_JTR = MySQLManager.execute_query(query_str, (), **CONFIG[db_key]['arya'])[:topN]
        return TopN_JTR
    
    @staticmethod
    def _get_user_info_from_db(db_key: str, id_key=None, id_type='user_id'):
        """Get user (job poster) info (first name, last name, email etc.) from db.\n
        `id_key`/`id_type` should be either `user_id` or `user_email`.
        """
        query_str = "SELECT UserId, UserName, Email, Organization, UserGuid FROM `user` WHERE "
        query_str += f"UserId={id_key};" if id_type == 'user_id' else f"Email='{id_key}';"
        return MySQLManager.execute_query(query_str, (), **CONFIG[db_key]['arya'])
    
    @staticmethod
    def _form_clientinfo_dict(user_info: dict, client_info: dict):
        """Form client info dict from provided user_info"""
        clientinfo_dict = {}
        if user_info and client_info:
            create_date = format_datetime(client_info.get('CreatedDate'), '%d-%b-%Y, %H:%M:%S IST')
            update_date = format_datetime(client_info.get('UpdateDate'), '%d-%b-%Y, %H:%M:%S IST')
            clientinfo_dict = {
                "User": user_info["UserName"],
                "UserEmail": user_info["Email"],
                "ClientID": client_info["CompanyID"],
                "ClientName": client_info["CompanyName"],
                "ATSClientID": client_info["ATSClientID"],
                "Organization": client_info["Organization"],
                "IsActive": client_info["IsActive"],
                "CreatedDate": create_date,
                "LastUpdateDate": update_date
            }
        return clientinfo_dict
    
    @staticmethod
    def delete_clients_from_user(db_key: str, company_names: list, id_key=None, id_type='user_id'):
        """Deletes clients, mapped to a user"""
        if not (company_names and id_key):
            return False
        user_info = MySQLHelpers._get_user_info_from_db(db_key, id_key, id_type)
        if not user_info:
            return False
        company_names, org_id = ", ".join(f"'{s}'" for s in company_names), user_info[0]["Organization"]
        delete_query = f"DELETE FROM `mstcompany` WHERE CompanyName IN ({company_names}) AND Organization={org_id};"
        return MySQLHelpers().mysql_query_execute(delete_query, (), **CONFIG[db_key]['arya'])

    @staticmethod
    def fetch_or_add_client_for_user(db_key: str, company_name: str, id_key=None, id_type='user_id'):
        """Extract or add a client for the given user"""
        if not (company_name and id_key):
            return {}
        company_name = company_name if company_name[0].isupper() else company_name.upper()
        user_info = MySQLHelpers._get_user_info_from_db(db_key, id_key, id_type)
        if not user_info:
            return {}
        user_info = user_info[0]
        user_id, org_id = user_info["UserId"], user_info["Organization"]
        select_query = "SELECT CompanyID, CompanyName, ATSClientID, Organization, IsActive, CONVERT_TZ(\
            CreatedDate,'+00:00','+05:30') AS CreatedDate" + (", CONVERT_TZ(LastUpdateTimeStamp,'+00:00','+05:30') AS \
                UpdateDate " if 'staging' not in db_key else " ") + f"FROM `mstcompany` WHERE `Organization`=\
                    {org_id} AND LOWER(`CompanyName`)=LOWER('{company_name}');"
        clientinfo_res = MySQLManager.execute_query(select_query, (), **CONFIG[db_key]['arya'])
        if not clientinfo_res:
            maxatsid_query = f"SELECT MAX(ATSClientID) AS max_ats_id from `mstcompany` WHERE `Organization`={org_id};"
            max_ats_clientid = MySQLManager.execute_query(maxatsid_query, (), **CONFIG[db_key]['arya'])
            max_ats_clientid = max_ats_clientid[0]['max_ats_id']
            insert_query = f"INSERT INTO `mstcompany` (CompanyName, ATSClientID, Organization, IsActive, CreatedById, \
                CreatedDate, ModifiedById, ModifiedDate, SourceCount) Values ('{company_name}', {max_ats_clientid+1},\
                    {org_id}, 1, {user_id}, CURRENT_TIMESTAMP(), {user_id}, CURRENT_TIMESTAMP(), NULL);"
            MySQLHelpers.mysql_query_execute(insert_query, (), **CONFIG[db_key]['arya'])
            clientinfo_res = MySQLManager.execute_query(select_query, (), **CONFIG[db_key]['arya'])
        clientinfo_res = clientinfo_res[0] if clientinfo_res else {}
        return MySQLHelpers._form_clientinfo_dict(user_info, clientinfo_res)

    @staticmethod
    def get_clientsmapping_for_user(db_key: str, id_key=None, id_type='user_id', save_path=False):
        """Get all clients mapped to a particular user"""
        clients_mapping = {}
        user_info = MySQLHelpers._get_user_info_from_db(db_key, id_key, id_type)
        if not user_info:
            return clients_mapping
        user_info = user_info[0]
        org_id = user_info["Organization"]
        query_str = "SELECT CompanyID, CompanyName, ATSClientID, Organization, IsActive, CONVERT_TZ(\
            CreatedDate,'+00:00','+05:30') AS CreatedDate" + (", CONVERT_TZ(LastUpdateTimeStamp,'+00:00','+05:30') AS \
                UpdateDate " if 'staging' not in db_key else " ") + f"FROM `mstcompany` WHERE `Organization`={org_id};"
        query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key]['arya'])
        [clients_mapping.update({client_info["CompanyName"]: MySQLHelpers._form_clientinfo_dict(
            user_info, client_info)}) for idx, client_info in enumerate(query_res)]
        save_path = save_path if org_id else False
        save_files(clients_mapping, save_path, f"orgId{org_id}_allClients", '.json', indent=4)
        return clients_mapping

    @staticmethod
    def _get_job_metadata(db_key: str, job_id: int):
        """Extract job posting details -- created/updated dates, job poster details  etc."""
        job_metadata = {}
        query_str = "SELECT CreatedById, CONVERT_TZ(CreatedDate,'+00:00','+05:30') AS CreatedDate" + (", CONVERT_TZ(\
            LastUpdateTimeStamp,'+00:00','+05:30') AS UpdateDate " if 'staging' not in db_key else " ") + \
            f"FROM `job` WHERE JobId={job_id};"
        query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key]['arya'])
        if not query_res:
            return job_metadata
        user_id = query_res[0]["CreatedById"]
        create_date = format_datetime(query_res[0].get('CreatedDate'), '%d-%b-%Y, %H:%M:%S IST')
        update_date = format_datetime(query_res[0].get('UpdateDate'), '%d-%b-%Y, %H:%M:%S IST')
        user_info = MySQLHelpers._get_user_info_from_db(db_key, user_id)
        job_metadata = {
            "JobEnv": db_key.split('.')[-1].title() if '.' in db_key else 'QA',
            "JobCreatedBy": user_info[0]["UserName"] if user_info else "",
            "JobCreatedEmail": user_info[0]["Email"] if user_info else "",
            "JobCreatedDate": create_date,
            "JobLastUpdateDate": update_date
        }
        return job_metadata

    @staticmethod
    def extract_arya_jobdetails(db_key: str, job_id: int):
        """Extract details for the given job_id"""
        arya_jobdetails = {}
        try:
            job_details = MySQLManager.call_proc('get_arya_job_params', (job_id, ), **CONFIG[db_key]['arya'])[0][0]
            client_company, job_title, job_desc, loc_info = \
                job_details['ClientCompany'], job_details['JobTitle'], job_details['JobDesc'], ''
            job_metadata = MySQLHelpers._get_job_metadata(db_key, job_id)
            if client_company and job_title:
                _prefix = ", " if job_details['Location'] else ""
                loc_info += null_handler(job_details['Location'], "") + _prefix + \
                    null_handler(job_details['Country'], "")
                arya_jobdetails = {
                    "ClientCompany": client_company,
                    "JobTitle": job_title,
                    "Location": loc_info
                }
                arya_jobdetails = merge_dicts((arya_jobdetails, job_metadata, {"JobDesc": job_desc}))
        except Exception as error:
            LOGGER.error(error)
            LOGGER.error("Error in extracting Arya job details !!")
        return arya_jobdetails

    @staticmethod
    def get_contd_details(db_key: str, db_name: str, tbl_name: str, jobid_key: str, guid_key: str, job_id=None):
        """Obtain existing job & candidate details from the toprocess/custom toprocess table"""
        wh_clause = "WHERE {}={}".format(jobid_key, job_id) if job_id else ""
        query_str = "SELECT {0}, {1} FROM {2} {3} GROUP BY {0}, {1};".format(jobid_key, guid_key, tbl_name, wh_clause)
        query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
        found_jobids = {job_id} if job_id else set([d[jobid_key] for d in query_res])
        contd_details = {jid: {"source_count": sum([1 for d in query_res if d[jobid_key] == jid]),
                               "contd_guids": set([d[guid_key] for d in query_res if d[jobid_key] == jid])}
                         for jid in found_jobids}
        return contd_details
    
    @staticmethod
    def get_all_distinct_jobs(db_key: str, db_name: str, tbl_name: str, jobid_key: str):
        """Get the set of all distinct jobs from the given table"""
        try:
            distinct_jobs = MySQLManager.execute_query("SELECT DISTINCT {} FROM {};".format(
                jobid_key, tbl_name), (), **CONFIG[db_key][db_name])
            return set([d[jobid_key] for d in distinct_jobs])
        except Exception:
            return set()
    
    @staticmethod
    def transact_to_jobsretain_tbl(db_key: str, db_name: str, job_ids: list, transact_type='check'):
        """Check existence/insert/delete jobs to the `jobs_to_be_retained` table.
        - The param: `transact_type` can be one of `'check'`, `'insert'` or `'delete'`"""
        tbl_name = 'jobs_to_be_retained'
        select_query = "SELECT DISTINCT JobId FROM {};".format(tbl_name)
        all_jobs = MySQLManager.execute_query(select_query, (), **CONFIG[db_key][db_name])
        all_jobs = set([d['JobId'] for d in all_jobs])
        insert_jobs = reduce(lambda x, y: x+y, [['({})'.format(jid)] for jid in job_ids if jid not in all_jobs], [])
        query_str = "INSERT INTO {} (`JobId`) VALUES {};".format(tbl_name, ", ".join(insert_jobs)) if \
            transact_type == 'insert' else "DELETE FROM {} WHERE JobId in {};".format(
                tbl_name, tuple(job_ids)) if transact_type == 'delete' else ""
        if transact_type in ['insert', 'delete']:
            return MySQLHelpers.mysql_query_execute(query_str, (), **CONFIG[db_key][db_name])
        return all_jobs & set(job_ids)  # return all retained jobs
    
    @staticmethod
    def create_sql_query(base_query: str, table_name: str, copy_info={}, where_clause=True):
        """This function formulates the MySql query str for a db operation.
        Args:
            base_query (str): The base query, e.g. `"SELECT * FROM"`, `"DELETE FROM"`. 
            table_name (str): The table name for the query.
            copy_info (dict, optional): A dict/path of copy info, the keys mapping to the columns of `table_name`.
            where_clause (bool, optional): Whether the query is a `WHERE` clause or not. Defaults to ``True``.
        
        Returns:
            The formulated query string.
        """
        _copy_info = import_file(copy_info)
        if _copy_info is None:
            _copy_info = {}
        # +++++++++++++++++
        if not where_clause:
            return "{} {};".format(base_query, table_name)
        get_query = "{} {} WHERE ".format(base_query, table_name)
        [get_query := get_query + '{}{} AND '.format(str(_item[0]), "='" + str(_item[1]).replace(
            "'", "\\'") + "'" if _item[1] is not None else ' IS NULL') for _item in _copy_info.items()]
        get_query = re.sub('\\sAND\\s$', ';', get_query)
        if not len(_copy_info):
            get_query += 'TRUE;'
        # +++++++++++++++++
        return get_query

    @staticmethod
    def qa_job_mysql_operations(job_id, query_seq=['all'], copy_info=False, to_print=True):
        """This function executes a sequence of MySql queries for sourcing a new/existing QA job.

        Args:
            job_id (int): The Job ID.
            query_seq (list, optional): The query sequence to execute for the `job_id`. Defaults to ['all'].
            to_print (bool, optional): Whether to print queries execution status. Defaults to ``True``.

            - 1 : INSERT INTO `jobs_to_be_retained` WHERE `<cond>`
            - 2 : DELETE FROM `jobs_to_be_retained` WHERE `<cond>`
            - 3 : SELECT * FROM `jobs_to_be_retained` WHERE `<cond>`
            - 4 : SELECT COUNT(*) FROM `toprocess_candidates` WHERE `<cond>`
            - 5 : DELETE FROM `toprocess_candidates` WHERE `<cond>`
            - 6 : SELECT `<...>` FROM `filtered_toprocess_candidates` WHERE `<cond>`
            - 7 : DELETE FROM `filtered_toprocess_candidates` WHERE `<cond>`
            - 8 : SELECT * FROM `intel`.`search_string` WHERE `<cond>`
            - 9 : SELECT * FROM `intel`.`keyword` WHERE `<cond>`
            - 10: DELETE FROM `toprocess_analyzed_candidate_details_info` WHERE `<cond>`
            - 'all' : the `query_seq` = [1, 5, 7]

            copy_info (dict/bool/None, optional): A dict/path of copy info. The key for job_id can be excluded as
                we are externally pssing it to the function.

        Returns:
            The query results, asked for in the `query_seq`.
        """
        # +++++++++++++++++
        def execute_query(q_type, q_str, db_name):
            """This function executes the given query w.r.t. the query params."""
            exec_fun = "MySQLHelpers.mysql_query_execute" if q_type == 1 else "MySQLManager.execute_query"
            return eval(exec_fun)(q_str, (), **CONFIG['database'][db_name])

        def revised_copy_info(q_sec: int, job_id, raw_copy_info):
            _copy_info = deepcopy(raw_copy_info)
            if not bool(_copy_info):
                _copy_info = {}
            if q_sec not in [8, 9, 10]:
                _copy_info = {**{'job_id': '{}'.format(job_id)}, **_copy_info}
            elif q_sec in [8, 9]:
                _copy_info = {**{'jobid': '{}'.format(job_id)}, **_copy_info}
            else:
                _copy_info = {**{'jobId': '{}'.format(job_id)}, **_copy_info}
            return _copy_info
        # +++++++++++++++++
        if not isinstance(query_seq, list):
            query_seq = [query_seq]
        queries_status = dict()  # queries status -- success/failure
        queries_res = dict()  # queries actual outputs
        raw_copy_info = import_file(copy_info)
        # +++++++++++++++++
        for _qseq in query_seq:
            _copy_info = revised_copy_info(_qseq, job_id, raw_copy_info)
            query_str = {
                1: "INSERT INTO `jobs_to_be_retained` (`JobId`) VALUES ({});".format(job_id),
                2: "DELETE FROM `jobs_to_be_retained` WHERE jobId={};".format(job_id),
                3: "SELECT * FROM `jobs_to_be_retained` WHERE jobId={};".format(job_id),
                4: MySQLHelpers.create_sql_query("SELECT COUNT(*) FROM", "toprocess_candidates", _copy_info,),
                5: MySQLHelpers.create_sql_query("DELETE FROM", "toprocess_candidates", _copy_info),
                6: MySQLHelpers.create_sql_query("SELECT DISTINCT portal_candidate_id, candidate_score FROM",
                                                 "filtered_toprocess_candidates", _copy_info),
                7: MySQLHelpers.create_sql_query("DELETE FROM", "filtered_toprocess_candidates", _copy_info),
                8: MySQLHelpers.create_sql_query("SELECT * FROM", "search_string", _copy_info),
                9: MySQLHelpers.create_sql_query("SELECT * FROM", "keyword", _copy_info),
                10: MySQLHelpers.create_sql_query("DELETE FROM", "toprocess_analyzed_candidate_details_info", _copy_info)
            }
            if _qseq == 1:
                _key = "INSERT INTO `jobs_to_be_retained`"
                _res_1 = execute_query(1, query_str[1], 'candidate_reservoir')
                _res_2 = execute_query(2, query_str[3], 'candidate_reservoir')
                queries_status[_key] = _res_1
                queries_res[_key] = _res_2
            elif _qseq == 2:
                _key = "DELETE FROM `jobs_to_be_retained`"
                _res_1 = execute_query(1, query_str[2], 'candidate_reservoir')
                _res_2 = execute_query(2, query_str[3], 'candidate_reservoir')
                queries_status[_key] = _res_1
                queries_res[_key] = _res_2
            elif _qseq == 3:
                _key = "SELECT * FROM `jobs_to_be_retained`"
                _res = execute_query(2, query_str[3], 'candidate_reservoir')
                queries_status[_key] = bool(len(_res))
                queries_res[_key] = _res
            elif _qseq == 4:
                _key = "SELECT COUNT(*) FROM `toprocess_candidates`"
                _res = execute_query(2, query_str[4], 'candidate_reservoir')
                queries_status[_key] = _res[0]
                queries_res[_key] = _res[0]
            elif _qseq == 5:
                _key = "DELETE FROM `toprocess_candidates`"
                _res_1 = execute_query(1, query_str[5], 'candidate_reservoir')
                _res_2 = execute_query(2, query_str[4], 'candidate_reservoir')
                queries_status[_key] = {"status": _res_1, "count": _res_2[0]["COUNT(*)"]}
                queries_res[_key] = _res_2
            elif _qseq == 6:
                _key = "SELECT * FROM `filtered_toprocess_candidates`"
                _res = execute_query(2, query_str[6], 'candidate_reservoir')
                cscore_types = [v['candidate_score'] for v in _res]
                queries_status[_key] = {**{'filtered_out': len(_res)}, **dict(Counter(cscore_types))}
                queries_res[_key] = _res
            elif _qseq == 7:
                _key = "DELETE FROM `filtered_toprocess_candidates`"
                _res_1 = execute_query(1, query_str[7], 'candidate_reservoir')
                _res_2 = execute_query(2, query_str[6], 'candidate_reservoir')
                queries_status[_key] = {"status": _res_1, "count": len(_res_2)}
                queries_res[_key] = _res_2
            elif _qseq == 8:
                _key = "SELECT * FROM `search_string`"
                _res = execute_query(2, query_str[8], 'intel')
                srch_str_df = pd.DataFrame(_res, index=range(len(_res)))
                srch_str_dict = dict()
                for i in range(srch_str_df.shape[0]):
                    _dkey = (srch_str_df.iloc[i, 4], srch_str_df.iloc[i, 5])
                    _str = srch_str_df.iloc[i, 2]
                    srch_str_dict[_dkey] = _str
                queries_status[_key] = bool(_res)
                queries_res[_key] = {
                    "search_string_tbl": srch_str_df,
                    "search_strings": srch_str_dict
                }
            elif _qseq == 9:
                _key = "SELECT * FROM `keyword`"
                _res = execute_query(2, query_str[9], 'intel')
                kwds_df = pd.DataFrame(_res, index=range(len(_res)))
                queries_status[_key] = bool(_res)
                queries_res[_key] = kwds_df
            elif _qseq == 10:
                _key = "DELETE FROM `toprocess_analyzed_candidate_details_info`"
                verify_query = MySQLHelpers.create_sql_query("SELECT * FROM", "toprocess_analyzed_candidate_details_info", _copy_info)
                _res_1 = execute_query(1, query_str[10], 'candidate_reservoir')
                _res_2 = execute_query(2, verify_query, 'candidate_reservoir')
                queries_status[_key] = {"status": _res_1, "count": len(_res_2)}
                queries_res[_key] = _res_2
            elif _qseq == 'all':
                queries_status, queries_res = MySQLHelpers.qa_job_mysql_operations(job_id, [1, 5, 7], False)
            else:
                return
        # +++++++++++++++++
        if to_print:
            if query_seq == [8]:
                display(queries_res["SELECT * FROM `search_string`"]["search_string_tbl"])
                pprint.pprint(queries_res["SELECT * FROM `search_string`"]["search_strings"])
            elif query_seq == [9]:
                display(queries_res["SELECT * FROM `keyword`"])
            else:
                print(json.dumps(queries_status, indent=4))
        return queries_status, queries_res

    @staticmethod
    def _create_sql_table(db_key: str, db_name: str, base_table: str, table_name: str):
        """Checks existence of `table_name` and creates if doesn't exist"""
        try:
            query_str = "SHOW TABLES FROM `{}` LIKE '{}';".format(db_name, table_name)
            query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
            if not len(query_res):
                query_str = "CREATE TABLE {} LIKE {};".format(table_name, base_table)
                MySQLHelpers.mysql_query_execute(query_str, (), **CONFIG[db_key][db_name])
            return True
        except Exception:
            return False
        
    @staticmethod
    def _get_sql_table_cols(db_key: str, db_name: str, table_name: str):
        """Get the columns of the MySQL table: `table_name`"""
        try:
            query_str = "SHOW COLUMNS FROM {};".format(table_name)
            cols_dict = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
            table_cols = [val['Field'] for val in cols_dict]
            return table_cols
        except Exception:
            return []

    @staticmethod
    def insert_bulk_data(insert_data: list, db_key: str, db_name: str, base_table: str, table_name: str):
        """Bulk insert data into a custom table"""
        try:
            tot_contds = len(insert_data)
            MySQLHelpers._create_sql_table(db_key, db_name, base_table, table_name)  # create table if doesn't exist
            table_cols = MySQLHelpers._get_sql_table_cols(db_key, db_name, table_name)  # get columns list
            _count = 0
            while _count <= tot_contds:
                _data = insert_data[_count: _count + 200]
                MySQLManager.bulk_insert(table_name, table_cols, _data, **CONFIG[db_key][db_name])
                _count += 200
            return True
        except Exception:
            LOGGER.error("Error in bulk insertion of analyzed info, total contenders: %s", tot_contds)
            return False

    @staticmethod
    def transact_cands_from_tbl(from_table, db_key, db_name, transact_type, to_table=None, select_cols=None,
                                to_truncate=False, copy_info=None, where_clause='', save_path=False, **kwargs):
        """This function does transaction of candidates (COPY/DELETE/EXTRACT) from `from_table`
        based on the `copy_info` dict.

        Args:
            from_table (str):
                The table from which candidates details are to be copied.
            db_key (str):
                Key in CONFIG for the particular db operations.
            db_name (str):
                Name of the db table for the particular transaction operation.
            transact_type (str):
                The type of the particular transaction that is to be performed from `from_table`.
                The valid options are: ["copy","delete","extract"].
            to_table (str, optional):
                The table to which copy or delete transactions are to be performed. `to_table` needs to be
                provided only if `transact_type` = "copy" or "delete". It defaults to ``None``.
            select_cols (list, optional):
                Optionally pass list of columns to be extracted from the `from_table`. Only applicable when
                `transact_type` = "extract". It defaults to ``None``.
            to_truncate (bool, optional):
                Whether to truncate the to_table before copying. Only applicable when `transact_type` = "copy".
                It defaults to ``False``.
            copy_info (list, bool, optional):
                The list of dicts, comprising of the copy info, the keys of which should map
                to the columns of the `from_table`. It can be ``True``, ``False``, ``None`` (default)
                or list. In case of empty list, all candidates are copied from `from_table`.
                Also, it can be given as a path as well. It defaults to ``None``.
            where_clause (str, optional):
                An optional WHERE clause str. It defaults to an empty str.
            save_path (str, bool, optional):
                The path to save extracted candidates. Defaults to ``False``.
            **kwargs
                Optional valid arguments for `save_files()` func.

        Returns:
            A dict of extracted candidates.
        """
        # =================
        transact_res_dict = {'Total_candidates': 0, 'extractFlag': True, 'transactFlag': True, 'idsFlagged': []}
        extractCands = list()
        _copy_info, checkFlag = import_file(copy_info), True
        if (_copy_info is None) and checkFlag:
            _copy_info, checkFlag = [], False
        if (not len(_copy_info)) and checkFlag:
            _copy_info, checkFlag = [{}], False
        # +++++++++++++++++
        # Create the 'to_table' in the db if it doesn't exist already
        if bool(_copy_info) and transact_type == "copy":
            MySQLHelpers._create_sql_table(db_key, db_name, from_table, to_table)
            if to_truncate:
                MySQLHelpers.mysql_query_execute("TRUNCATE TABLE {};".format(to_table), (), **CONFIG[db_key][db_name])
        tblCols = MySQLHelpers._get_sql_table_cols(db_key, db_name, to_table)  # get columns list
        # +++++++++++++++++
        # Formulate transaction query command
        mysqlExecuterFunc = "MySQLManager.execute_query" if transact_type in [
            "copy", "extract"] else "MySQLHelpers.mysql_query_execute"
        # =================
        
        # =================
        for idx, candInfo in enumerate(_copy_info):
            get_query = "SELECT * FROM {} WHERE ".format(from_table) if transact_type in [
                "copy", "extract"] else "DELETE FROM {} WHERE ".format(to_table)
            if (transact_type == "extract") and isinstance(select_cols, list):
                validCols = [c for c in select_cols if c in tblCols]
                validCols = ", ".join(validCols)
                if validCols:
                    get_query = "SELECT {} FROM {} WHERE ".format(validCols, from_table)
            [get_query := get_query + '{}{} AND '.format(dicitem[0], "='" + dicitem[1].replace(
                "'", "\\'") + "'" if dicitem[1] is not None else ' IS NULL') for dicitem in candInfo.items()]
            get_query += "{};".format(where_clause) if where_clause else 'TRUE;'
            # +++++++++++++++++
            '''getCands = [] # initialize 'getCands' as empty list'''
            # copy/delete/extract candidates
            try:
                getCands = eval(mysqlExecuterFunc)(get_query, (), **CONFIG[db_key][db_name])
            except Exception:
                transact_res_dict['idsFlagged'].append(idx)
                transact_res_dict['extractFlag'] = False
                transact_res_dict['transactFlag'] = False
                continue
            # +++++++++++++++++
            if transact_type == "delete":
                continue
            transact_res_dict['Total_candidates'] += len(getCands)
            extractCands.extend(getCands)
            if transact_type == "copy":
                try:
                    count = 0
                    while count <= len(getCands):
                        _data = getCands[count:count + 200]
                        MySQLManager.bulk_insert(to_table, tblCols, _data, **CONFIG[db_key][db_name])
                        count += 200
                except Exception as ex:
                    LOGGER.error("Error in bulk insert for: %s" % (idx))
                    LOGGER.exception(ex)
                    if idx not in transact_res_dict['idsFlagged']:
                        transact_res_dict['idsFlagged'].append(idx)
                    transact_res_dict['transactFlag'] = False
        # =================
        
        # =================
        # Finaly save extracted candidates
        save_files(extractCands, save_path, **kwargs)
        return extractCands, transact_res_dict

    @staticmethod
    def store_cands_details_to_db(UniqueIds, db_key, db_name, from_table, to_table,
                                  uidField_name='job_id', to_truncate=False, where_clause='', ):
        """Custom function to extract candidates from database and save in another custom-defined table.
        
        The parameter: `UniqueIds` provide the list of keys (e.g. job ids) for which the candidate details 
        are to be saved. It can be either a list, bool or a (json) path of keys. An optional WHERE clause
        (`where_clause`) can additionally be provided.
        """
        # =================
        # First create the 'to_table' in the db if it doesn't exist already
        query_str = "SHOW TABLES FROM `{}` LIKE '{}';".format(db_name, to_table)
        query_res = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
        if not len(query_res):
            query_str = "CREATE TABLE {} LIKE {};".format(to_table, from_table)
            MySQLHelpers.mysql_query_execute(query_str, (), **CONFIG[db_key][db_name])
        if to_truncate:
            MySQLHelpers.mysql_query_execute("TRUNCATE TABLE {};".format(to_table), (), **CONFIG[db_key][db_name])
        # +++++++++++++++++
        # Get the job ids to copy from: 'from_table'
        checkFlag = True
        _UniqueIds = import_file(UniqueIds)
        if (_UniqueIds is None) and checkFlag:
            _UniqueIds, checkFlag = [], False
        if (not len(_UniqueIds)) and checkFlag:
            get_query = 'SELECT {} FROM {};'.format(uidField_name, from_table)
            query_res = MySQLManager.execute_query(get_query, (), **CONFIG[db_key][db_name])
            _UniqueIds = sorted(list(set([val[uidField_name] for val in query_res])))
            checkFlag = False
        # +++++++++++++++++
        totCands, uid_count_str = 0, "Total {}".format(uidField_name) 
        counts_dict = {uid_count_str: len(_UniqueIds), 'Total_candidates': 0}
        flags_dict = {'extractFlag': True, 'insertFlag': True, 'flaggeIds':[]}
        # +++++++++++++++++
        # Get columns list of the table
        query_str = "SHOW COLUMNS FROM {};".format(from_table)
        cols_dict = MySQLManager.execute_query(query_str, (), **CONFIG[db_key][db_name])
        tblCols = [val['Field'] for val in cols_dict]
        if not where_clause:
            where_clause = 'TRUE'
        # =================
        for uid in _UniqueIds:
            get_query = "SELECT * FROM {} WHERE {}=\'{}\' AND {};".format(from_table, uidField_name, uid, where_clause)
            getCands = MySQLManager.execute_query(get_query, (), **CONFIG[db_key][db_name])
            totCands += len(getCands)
            if not getCands:
                flags_dict['flaggeIds'].append(uid)
                flags_dict['extractFlag'] = False
                flags_dict['insertFlag'] = False
            else:
                try:
                    count = 0
                    while count <= len(getCands):
                        _data = getCands[count:count + 200]
                        MySQLManager.bulk_insert(to_table, tblCols, _data, **CONFIG[db_key][db_name])
                        count += 200
                except Exception as ex:
                    LOGGER.error("Error in bulk insert for: %s" % (uid))
                    LOGGER.exception(ex)
                    if uid not in flags_dict['flaggeIds']: flags_dict['flaggeIds'].append(uid)
                    flags_dict['insertFlag'] = False
        # =================
        counts_dict['Total_candidates'] = totCands
        return counts_dict, flags_dict
    