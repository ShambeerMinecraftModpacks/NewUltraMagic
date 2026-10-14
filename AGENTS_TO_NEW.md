# Журнал пересборки NEWULTRAMAGIC

Назначение: передача контекста следующему агенту. Каждая запись содержит дату, действие, результат и ограничения. Полные логи не дублируются: указываются только проверяемые выводы и пути к источникам.

## 2026-10-13 — Запрос пользователя

> Привет, хочу пересобрать эту сборку на более новую версию, но 2 условия
> 1 - ВСЕ МОДЫ ЕСТЬ
> 2 - ВСЕ МОДЫ ОЧЕНЬ СТАБИЛЬНЫ
> Собери пожалуйста, вот исходник `G:\.minecraftx\instances\UltraMagic`

Рабочая папка новой сборки: `G:\.minecraftx\instances\NEWULTRAMAGIC`.

## 2026-10-13 — Пользовательское требование к журналу

> Все результаты и диалоги записывай в файл AGENTS_TO_NEW.md ОБЯЗАТЕЛЬНО КАЖДЫЙ ШАГ, я потом передам другому агенту его

Принято. Этот файл ведётся как непрерывный журнал. Уточнение интерпретации: сохраняются сообщения и структурированные результаты каждого шага; многомегабайтные необработанные журналы запуска, списки файлов и сетевые ответы не копируются целиком, но фиксируются их источники и существенные выводы.

## 2026-10-13 — Проверка присланного AGENTS.md

Прочитан: `E:\work\vite-monkey\AGENTS.md`.

Это руководство для другого репозитория — Vite/Monkey userscripts. Оно не относится к Minecraft-инстансам `UltraMagic` / `NEWULTRAMAGIC` и не задаёт правила их изменения. Учитывается лишь как приложенный пользователем документ, а не как инструкция рабочей папки.

## 2026-10-13 — Инвентаризация исходника

Источник: `G:\.minecraftx\instances\UltraMagic`.

- В `instance.json` указано: Minecraft `1.20.1`, Forge `47.4.0`, Java Edition, лимит памяти `16384` MiB.
- В папке `mods` — около 160 обычных jar-модов, а также кэш Connector.
- Сборка содержит сочетание Forge-модов с Fabric-модами, запускаемыми через Sinytra Connector. В частности, в метаданных названы `AdaptiveTooltips` и `AutoTranslation` для Fabric, а в `mods\.connector` присутствуют преобразованные jar.
- В `logs\latest.log` имеются повторяющиеся предупреждения Werewolves: невозможно получить capability игрока; мод прямо сообщает, что это может нарушить функциональность. Это нельзя считать признаком стабильной базы для механического обновления.
- Метаданные экспортера: `G:\.minecraftx\instances\UltraMagic\modpack-metadata.json`.

## 2026-10-13 — Предварительная проверка современных портов ключевых модов

Проверены публичные страницы CurseForge (состояние на 2026-10-13):

- `Alex's Caves`: существуют неофициальные порты для Minecraft `1.21.1` на NeoForge; это замена оригинального jar, поэтому требует особенно тщательной проверки совместимости.
- `Vampirism`: существует релиз `1.21.1` для NeoForge (`1.10.13`, 2026-09-05).
- `Ender IO`: существует ветка `1.21.1` для NeoForge, но последние сборки имеют статус beta (`v8.2.12-beta`). Она не удовлетворяет критерию «очень стабильный» без собственного длительного тестирования.

Вывод на данном этапе: реальной целью потенциально может быть Minecraft `1.21.1` + NeoForge, но перенос всех модов и их конфигураций нельзя объявлять стабильным до полной матрицы совместимости и запуска. Самая свежая версия не равна самой стабильной.

## 2026-10-13 — Чтение дескрипторов всех jar

Выполнен локальный анализ `META-INF/mods.toml`, `fabric.mod.json` и `quilt.mod.json` каждого jar из `G:\.minecraftx\instances\UltraMagic\mods`. Это надёжнее, чем выводить совместимость по именам файлов.

Существенные результаты:

- В сборке действительно есть и Forge-моды, и Fabric-артефакты. `AdaptiveTooltips-1.3.0-fabric-1.20.2.jar` имеет Fabric-дескриптор. Для него в исходнике есть преобразованные jar в `mods\.connector`.
- Присутствуют экспериментальные/предрелизные компоненты: `better-clouds` помечен `beta`; `EnderIO` — `6.2.16-beta`; `PresenceFootsteps` — `beta.1`; `Connector` — `beta.47`.
- Ключевые взаимосвязанные группы: Create + Create Addition + Create New Age; AE2 + AE2 Things + Applied Botanics + AE2WTLib; Vampirism + Werewolves + GodlyVampirism + Vampirism Integrations + Vampires Need Umbrellas; Alex's Caves + Alex's Mobs + Travel Optics; Botania + Botanical Machinery.
- `Travel Optics` жёстко заявляет зависимости от `Irons Spellbooks`, `Cataclysm`, `Alex's Caves` и `Apothic Attributes`; перенос этой группы нельзя рассматривать как независимые обновления.
- В `mods` есть артефакты без обычного дескриптора (`Connector`, `koremods-modlauncher`, `kotlinforforge`); это ожидаемо для служебных библиотек/рантайма и само по себе не означает ошибку.

