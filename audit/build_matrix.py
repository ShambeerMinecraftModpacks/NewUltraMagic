import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit'


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def main():
    audit = read('modrinth-audit.json')
    deps = read('dependency-audit.json')
    manual = {}

    def set_row(prefix, status, note, slug=None, version=None, channel='release', alternative=None):
        matches = [r for r in audit['rows'] if r['source_file'].lower().startswith(prefix.lower())]
        assert len(matches) == 1, (prefix, len(matches))
        manual[matches[0]['source_file']] = {'status': status, 'note': note, 'source_url': 'https://www.curseforge.com/minecraft/mc-mods/' + slug + '/files/all?page=1&pageSize=20&version=1.21.1' if slug else None, 'version': version, 'channel': channel, 'alternative': alternative}

    confirmed = [
        ('AE2-Things-', 'ae2-things-forge', '1.4.2-beta', 'beta', 'Нужен AE2; диапазон версий в целевом JAR ещё не проверен. Не путать с одноимённым Fabric-проектом ProjectET.'),
        ('betterfpsdist-', 'better-fps-render-distance', '1.21.1-6.1', 'release', 'Подтверждена публикация для 1.21.1; отношения зависимостей проверить по JAR.'),
        ('biomemusic-', 'biome-music', '1.21.1-4.1', 'release', 'Подтверждён кандидат, не утверждение о самой новой версии.'),
        ('buildinggadgets2-', 'building-gadgets', '1.3.9', 'release', 'Подтверждён NeoForge 1.21.1.'),
        ('Chunk-Pregenerator-', 'chunkpregenerator', 'NeoForge-1.21-4.5.4', 'release', 'Страница файла явно включает 1.21.1.'),
        ('cosmeticarmorreworked-', 'cosmetic-armor-reworked', '1.21.1-v1-neoforge', 'release', 'Подтверждён NeoForge 1.21.1.'),
        ('cupboard-', 'cupboard', '1.21.1-4.2', 'release', 'Библиотека; проверить требования потребителей.'),
        ('Disenchanting-', 'disenchantingforge', '1.21.1-2.3.0', 'release', 'Подтверждён NeoForge 1.21.1.'),
        ('ftb-library-', 'ftb-library-forge', '2101.1.37', 'release', 'Проверить зависимости и диапазоны версий FTB по целевым JAR.'),
        ('ftb-teams-', 'ftb-teams-forge', '2101.1.11', 'release', 'Связка FTB Library/Teams требует проверки диапазонов.'),
        ('ftbbackups2-', 'ftb-backups-2', '1.0.28 [NeoForge]', 'release', 'Именно 1.0.28 явно отмечена 1.21.1; 1.0.29 с меткой только 1.21 автоматически не выбрана.'),
        ('ironchest-', 'iron-chests', '1.21-neoforge-16.0.7', 'release', 'CurseForge явно включает 1.21.1, хотя Modrinth не дал точного совпадения тега.'),
        ('jerintegration-', 'jer-integration', '6.5.0', 'release', 'Нужен JER; выбранный кандидат самого JER имеет канал beta.'),
        ('lionfishapi-', 'lionfish-api', '3.1', 'release', 'Нужна Cataclysm; кандидат также найден в графе Modrinth.'),
        ('polyeng-', 'polymorphic-energistics', '0.4.1', 'release', 'CurseForge явно включает 1.21.1; проверить совместную работу с AE2 и Polymorph.'),
        ('celestisynth-', 'celestisynth-1-21-1', '1.21.1-1.3.9', 'release', 'Официальный порт, на который ссылается исходный проект. Нужны GeckoLib и PlayerAnimator; последний beta.'),
    ]
    for prefix, slug, version, channel, note in confirmed:
        set_row(prefix, 'native_release' if channel == 'release' else 'native_prerelease', note, slug, version, channel)

    alternatives = [
        ('AdaptiveTooltips-', 'better_tooltips', 'Better Tooltips 1.0.3: отдельный NeoForge-проект, замена требует согласования.'),
        ('AutoTranslation-', 'autotranslation-next', 'AutoTranslation Next 2.1.0: отдельное продолжение, не подтверждено полное равенство функций.'),
        ('canary-', 'lithium', 'Lithium имеет собственный NeoForge-релиз; замена Canary требует согласования.'),
        ('jeiintegration_', 'jei-integration-reborn', 'JEI Integration Reborn 1.0.2: отдельный проект.'),
        ('eeeabsmobs-', 'eeeabs-mobs-unofficial', 'Неофициальный порт: API предлагает 1.0.2 для 1.21.1; проверить JAR и содержимое перед включением.'),
    ]
    for prefix, slug, note in alternatives:
        set_row(prefix, 'replacement_review', note, alternative=slug)
    for prefix, slug, version, note in [
        ('alexscaves-', 'alexs-caves-unofficial-port', '1.21.1-2.0.10', 'Неофициальный порт требует Citadel (Unofficial Port), а не автоматически выбранный официальный Citadel.'),
        ('alexsmobs-', 'alexs-mobs-1-21-1-port', '1.21.1-1.22.17', 'Неофициальный порт требует Citadel (Unofficial Port); нельзя установить две библиотеки с одинаковым modId.'),
        ('Botania-', 'botania-revived', '1.0.2', 'Fork меняет внутренности и Java packages; автор предупреждает о несовместимости аддонов. Требует NeoForge 21.1.240+, Java 21, Patchouli 1.21.1-93+. Совместимость Applied Botanics не подтверждена.'),
        ('bloodmagic-', 'blood-magic-unofficial-port', 'v1.1', 'Несмотря на метку Release, автор описывает порт как ALPHA / WORK IN PROGRESS. Для стабильной сборки считать экспериментальным.'),
        ('Dungeon Now Loading-', 'dungeon-now-loading-1-21-1-port', '2.11.3 NeoForge', 'Неофициальный Tricky Trials Port. Подтверждён кандидат, не гарантируется последняя версия.'),
    ]:
        set_row(prefix, 'replacement_review', note, slug, version)
    for prefix, note, slug in [
        ('BotanicalMachinery-', 'Опубликованная версия 1.21.1 не найдена; перенос функций не решён.', 'botanical-machinery'),
        ('Ez-ae2-', 'Опубликованная версия 1.21.1 не найдена.', 'ez-ae2'),
        ('ItemProductionLib-', 'Версия 1.21.1 не найдена; возможность убрать библиотеку зависит от нового состава.', 'item-production-lib'),
        ('koremods-', 'Версия 1.21.1 не найдена; необходимость библиотеки надо пересмотреть по новому составу.', None),
        ('Mantle-', 'Опубликованная версия 1.21.1 не найдена; не переносить старую библиотеку без потребителя.', None),
        ('memoryleakfix-', 'Версия 1.21.1 не найдена; отсутствие потребности в старом исправлении ещё не доказано.', None),
        ('piercingpaxels-', 'Опубликованная версия 1.21.1 не найдена; функциональная замена не согласована.', None),
        ('starlight-', 'Версия 1.21.1 не найдена; старый Forge JAR не является кандидатом для NeoForge 1.21.1.', None),
    ]:
        set_row(prefix, 'no_verified_build', note, slug)
    set_row('traveloptics-', 'deprecated', 'Найдена только Alpha-4.4.0.1 с явной пометкой DEPRECATED DONT USE. Поддерживаемый перенос не подтверждён.', 'to-tweaks-irons-spells', 'Alpha-4.4.0.1', 'alpha')
    set_row('terramity-', 'excluded', 'Исключение уже согласовано пользователем.')
    for prefix in ['EnigmaticLegacy-', 'enigmaticaddons-']:
        set_row(prefix, 'approved_replacement', 'Согласован переход на Enigmatic Legacy Plus. Две исходные строки ведут к одному целевому моду; равенство всех функций Addons не подтверждено.', alternative='enigmaticlegacy+')

    labels = {'native_release': 'Релиз найден', 'native_prerelease': 'Только prerelease', 'replacement_review': 'Замена на согласование', 'no_verified_build': 'Версия не найдена', 'deprecated': 'Устаревшая alpha — не брать', 'excluded': 'Исключён по решению', 'approved_replacement': 'Замена согласована'}
    rows = []
    for source in audit['rows']:
        p = source.get('project')
        candidate = p['candidates']['neoforge']['preferred'] if p else None
        row = {'source_file': source['source_file'], 'source_sha1': source['source_sha1'], 'source_names': source['names'], 'identity_basis': source.get('identity_basis', 'manual_source_project_review'), 'status': 'native_release' if candidate and candidate['version_type'] == 'release' else 'native_prerelease' if candidate else 'no_verified_build', 'candidate': candidate, 'candidate_project_url': p['url'] if p else None, 'notes': [], 'required_dependencies': []}
        override = manual.get(source['source_file'])
        if override:
            row['status'] = override['status']
            row['notes'].append(override['note'])
            row['manual_evidence'] = override
            candidate = None
            row['candidate_project_url'] = override['source_url'] or row['candidate_project_url']
            if override['alternative']:
                alt = deps['alternatives'][override['alternative']]
                candidate = alt['candidates']['neoforge']['preferred']
                row['candidate_project_url'] = alt['url']
            elif override['version']:
                candidate = {'version_number': override['version'], 'version_type': override['channel'], 'game_versions': ['1.21.1'], 'loaders': ['neoforge'], 'verification_basis': 'CurseForge publication; target JAR not inspected'}
            row['candidate'] = candidate
        if candidate:
            for edge in candidate.get('dependencies', []):
                if edge['dependency_type'] == 'required':
                    dp = deps['projects'].get(edge.get('project_id'), {})
                    row['required_dependencies'].append({'name': dp.get('title', edge.get('project_id') or edge.get('version_id') or edge.get('file_name')), **edge})
        filename = source['source_file'].lower()
        if filename.startswith('applied-botanics-'):
            row['notes'].append('БЛОКЕР: требуется официальный Botania, для которого нет кандидата 1.21.1. Botania Revived не подтверждена как совместимая замена; alpha самого аддона также не согласована.')
        if filename.startswith(('chloride-', 'embeddium-', 'sodiumdynamiclights-', 'sodiumoptionsapi-')):
            row['notes'].append('Выбор рендера не завершён: граф содержит Sodium и исходный Embeddium. Проверить требования и выбрать совместимый комплект; не считать их совместную установку подтверждённой.')
        if filename.startswith('citadel-'):
            row['notes'].append('Официальный Citadel не считать автоматически совместимым с неофициальными портами Alex: они требуют отдельный Citadel (Unofficial Port).')
        if filename.startswith('lmft-'):
            row['notes'].append('API отмечает выбранный файл как совместимый с 1.21.1, но имя содержит 1.21.9. До включения проверить дескриптор; доступен также более ранний 1.0.4+1.21.')
        if filename.startswith('octolib-'):
            row['notes'].append('Проект Modrinth переименован в Shatterbyte Lib; для 1.21.1 выбран файл OctoLib. Исходная идентичность подтверждена SHA-1.')
        if row['status'] == 'native_prerelease':
            row['prerelease_approval'] = 'approved' if filename.startswith(('connector-', 'enderio-')) else 'not_yet_approved'
        row['dependency_verification'] = 'published_Modrinth_relations_only' if candidate and 'dependencies' in candidate else 'manual_notes_only; complete_target_descriptor_check_pending'
        rows.append(row)
    assert len(rows) == 139 and len({r['source_file'] for r in rows}) == 139
    assert all(not r['candidate'] or ('1.21.1' in r['candidate']['game_versions'] and 'neoforge' in r['candidate']['loaders']) for r in rows)
    assert all(not r['candidate'] or not r['candidate'].get('date_published') or r['candidate']['date_published'] <= audit['cutoff_utc'] for r in rows)
    counts = dict(collections.Counter(r['status'] for r in rows))
    report = {'checked_date': audit['checked_date'], 'scope': 'Published candidates, not an install manifest or runtime compatibility guarantee', 'counts': counts, 'rows': rows}
    (OUT / 'manual-review.json').write_text(json.dumps(manual, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'compatibility-matrix.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# UltraMagic: проверка перехода на Minecraft 1.21.1 / NeoForge', '', 'Дата проверки: 14.10.2026. Проверены все **139 исходных JAR**. Это список опубликованных кандидатов и препятствий, **не готовая совместимая сборка**. Исходник не изменён, целевые JAR не скачивались, игра не запускалась.', '', '## Результат', '', '| Категория | Исходных JAR |', '|---|---:|']
    lines += [f'| {labels[k]} | {v} |' for k, v in counts.items()]
    lines += ['', 'Числа относятся к исходным строкам: Enigmatic Legacy и Enigmatic Addons заменяются одним Enigmatic Legacy Plus. Количество целевых JAR будет другим из-за новых зависимостей и согласованных исключений.', '', '## Что мешает завершить перенос', '', '1. **Сохранить весь состав без дополнительных решений пока нельзя.** Для восьми исходных модов/библиотек не найден опубликованный кандидат; десять других требуют согласования отдельных замен. Отсутствие публикации в проверенных источниках не доказывает невозможность будущего порта.', '2. **Botania → Applied Botanics / Botanical Machinery.** У официального Botania нет найденной публикации 1.21.1. Botania Revived предупреждает об изменении внутренних пакетов и риске несовместимости аддонов. Applied Botanics 1.6.0-alpha.3 опубликован, но его обязательная зависимость остаётся нерешённой. Botanical Machinery также без найденного переноса.', '3. **Travel Optics.** Найденный порт прямо помечен DEPRECATED DONT USE. Его нельзя выдавать за пригодную замену.', '4. **Неофициальные Alex’s Caves / Mobs** требуют отдельный Citadel (Unofficial Port). Официальный Citadel 2.7.1 найден, но это не доказательство совместимости с данными портами.', '5. **Blood Magic.** Неофициальный порт с меткой Release по описанию автора остаётся ALPHA / WORK IN PROGRESS.', '6. **Рендер.** В опубликованном графе Chloride, Sodium Dynamic Lights и Sodium Options API требуют Sodium. Наличие Embeddium в исходнике не решает выбор нового комплекта. Нужна проверка JAR и запуск; совместная установка двух рендереров не утверждается.', '7. **Дополнительные prerelease:** AE2 Things, Applied Botanics, JER, Pipez, PlayerAnimator, Tempad, WTHIT. Ранее согласованы Connector и beta Ender IO; разрешение на них не распространяется автоматически на остальные.', '8. **LMFT:** API относит последнюю release к 1.21.1, но имя файла содержит 1.21.9. До включения требуется сверка целевого дескриптора; более ранний кандидат 1.0.4+1.21 тоже есть в API.', '', '## Подтверждённые уточнения', '', '- Vampirism Integrations имеет официальный релиз 1.21.1: исключать его из-за отсутствия версии неверно.', '- Для Celestisynth найден официальный порт 1.21.1-1.3.9; исходная страница ссылается на него. Нужны GeckoLib и PlayerAnimator.', '- Iron Chests и Polymorphic Energistics отмечены 1.21.1 на CurseForge, хотя фильтр Modrinth не нашёл этот тег.', '- FTB Backups 2: выбран явно отмеченный 1.21.1 файл 1.0.28, а не автоматически более новый 1.0.29 с тегом только 1.21.', '- При выборе Modrinth используется последний release, затем beta, затем alpha. Метка Release характеризует канал публикации, а не подтверждённую стабильность.', '', '## Проверка зависимостей и её границы', '', 'В графе Modrinth: **129 проектов, 107 кандидатов, 123 связи**. Найдена одна обязательная зависимость без NeoForge-кандидата: Botania для Applied Botanics. Не найдено конфликтов зафиксированных version_id или явно объявленных несовместимых кандидатов. Это не означает отсутствие реальных конфликтов.', '', 'Дополнительно к исходным проектам в графе появились Simply Tooltips, Bookshelf, Prickle, Lionfish-API и Sodium; Lionfish-API уже присутствует в исходнике, но исходный JAR не распознан по хешу Modrinth. Enigmatic Legacy Plus внесён как согласованная замена.', '', 'Граф исследовательский: он строится по найденным Modrinth-кандидатам, до полного применения ручных решений и исключений. Для кандидатов только с CurseForge использованы доступные описания; полный граф их зависимостей ещё не проверен. Пустой список зависимостей API не доказывает их отсутствие в JAR. Диапазоны версий, modId, вложенные библиотеки, mixin-конфликты, совместимость конфигов и миров проверяются на следующем этапе.', '', '## Полная матрица', '', 'Ссылка в колонке кандидата ведёт к первоисточнику. Для CurseForge указан подтверждённый кандидат, который не обязательно является самым новым. «Замена» не означает разрешение на установку. Список зависимостей ниже — только опубликованные обязательные связи API, а не полный дескриптор.', '', '| Исходный JAR | Статус | Кандидат NeoForge 1.21.1 | Зависимости / примечания |', '|---|---|---|---|']
    for row in rows:
        c = row['candidate']
        target = f"{c['version_number']} ({c['version_type']})" if c else '—'
        if c and row['candidate_project_url']:
            target = f"[{target}]({row['candidate_project_url']})"
        notes = list(row['notes'])
        required = ', '.join(str(d['name']) for d in row['required_dependencies'])
        if required:
            notes.insert(0, 'API требует: ' + required + '.')
        if row.get('prerelease_approval'):
            notes.append('Prerelease согласован.' if row['prerelease_approval'] == 'approved' else 'Prerelease ещё не согласован.')
        lines.append('| `' + row['source_file'] + '` | ' + labels[row['status']] + ' | ' + target.replace('|', '/') + ' | ' + ' '.join(notes).replace('|', '/') + ' |')
    lines += ['', '## Артефакты и воспроизводимость', '', '- `source-audit.json`: исходные JAR, SHA-256, дескрипторы, результаты CRC, конфиги и журналы.', '- `audit/modrinth-audit.json`: 139 строк; 102 точных совпадения по SHA-1, 21 ручное сопоставление проектов, 16 строк дополнительно разобраны по первоисточникам CurseForge.', '- `audit/manual-review.json`: ручные уточнения и ссылки; `audit/compatibility-matrix.json`: итоговые 139 строк.', '- `audit/dependency-audit.json`: опубликованные связи, кандидаты, альтернативы и ограничения графа.', '- `audit/modrinth-cache/`: исходные ответы API с URL и временем получения; `audit/web/`: сохранённые результаты проверок страниц.', '- `audit/check_modrinth.py`, `audit/check_dependencies.py`, `audit/build_matrix.py`: сбор и формирование отчёта. Кэш сохраняет снимок; повторный запуск с существующим кэшем не является новой проверкой актуальности.', '', '## Следующий спринт после согласования состава', '', 'Согласовать отдельно десять предложенных замен, семь дополнительных prerelease и судьбу восьми строк без найденной версии плюс Travel Optics. Затем подготовить отдельный целевой каталог, скачать разрешённые кандидаты, проверить реальные дескрипторы и диапазоны зависимостей, выбрать рендерер и проверить запуск на новом тестовом мире. Перенос существующего мира требует отдельной резервной копии и теста. Стабильность до этих проверок не заявляется.', '']
    (ROOT / 'COMPATIBILITY_1.21.1.md').write_text('\n'.join(lines), encoding='utf-8')
    original = json.loads((ROOT / 'source-audit.json').read_text(encoding='utf-8'))
    changed = []
    for mod in original['mods']:
        with (ROOT / 'UltraMagic' / 'mods' / mod['file']).open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != mod['sha256']:
                changed.append(mod['file'])
    assert not changed, changed
    verification = {'rows': len(rows), 'unique_source_files': len({r['source_file'] for r in rows}), 'all_candidates_tagged_target': True, 'publication_cutoff_checked': True, 'source_jar_sha256_unchanged': len(original['mods']), 'counts': counts}
    (OUT / 'matrix-validation.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(verification))


if __name__ == '__main__':
    main()
