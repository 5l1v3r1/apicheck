from typing import Any, Dict

from apicheck.core.generator import _type_matcher
from apicheck.core.generator.open_api_strategy import strategy
from apicheck.core.generator.dict_strategy import dict_generator


rules_strategy = strategy + [
    (_type_matcher("dictionary"), dict_generator)
]


def rules_processor(rules: Dict[str, Any]):
    import apicheck.core.rules.path as pa
    import apicheck.core.rules.body as bo
    import apicheck.core.rules.headers as he

    def _proc(request: Dict[str, Any]):
        # TODO: a request without path it's a valid request?
        if "path" in request:
            endpoint = pa.find_endpoint(rules, request["path"])
            # TODO: how can i deal if no endpoint found?
        else:
            return request
        rule = rules[endpoint]
        if "method" in rule and "method" in request:
            rules_method = rule["method"]
            is_list = isinstance(rules_method, list)
            is_not_in_method = not request["method"] in rules_method
            if is_list and is_not_in_method:
                return request
            elif request["method"] != rules_method:
                return request

        if "pathParams" in rule:
            request["path"] = pa.merge_paths(
                    request["path"],
                    endpoint,
                    rule["pathParams"]
                )
        if "queryParams" in rule:
            if "override" in rule and "queryParams" in rule["override"]:
                proc = pa.override_query
            else:
                proc = pa.merge_queries
            request["path"] = proc(request["path"], rule["queryParams"])
        if "body" in rule:
            if "override" in rule and "body" in rule["override"]:
                proc = bo.override_body
            else:
                proc = bo.merge_body
            request["body"] = proc(request["body"], rule["body"])
        if "headers" in rule:
            if "override" in rule and "headers" in rule["override"]:
                raise NotImplementedError("no headers override yet")
            else:
                proc = he.merge_headers
            request["headers"] = proc(request["headers"], rule["headers"])
        return request
    if not rules or len(rules) == 0:
        return lambda x: x
    return _proc