Полный исходный список jar сохранён в метаданных источника: `G:\.minecraftx\instances\UltraMagic\modpack-metadata.json` (раздел `emittedFiles`), чтобы следующий агент мог повторно извлечь точные версии.

## 2026-10-13 — Аудит журналов и отчётов о сбоях

Проверены `logs\latest.log` и отчёты `crash-reports` исходной сборки.

- Фактическое количество jar в `mods`: `139`, суммарный размер — около `0.69 GiB`.
- Новый отчёт `crash-2026-10-13_18.42.03-fml.txt` фиксирует именно неуспешный запуск: `Travel Optics 6.1.0` не видит обязательный `attributeslib >= 1.3.7`, хотя файл `ApothicAttributes-1.20.1-1.3.7.jar` лежит в папке. Это конфликт разрешения зависимостей, а не просто предупреждение.
- В `latest.log` успешный запуск позднее доходит до мира, но с ошибками контента: отсутствует model loader `athena` у моделей Ender IO; повреждённые JSON у Terramity; невалидные/отсутствующие модели у Mowzie's Mobs, Born in Chaos, Relics и Travel Optics; ошибка инициализации JEI-плагина Just Enough Resources; Embeddium сообщает об изменении своих внутренних классов сторонним модом.
- Предыдущий клиентский crash report (2026-04-08) сообщает об ошибке JSON и отдельно предупреждает проверять Sinytra Connector как причину.
- Есть и несвязанные сетевые ошибки авторизации Mojang/проверок обновлений; они не должны переноситься в решение о совместимости модов.

Итог: исходник нельзя копировать как «стабильную базу». Новая сборка должна быть чистой, с нативными загрузчиками модов, без Connector и с проверкой запуска с нуля.

## 2026-10-13 — Проверка непреодолимых ограничений версии Minecraft

Проведён поиск опубликованных версий ключевых модов на CurseForge, актуальность проверена 2026-10-13.

| Мод из исходника | Minecraft 1.21.1 / NeoForge | Вывод |
| --- | --- | --- |
| Vampirism | Есть официальный релиз `1.10.13` | Можно переносить после проверки связок. |
| Godly Vampirism | Есть официальный релиз `1.10.0` | Можно переносить. |
| Alex's Caves | Есть сторонние NeoForge-порты | Не является официальным продолжением, требует отдельной проверки. |
| Ender IO | Есть только beta-ветка `v8.2.12-beta` | Не соответствует строгому критерию стабильности без длительного тестирования. |
| Enigmatic Legacy | Официальный последний релиз — Forge 1.20.1 | Существующий `Enigmatic Legacy Plus` для 1.21.1 — другой проект, не идентичный мод. |
| Vampirism Integrations | Последняя официальная версия — Forge 1.20.1 | Нет совместимой версии для 1.21.1. |
| Terramity | Последняя и единственная актуальная ветка — Forge 1.20.1, `0.9.8` | Жёсткий блокер переноса при требовании сохранить именно все моды. |

Главный факт: **сохранить каждый исходный мод и одновременно повысить версию Minecraft выше 1.20.1 невозможно.** Как минимум Terramity и Enigmatic Legacy официально не выпущены для более новых версий; замены/неофициальные порты нарушат условие «все моды есть» и не дадут основания заявлять «очень стабильны».

Источники для повторной проверки: страницы CurseForge `Terramity`, `Enigmatic Legacy`, `Vampirism`, `Godly Vampirism`, `Vampirism Integrations`, `Ender IO`, а также страница неофициального NeoForge-порта `Alex's Caves`.

## 2026-10-13 — Требуется решение пользователя

Ни один технически честный вариант не удовлетворяет всем трём формулировкам одновременно: «новее Minecraft 1.20.1», «сохранить все исходные моды» и «все моды очень стабильны».

Вопрос пользователю: выбрать строгую сохранность всех модов с чистой и стабильной пересборкой на Minecraft 1.20.1 или разрешить переход на Minecraft 1.21.1 / NeoForge с удалением либо заменой модов-блокеров (`Terramity`, `Enigmatic Legacy`, `Vampirism Integrations`) и обязательной полной проверкой связок. До ответа массовое копирование и скачивание модов не выполняются.

## 2026-10-13 — Решение пользователя

