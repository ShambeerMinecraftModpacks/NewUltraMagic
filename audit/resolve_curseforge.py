import concurrent.futures
import json
import subprocess
import urllib.parse

from assemble_pack import AUDIT, save


def resolve(row):
    slug = row['candidate_project_url'].split('/mc-mods/')[1].split('/')[0]
    path = AUDIT / ('cfwidget-' + slug + '.json')
    if not path.exists():
        subprocess.run(['curl.exe', '--fail', '--location', '--silent', '--show-error', '--max-time', '60', '--output', str(path), 'https://api.cfwidget.com/minecraft/mc-mods/' + slug], check=True, capture_output=True)
    project = json.loads(path.read_text(encoding='utf-8'))
    versions = [f for f in project['files'] if '1.21.1' in f['versions'] and 'NeoForge' in f['versions'] and f['uploaded_at'] <= '2026-10-14T20:59:59Z']
    expected = row['candidate']['version_number'].replace(' [NeoForge]', '').replace('NeoForge-', '')
    matched = [f for f in versions if expected.lower() in f['name'].lower() or expected.lower() in f['display'].lower()]
    assert matched, (slug, expected, [f['name'] for f in versions[:3]])
    f = sorted(matched, key=lambda v: v['uploaded_at'], reverse=True)[0]
    fid = str(f['id'])
    return {'source_file': row['source_file'], 'provider': 'curseforge', 'project_id': project['id'], 'file_id': f['id'], 'filename': f['name'], 'version': row['candidate']['version_number'], 'channel': f['type'], 'url': 'https://mediafilez.forgecdn.net/files/' + fid[:-3] + '/' + str(int(fid[-3:])) + '/' + urllib.parse.quote(f['name']), 'source_url': f['url'], 'catalog_metadata': 'CFWidget; binary from official CurseForge CDN', 'expected_size': f['filesize']}


def main():
    rows = json.loads((AUDIT / 'pack-pending.json').read_text(encoding='utf-8'))
    result, errors = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {pool.submit(resolve, r): r for r in rows}
        for job in concurrent.futures.as_completed(jobs):
            try:
                result.append(job.result())
            except Exception as error:
                errors.append({'source': jobs[job]['source_file'], 'error': str(error)})
    save(AUDIT / 'curseforge-downloads.json', result)
    print(json.dumps({'resolved': len(result), 'errors': errors, 'files': [r['filename'] for r in result]}))


if __name__ == '__main__':
    main()
