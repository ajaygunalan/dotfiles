#!/usr/bin/env python3
"""Thin CLI wrapper around Semantic Scholar API for use by the literature-review agent.

Auth: set S2_API_KEY in ~/.env or environment. Works without a key (shared rate pool).
Rate limiting: 1 req/sec self-throttle + exponential backoff with jitter on 429.
"""

import argparse
import json
import os
import random
import sys
import time

import requests

GRAPH_API = "https://api.semanticscholar.org/graph/v1"
RECS_API = "https://api.semanticscholar.org/recommendations/v1"
ENV_FILE = os.path.expanduser("~/.env")

_last_request_time = 0
_MIN_DELAY = 1.05
_RETRYABLE = {429, 500, 502, 503, 504}


def load_api_key():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                if line.startswith("S2_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return os.environ.get("S2_API_KEY")


API_KEY = load_api_key()

_session = requests.Session()
_session.headers["User-Agent"] = "lit-review-agent/1.0"
if API_KEY:
    _session.headers["x-api-key"] = API_KEY


def _throttle():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _MIN_DELAY:
        time.sleep(_MIN_DELAY - elapsed)
    _last_request_time = time.time()


def _request(method, url, **kwargs):
    kwargs.setdefault("timeout", 20)
    for attempt in range(4):
        _throttle()
        r = _session.request(method, url, **kwargs)
        if r.status_code in _RETRYABLE:
            retry_after = r.headers.get("Retry-After")
            delay = (
                float(retry_after)
                if retry_after
                else (2**attempt) * (0.5 + random.random())
            )
            time.sleep(min(delay, 60))
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()


# -- Field constants --------------------------------------------------------

_BASE_FIELDS = [
    "paperId",
    "title",
    "authors",
    "authors.name",
    "authors.hIndex",
    "year",
    "citationCount",
    "influentialCitationCount",
    "abstract",
    "url",
    "externalIds",
    "isOpenAccess",
    "openAccessPdf",
    "publicationTypes",
    "fieldsOfStudy",
    "publicationVenue",
    "journal",
]

SEARCH_FIELDS = ",".join(_BASE_FIELDS + ["tldr"])
_SIMPLE_FIELDS = [f for f in _BASE_FIELDS if not f.startswith("authors.")]
SIMPLE_FIELDS = ",".join(_SIMPLE_FIELDS)

_CITE_PAPER_FIELDS = [
    "paperId",
    "title",
    "authors",
    "year",
    "citationCount",
    "influentialCitationCount",
    "abstract",
    "url",
    "externalIds",
    "isOpenAccess",
    "openAccessPdf",
    "publicationTypes",
    "fieldsOfStudy",
    "publicationVenue",
    "journal",
]
_CITE_META = "contexts,intents,isInfluential"
CITE_FIELDS_FWD = (
    _CITE_META + "," + ",".join(f"citingPaper.{f}" for f in _CITE_PAPER_FIELDS)
)
CITE_FIELDS_BWD = (
    _CITE_META + "," + ",".join(f"citedPaper.{f}" for f in _CITE_PAPER_FIELDS)
)


# -- Helpers ----------------------------------------------------------------


def _safe_dict(val):
    """Return val if it's a dict, else empty dict. Handles fields that may arrive as
    a string (e.g. publicationVenue UUID) or None instead of the expected object."""
    return val if isinstance(val, dict) else {}


def _safe_list(val):
    """Return val if it's a list, else empty list."""
    return val if isinstance(val, list) else []


def _parse_author(a):
    """Parse an author entry that may be a dict (search/batch) or a string (snippet)."""
    if isinstance(a, dict):
        entry = {"name": a.get("name") or a.get("displayName") or ""}
        if a.get("hIndex"):
            entry["h_index"] = a["hIndex"]
        return entry
    return {"name": str(a)} if a else {"name": ""}


# -- Formatters -------------------------------------------------------------


def _format_paper(p):
    if not p or not isinstance(p, dict):
        return None

    authors = [_parse_author(a) for a in _safe_list(p.get("authors"))[:4]]

    ext = _safe_dict(p.get("externalIds"))
    oa_pdf = p.get("openAccessPdf")
    tldr = _safe_dict(p.get("tldr"))
    venue = p.get("publicationVenue")
    journal = p.get("journal")

    # openAccessPdf: could be dict {url, status, ...} or a bare URL string
    if isinstance(oa_pdf, dict):
        pdf_url = oa_pdf.get("url")
    elif isinstance(oa_pdf, str) and oa_pdf:
        pdf_url = oa_pdf
    else:
        pdf_url = None

    result = {
        "s2_id": p.get("paperId"),
        "title": p.get("title", ""),
        "authors": authors,
        "year": p.get("year"),
        "doi": ext.get("DOI"),
        "arxiv": ext.get("ArXiv"),
        "cited_by": p.get("citationCount", 0),
        "influential_cites": p.get("influentialCitationCount", 0),
        "is_open_access": p.get("isOpenAccess"),
        "pdf_url": pdf_url,
        "fields": p.get("fieldsOfStudy"),
        "pub_types": p.get("publicationTypes"),
        "tldr": tldr.get("text") if tldr else None,
        "abstract": p.get("abstract"),
        "url": p.get("url"),
    }

    # Venue: publicationVenue may be dict, string UUID, or None
    venue_dict = _safe_dict(venue)
    journal_dict = _safe_dict(journal)
    if venue_dict.get("name"):
        result["venue"] = venue_dict["name"]
        result["venue_type"] = venue_dict.get("type")
    elif isinstance(venue, str) and venue:
        result["venue"] = venue
    elif journal_dict.get("name"):
        result["venue"] = journal_dict["name"]

    return result


def _format_citation(c):
    paper = c.get("citingPaper") or c.get("citedPaper") or {}
    result = _format_paper(paper)
    if result is None:
        return None
    result["contexts"] = c.get("contexts")
    result["intents"] = c.get("intents")
    result["is_influential"] = c.get("isInfluential")
    return result


# -- Commands ---------------------------------------------------------------


def cmd_search(args):
    params = {
        "query": args.query,
        "fields": SEARCH_FIELDS,
        "limit": args.n,
        "offset": args.offset,
    }
    if args.year:
        params["year"] = args.year
    if args.min_cites:
        params["minCitationCount"] = args.min_cites
    if args.fields_of_study:
        params["fieldsOfStudy"] = args.fields_of_study
    if args.venue:
        params["venue"] = args.venue
    if args.open_access:
        params["openAccessPdf"] = ""
    if args.pub_types:
        params["publicationTypes"] = args.pub_types

    data = _request("GET", f"{GRAPH_API}/paper/search", params=params)
    results = [_format_paper(p) for p in data.get("data", [])]
    print(
        json.dumps(
            {
                "total": data.get("total", 0),
                "offset": data.get("offset", 0),
                "next": data.get("next"),
                "results": results,
            },
            indent=2,
        )
    )


def cmd_bulk_search(args):
    params = {"query": args.query, "fields": SIMPLE_FIELDS}
    if args.sort:
        params["sort"] = args.sort
    if args.year:
        params["year"] = args.year
    if args.min_cites:
        params["minCitationCount"] = args.min_cites
    if args.fields_of_study:
        params["fieldsOfStudy"] = args.fields_of_study
    if args.pub_types:
        params["publicationTypes"] = args.pub_types
    if args.venue:
        params["venue"] = args.venue
    if args.open_access:
        params["openAccessPdf"] = ""
    if args.token:
        params["token"] = args.token

    data = _request("GET", f"{GRAPH_API}/paper/search/bulk", params=params)
    results = [_format_paper(p) for p in data.get("data", [])][: args.n]
    print(
        json.dumps(
            {
                "total": data.get("total", 0),
                "token": data.get("token"),
                "results": results,
            },
            indent=2,
        )
    )


def cmd_match(args):
    params = {"query": args.title, "fields": SEARCH_FIELDS}
    try:
        data = _request("GET", f"{GRAPH_API}/paper/search/match", params=params)
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            print(json.dumps({"error": f"No match found for: {args.title}", "suggestion": "Try `search` with broader terms instead of `match`"}))
            sys.exit(1)
        raise
    paper = data.get("data", [{}])[0] if data.get("data") else {}
    result = _format_paper(paper)
    if result:
        result["match_score"] = paper.get("matchScore")
    print(json.dumps(result, indent=2))


def cmd_work(args):
    fields = (
        SEARCH_FIELDS
        + ",referenceCount,references.paperId,references.title"
        + ",citations.paperId,citations.title"
    )
    data = _request(
        "GET", f"{GRAPH_API}/paper/{args.paper_id}", params={"fields": fields}
    )
    result = _format_paper(data)
    if result is None:
        print(json.dumps({"error": "Paper not found"}), file=sys.stderr)
        sys.exit(1)
    result["reference_count"] = data.get("referenceCount", 0)
    result["references"] = [
        {"s2_id": r.get("paperId"), "title": r.get("title")}
        for r in _safe_list(data.get("references"))[:20]
    ]
    result["citation_sample"] = [
        {"s2_id": c.get("paperId"), "title": c.get("title")}
        for c in _safe_list(data.get("citations"))[:20]
    ]
    print(json.dumps(result, indent=2))


def _cmd_citations(args, fields, endpoint):
    params = {"fields": fields, "limit": args.n, "offset": args.offset}
    data = _request(
        "GET", f"{GRAPH_API}/paper/{args.paper_id}/{endpoint}", params=params
    )
    results = [r for r in (_format_citation(c) for c in data.get("data", [])) if r]
    print(
        json.dumps(
            {
                "total": len(results),
                "next": data.get("next"),
                "results": results,
            },
            indent=2,
        )
    )


def cmd_cites(args):
    _cmd_citations(args, CITE_FIELDS_FWD, "citations")


def cmd_cited_by(args):
    _cmd_citations(args, CITE_FIELDS_BWD, "references")


def _resolve_id(paper_id):
    """Ensure paper_id is a full S2 ID or a recognized prefix format (ARXIV:, DOI:, CorpusId:).
    Short hex strings from search results cause 400 errors on some endpoints."""
    if ":" in paper_id:
        return paper_id  # Already prefixed (ARXIV:xxx, DOI:xxx, etc.)
    if len(paper_id) < 40:
        # Likely a truncated S2 ID — try to resolve via a quick lookup
        try:
            data = _request("GET", f"{GRAPH_API}/paper/{paper_id}", params={"fields": "paperId"})
            return data.get("paperId", paper_id)
        except Exception:
            return paper_id
    return paper_id


def cmd_recommend(args):
    resolved_ids = [_resolve_id(pid) for pid in args.paper_ids]
    if len(resolved_ids) == 1 and not args.negative and args.pool:
        params = {"fields": SIMPLE_FIELDS, "limit": args.n, "from": args.pool}
        try:
            data = _request(
                "GET", f"{RECS_API}/papers/forpaper/{resolved_ids[0]}", params=params
            )
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 400:
                print(json.dumps({"error": f"Recommend failed for ID {resolved_ids[0]}. Try using full S2 ID or ARXIV:xxx format.", "results": []}))
                return
            raise
    else:
        body = {
            "positivePaperIds": resolved_ids,
            "negativePaperIds": [_resolve_id(x) for x in args.negative.split(",")] if args.negative else [],
        }
        try:
            data = _request(
                "POST",
                f"{RECS_API}/papers/",
                json=body,
                params={"fields": SIMPLE_FIELDS, "limit": args.n},
            )
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 400:
                print(json.dumps({"error": f"Recommend failed. Ensure all IDs are full S2 IDs or ARXIV:xxx format. IDs: {resolved_ids}", "results": []}))
                return
            raise
    results = [_format_paper(p) for p in data.get("recommendedPapers", [])]
    print(json.dumps({"results": results}, indent=2))


def cmd_author(args):
    if args.author_id:
        author = _request(
            "GET",
            f"{GRAPH_API}/author/{args.author_id}",
            params={"fields": "name,affiliations,paperCount,citationCount,hIndex"},
        )
        data = _request(
            "GET",
            f"{GRAPH_API}/author/{args.author_id}/papers",
            params={"fields": SIMPLE_FIELDS, "limit": args.n, "offset": args.offset},
        )
        results = [_format_paper(p) for p in data.get("data", [])]
        print(
            json.dumps(
                {
                    "author": author.get("name"),
                    "affiliations": author.get("affiliations"),
                    "h_index": author.get("hIndex"),
                    "total_papers": author.get("paperCount"),
                    "total_citations": author.get("citationCount"),
                    "results": results,
                },
                indent=2,
            )
        )
    elif args.query:
        data = _request(
            "GET",
            f"{GRAPH_API}/author/search",
            params={
                "query": args.query,
                "fields": "name,affiliations,paperCount,citationCount,hIndex",
                "limit": args.n,
                "offset": args.offset,
            },
        )
        print(
            json.dumps(
                {
                    "total": data.get("total", 0),
                    "results": data.get("data", []),
                },
                indent=2,
            )
        )
    else:
        print(json.dumps({"error": "Provide --id or --query"}), file=sys.stderr)
        sys.exit(1)


def cmd_batch(args):
    data = _request(
        "POST",
        f"{GRAPH_API}/paper/batch",
        json={"ids": args.paper_ids},
        params={"fields": SEARCH_FIELDS},
    )
    results = [_format_paper(p) for p in _safe_list(data) if p]
    print(json.dumps({"results": results}, indent=2))


def cmd_snippet(args):
    params = {"query": args.query, "limit": args.n}
    if args.min_cites:
        params["minCitationCount"] = args.min_cites
    if args.fields_of_study:
        params["fieldsOfStudy"] = args.fields_of_study
    data = _request("GET", f"{GRAPH_API}/snippet/search", params=params)

    results = []
    for item in data.get("data", [])[:args.n]:
        paper = _safe_dict(item.get("paper"))
        snippet = _safe_dict(item.get("snippet"))
        raw_authors = _safe_list(paper.get("authors"))[:4]
        authors = [
            a.get("name", "") if isinstance(a, dict) else str(a) for a in raw_authors
        ]
        results.append(
            {
                "s2_id": paper.get("paperId")
                or (f"CorpusId:{paper['corpusId']}" if paper.get("corpusId") else None),
                "title": paper.get("title"),
                "authors": authors,
                "year": paper.get("year"),
                "cited_by": paper.get("citationCount", 0),
                "url": paper.get("url"),
                "score": item.get("score"),
                "snippet": {
                    "text": snippet.get("text"),
                    "section": snippet.get("section"),
                    "kind": snippet.get("snippetKind"),
                },
            }
        )

    print(json.dumps({"results": results}, indent=2))


# -- CLI --------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Semantic Scholar CLI for literature search"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("search", help="Relevance-ranked paper search")
    p.add_argument("query", help="Search query")
    p.add_argument("-n", type=int, default=10, help="Results (max 100)")
    p.add_argument("--offset", type=int, default=0, help="Pagination offset")
    p.add_argument("--year", help="Year filter: 2024, 2020-2024")
    p.add_argument("--min-cites", type=int, help="Minimum citation count")
    p.add_argument("--fields-of-study", help="e.g. 'Computer Science,Physics'")
    p.add_argument("--venue", help="Venue filter")
    p.add_argument("--open-access", action="store_true", help="Open access only")
    p.add_argument("--pub-types", help="JournalArticle,Conference,Review,...")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser(
        "bulk-search", help="Bulk search with boolean syntax (up to 10M)"
    )
    p.add_argument("query", help="Boolean query: +robot +manipulation -survey")
    p.add_argument("--sort", help="citationCount:desc, publicationDate:asc")
    p.add_argument("--year", help="Year filter")
    p.add_argument("--min-cites", type=int, help="Minimum citation count")
    p.add_argument("--fields-of-study", help="Comma-separated fields")
    p.add_argument("--pub-types", help="JournalArticle,Conference,Review,...")
    p.add_argument("--venue", help="Venue filter")
    p.add_argument("--open-access", action="store_true", help="Open access only")
    p.add_argument("--token", help="Continuation token for next page")
    p.add_argument("-n", type=int, default=10, help="Max results to return (truncates)")
    p.set_defaults(func=cmd_bulk_search)

    p = sub.add_parser("match", help="Find single paper by closest title match")
    p.add_argument("title", help="Paper title to match")
    p.set_defaults(func=cmd_match)

    p = sub.add_parser("work", help="Full details for a single paper")
    p.add_argument(
        "paper_id", help="S2 ID, DOI:10.xxx, ARXIV:xxx, CorpusId:NNN, or URL:..."
    )
    p.set_defaults(func=cmd_work)

    p = sub.add_parser(
        "cites", help="Papers that cite this one (with citation context)"
    )
    p.add_argument("paper_id", help="S2 paper ID or DOI:10.xxx")
    p.add_argument("-n", type=int, default=10, help="Results (max 1000)")
    p.add_argument("--offset", type=int, default=0)
    p.set_defaults(func=cmd_cites)

    p = sub.add_parser("cited-by", help="Papers referenced by this one")
    p.add_argument("paper_id", help="S2 paper ID or DOI:10.xxx")
    p.add_argument("-n", type=int, default=10, help="Results (max 1000)")
    p.add_argument("--offset", type=int, default=0)
    p.set_defaults(func=cmd_cited_by)

    p = sub.add_parser(
        "recommend", help="Paper recommendations (positive/negative seeds)"
    )
    p.add_argument("paper_ids", nargs="+", help="Positive seed paper IDs")
    p.add_argument("--negative", help="Comma-separated negative seed IDs")
    p.add_argument(
        "--pool", choices=["recent", "all-cs"], help="Pool (single-paper only)"
    )
    p.add_argument("-n", type=int, default=10)
    p.set_defaults(func=cmd_recommend)

    p = sub.add_parser("author", help="Search authors or get author's papers")
    p.add_argument("--id", dest="author_id", help="S2 author ID (get papers)")
    p.add_argument("--query", "-q", help="Search by name")
    p.add_argument("-n", type=int, default=10)
    p.add_argument("--offset", type=int, default=0)
    p.set_defaults(func=cmd_author)

    p = sub.add_parser("batch", help="Batch lookup of up to 500 papers")
    p.add_argument("paper_ids", nargs="+", help="Paper IDs")
    p.set_defaults(func=cmd_batch)

    p = sub.add_parser("snippet", help="Search within paper text for passages")
    p.add_argument("query", help="Text to search for")
    p.add_argument("-n", type=int, default=10)
    p.add_argument("--min-cites", type=int, help="Minimum citation count")
    p.add_argument(
        "--fields-of-study",
        help="Post-filter by field (e.g. 'Computer Science,Medicine')",
    )
    p.set_defaults(func=cmd_snippet)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        msg = str(e).replace(API_KEY, "***") if API_KEY else str(e)
        print(json.dumps({"error": msg}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
