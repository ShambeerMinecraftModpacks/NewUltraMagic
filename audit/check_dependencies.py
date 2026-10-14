import concurrent.futures
import json

from check_modrinth import OUT, inspect_project, request


def main():
    audit = json.loads((OUT / 'modrinth-audit.json').read_text(encoding='utf-8'))
    projects = {r['project']['id']: r['project'] for r in audit['rows'] if r.get('project')}
    selected = {}
    for pid, project in projects.items():
        neo = project['candidates']['neoforge']
        if neo['release'] or neo['latest']:
            selected[pid] = neo['preferred']
    alternatives = {}
    for slug in ['enigmaticlegacy+', 'autotranslation-next', 'lithium', 'tooltip-scroll', 'better_tooltips', 'jei-integration-reborn', 'eeeabs-mobs-unofficial']:
        try:
            p = inspect_project(slug)
            alternatives[slug] = p
            if slug == 'enigmaticlegacy+':
                projects[p['id']] = p
                selected[p['id']] = p['candidates']['neoforge']['preferred']
        except Exception as e:
            alternatives[slug] = {'error': str(e)}
    edges, errors, visited = [], {}, set()
    while True:
        frontier = [(pid, v) for pid, v in selected.items() if v and pid not in visited]
        if not frontier:
            break
        needed = set()
        for pid, version in frontier:
            visited.add(pid)
            for dependency in version.get('dependencies', []):
                edge = {'from_project': pid, 'from_version': version['id'], **dependency}
                if not edge.get('project_id') and edge.get('version_id'):
                    try:
                        edge['project_id'] = request('version/' + edge['version_id'])['project_id']
                    except Exception as e:
                        edge['lookup_error'] = str(e)
                edges.append(edge)
                if edge['dependency_type'] == 'required' and edge.get('project_id') and edge['project_id'] not in projects:
                    needed.add(edge['project_id'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            jobs = {pool.submit(inspect_project, pid): pid for pid in needed if pid not in errors}
            for future in concurrent.futures.as_completed(jobs):
                pid = jobs[future]
                try:
                    projects[pid] = future.result()
                except Exception as e:
                    errors[pid] = str(e)
        for pid in needed:
            if pid in projects:
                neo = projects[pid]['candidates']['neoforge']
                if neo['release'] or neo['latest']:
                    selected[pid] = neo['preferred']
    missing, pinned_conflicts, incompatible = [], [], []
    for edge in edges:
        pid = edge.get('project_id')
        if edge['dependency_type'] == 'required':
            if pid not in selected:
                missing.append(edge)
            elif edge.get('version_id') and edge['version_id'] != selected[pid]['id']:
                pinned_conflicts.append(edge)
        if edge['dependency_type'] == 'incompatible' and pid in selected:
            if not edge.get('version_id') or edge['version_id'] == selected[pid]['id']:
                incompatible.append(edge)
    report = {'scope': 'Modrinth candidate availability and published required dependency graph; not a solved install manifest or JAR descriptor validation', 'projects': projects, 'selected_candidates': selected, 'edges': edges, 'missing_neoforge_candidates': missing, 'pinned_version_conflicts': pinned_conflicts, 'incompatible_selected_candidates': incompatible, 'errors': errors, 'alternatives': alternatives}
    (OUT / 'dependency-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'projects': len(projects), 'candidates': len(selected), 'edges': len(edges), 'missing': len(missing), 'pinned_conflicts': len(pinned_conflicts), 'incompatible': len(incompatible), 'errors': errors}))


if __name__ == '__main__':
    main()
