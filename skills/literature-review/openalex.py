#!/usr/bin/env python3
"""Thin CLI wrapper around OpenAlex REST API for use by the literature-review agent."""

import argparse
import json
import os
import re
import sys
import time

import requests

API = "https://api.openalex.org"
ENV_FILE = os.path.expanduser("~/.env")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load_api_key():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                if line.startswith("OPENALEX_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return os.environ.get("OPENALEX_API_KEY")


API_KEY = load_api_key()
BASE_PARAMS = {"api_key": API_KEY} if API_KEY else {}

SEARCH_SELECT = (
    "id,title,authorships,publication_year,doi,cited_by_count,open_access,"
    "primary_topic,abstract_inverted_index,type,language,is_retracted,fwci,"
    "citation_normalized_percentile,has_fulltext"
)


# -- Trusted institutions ---------------------------------------------------


def _normalize_inst(name):
    name = name.lower().strip()
    for a, b in [
        ("ä", "a"),
        ("ö", "o"),
        ("ü", "u"),
        ("é", "e"),
        ("è", "e"),
        ("ë", "e"),
        ("à", "a"),
        ("ç", "c"),
    ]:
        name = name.replace(a, b)
    name = re.sub(r"[-\u2013\u2014,]+", " ", name)
    name = re.sub(r"\([^)]*\)", "", name)
    name = re.sub(r"\be\.?\s*v\.?\b", "", name)
    name = re.sub(r"\b(inc\.?|ltd\.?|gmbh|corp\.?)\b", "", name)
    name = name.replace(".", "")
    name = re.sub(r"\s+", " ", name).strip()
    return name


def _load_trusted_institutions():
    path = os.path.join(DATA_DIR, "trusted_institutions.csv")
    if not os.path.exists(path):
        return set()
    names = set()
    with open(path) as f:
        for line in f:
            if line.startswith("#") or line.startswith("institution,"):
                continue
            name = line.split(",", 1)[0].strip()
            if name:
                names.add(_normalize_inst(name))
    return names


_TRUSTED = _load_trusted_institutions()


def _is_trusted(institution_name):
    if not institution_name or not _TRUSTED:
        return False
    return _normalize_inst(institution_name) in _TRUSTED


# -- HTTP -------------------------------------------------------------------

_RETRYABLE = {429, 500, 502, 503, 504}
_session = requests.Session()
_session.headers["User-Agent"] = "openalex-cli/1.0"


def _get(endpoint, params=None, timeout=20):
    p = {**BASE_PARAMS, **(params or {})}
    for attempt in range(3):
        r = _session.get(f"{API}{endpoint}", params=p, timeout=timeout)
        if r.status_code in _RETRYABLE:
            time.sleep(2**attempt)
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()


# -- Formatters -------------------------------------------------------------


def _reconstruct_abstract(inverted_index):
    if not inverted_index or not isinstance(inverted_index, dict):
        return None
    words = {}
    for word, positions in inverted_index.items():
        if not isinstance(positions, list):
            continue
        for pos in positions:
            words[pos] = word
    if not words:
        return None
    return " ".join(words[i] for i in sorted(words))


def _format_work(w):
    if not w or not isinstance(w, dict):
        return None

    all_authorships = w.get("authorships") or []
    authors = []
    any_trusted = False
    for i, a in enumerate(all_authorships):
        if not isinstance(a, dict):
            continue
        insts = [
            inst.get("display_name")
            for inst in (a.get("institutions") or [])
            if isinstance(inst, dict) and inst.get("display_name")
        ]
        if any(_is_trusted(inst) for inst in insts):
            any_trusted = True
        if i < 4:
            author_obj = a.get("author") or {}
            if not isinstance(author_obj, dict):
                author_obj = {}
            entry = {"name": author_obj.get("display_name", "")}
            if insts:
                entry["institutions"] = insts
                if any(_is_trusted(inst) for inst in insts):
                    entry["trusted"] = True
            authors.append(entry)

    topic = w.get("primary_topic") or {}
    if not isinstance(topic, dict):
        topic = {}
    oa = w.get("open_access") or {}
    if not isinstance(oa, dict):
        oa = {}
    doi_raw = w.get("doi") or ""

    result = {
        "openalex_id": (w.get("id") or "").replace("https://openalex.org/", ""),
        "title": w.get("title") or w.get("display_name") or "",
        "authors": authors,
        "year": w.get("publication_year"),
        "doi": doi_raw.replace("https://doi.org/", "") if doi_raw else None,
        "cited_by": w.get("cited_by_count", 0),
        "oa_url": oa.get("oa_url"),
        "topic": topic.get("display_name"),
        "subfield": (topic.get("subfield") or {}).get("display_name"),
        "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
    }

    result["trusted"] = any_trusted
    result["is_retracted"] = bool(w.get("is_retracted"))

    if w.get("type"):
        result["type"] = w["type"]
    if w.get("language"):
        result["language"] = w["language"]
    if w.get("fwci") is not None:
        result["fwci"] = round(w["fwci"], 2)
    cnp = w.get("citation_normalized_percentile") or {}
    if isinstance(cnp, dict):
        if cnp.get("is_in_top_1_percent"):
            result["top_1_pct"] = True
        elif cnp.get("is_in_top_10_percent"):
            result["top_10_pct"] = True
    if w.get("has_fulltext"):
        result["has_fulltext"] = True

    return result


# -- Commands ---------------------------------------------------------------


def cmd_search(args):
    params = {"select": SEARCH_SELECT, "per_page": args.n}

    use_semantic = args.semantic
    if args.subfield and not use_semantic:
        use_semantic = True
        print(
            "Note: auto-switching to semantic search"
            " (--subfield + keyword search degrades relevance)",
            file=sys.stderr,
        )

    if use_semantic:
        params["search.semantic"] = args.query
    else:
        params["search"] = args.query

    def _add(filt, semantic_ok=True):
        if use_semantic and not semantic_ok:
            name = filt.split(":")[0]
            print(
                f"Warning: {name} filter not supported with --semantic, ignoring",
                file=sys.stderr,
            )
            return
        filters.append(filt)

    filters = []
    if args.year:
        _add(f"publication_year:{args.year}", semantic_ok=False)
    if args.from_date:
        _add(f"from_publication_date:{args.from_date}", semantic_ok=False)
    if args.to_date:
        _add(f"to_publication_date:{args.to_date}", semantic_ok=False)
    if args.cited_by_min is not None:
        _add(f"cited_by_count:>{args.cited_by_min - 1}", semantic_ok=False)
    if args.oa:
        _add("is_oa:true", semantic_ok=False)
    if args.subfield:
        ids = "|".join(f"subfields/{s.strip()}" for s in args.subfield.split(","))
        _add(f"primary_topic.subfield.id:{ids}", semantic_ok=False)
    if args.type:
        _add(f"type:{args.type}")
    if args.language:
        _add(f"language:{args.language}")
    if args.no_retracted:
        _add("is_retracted:false")
    if args.has_abstract:
        _add("has_abstract:true")
    if args.has_fulltext:
        _add("has_fulltext:true")
    if args.fwci_min is not None:
        _add(f"fwci:>{args.fwci_min}", semantic_ok=False)
    if args.related_to:
        _add(f"related_to:{args.related_to}", semantic_ok=False)

    client_sort = None
    if args.sort:
        if "cited_by_count" in args.sort:
            client_sort = args.sort
        else:
            params["sort"] = args.sort

    if filters:
        params["filter"] = ",".join(filters)

    data = _get("/works", params)
    results = [r for r in (_format_work(w) for w in data.get("results", [])) if r]

    if client_sort:
        reverse = client_sort.endswith(":desc")
        results.sort(key=lambda r: r.get("cited_by", 0), reverse=reverse)
        results = results[: args.n]

    meta = data.get("meta") or {}
    print(
        json.dumps(
            {"count": meta.get("count", 0), "results": results},
            indent=2,
        )
    )


def _cmd_citation_graph(args, filter_key):
    filters = [f"{filter_key}:{args.work_id}"]
    if args.year:
        filters.append(f"publication_year:{args.year}")

    params = {
        "filter": ",".join(filters),
        "select": SEARCH_SELECT,
        "per_page": args.n,
        "sort": "cited_by_count:desc",
    }

    if args.cursor:
        params["cursor"] = args.cursor

    data = _get("/works", params)
    results = [r for r in (_format_work(w) for w in data.get("results", [])) if r]
    meta = data.get("meta", {})
    output = {"count": meta.get("count", 0), "results": results}

    next_cursor = meta.get("next_cursor")
    if next_cursor:
        output["next_cursor"] = next_cursor

    print(json.dumps(output, indent=2))


def cmd_cites(args):
    _cmd_citation_graph(args, "cites")


def cmd_cited_by(args):
    _cmd_citation_graph(args, "cited_by")


def cmd_author(args):
    if args.query:
        data = _get("/authors", params={"search": args.query, "per_page": args.n})
        results = []
        for a in data.get("results", []):
            if not isinstance(a, dict):
                continue
            stats = a.get("summary_stats") or {}
            entry = {
                "openalex_id": (a.get("id") or "").replace("https://openalex.org/", ""),
                "name": a.get("display_name"),
                "works_count": a.get("works_count"),
                "cited_by_count": a.get("cited_by_count"),
                "last_known_institutions": [
                    i.get("display_name")
                    for i in (a.get("last_known_institutions") or [])
                    if isinstance(i, dict)
                ],
            }
            if stats.get("h_index"):
                entry["h_index"] = stats["h_index"]
            if stats.get("i10_index"):
                entry["i10_index"] = stats["i10_index"]
            orcid = a.get("orcid")
            if orcid:
                entry["orcid"] = orcid.replace("https://orcid.org/", "")
            results.append(entry)
        meta = data.get("meta") or {}
        print(
            json.dumps(
                {"count": meta.get("count", 0), "results": results},
                indent=2,
            )
        )
    elif args.author_id:
        author_data = _get(f"/authors/{args.author_id}")
        author_name = (author_data or {}).get("display_name", "Unknown")

        params = {
            "filter": f"authorships.author.id:{args.author_id}",
            "select": SEARCH_SELECT,
            "per_page": args.n,
            "sort": "publication_date:desc",
        }
        data = _get("/works", params)
        results = [r for r in (_format_work(w) for w in data.get("results", [])) if r]
        meta = data.get("meta") or {}
        print(
            json.dumps(
                {
                    "author": author_name,
                    "total_works": meta.get("count", 0),
                    "results": results,
                },
                indent=2,
            )
        )
    else:
        print(json.dumps({"error": "Provide author_id or --query"}), file=sys.stderr)
        sys.exit(1)


def cmd_work(args):
    w = _get(f"/works/{args.work_id}")
    if not w or not isinstance(w, dict):
        print(json.dumps({"error": "Work not found"}), file=sys.stderr)
        sys.exit(1)
    result = _format_work(w)
    if result is None:
        print(json.dumps({"error": "Work not found"}), file=sys.stderr)
        sys.exit(1)
    result["referenced_works"] = [
        rid.replace("https://openalex.org/", "")
        for rid in (w.get("referenced_works") or [])
        if isinstance(rid, str)
    ]
    result["related_works"] = [
        rid.replace("https://openalex.org/", "")
        for rid in (w.get("related_works") or [])
        if isinstance(rid, str)
    ]
    result["pdf_url"] = (w.get("best_oa_location") or {}).get("pdf_url")
    locations = w.get("locations") or []
    result["all_urls"] = [
        loc.get("pdf_url") or loc.get("landing_page_url")
        for loc in locations
        if isinstance(loc, dict) and (loc.get("pdf_url") or loc.get("landing_page_url"))
    ]
    print(json.dumps(result, indent=2))


def cmd_download(args):
    work_id = args.identifier
    if re.match(r"^10\.", work_id):
        work_id = f"doi:{work_id}"

    w = _get(f"/works/{work_id}")
    if not w or not isinstance(w, dict):
        print(json.dumps({"error": f"Work not found: {work_id}"}), file=sys.stderr)
        sys.exit(1)
    title = w.get("title", "unknown")
    oa_id = (w.get("id") or "").replace("https://openalex.org/", "")

    pdf_url = None
    if API_KEY:
        hosted_url = f"{API}/works/{oa_id}.pdf"
        try:
            r = _session.head(
                hosted_url,
                params={"api_key": API_KEY},
                timeout=10,
                allow_redirects=True,
            )
            if r.status_code == 200:
                pdf_url = hosted_url + f"?api_key={API_KEY}"
        except requests.RequestException:
            pass

    if not pdf_url:
        oa = w.get("open_access") or {}
        best_oa = w.get("best_oa_location") or {}
        if isinstance(best_oa, dict):
            pdf_url = best_oa.get("pdf_url")
        if not pdf_url and isinstance(oa, dict):
            pdf_url = oa.get("oa_url")

    if not pdf_url:
        for loc in w.get("locations") or []:
            if isinstance(loc, dict) and loc.get("pdf_url"):
                pdf_url = loc["pdf_url"]
                break

    if not pdf_url:
        print(json.dumps({"error": f"No PDF found for: {title}", "doi": w.get("doi")}))
        sys.exit(1)

    dl_dir = args.output_dir or "./downloads"
    os.makedirs(dl_dir, exist_ok=True)

    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    safe_name = re.sub(r"[^\w\-.]", "_", doi or oa_id)
    filepath = os.path.join(dl_dir, f"{safe_name}.pdf")

    if os.path.exists(filepath) and not args.force:
        print(
            json.dumps({"path": filepath, "status": "already_exists", "title": title})
        )
        return

    r = _session.get(pdf_url, timeout=60)
    r.raise_for_status()

    if not r.content[:5] == b"%PDF-":
        print(json.dumps({"error": f"Response is not a PDF (got {r.headers.get('Content-Type', 'unknown')})", "title": title, "doi": doi}))
        sys.exit(1)

    with open(filepath, "wb") as f:
        f.write(r.content)

    print(
        json.dumps(
            {
                "path": filepath,
                "status": "downloaded",
                "title": title,
                "size_kb": len(r.content) // 1024,
            }
        )
    )


# -- CLI --------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="OpenAlex CLI for literature search")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search for papers")
    p_search.add_argument(
        "query",
        help='Search query (supports AND/OR/NOT, "phrases", wildcards*)',
    )
    p_search.add_argument(
        "-n", type=int, default=10, help="Number of results (max 200)"
    )
    p_search.add_argument(
        "--semantic", action="store_true", help="Use semantic (embedding) search"
    )
    p_search.add_argument("--year", help="Year filter: 2024, >2022, <2020")
    p_search.add_argument("--from-date", help="From date: YYYY-MM-DD")
    p_search.add_argument("--to-date", help="To date: YYYY-MM-DD")
    p_search.add_argument("--cited-by-min", type=int, help="Minimum citation count")
    p_search.add_argument("--oa", action="store_true", help="Open access only")
    p_search.add_argument(
        "--subfield",
        help="Subfield IDs: 2207=Control, 1707=CV, 1702=AI, 2210=MechE",
    )
    p_search.add_argument(
        "--type",
        help="Work type: article, book, dataset, preprint, review, thesis",
    )
    p_search.add_argument("--language", help="Language code: en, fr, de, zh, etc.")
    p_search.add_argument(
        "--no-retracted", action="store_true", help="Exclude retracted papers"
    )
    p_search.add_argument(
        "--has-abstract", action="store_true", help="Only papers with abstracts"
    )
    p_search.add_argument(
        "--has-fulltext",
        action="store_true",
        help="Only papers with full text indexed",
    )
    p_search.add_argument(
        "--fwci-min",
        type=float,
        help="Min field-weighted citation impact (1.0 = average)",
    )
    p_search.add_argument("--related-to", help="OpenAlex work ID to find related works")
    p_search.add_argument(
        "--sort", help="Sort: cited_by_count:desc, publication_date:desc"
    )
    p_search.set_defaults(func=cmd_search)

    p_cites = sub.add_parser("cites", help="Papers that cite a given work")
    p_cites.add_argument("work_id", help="OpenAlex work ID (e.g. W2741809807)")
    p_cites.add_argument("-n", type=int, default=10)
    p_cites.add_argument("--year", help="Filter citing papers by year: 2024, >2022")
    p_cites.add_argument(
        "--cursor", default=None, help="Pagination cursor (use * for first page)"
    )
    p_cites.set_defaults(func=cmd_cites)

    p_citedby = sub.add_parser("cited-by", help="Papers referenced by a given work")
    p_citedby.add_argument("work_id", help="OpenAlex work ID")
    p_citedby.add_argument("-n", type=int, default=10)
    p_citedby.add_argument("--year", help="Filter referenced papers by year")
    p_citedby.add_argument(
        "--cursor", default=None, help="Pagination cursor (use * for first page)"
    )
    p_citedby.set_defaults(func=cmd_cited_by)

    p_author = sub.add_parser("author", help="Search authors or get author's papers")
    p_author.add_argument(
        "author_id", nargs="?", help="OpenAlex author ID (e.g. A5023888391)"
    )
    p_author.add_argument("--query", "-q", help="Search by name")
    p_author.add_argument("-n", type=int, default=10)
    p_author.set_defaults(func=cmd_author)

    p_work = sub.add_parser("work", help="Get full details for a single work")
    p_work.add_argument("work_id", help="OpenAlex ID, DOI (doi:10.xxx), or full URL")
    p_work.set_defaults(func=cmd_work)

    p_dl = sub.add_parser("download", help="Download paper PDF")
    p_dl.add_argument(
        "identifier",
        help="OpenAlex ID or DOI (e.g. 10.1109/LRA.2020.3010739)",
    )
    p_dl.add_argument("--output-dir", default="./downloads", help="Download directory")
    p_dl.add_argument("--force", action="store_true", help="Overwrite existing files")
    p_dl.set_defaults(func=cmd_download)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        msg = str(e).replace(API_KEY, "***") if API_KEY else str(e)
        print(json.dumps({"error": msg}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