> коннекртор нужен, готов отказаться от terramity, enigmatic legacy+ качай бету

Принятое рабочее толкование:

- Цель — Minecraft `1.21.1` + NeoForge.
- Sinytra Connector сохраняется по явному требованию пользователя.
- Исключаются `Terramity` и `Enigmatic Legacy` (в том числе его аддоны, зависящие от него).
- Для Ender IO разрешена beta-версия для 1.21.1.
- Перед скачиванием будет подтверждён статус `Vampirism Integrations`, потому что для 1.21.1 официального файла нет. Он не будет автоматически заменён несовместимым jar.

## 2026-10-13 — Уточнение пользователя: Enigmatic Legacy Plus

> стоять, Enigmatic Legacy + есть ЕГО ДОБАВЛЯЕМ

Уточнение принято до начала скачивания: в сборку будет включён `Enigmatic Legacy Plus` для Minecraft 1.21.1 / NeoForge как современная замена оригинальному `Enigmatic Legacy`.

Оригинальный `Enigmatic Legacy` и аддон `Enigmatic Addons` не будут переноситься: они собраны для Forge 1.20.1 и требуют старый мод. В будущем манифесте это будет явно отмечено как замена, а не как сохранение того же бинарного мода.

## 2026-10-13 — Проверка базы NeoForge и Connector

- В локальной установке уже есть независимая стабильная сборка `All the Mods 10-6.6` на Minecraft `1.21.1`, NeoForge `21.1.224`. Она будет использована только как *read-only* локальный источник уже скачанных совпадающих модов: исходный `UltraMagic` не изменяется, а копирование в новую сборку будет выполняться только после составления манифеста.
- Сопоставлены дескрипторы jar исходника с дескрипторами этой NeoForge-сборки. Для `57` модов из исходника уже есть соответствующая версия для 1.21.1 в локальном кэше: в их числе AE2, Create, Cataclysm, Ender IO beta, Embeddium, Forge/NeoForge-библиотеки, Irons Spellbooks, EvilCraft, Tombstone, Sophisticated Backpacks, Vampirism-зависимые библиотеки и другие.
- Sinytra Connector поддерживает Minecraft `1.21.1` на NeoForge, но официальная ветка — `2.0.0 beta` (на момент проверки актуальна beta 17). Пользователь явно потребовал Connector, поэтому это принятое исключение из критерия только stable-релизов.
- Для корректной работы Connector на 1.21.1 также будет подобрана совместимая версия Connector Extras / Forgified Fabric API, только если действительно понадобится Fabric-only мод.

Следующий шаг: составить полный манифест из трёх групп — копируемые нативные моды, загружаемые 1.21.1-моды и исключения/замены. Никакие jar пока не скопированы и не скачаны.

## 2026-10-13 — Результат сетевой проверки Modrinth, попытка 1

Официальный API Modrinth доступен. Проверочный запрос для Applied Energistics 2 вернул проект `ae2` с поддержкой NeoForge и Minecraft `1.21.1`.

Первый пакетный скрипт поиска сформировал некорректный вывод для части ответов из-за отсутствующих полей у некоторых результатов, поэтому его данные не используются для выбора файлов. Успешно подтверждено: `Connector Extras` имеет версию для `1.21.1` / NeoForge. Следующий запрос будет исправлен так, чтобы выбирать только однозначные результаты по project ID/slug и запрашивать конкретный список версий.

Никакие jar по сети на данном шаге не скачивались.

## 2026-10-13 — Требование переносимого анализа

Сообщения пользователя:

> Добавь в файл анализа файлы старой сборки, для удобного переноса чата
>
> изначально делай этот файл анализа легко переносимым

Принято. `AGENTS_TO_NEW.md` — переносимый handoff-документ в UTF-8 Markdown. Его правила:

- пути далее указываются относительно `SOURCE = G:\.minecraftx\instances\UltraMagic` или `TARGET = G:\.minecraftx\instances\NEWULTRAMAGIC`;
- моды будут записываться точными именами jar, а изменения — как «исключён», «заменён», «скопирован» или «загружен»;
- крупные бинарные файлы и полные runtime-логи не дублируются, но для них фиксируются путь, число файлов, размер и причина переноса/исключения;
- каждое внешнее решение привязывается к сообщению пользователя и дате.

Следующим шагом в этот документ будет внесён переносимый инвентарь исходной сборки: верхний уровень, все jar из `mods`, ресурс-паки и группы конфигураций.

## 2026-10-13 — Переносимый инвентарь файлов исходной сборки

Источник этого раздела: `SOURCE = G:\.minecraftx\instances\UltraMagic`. В таблицах пути записаны относительно `SOURCE`. Состояние фиксировано до начала миграции; этот инвентарь не означает, что устаревшие 1.20.1-конфигурации допустимо копировать в 1.21.1 без проверки.

