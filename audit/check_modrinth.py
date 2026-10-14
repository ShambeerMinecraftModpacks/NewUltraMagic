import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit'
CACHE = OUT / 'modrinth-cache'
CACHE.mkdir(parents=True, exist_ok=True)
API = 'https://api.modrinth.com/v2/'
HEADERS = {'User-Agent': 'NewUltraMagic-CompatibilityAudit/1.0', 'Content-Type': 'application/json'}
CUTOFF = '2026-10-14T20:59:59Z'


def request(endpoint, data=None):
    key = hashlib.sha256((endpoint + json.dumps(data, sort_keys=True)).encode()).hexdigest()
    path = CACHE / (key + '.json')
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))['response']
    for attempt in range(4):
        try:
            req = urllib.request.Request(API + endpoint, headers=HEADERS, data=None if data is None else json.dumps(data).encode())
            with urllib.request.urlopen(req, timeout=35) as response:
                result = json.load(response)
            path.write_text(json.dumps({'url': API + endpoint, 'request': data, 'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'response': result}, ensure_ascii=False, indent=2), encoding='utf-8')
            return result
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 3:
                raise
            time.sleep(min(10, int(error.headers.get('Retry-After', 3))))
        except urllib.error.URLError:
            if attempt == 3:
                raise
            time.sleep(2)


def source_info(mod):
    names, ids, links = [], [], []
    for key, desc in mod['descriptors'].items():
        if key.endswith('.toml'):
            for item in desc.get('mods', []):
                names.append(item.get('displayName', item.get('modId', '')))
                ids.append(item.get('modId', ''))
                links.extend([item.get('displayURL', ''), desc.get('issueTrackerURL', '')])
        elif key == 'fabric.mod.json':
            names.append(desc.get('name', desc.get('id', '')))
            ids.append(desc.get('id', ''))
            links.extend(desc.get('contact', {}).values())
    return {'names': names, 'ids': ids, 'source_links': sorted(set(x for x in links if x))}


def eligible(versions, loader):
    return sorted([v for v in versions if loader in v['loaders'] and '1.21.1' in v['game_versions'] and v['date_published'] <= CUTOFF], key=lambda v: v['date_published'], reverse=True)


def candidate(version):
    return {k: version.get(k) for k in ['id', 'project_id', 'name', 'version_number', 'version_type', 'date_published', 'game_versions', 'loaders', 'dependencies', 'files']}


def inspect_project(project_id):
    p = request('project/' + urllib.parse.quote(project_id, safe=''))
    versions = request('project/' + p['id'] + '/version?' + urllib.parse.urlencode({'game_versions': json.dumps(['1.21.1'])}))
    result = {'id': p['id'], 'slug': p['slug'], 'title': p['title'], 'url': 'https://modrinth.com/mod/' + p['slug'], 'source_url': p.get('source_url'), 'issues_url': p.get('issues_url'), 'license': p.get('license'), 'game_versions': p.get('game_versions'), 'loaders': p.get('loaders'), 'candidates': {}}
    for loader in ['neoforge', 'fabric', 'forge']:
        vs = eligible(versions, loader)
        stable = [v for v in vs if v['version_type'] == 'release']
        beta = [v for v in vs if v['version_type'] == 'beta']
        preferred = (stable or beta or vs)
        result['candidates'][loader] = {'latest': candidate(vs[0]) if vs else None, 'release': candidate(stable[0]) if stable else None, 'preferred': candidate(preferred[0]) if preferred else None, 'count': len(vs)}
    return result


def run():
    audit = json.loads((ROOT / 'source-audit.json').read_text(encoding='utf-8'))
    hashes = {}
    for m in audit['mods']:
        with (ROOT / 'UltraMagic' / 'mods' / m['file']).open('rb') as stream:
            hashes[m['file']] = hashlib.file_digest(stream, 'sha1').hexdigest()
    matches = request('version_files', {'hashes': list(hashes.values()), 'algorithm': 'sha1'})
    overrides_path = OUT / 'project-overrides.json'
    overrides = json.loads(overrides_path.read_text(encoding='utf-8')) if overrides_path.exists() else {}
    rows = []
    for mod in audit['mods']:
        row = {'source_file': mod['file'], 'source_sha1': hashes[mod['file']], **source_info(mod)}
        match = matches.get(hashes[mod['file']])
        override = overrides.get(mod['file'])
        if override:
            row['project_id'] = override['project']
            row['identity_basis'] = override['basis']
        elif match:
            row['project_id'] = match['project_id']
            row['source_version_id'] = match['id']
            row['identity_basis'] = 'exact_source_jar_sha1'
        rows.append(row)
    projects = {}
    failures = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {pool.submit(inspect_project, p): p for p in sorted({r['project_id'] for r in rows if r.get('project_id')})}
        for task in concurrent.futures.as_completed(jobs):
            key = jobs[task]
            try:
                projects[key] = task.result()
            except Exception as e:
                failures[key] = str(e)
    for row in rows:
        if row.get('project_id') in projects:
            row['project'] = projects[row['project_id']]
        if row.get('project_id') in failures:
            row['error'] = failures[row['project_id']]
    for row in rows:
        if not row.get('project_id'):
            query = row['names'][0] if row['names'] else row['source_file'].split('-')[0]
            try:
                hits = request('search?' + urllib.parse.urlencode({'query': query, 'limit': 5, 'facets': json.dumps([['project_type:mod']])}))['hits']
                row['search_candidates'] = [{k: hit.get(k) for k in ['project_id', 'slug', 'title', 'author', 'versions']} for hit in hits]
            except Exception as e:
                row['search_error'] = str(e)
    result = {'target': {'minecraft': '1.21.1', 'loader': 'neoforge'}, 'checked_date': '2026-10-14', 'cutoff_utc': CUTOFF, 'rows': rows}
    (OUT / 'modrinth-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    unresolved = [{k: r.get(k) for k in ['source_file', 'names', 'source_links', 'search_candidates', 'error']} for r in rows if not r.get('project')]
    (OUT / 'unresolved.json').write_text(json.dumps(unresolved, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'total': len(rows), 'exact_hash_matches': len(matches), 'resolved': len(rows)-len(unresolved), 'unresolved': len(unresolved), 'failures': failures}))


if __name__ == '__main__':
    run()
