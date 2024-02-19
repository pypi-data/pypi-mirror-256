import string
import time
from typing import Optional

from .. import procfile, procrec, proctree, utility
from . import CommandError


__all__ = 'run',


def run(
    procfile_list: list,
    database_file: str,
    interval: int,
    environment: Optional[list] = None,
    query: Optional[str] = None,
    pid_list: Optional[str] = None,
    recnum: Optional[int] = None,
    reevalnum: Optional[int] = None,
    stop_without_result: bool = False,
):
    readers = {k: v for k, v in procfile.registry.items() if k in procfile_list}
    forest = proctree.Forest(readers)

    count = 1
    query_tpl = string.Template(query)
    pid_list_tpl = string.Template(pid_list)
    meta = utility.get_meta(procfile_list)
    with procrec.SqliteStorage(database_file, procfile_list, meta) as store:
        while True:
            start = time.time()
            if environment and (count == 1 or reevalnum and (count + 1) % reevalnum == 0):
                env_dict = utility.evaluate(environment)
                if query:
                    query = query_tpl.safe_substitute(env_dict)
                if pid_list:
                    pid_list = pid_list_tpl.safe_substitute(env_dict)

            branch_pids = [int(p) for p in pid_list.split(',') if p] if pid_list else None
            result = forest.get_roots(branch_pids)

            if query:
                try:
                    result = proctree.query(result, query)
                except proctree.JsonPathQueryError as ex:
                    raise CommandError(str(ex)) from ex

            flat_node_list = proctree.flatten(result, procfile_list)
            store.record(start, flat_node_list)

            count += 1
            if recnum and count > recnum or stop_without_result and not flat_node_list:
                break

            latency = time.time() - start
            time.sleep(max(0, interval - latency))