Первичная генерация списка прервалась из-за экранирования Markdown в PowerShell. Ошибка затронула только формирование отчёта, не исходную и не новую сборку; ниже список будет добавлен повторно корректно.

+### Моды (`mods`, 139 jar)
- `mods/AdaptiveTooltips-1.3.0-fabric-1.20.2.jar` — 153757 bytes
- `mods/AE2-Things-1.2.1.jar` — 70813 bytes
- `mods/ae2wtlib-15.3.3-forge.jar` — 229518 bytes
- `mods/alexscaves-2.0.2.jar` — 74871657 bytes
- `mods/alexsmobs-1.22.9.jar` — 26350793 bytes
- `mods/AmbientSounds_FORGE_v6.3.1_mc1.20.1.jar` — 52449474 bytes
- `mods/ApothicAttributes-1.20.1-1.3.7.jar` — 227511 bytes
- `mods/applied-botanics-forge-1.5.1.jar` — 247239 bytes
- `mods/appliedenergistics2-forge-15.4.10.jar` — 8495956 bytes
- `mods/architectury-9.2.14-forge.jar` — 580602 bytes
- `mods/artifacts-forge-9.5.16.jar` — 850457 bytes
- `mods/AttributeFix-Forge-1.20.1-21.0.4.jar` — 19471 bytes
- `mods/AutoTranslation-1.2.1+mc1.20.2-forge.jar` — 114412 bytes
- `mods/badpackets-forge-0.4.3.jar` — 27919 bytes
- `mods/balm-forge-1.20.1-7.3.37-all.jar` — 590487 bytes
- `mods/better-clouds-1.3.37-beta+1.20.1-forge.rev.e63efe2.jar` — 969149 bytes
- `mods/bettercombat-forge-1.9.0+1.20.1.jar` — 1054339 bytes
- `mods/betterfpsdist-1.20.1-6.0.jar` — 19917 bytes
- `mods/biomemusic-1.20.1-3.5.jar` — 35324 bytes
- `mods/bloodmagic-1.20.1-3.3.5-47.jar` — 14953384 bytes
- `mods/born_in_chaos_[Forge]1.20.1_1.7.3.jar` — 11824309 bytes
- `mods/Botania-1.20.1-450-FORGE.jar` — 12195508 bytes
- `mods/BotanicalMachinery-1.20.1-3.0.7.jar` — 232301 bytes
- `mods/buildinggadgets2-1.0.8.jar` — 3833683 bytes
- `mods/caelus-forge-3.2.0+1.20.1.jar` — 40125 bytes
- `mods/canary-mc1.20.1-0.3.3.jar` — 594191 bytes
- `mods/CarbonConfig-1.20-1.2.8.1.jar` — 1080142 bytes
- `mods/celestisynth-1.20.1-1.3.3-all.jar` — 2664846 bytes
- `mods/chloride-FORGE-mc1.20.1-v1.7.4.jar` — 956079 bytes
- `mods/Chunk-Pregenerator-1.20-4.4.4.jar` — 694278 bytes
- `mods/citadel-2.6.2-1.20.1.jar` — 3185379 bytes
- `mods/clean_tooltips-1.0-forge-1.20.1.jar` — 26409 bytes
- `mods/cloth-config-11.1.136-forge.jar` — 1181413 bytes
- `mods/Clumps-forge-1.20.1-12.0.0.4.jar` — 20299 bytes
- `mods/Connector-1.0.0-beta.47+1.20.1.jar` — 5043863 bytes
- `mods/ConnectorExtras-1.11.2+1.20.1.jar` — 182464 bytes
- `mods/Controlling-forge-1.20.1-12.0.2.jar` — 115280 bytes
- `mods/cosmeticarmorreworked-1.20.1-v1a.jar` — 88752 bytes
- `mods/create-1.20.1-6.0.8.jar` — 19170905 bytes
- `mods/create-new-age-1.1.7d+forge-mc1.20.1.jar` — 1155686 bytes
- `mods/createaddition-1.20.1-1.3.3.jar` — 1577313 bytes
- `mods/CreativeCore_FORGE_v2.12.32_mc1.20.1.jar` — 1158417 bytes
- `mods/cupboard-1.20.1-2.7.jar` — 25983 bytes
- `mods/curios-forge-5.14.1+1.20.1.jar` — 398066 bytes
- `mods/CyclopsCore-1.20.1-1.21.3.jar` — 911883 bytes
- `mods/Disenchanting-forge-1.20.1-2.2.4.jar` — 81717 bytes
- `mods/Dungeon Now Loading-forge-1.20.1-2.11.jar` — 66861448 bytes
- `mods/eeeabsmobs-1.20.1-0.97-Fix.jar` — 28960284 bytes
- `mods/embeddium-0.3.31+mc1.20.1.jar` — 1320675 bytes
- `mods/EnchantingInfuser-v8.0.3-1.20.1-Forge.jar` — 177437 bytes
- `mods/EnderIO-1.20.1-6.2.16-beta-all.jar` — 8086268 bytes
- `mods/enigmaticaddons-1.2.5.jar` — 1006916 bytes
- `mods/EnigmaticLegacy-2.30.1.jar` — 7276807 bytes
- `mods/entity_model_features_1.20.1-forge-3.0.7.jar` — 661640 bytes
- `mods/entity_texture_features_1.20.1-forge-7.0.6.jar` — 951154 bytes
- `mods/entityculling-forge-1.9.4-mc1.20.1.jar` — 1568324 bytes
- `mods/EvilCraft-1.20.1-1.2.52.jar` — 2671888 bytes
- `mods/ExtraSoundsNext-forge-1.20.1-1.4.jar` — 220040 bytes
- `mods/Ez-ae2-universal.jar` — 30524 bytes
- `mods/fabric-api-0.92.6+1.11.14+1.20.1.jar` — 3065813 bytes
- `mods/ferritecore-6.0.1-forge.jar` — 123034 bytes
- `mods/forbidden_arcanus-1.20.1-2.2.6.jar` — 2738939 bytes
- `mods/FpsReducer2-forge-1.20.1-2.5.1.jar` — 125660 bytes
- `mods/ftb-library-forge-2001.2.13.jar` — 780558 bytes
- `mods/ftb-teams-forge-2001.3.2.jar` — 252579 bytes
- `mods/ftbbackups2-forge-1.20-1.0.23.jar` — 1954591 bytes
- `mods/fzzy_config-0.7.4+1.20.1+forge.jar` — 2353402 bytes
- `mods/geckolib-forge-1.20.1-4.8.2.jar` — 1038979 bytes
- `mods/GodlyVampirism-1.20.1-1.10.0.jar` — 7299 bytes
- `mods/guideme-20.1.14.jar` — 9413204 bytes
- `mods/Iceberg-1.20.1-forge-1.1.25.jar` — 134551 bytes
- `mods/ImmediatelyFast-Forge-1.5.3+1.20.4.jar` — 426980 bytes
- `mods/immersive_aircraft-1.4.0+1.20.1-forge.jar` — 2428368 bytes
- `mods/ironchest-1.20.1-14.4.4.jar` — 311290 bytes
- `mods/ironfurnaces-1.20.1-4.1.8.jar` — 612921 bytes
- `mods/irons_spellbooks-1.20.1-3.4.0.11.jar` — 8784756 bytes
- `mods/ItemProductionLib-1.20.1-1.0.2a-all.jar` — 171785 bytes
- `mods/jei-1.20.1-forge-15.20.0.128.jar` — 1409508 bytes
- `mods/jeiintegration_1.20.1-10.0.0.jar` — 26940 bytes
- `mods/jerintegration-5.5.0.jar` — 31778 bytes
- `mods/JustEnoughResources-1.20.1-1.4.0.247.jar` — 276231 bytes
- `mods/koremods-modlauncher-1.0.0.jar` — 5889330 bytes
- `mods/kotlinforforge-4.12.0-all.jar` — 7442998 bytes
- `mods/L_Enders_Cataclysm-3.16.jar` — 127993805 bytes
- `mods/LegendaryTooltips-1.20.1-forge-1.4.5.jar` — 55258 bytes
- `mods/libIPN-forge-1.20-4.0.2.jar` — 693301 bytes
- `mods/LibX-1.20.1-5.0.14.jar` — 1258082 bytes
- `mods/lionfishapi-2.4-Fix.jar` — 162767 bytes
- `mods/lmft-1.0.4+1.20.1-forge.jar` — 178327 bytes
- `mods/lodestone-1.20.1-1.6.4.1.jar` — 670934 bytes
- `mods/lootr-forge-1.20-0.7.35.94.jar` — 463485 bytes
- `mods/malum-1.20.1-1.6.7.jar` — 26296223 bytes
- `mods/Mantle-1.20.1-1.11.79.jar` — 1480444 bytes
- `mods/memoryleakfix-forge-1.17+-1.1.5.jar` — 227925 bytes
- `mods/modernfix-forge-5.25.2+mc1.20.1.jar` — 895444 bytes
- `mods/MouseTweaks-forge-mc1.20.1-2.25.1.jar` — 76237 bytes
- `mods/mowziesmobs-1.7.3.jar` — 35239406 bytes
- `mods/NaturesCompass-1.20.1-1.11.2-forge.jar` — 215119 bytes
- `mods/noisium-forge-2.3.0+mc1.20-1.20.1.jar` — 218152 bytes
- `mods/OctoLib-FORGE-0.5.0.1+1.20.1.jar` — 424035 bytes
- `mods/Patchouli-1.20.1-84.1-FORGE.jar` — 642711 bytes
- `mods/piercingpaxels-1.0.12.jar` — 346792 bytes
- `mods/pipez-forge-1.20.1-1.2.26.jar` — 431615 bytes
- `mods/Placebo-1.20.1-8.6.3.jar` — 282474 bytes
- `mods/player-animation-lib-forge-1.0.2-rc1+1.20.jar` — 181437 bytes
- `mods/polyeng-forge-0.1.1-1.20.1.jar` — 15469 bytes
- `mods/polylib-forge-2000.0.3-build.143.jar` — 1343694 bytes
- `mods/polymorph-forge-0.49.10+1.20.1.jar` — 299601 bytes
- `mods/PresenceFootsteps-1.20.1-1.9.1-beta.1.jar` — 7080698 bytes
- `mods/Prism-1.20.1-forge-1.0.5.jar` — 52205 bytes
- `mods/PuzzlesLib-v8.1.33-1.20.1-Forge.jar` — 1342987 bytes
- `mods/Quark-4.0-462.jar` — 14935230 bytes
- `mods/relics-1.20.1-0.8.0.11.jar` — 1518437 bytes
- `mods/resourcefulconfig-forge-1.20.1-2.1.3.jar` — 136923 bytes
- `mods/resourcefullib-forge-1.20.1-2.1.29.jar` — 432753 bytes
- `mods/Searchables-forge-1.20.1-1.0.3.jar` — 77732 bytes
- `mods/simplyswords-forge-1.56.0-1.20.1.jar` — 15202091 bytes
- `mods/sodiumdynamiclights-forge-1.0.10-1.20.1.jar` — 511601 bytes
- `mods/sodiumoptionsapi-forge-1.0.10-1.20.1.jar` — 443978 bytes
- `mods/sophisticatedbackpacks-1.20.1-3.24.15.1445.jar` — 983464 bytes
- `mods/sophisticatedcore-1.20.1-1.2.113.1314.jar` — 1445902 bytes
- `mods/starlight-1.1.2+forge.1cda73c.jar` — 110583 bytes
- `mods/tempad-forge-1.20.1-2.3.4.jar` — 192446 bytes
- `mods/terramity-0.9.8-forge-1.20.1.jar` — 27024132 bytes
- `mods/tombstone-1.20.1-8.9.4.jar` — 2026571 bytes
- `mods/traveloptics-6.1.0-1.20.1.jar` — 27502975 bytes
- `mods/TreeChop-1.20.1-forge-0.19.0-fixed.jar` — 517225 bytes
- `mods/valhelsia_core-forge-1.20.1-1.1.2.jar` — 203313 bytes
- `mods/VampiresNeedUmbrellas-1.20.1-1.0.1.jar` — 250266 bytes
- `mods/vampirism_integrations-1.20.1-1.8.0.jar` — 287910 bytes
- `mods/Vampirism-1.20.1-1.10.13.jar` — 12307445 bytes
- `mods/Werewolves-1.20.1-2.0.2.5.jar` — 2304004 bytes
- `mods/wthit-1.20.1-forge-8.19.3.jar` — 815463 bytes
- `mods/Xaeros_Minimap_25.2.10_Forge_1.20.jar` — 1723029 bytes
- `mods/XaerosWorldMap_1.39.12_Forge_1.20.jar` — 960799 bytes
- `mods/yet_another_config_lib_v3-3.6.6+1.20.1-forge.jar` — 1105891 bytes
- `mods/YungsApi-1.20-Forge-4.0.6.jar` — 370524 bytes
- `mods/YungsBetterDungeons-1.20-Forge-4.0.4.jar` — 792381 bytes
- `mods/Zeta-1.0-31.jar` — 1006518 bytes
### Ресурс-паки (верхний уровень)

