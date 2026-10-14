import concurrent.futures
import hashlib
import json
import subprocess
from pathlib import Path
import urllib.request
import zipfile

from check_modrinth import request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build' / 'UltraMagic-1.21.1-NeoForge'
AUDIT = ROOT / 'audit'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def download(item):
    target = OUT / 'mods' / item['filename']
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        temporary = target.with_suffix('.part')
        subprocess.run(['curl.exe', '--fail', '--location', '--silent', '--show-error', '--retry', '2', '--max-time', '180', '--output', str(temporary), item['url']], check=True, capture_output=True)
        data = temporary.read_bytes()
        for alg, expected in item.get('hashes', {}).items():
            assert hashlib.new(alg, data).hexdigest() == expected, item['filename']
        temporary.replace(target)
    data = target.read_bytes()
    for alg, expected in item.get('hashes', {}).items():
        assert hashlib.new(alg, data).hexdigest() == expected, item['filename']
    with zipfile.ZipFile(target) as jar:
        assert jar.testzip() is None, item['filename']
    return {**item, 'sha256': hashlib.sha256(data).hexdigest(), 'sha512': hashlib.sha512(data).hexdigest(), 'sha1': hashlib.sha1(data).hexdigest(), 'size': len(data)}


def main():
    matrix = json.loads((AUDIT / 'compatibility-matrix.json').read_text(encoding='utf-8'))
    deps = json.loads((AUDIT / 'dependency-audit.json').read_text(encoding='utf-8'))
    selected, excluded, pending = {}, [], []
    for row in matrix['rows']:
        reason = None
        if row['status'] not in ['native_release', 'native_prerelease', 'approved_replacement']:
            reason = '; '.join(row['notes'])
        if row['source_file'].lower().startswith('applied-botanics-'):
            reason = 'Нет совместимой обязательной зависимости Botania; сторонняя замена не согласована.'
        if row['source_file'].lower().startswith('embeddium-'):
            reason = 'Выбран Sodium как обязательная зависимость актуальных Chloride и Sodium Dynamic Lights. Два рендерера вместе не установлены.'
        if reason:
            excluded.append({'source_file': row['source_file'], 'reason': reason, 'status': row['status']})
            continue
        c = row['candidate']
        if not c.get('files'):
            if row['source_file'].lower().startswith('lionfishapi-'):
                p = next(p for p in deps['projects'].values() if p['slug'] == 'lionfish-api')
                c = p['candidates']['neoforge']['preferred']
            else:
                pending.append(row)
                continue
        if row['source_file'].lower().startswith('lmft-'):
            versions = request('project/' + c['project_id'] + '/version')
            c = next(v for v in versions if v['version_number'] == '1.0.4+1.21' and 'neoforge' in v['loaders'])
        selected[c['project_id']] = c
    frontier = list(selected)
    for pid in frontier:
        for d in selected[pid].get('dependencies', []):
            if d['dependency_type'] != 'required':
                continue
            dp = d.get('project_id')
            pinned = request('version/' + d['version_id']) if d.get('version_id') else None
            if pinned:
                dp = pinned['project_id']
            if dp and dp not in selected:
                c = pinned or deps['projects'][dp]['candidates']['neoforge']['preferred']
                assert c, ('Missing dependency', dp)
                selected[dp] = c
                frontier.append(dp)
    downloads = []
    for pid, v in selected.items():
        primary = next((f for f in v['files'] if f.get('primary')), v['files'][0])
        downloads.append({'project_id': pid, 'version_id': v['id'], 'version': v['version_number'], 'channel': v['version_type'], **primary})
    extra = AUDIT / 'curseforge-downloads.json'
    if extra.exists():
        downloads.extend(json.loads(extra.read_text(encoding='utf-8')))
    results, errors = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {pool.submit(download, d): d for d in downloads}
        for job in concurrent.futures.as_completed(jobs):
            try:
                results.append(job.result())
            except Exception as error:
                errors.append({'file': jobs[job]['filename'], 'error': str(error)})
    save(AUDIT / 'pack-downloads.json', sorted(results, key=lambda r: r['filename'].lower()))
    save(AUDIT / 'pack-excluded.json', excluded)
    save(AUDIT / 'pack-pending.json', pending)
    save(AUDIT / 'pack-download-errors.json', errors)
    print(json.dumps({'downloaded': len(results), 'excluded': len(excluded), 'pending_cf': len(pending), 'errors': len(errors), 'first_error': errors[:1]}))


if __name__ == '__main__':
    main()
