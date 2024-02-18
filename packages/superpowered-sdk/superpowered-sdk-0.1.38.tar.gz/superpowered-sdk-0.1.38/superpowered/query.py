import time
import warnings

from . import superpowered
from . import exceptions


def query(knowledge_base_ids: list, query: str, top_k: int = 5, summarize_results: bool = False):
    """
    BACKWARD COMPATIBILITY
    POST /knowledge_bases/query
    """
    class RenameWarning(Warning):
        pass
    
    warnings.warn(
        message="The 'query' function has been renamed to 'query_knowledge_bases' for clarity.",
        category=RenameWarning,
        stacklevel=2
    )
    return query_knowledge_bases(knowledge_base_ids, query, top_k, summarize_results)


def query_knowledge_bases(knowledge_base_ids: list, query: str, top_k: int = 5, summarize_results: bool = False, summary_system_message: str = None, summary_config: dict = {}, exclude_irrelevant_results: bool = True, use_auto_query: bool = False, use_rse: bool = True, segment_length: str = 'medium', model: str = 'gpt-3.5-turbo', timeout: int = 90, auto_query_guidance: str = '') -> dict:
    """
    Query one or more knowledge bases.

    Args:
        knowledge_base_ids (list): A list of knowledge base IDs to query.
        query (str): The query string.
        top_k (int, optional): The maximum number of results to return. Ignored if `use_rse` is True. Defaults to 5.
        summarize_results (bool, optional): Whether to summarize the results. Defaults to False.
        summary_config (dict, optional): A dictionary of summary configuration options. Defaults to {}.
        exclude_irrelevant_results (bool, optional): Whether to exclude irrelevant results. Defaults to True.
        use_auto_query (bool, optional): Whether to use the auto query feature. Defaults to False.
        auto_query_guidance (str, optional): Ignored if `use_auto_query` is False. When we automatically generate queries based on user input, you may want to provide some additional guidance and/or context to the system. Defaults to ''.
        use_rse (bool, optional): Whether to use the RSE feature. Defaults to False.
        segment_length (str, optional): Ignored if `use_rse` is False. This parameter determines how long each result (segment) is. Defaults to 'medium'. Must be one of 'very_short', 'short', 'medium', or 'long'.
        model (str, optional): The model to use for summarization. Defaults to 'gpt-3.5-turbo'.

    Note:
        The ``summary_config`` dictionary will look as follows:
        
        .. code-block:: python

            {
                'system_message': 'string',  # a system message to guide the LLM summary.
            }

    Returns:
        dict: A query response object.

    Note:
        The returned object will look as follows:
        
        .. code-block:: python

            {
                'ranked_results': [
                    {
                        'cosine_similarity': 0.0,  # the cosine similarity score
                        'reranker_score': 0.0,  # the relevance score
                        'metadata': {
                            'content': 'content of the chunk,
                            'original_content': 'content of the chunk before prepending chunk headers',
                            'knowledge_base_id': 'uuid',
                            'document_id': 'uuid',
                            'account_id': 'uuid',
                            'document': {}  # document object
                        },  # a dictionary of metadata
                        'content': 'string',  # the text of the chunk
                    }
                ],
                'summary': 'string',  # the summary text
                'search_queries': [{'knowledge_base': {}, 'query': 'string'}],
            }

    References:
        ``POST /knowledge_bases/query``
    """
    data = {
        'async': True,
        'query': query,
        'knowledge_base_ids': knowledge_base_ids,
        'summary_config': summary_config or {},
    }

    if top_k:
        data['top_k'] = top_k
    if summarize_results is not None:
        data['summarize_results'] = summarize_results
    if exclude_irrelevant_results is not None:
        data['exclude_irrelevant_results'] = exclude_irrelevant_results
    if use_auto_query is not None:
        data['use_auto_query'] = use_auto_query
    if auto_query_guidance is not None:
        data['auto_query_guidance'] = auto_query_guidance
    if use_rse is not None:
        data['use_rse'] = use_rse
    if segment_length is not None:
        data['segment_length'] = segment_length
    if model is not None:
        data['model'] = model
    # handle the deprecated summary_system_message argument
    if summary_system_message and not data['summary_config'].get('system_message'):
        data['summary_config']['system_message'] = summary_system_message
    args = {
        'method': 'POST',
        'url': f'{superpowered.get_base_url()}/knowledge_bases/query',
        'json': data,
        'auth': superpowered.auth(),
    }
    resp = superpowered.make_api_call(args)
    t0 = time.time()
    while time.time() - t0 < timeout and resp.get('status') in {'PENDING', 'IN_PROGRESS'}:
        time.sleep(1)
        args = {
            'method': 'GET',
            'url': resp['status_url'],
            'auth': superpowered.auth(),
        }
        resp = superpowered.make_api_call(args)
    if resp['status'] == 'FAILED':
        raise exceptions.InternalServerError
    else:
        return resp['response']