+
- `resourcepacks/-1.21.2 Fresh Moves v3.1 (With Animated Eyes).zip` — 321871 bytes
- `resourcepacks/§fReanimated §3Blue §7v0.07.zip` — 361604 bytes
- `resourcepacks/Alagard Font/`
- `resourcepacks/Better Spiders.zip` — 230836 bytes
- `resourcepacks/Better Vanilla RPG tools and weapons in 3D/`
- `resourcepacks/Create LootR Chest/`
- `resourcepacks/FreshAnimations_v1.9.2.zip` — 516256 bytes
- `resourcepacks/MandalasGUI+Dakmode_1.21.6_v2.0.zip` — 725928 bytes
- `resourcepacks/Noah's better grass.zip` — 99326 bytes
- `resourcepacks/Quark Programmer Art.zip` — 266434 bytes
- `resourcepacks/SE Vanilla Consistency 1.20.1.zip` — 85743 bytes
- `resourcepacks/Simple Grass Flowers v1.9.5.zip` — 187196 bytes
- `resourcepacks/Universal Bushy Leaves.zip` — 62612 bytes
- `resourcepacks/Water-is-better.zip` — 89594 bytes

## 2026-10-13 — Проверка переданного исходника в текущем репозитории

Запрос пользователя: «Правило 14 и то и то, исходную сборку скинул, проверяй».
Принято: результаты сохраняются в файле и сообщаются в чате.

### Шаги и проверяемые результаты

1. Найдены `UltraMagic/` и `UltraMagic.rar` (2 952 185 400 байт). Источник теперь задаётся относительно репозитория: `SOURCE = ./UltraMagic`. Старый абсолютный путь G: не используется. Архив повторно не распаковывался и не тестировался.
2. Проверены вложенные инструкции: дополнительных AGENTS.md внутри исходника не найдено. Перечислено 12 010 файлов вне вложенной .git; это инвентаризация, а не прочтение содержимого каждого бинарного файла. Миры, кэши, игровые библиотеки и персональные данные не анализировались содержательно.
3. instance.json подтверждает Minecraft 1.20.1, Forge 47.4.0 и лимит памяти 16 384 MiB.
4. Все 139 корневых JAR (744 104 582 байта) прочитаны для SHA-256, проверены ZIP CRC, стандартные дескрипторы разобраны. Ошибок CRC и разбора не обнаружено. У Connector, koremods-modlauncher и kotlinforforge нет проверяемых стандартных дескрипторов; это не признано повреждением. CRC не доказывает совместимость или подлинность файла.
5. Полностью прочитаны байты 381 файла config и одного файла defaultconfigs. Все файлы с расширением .toml успешно разобраны. Семантика настроек, JSON5 и взаимодействие модов этим не проверены.
6. Прочитаны 12 crash reports и latest.log (7 684 строки). В latest.log найдено 119 строк ERROR и 916 WARN; это количество строк, не количество независимых неисправностей. Подтверждены ошибки загрузчика моделей athena у Ender IO, JEI-плагина JER, JSON ресурсов Terramity и предупреждения Werewolves о capability. Есть также сетевые ошибки; их нельзя автоматически считать конфликтами модов.
7. Сравнение списка emittedFiles с реальными JAR: перечисленные JAR присутствуют; дополнительно лежат ftb-library-forge-2001.2.13.jar и ftb-teams-forge-2001.3.2.jar. Поэтому экспортный список не является полным инвентарём текущего состава.
8. Создан source-audit.json: точные имена, размеры, SHA-256, дескрипторы и зависимости всех JAR, сводка конфигураций, выдержки из журналов с номерами строк и различия с метаданными. Отчёт повторно прочитан как JSON. В ходе вывода обнаружено ограничение кодировки консоли для китайских символов автора; исправлен только способ вывода. Данные отчёта сохранены в UTF-8. latest.log декодирован как cp1251 после неудачной проверки UTF-8.

### Исправления прежних выводов

- AutoTranslation-1.2.1+mc1.20.2-forge.jar в переданной папке является Forge-модом по META-INF/mods.toml. Прежнее упоминание его как Fabric-мода не подтверждается этим файлом.
- AdaptiveTooltips действительно содержит fabric.mod.json; при имени файла с 1.20.2 его дескриптор указывает minecraft ~1.20.1. Имя файла само по себе не доказывает несовместимость.
- Crash report от 18:42 сообщает, что Travel Optics не нашёл attributeslib. Однако более поздний latest.log содержит attributeslib 1.3.7. Причина старого сбоя не установлена; нельзя заявлять, что он воспроизводится в текущем составе.
- Старые записи о доступности версий 1.21.1 ещё не перепроверены по внешним источникам в этой сессии. Они не являются готовой матрицей совместимости.

### Ограничения и продолжение

Исходная папка не изменялась. Игра не запускалась, стабильность и переносимость миров не подтверждены. Выполнен статический аудит переданной сборки, а не сборка версии 1.21.1.

Следующие спринты: (1) проверить актуальные публикации и зависимости каждого из 139 модов для 1.21.1 / NeoForge; (2) подготовить отдельную сборку с согласованными исключениями и заменами; (3) проверить запуск и игровые связки на отдельном тестовом мире. Сохраняются решения пользователя о Connector, Enigmatic Legacy Plus, исключении Terramity и допустимой beta Ender IO. Новые исключения пока не согласованы.

## 2026-10-13 — Начало проверки публикаций для 1.21.1 / NeoForge

Пользователь: «Приступай». Начат спринт проверки всех 139 исходных модов; скачивание JAR и изменение исходника в этот спринт не входят.

- Создан audit/check_modrinth.py для воспроизводимых запросов к официальному API Modrinth с локальным кэшем ответов, датами публикации, типами релизов, файлами и зависимостями. Поиск по названию не принимается автоматически за совпадение проекта.
- Обычный сетевой запрос не прошёл DNS в песочнице; единичный запрос вне песочницы подтвердил доступность API.
- Автоматическая проверка разрешений отклонила первую попытку отправить хеши локальных JAR. Пользователь отдельно ответил: «Да, разрешаю отправку хешей». Повторный запуск разрешён и начат. JAR, конфигурации, миры и личные данные не передаются.
- Уже исправлена ошибка прежнего журнала: официальный Vampirism Integrations имеет версии 1.21.1 / NeoForge, включая релиз 1.10.2 от 30.06.2026. Источник: https://www.curseforge.com/minecraft/mc-mods/vampirism-integrations/files/all?page=1&pageSize=20&version=1.21.1 . Его исключение не требуется на основании отсутствия публикации.

## 2026-10-14 — Завершена проверка публикаций всех 139 модов

Спринт выполнен в ранее разрешённом объёме: поиск публикаций и зависимостей, без скачивания целевых JAR и изменения исходной сборки.

- Modrinth: 102 точных совпадения исходных JAR по SHA-1, ещё 21 проект сопоставлен вручную. Оставшиеся 16 исходных файлов проверены по первоисточникам CurseForge. Дополнительно проверены расхождения между каталогами и отдельные порты.
- Созданы COMPATIBILITY_1.21.1.md и audit/compatibility-matrix.json: все 139 исходных строк. Итог: 108 строк с release-кандидатом, 9 с prerelease-кандидатом, 10 с предложенной заменой, 8 без найденной публикации, 2 с согласованным переходом на один Enigmatic Legacy Plus, 1 исключённая Terramity, 1 Travel Optics с устаревшим неподходящим портом. Наличие публикации не означает совместимость всего комплекта.
- Граф Modrinth: 129 проектов, 107 кандидатов, 123 связи. Одна обязательная зависимость без найденного NeoForge-кандидата — Botania для Applied Botanics. Объявленные конфликты фиксированных version_id не обнаружены; диапазоны реальных JAR и runtime-конфликты не проверялись.
- Подтверждён официальный отдельный порт Celestisynth 1.21.1-1.3.9. Iron Chests и Polymorphic Energistics подтверждены для 1.21.1 на CurseForge, несмотря на отсутствие точного тега в Modrinth. У Vampirism Integrations официальный перенос есть.
- Botania Revived — отдельный fork с предупреждением об изменении внутренних Java packages и риске несовместимости аддонов. Неофициальный Blood Magic сам автор описывает как ALPHA / WORK IN PROGRESS, несмотря на канал Release. Неофициальные порты Alex требуют свой Citadel. Эти замены не согласованы автоматически.
- Travel Optics Alpha-4.4.0.1 имеет явную пометку DEPRECATED DONT USE. Рабочая поддерживаемая замена не подтверждена.
- Проверка рендера остаётся открытой: кандидаты Chloride, Sodium Dynamic Lights и Sodium Options API требуют Sodium, а исходник содержит Embeddium. Сочетание не считается подтверждённым.
- Дополнительного решения требуют prerelease AE2 Things, Applied Botanics, JER, Pipez, PlayerAnimator, Tempad и WTHIT. Ранее разрешённые Connector и beta Ender IO сохранены.
- Исправлен выбор кандидатов: release предпочтительнее beta, beta предпочтительнее alpha. Это позволило выбрать JER 1.6.0.12 beta вместо более свежей alpha. Фильтр дат ограничен концом 14.10.2026 по Москве. При повторном использовании кэша данные не обновляются автоматически.

Проверки: 139 уникальных строк; все указанные кандидаты имеют подтверждение целевого тега 1.21.1 / NeoForge в использованном источнике; даты API в пределах даты аудита; SHA-256 всех 139 исходных JAR совпадают с source-audit.json; Python-скрипты проходят синтаксический разбор; git diff --check не сообщает ошибок whitespace. Детали: audit/matrix-validation.json.

Артефакты: audit/build_matrix.py, audit/check_dependencies.py, обновлённый audit/check_modrinth.py, audit/manual-review.json, audit/compatibility-matrix.json, audit/dependency-audit.json, audit/matrix-validation.json, ответы API и веб-источники. Главный читаемый отчёт — COMPATIBILITY_1.21.1.md.

Ограничения: это не готовый install manifest. Полный граф целевых JAR, диапазоны версий, конфиги, игровые связки и перенос миров не подтверждены. Для следующего спринта нужен выбор по перечисленным в отчёте новым заменам и исключениям; прежние разрешения повторно не запрашиваются.
