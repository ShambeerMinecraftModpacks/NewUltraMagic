# UltraMagic: проверка перехода на Minecraft 1.21.1 / NeoForge

Дата проверки: 14.10.2026. Проверены все **139 исходных JAR**. Это список опубликованных кандидатов и препятствий, **не готовая совместимая сборка**. Исходник не изменён, целевые JAR не скачивались, игра не запускалась.

## Результат

| Категория | Исходных JAR |
|---|---:|
| Замена на согласование | 10 |
| Только prerelease | 9 |
| Релиз найден | 108 |
| Версия не найдена | 8 |
| Замена согласована | 2 |
| Исключён по решению | 1 |
| Устаревшая alpha — не брать | 1 |

Числа относятся к исходным строкам: Enigmatic Legacy и Enigmatic Addons заменяются одним Enigmatic Legacy Plus. Количество целевых JAR будет другим из-за новых зависимостей и согласованных исключений.

## Что мешает завершить перенос

1. **Сохранить весь состав без дополнительных решений пока нельзя.** Для восьми исходных модов/библиотек не найден опубликованный кандидат; десять других требуют согласования отдельных замен. Отсутствие публикации в проверенных источниках не доказывает невозможность будущего порта.
2. **Botania → Applied Botanics / Botanical Machinery.** У официального Botania нет найденной публикации 1.21.1. Botania Revived предупреждает об изменении внутренних пакетов и риске несовместимости аддонов. Applied Botanics 1.6.0-alpha.3 опубликован, но его обязательная зависимость остаётся нерешённой. Botanical Machinery также без найденного переноса.
3. **Travel Optics.** Найденный порт прямо помечен DEPRECATED DONT USE. Его нельзя выдавать за пригодную замену.
4. **Неофициальные Alex’s Caves / Mobs** требуют отдельный Citadel (Unofficial Port). Официальный Citadel 2.7.1 найден, но это не доказательство совместимости с данными портами.
5. **Blood Magic.** Неофициальный порт с меткой Release по описанию автора остаётся ALPHA / WORK IN PROGRESS.
6. **Рендер.** В опубликованном графе Chloride, Sodium Dynamic Lights и Sodium Options API требуют Sodium. Наличие Embeddium в исходнике не решает выбор нового комплекта. Нужна проверка JAR и запуск; совместная установка двух рендереров не утверждается.
7. **Дополнительные prerelease:** AE2 Things, Applied Botanics, JER, Pipez, PlayerAnimator, Tempad, WTHIT. Ранее согласованы Connector и beta Ender IO; разрешение на них не распространяется автоматически на остальные.
8. **LMFT:** API относит последнюю release к 1.21.1, но имя файла содержит 1.21.9. До включения требуется сверка целевого дескриптора; более ранний кандидат 1.0.4+1.21 тоже есть в API.

## Подтверждённые уточнения

- Vampirism Integrations имеет официальный релиз 1.21.1: исключать его из-за отсутствия версии неверно.
- Для Celestisynth найден официальный порт 1.21.1-1.3.9; исходная страница ссылается на него. Нужны GeckoLib и PlayerAnimator.
- Iron Chests и Polymorphic Energistics отмечены 1.21.1 на CurseForge, хотя фильтр Modrinth не нашёл этот тег.
- FTB Backups 2: выбран явно отмеченный 1.21.1 файл 1.0.28, а не автоматически более новый 1.0.29 с тегом только 1.21.
- При выборе Modrinth используется последний release, затем beta, затем alpha. Метка Release характеризует канал публикации, а не подтверждённую стабильность.

## Проверка зависимостей и её границы

В графе Modrinth: **129 проектов, 107 кандидатов, 123 связи**. Найдена одна обязательная зависимость без NeoForge-кандидата: Botania для Applied Botanics. Не найдено конфликтов зафиксированных version_id или явно объявленных несовместимых кандидатов. Это не означает отсутствие реальных конфликтов.

Дополнительно к исходным проектам в графе появились Simply Tooltips, Bookshelf, Prickle, Lionfish-API и Sodium; Lionfish-API уже присутствует в исходнике, но исходный JAR не распознан по хешу Modrinth. Enigmatic Legacy Plus внесён как согласованная замена.

Граф исследовательский: он строится по найденным Modrinth-кандидатам, до полного применения ручных решений и исключений. Для кандидатов только с CurseForge использованы доступные описания; полный граф их зависимостей ещё не проверен. Пустой список зависимостей API не доказывает их отсутствие в JAR. Диапазоны версий, modId, вложенные библиотеки, mixin-конфликты, совместимость конфигов и миров проверяются на следующем этапе.

## Полная матрица

Ссылка в колонке кандидата ведёт к первоисточнику. Для CurseForge указан подтверждённый кандидат, который не обязательно является самым новым. «Замена» не означает разрешение на установку. Список зависимостей ниже — только опубликованные обязательные связи API, а не полный дескриптор.

| Исходный JAR | Статус | Кандидат NeoForge 1.21.1 | Зависимости / примечания |
|---|---|---|---|
| `AdaptiveTooltips-1.3.0-fabric-1.20.2.jar` | Замена на согласование | [1.0.3 (release)](https://modrinth.com/mod/better_tooltips) | Better Tooltips 1.0.3: отдельный NeoForge-проект, замена требует согласования. |
| `AE2-Things-1.2.1.jar` | Только prerelease | [1.4.2-beta (beta)](https://www.curseforge.com/minecraft/mc-mods/ae2-things-forge/files/all?page=1&pageSize=20&version=1.21.1) | Нужен AE2; диапазон версий в целевом JAR ещё не проверен. Не путать с одноимённым Fabric-проектом ProjectET. Prerelease ещё не согласован. |
| `ae2wtlib-15.3.3-forge.jar` | Релиз найден | [19.5.1 (release)](https://modrinth.com/mod/applied-energistics-2-wireless-terminals) | API требует: Applied Energistics 2. |
| `alexscaves-2.0.2.jar` | Замена на согласование | [1.21.1-2.0.10 (release)](https://www.curseforge.com/minecraft/mc-mods/alexs-caves-unofficial-port/files/all?page=1&pageSize=20&version=1.21.1) | Неофициальный порт требует Citadel (Unofficial Port), а не автоматически выбранный официальный Citadel. |
| `alexsmobs-1.22.9.jar` | Замена на согласование | [1.21.1-1.22.17 (release)](https://www.curseforge.com/minecraft/mc-mods/alexs-mobs-1-21-1-port/files/all?page=1&pageSize=20&version=1.21.1) | Неофициальный порт требует Citadel (Unofficial Port); нельзя установить две библиотеки с одинаковым modId. |
| `AmbientSounds_FORGE_v6.3.1_mc1.20.1.jar` | Релиз найден | [6.3.10 (release)](https://modrinth.com/mod/ambientsounds) | API требует: CreativeCore. |
| `ApothicAttributes-1.20.1-1.3.7.jar` | Релиз найден | [1.21.1-2.11.0 (release)](https://modrinth.com/mod/apothic-attributes) | API требует: Placebo. |
| `applied-botanics-forge-1.5.1.jar` | Только prerelease | [1.6.0-alpha.3 (alpha)](https://modrinth.com/mod/applied-botanics) | API требует: Botania, Applied Energistics 2. БЛОКЕР: требуется официальный Botania, для которого нет кандидата 1.21.1. Botania Revived не подтверждена как совместимая замена; alpha самого аддона также не согласована. Prerelease ещё не согласован. |
| `appliedenergistics2-forge-15.4.10.jar` | Релиз найден | [19.2.18 (release)](https://modrinth.com/mod/ae2) | API требует: GuideME. |
| `architectury-9.2.14-forge.jar` | Релиз найден | [13.0.11+neoforge (release)](https://modrinth.com/mod/architectury-api) |  |
| `artifacts-forge-9.5.16.jar` | Релиз найден | [13.2.5 (release)](https://modrinth.com/mod/artifacts) |  |
| `AttributeFix-Forge-1.20.1-21.0.4.jar` | Релиз найден | [21.1.3 (release)](https://modrinth.com/mod/attributefix) | API требует: Prickle, Bookshelf. |
| `AutoTranslation-1.2.1+mc1.20.2-forge.jar` | Замена на согласование | [2.1.0 (release)](https://modrinth.com/mod/autotranslation-next) | API требует: Cloth Config API. AutoTranslation Next 2.1.0: отдельное продолжение, не подтверждено полное равенство функций. |
| `badpackets-forge-0.4.3.jar` | Релиз найден | [neo-0.8.2 (release)](https://modrinth.com/mod/badpackets) |  |
| `balm-forge-1.20.1-7.3.37-all.jar` | Релиз найден | [21.0.66+neoforge-1.21.1 (release)](https://modrinth.com/mod/balm) |  |
| `better-clouds-1.3.37-beta+1.20.1-forge.rev.e63efe2.jar` | Релиз найден | [1.13.11+1.21.1-neoforge-release (release)](https://modrinth.com/mod/better-clouds) | API требует: YetAnotherConfigLib (YACL). |
| `bettercombat-forge-1.9.0+1.20.1.jar` | Релиз найден | [2.4.0+1.21.1-neoforge (release)](https://modrinth.com/mod/better-combat) | API требует: playerAnimator, Cloth Config API. |
| `betterfpsdist-1.20.1-6.0.jar` | Релиз найден | [1.21.1-6.1 (release)](https://www.curseforge.com/minecraft/mc-mods/better-fps-render-distance/files/all?page=1&pageSize=20&version=1.21.1) | Подтверждена публикация для 1.21.1; отношения зависимостей проверить по JAR. |
| `biomemusic-1.20.1-3.5.jar` | Релиз найден | [1.21.1-4.1 (release)](https://www.curseforge.com/minecraft/mc-mods/biome-music/files/all?page=1&pageSize=20&version=1.21.1) | Подтверждён кандидат, не утверждение о самой новой версии. |
| `bloodmagic-1.20.1-3.3.5-47.jar` | Замена на согласование | [v1.1 (release)](https://www.curseforge.com/minecraft/mc-mods/blood-magic-unofficial-port/files/all?page=1&pageSize=20&version=1.21.1) | Несмотря на метку Release, автор описывает порт как ALPHA / WORK IN PROGRESS. Для стабильной сборки считать экспериментальным. |
| `born_in_chaos_[Forge]1.20.1_1.7.3.jar` | Релиз найден | [1.7.6 (release)](https://modrinth.com/mod/borninchaos) | API требует: Geckolib. |
| `Botania-1.20.1-450-FORGE.jar` | Замена на согласование | [1.0.2 (release)](https://www.curseforge.com/minecraft/mc-mods/botania-revived/files/all?page=1&pageSize=20&version=1.21.1) | Fork меняет внутренности и Java packages; автор предупреждает о несовместимости аддонов. Требует NeoForge 21.1.240+, Java 21, Patchouli 1.21.1-93+. Совместимость Applied Botanics не подтверждена. |
| `BotanicalMachinery-1.20.1-3.0.7.jar` | Версия не найдена | — | Опубликованная версия 1.21.1 не найдена; перенос функций не решён. |
| `buildinggadgets2-1.0.8.jar` | Релиз найден | [1.3.9 (release)](https://www.curseforge.com/minecraft/mc-mods/building-gadgets/files/all?page=1&pageSize=20&version=1.21.1) | Подтверждён NeoForge 1.21.1. |
| `caelus-forge-3.2.0+1.20.1.jar` | Релиз найден | [7.0.1+1.21.1 (release)](https://modrinth.com/mod/caelus) |  |
| `canary-mc1.20.1-0.3.3.jar` | Замена на согласование | [mc1.21.1-0.15.4-neoforge (release)](https://modrinth.com/mod/lithium) | Lithium имеет собственный NeoForge-релиз; замена Canary требует согласования. |
| `CarbonConfig-1.20-1.2.8.1.jar` | Релиз найден | [2.0.2.1 (release)](https://modrinth.com/mod/carbon-config) |  |
| `celestisynth-1.20.1-1.3.3-all.jar` | Релиз найден | [1.21.1-1.3.9 (release)](https://www.curseforge.com/minecraft/mc-mods/celestisynth-1-21-1/files/all?page=1&pageSize=20&version=1.21.1) | Официальный порт, на который ссылается исходный проект. Нужны GeckoLib и PlayerAnimator; последний beta. |
| `chloride-FORGE-mc1.20.1-v1.7.4.jar` | Релиз найден | [1.8.1-NEO-1.21.1 (release)](https://modrinth.com/mod/chloride) | API требует: Sodium. Выбор рендера не завершён: граф содержит Sodium и исходный Embeddium. Проверить требования и выбрать совместимый комплект; не считать их совместную установку подтверждённой. |
| `Chunk-Pregenerator-1.20-4.4.4.jar` | Релиз найден | [NeoForge-1.21-4.5.4 (release)](https://www.curseforge.com/minecraft/mc-mods/chunkpregenerator/files/all?page=1&pageSize=20&version=1.21.1) | Страница файла явно включает 1.21.1. |
| `citadel-2.6.2-1.20.1.jar` | Релиз найден | [2.7.1 (release)](https://modrinth.com/mod/citadel) | Официальный Citadel не считать автоматически совместимым с неофициальными портами Alex: они требуют отдельный Citadel (Unofficial Port). |
| `clean_tooltips-1.0-forge-1.20.1.jar` | Релиз найден | [1.1 (release)](https://modrinth.com/mod/clean-tooltips) |  |
| `cloth-config-11.1.136-forge.jar` | Релиз найден | [15.0.140+neoforge (release)](https://modrinth.com/mod/cloth-config) |  |
| `Clumps-forge-1.20.1-12.0.0.4.jar` | Релиз найден | [19.0.0.1 (release)](https://modrinth.com/mod/clumps) |  |
| `Connector-1.0.0-beta.47+1.20.1.jar` | Только prerelease | [2.0.0-beta.17+1.21.1 (beta)](https://modrinth.com/mod/connector) | API требует: Forgified Fabric API. Prerelease согласован. |
| `ConnectorExtras-1.11.2+1.20.1.jar` | Релиз найден | [1.12.1+1.21.1 (release)](https://modrinth.com/mod/connector-extras) | API требует: Sinytra Connector. |
| `Controlling-forge-1.20.1-12.0.2.jar` | Релиз найден | [19.0.5 (release)](https://modrinth.com/mod/controlling) | API требует: Searchables. |
| `cosmeticarmorreworked-1.20.1-v1a.jar` | Релиз найден | [1.21.1-v1-neoforge (release)](https://www.curseforge.com/minecraft/mc-mods/cosmetic-armor-reworked/files/all?page=1&pageSize=20&version=1.21.1) | Подтверждён NeoForge 1.21.1. |
| `create-1.20.1-6.0.8.jar` | Релиз найден | [6.0.10+mc1.21.1 (release)](https://modrinth.com/mod/create) |  |
| `create-new-age-1.1.7d+forge-mc1.20.1.jar` | Релиз найден | [1.2.0+mc1.21.1 (release)](https://modrinth.com/mod/create-new-age) | API требует: Create. |
| `createaddition-1.20.1-1.3.3.jar` | Релиз найден | [neoforge-1.21.1-1.6.0 (release)](https://modrinth.com/mod/createaddition) |  |
| `CreativeCore_FORGE_v2.12.32_mc1.20.1.jar` | Релиз найден | [2.13.51 (release)](https://modrinth.com/mod/creativecore) |  |
| `cupboard-1.20.1-2.7.jar` | Релиз найден | [1.21.1-4.2 (release)](https://www.curseforge.com/minecraft/mc-mods/cupboard/files/all?page=1&pageSize=20&version=1.21.1) | Библиотека; проверить требования потребителей. |
| `curios-forge-5.14.1+1.20.1.jar` | Релиз найден | [9.5.1+1.21.1 (release)](https://modrinth.com/mod/curios) |  |
| `CyclopsCore-1.20.1-1.21.3.jar` | Релиз найден | [1.21.1-1.30.0 (release)](https://modrinth.com/mod/cyclops-core) |  |
| `Disenchanting-forge-1.20.1-2.2.4.jar` | Релиз найден | [1.21.1-2.3.0 (release)](https://www.curseforge.com/minecraft/mc-mods/disenchantingforge/files/all?page=1&pageSize=20&version=1.21.1) | Подтверждён NeoForge 1.21.1. |
| `Dungeon Now Loading-forge-1.20.1-2.11.jar` | Замена на согласование | [2.11.3 NeoForge (release)](https://www.curseforge.com/minecraft/mc-mods/dungeon-now-loading-1-21-1-port/files/all?page=1&pageSize=20&version=1.21.1) | Неофициальный Tricky Trials Port. Подтверждён кандидат, не гарантируется последняя версия. |
| `eeeabsmobs-1.20.1-0.97-Fix.jar` | Замена на согласование | [1.0.2 (release)](https://modrinth.com/mod/eeeabs-mobs-unofficial) | Неофициальный порт: API предлагает 1.0.2 для 1.21.1; проверить JAR и содержимое перед включением. |
| `embeddium-0.3.31+mc1.20.1.jar` | Релиз найден | [1.0.15+mc1.21.1 (release)](https://modrinth.com/mod/embeddium) | Выбор рендера не завершён: граф содержит Sodium и исходный Embeddium. Проверить требования и выбрать совместимый комплект; не считать их совместную установку подтверждённой. |
| `EnchantingInfuser-v8.0.3-1.20.1-Forge.jar` | Релиз найден | [v21.1.4-1.21.1-NeoForge (release)](https://modrinth.com/mod/enchanting-infuser) | API требует: Puzzles Lib. |
| `EnderIO-1.20.1-6.2.16-beta-all.jar` | Только prerelease | [v8.2.12-beta (beta)](https://modrinth.com/mod/enderio) | Prerelease согласован. |
| `enigmaticaddons-1.2.5.jar` | Замена согласована | [1.21.1-1.1.2 (release)](https://modrinth.com/mod/enigmaticlegacy-plus) | Согласован переход на Enigmatic Legacy Plus. Две исходные строки ведут к одному целевому моду; равенство всех функций Addons не подтверждено. |
| `EnigmaticLegacy-2.30.1.jar` | Замена согласована | [1.21.1-1.1.2 (release)](https://modrinth.com/mod/enigmaticlegacy-plus) | Согласован переход на Enigmatic Legacy Plus. Две исходные строки ведут к одному целевому моду; равенство всех функций Addons не подтверждено. |
| `entity_model_features_1.20.1-forge-3.0.7.jar` | Релиз найден | [3.3.11-neoforge-1.21 (release)](https://modrinth.com/mod/entity-model-features) | API требует: [ETF] Entity Texture Features. |
| `entity_texture_features_1.20.1-forge-7.0.6.jar` | Релиз найден | [7.2.5-neoforge-1.21 (release)](https://modrinth.com/mod/entitytexturefeatures) |  |
| `entityculling-forge-1.9.4-mc1.20.1.jar` | Релиз найден | [1.11.3 (release)](https://modrinth.com/mod/entityculling) |  |
| `EvilCraft-1.20.1-1.2.52.jar` | Релиз найден | [1.21.1-1.2.98 (release)](https://modrinth.com/mod/evilcraft) | API требует: Cyclops Core. |
| `ExtraSoundsNext-forge-1.20.1-1.4.jar` | Релиз найден | [1.5.6+1.21.1-neoforge (release)](https://modrinth.com/mod/extrasoundsforge) |  |
| `Ez-ae2-universal.jar` | Версия не найдена | — | Опубликованная версия 1.21.1 не найдена. |
| `fabric-api-0.92.6+1.11.14+1.20.1.jar` | Релиз найден | [0.116.15+2.3.5+1.21.1 (release)](https://modrinth.com/mod/forgified-fabric-api) |  |
| `ferritecore-6.0.1-forge.jar` | Релиз найден | [7.0.3-neoforge (release)](https://modrinth.com/mod/ferrite-core) |  |
| `forbidden_arcanus-1.20.1-2.2.6.jar` | Релиз найден | [2.6.1 (release)](https://modrinth.com/mod/forbidden-arcanus) | API требует: Valhelsia Core. |
| `FpsReducer2-forge-1.20.1-2.5.1.jar` | Релиз найден | [1.21-2.10 (release)](https://modrinth.com/mod/fps-reducer) |  |
| `ftb-library-forge-2001.2.13.jar` | Релиз найден | [2101.1.37 (release)](https://www.curseforge.com/minecraft/mc-mods/ftb-library-forge/files/all?page=1&pageSize=20&version=1.21.1) | Проверить зависимости и диапазоны версий FTB по целевым JAR. |
| `ftb-teams-forge-2001.3.2.jar` | Релиз найден | [2101.1.11 (release)](https://www.curseforge.com/minecraft/mc-mods/ftb-teams-forge/files/all?page=1&pageSize=20&version=1.21.1) | Связка FTB Library/Teams требует проверки диапазонов. |
| `ftbbackups2-forge-1.20-1.0.23.jar` | Релиз найден | [1.0.28 [NeoForge] (release)](https://www.curseforge.com/minecraft/mc-mods/ftb-backups-2/files/all?page=1&pageSize=20&version=1.21.1) | Именно 1.0.28 явно отмечена 1.21.1; 1.0.29 с меткой только 1.21 автоматически не выбрана. |
| `fzzy_config-0.7.4+1.20.1+forge.jar` | Релиз найден | [0.7.7+1.21+neoforge (release)](https://modrinth.com/mod/fzzy-config) | API требует: Kotlin for Forge. |
| `geckolib-forge-1.20.1-4.8.2.jar` | Релиз найден | [4.9.3 (release)](https://modrinth.com/mod/geckolib) |  |
| `GodlyVampirism-1.20.1-1.10.0.jar` | Релиз найден | [1.10.0 (release)](https://modrinth.com/mod/godlyvampirism) |  |
| `guideme-20.1.14.jar` | Релиз найден | [21.1.19 (release)](https://modrinth.com/mod/guideme) |  |
| `Iceberg-1.20.1-forge-1.1.25.jar` | Релиз найден | [1.3.2 (release)](https://modrinth.com/mod/iceberg) |  |
| `ImmediatelyFast-Forge-1.5.3+1.20.4.jar` | Релиз найден | [1.6.15+1.21.1-neoforge (release)](https://modrinth.com/mod/immediatelyfast) |  |
| `immersive_aircraft-1.4.0+1.20.1-forge.jar` | Релиз найден | [1.6.0+1.21.1 (release)](https://modrinth.com/mod/immersive-aircraft) |  |
| `ironchest-1.20.1-14.4.4.jar` | Релиз найден | [1.21-neoforge-16.0.7 (release)](https://www.curseforge.com/minecraft/mc-mods/iron-chests/files/all?page=1&pageSize=20&version=1.21.1) | CurseForge явно включает 1.21.1, хотя Modrinth не дал точного совпадения тега. |
| `ironfurnaces-1.20.1-4.1.8.jar` | Релиз найден | [4.3.2 (release)](https://modrinth.com/mod/iron-furnaces) |  |
| `irons_spellbooks-1.20.1-3.4.0.11.jar` | Релиз найден | [1.21.1-3.16.3 (release)](https://modrinth.com/mod/irons-spells-n-spellbooks) |  |
| `ItemProductionLib-1.20.1-1.0.2a-all.jar` | Версия не найдена | — | Версия 1.21.1 не найдена; возможность убрать библиотеку зависит от нового состава. |
| `jei-1.20.1-forge-15.20.0.128.jar` | Релиз найден | [19.51.0.418 (release)](https://modrinth.com/mod/jei) |  |
| `jeiintegration_1.20.1-10.0.0.jar` | Замена на согласование | [1.0.2 (release)](https://modrinth.com/mod/jei-integration-reborn) | API требует: Kotlin for Forge. JEI Integration Reborn 1.0.2: отдельный проект. |
| `jerintegration-5.5.0.jar` | Релиз найден | [6.5.0 (release)](https://www.curseforge.com/minecraft/mc-mods/jer-integration/files/all?page=1&pageSize=20&version=1.21.1) | Нужен JER; выбранный кандидат самого JER имеет канал beta. |
| `JustEnoughResources-1.20.1-1.4.0.247.jar` | Только prerelease | [1.6.0.12 (beta)](https://modrinth.com/mod/just-enough-resources-jer) | Prerelease ещё не согласован. |
| `koremods-modlauncher-1.0.0.jar` | Версия не найдена | — | Версия 1.21.1 не найдена; необходимость библиотеки надо пересмотреть по новому составу. |
| `kotlinforforge-4.12.0-all.jar` | Релиз найден | [5.12.0 (release)](https://modrinth.com/mod/kotlin-for-forge) |  |
| `L_Enders_Cataclysm-3.16.jar` | Релиз найден | [3.33 (release)](https://modrinth.com/mod/l_enders-cataclysm) | API требует: Lionfish-API, Curios API. |
| `LegendaryTooltips-1.20.1-forge-1.4.5.jar` | Релиз найден | [1.5.5 (release)](https://modrinth.com/mod/legendary-tooltips) | API требует: Iceberg, Prism. |
| `libIPN-forge-1.20-4.0.2.jar` | Релиз найден | [neoforge-1.21.1-6.6.3 (release)](https://modrinth.com/mod/libipn) | API требует: Kotlin for Forge. |
| `LibX-1.20.1-5.0.14.jar` | Релиз найден | [1.21.1-6.0.9 (release)](https://modrinth.com/mod/libx) |  |
| `lionfishapi-2.4-Fix.jar` | Релиз найден | [3.1 (release)](https://www.curseforge.com/minecraft/mc-mods/lionfish-api/files/all?page=1&pageSize=20&version=1.21.1) | Нужна Cataclysm; кандидат также найден в графе Modrinth. |
| `lmft-1.0.4+1.20.1-forge.jar` | Релиз найден | [1.1.1+1.21.9 (release)](https://modrinth.com/mod/lmft) | API отмечает выбранный файл как совместимый с 1.21.1, но имя содержит 1.21.9. До включения проверить дескриптор; доступен также более ранний 1.0.4+1.21. |
| `lodestone-1.20.1-1.6.4.1.jar` | Релиз найден | [1.8.2 (release)](https://modrinth.com/mod/lodestonelib) |  |
| `lootr-forge-1.20-0.7.35.94.jar` | Релиз найден | [1.21.1-1.11.38.127 (release)](https://modrinth.com/mod/lootr) |  |
| `malum-1.20.1-1.6.7.jar` | Релиз найден | [1.8.2 (release)](https://modrinth.com/mod/malum) |  |
| `Mantle-1.20.1-1.11.79.jar` | Версия не найдена | — | Опубликованная версия 1.21.1 не найдена; не переносить старую библиотеку без потребителя. |
| `memoryleakfix-forge-1.17+-1.1.5.jar` | Версия не найдена | — | Версия 1.21.1 не найдена; отсутствие потребности в старом исправлении ещё не доказано. |
| `modernfix-forge-5.25.2+mc1.20.1.jar` | Релиз найден | [5.27.26+mc1.21.1 (release)](https://modrinth.com/mod/modernfix) |  |
| `MouseTweaks-forge-mc1.20.1-2.25.1.jar` | Релиз найден | [1.21-2.26.1-neoforge (release)](https://modrinth.com/mod/mouse-tweaks) |  |
| `mowziesmobs-1.7.3.jar` | Релиз найден | [1.8.2 (release)](https://modrinth.com/mod/mowzies-mobs) | API требует: Geckolib. |
| `NaturesCompass-1.20.1-1.11.2-forge.jar` | Релиз найден | [1.21.1-3.4.0-neoforge (release)](https://modrinth.com/mod/natures-compass) |  |
| `noisium-forge-2.3.0+mc1.20-1.20.1.jar` | Релиз найден | [2.3.0+mc1.21-1.21.1 (release)](https://modrinth.com/mod/noisium) |  |
| `OctoLib-FORGE-0.5.0.1+1.20.1.jar` | Релиз найден | [0.6.2 (release)](https://modrinth.com/mod/shatterbyte-lib) | Проект Modrinth переименован в Shatterbyte Lib; для 1.21.1 выбран файл OctoLib. Исходная идентичность подтверждена SHA-1. |
| `Patchouli-1.20.1-84.1-FORGE.jar` | Релиз найден | [1.21.1-93-neoforge (release)](https://modrinth.com/mod/patchouli) |  |
| `piercingpaxels-1.0.12.jar` | Версия не найдена | — | Опубликованная версия 1.21.1 не найдена; функциональная замена не согласована. |
| `pipez-forge-1.20.1-1.2.26.jar` | Только prerelease | [neoforge-1.21.1-1.2.31 (beta)](https://modrinth.com/mod/pipez) | Prerelease ещё не согласован. |
| `Placebo-1.20.1-8.6.3.jar` | Релиз найден | [1.21.1-9.9.4 (release)](https://modrinth.com/mod/placebo) |  |
| `player-animation-lib-forge-1.0.2-rc1+1.20.jar` | Только prerelease | [2.0.4+1.21.1-forge (beta)](https://modrinth.com/mod/playeranimator) | Prerelease ещё не согласован. |
| `polyeng-forge-0.1.1-1.20.1.jar` | Релиз найден | [0.4.1 (release)](https://www.curseforge.com/minecraft/mc-mods/polymorphic-energistics/files/all?page=1&pageSize=20&version=1.21.1) | CurseForge явно включает 1.21.1; проверить совместную работу с AE2 и Polymorph. |
| `polylib-forge-2000.0.3-build.143.jar` | Релиз найден | [2100.0.3-build.160 (release)](https://modrinth.com/mod/polylib) | API требует: Architectury API. |
| `polymorph-forge-0.49.10+1.20.1.jar` | Релиз найден | [1.1.0+1.21.1 (release)](https://modrinth.com/mod/polymorph) |  |
| `PresenceFootsteps-1.20.1-1.9.1-beta.1.jar` | Релиз найден | [1.1.0 (release)](https://modrinth.com/mod/presence-footsteps-forge) |  |
| `Prism-1.20.1-forge-1.0.5.jar` | Релиз найден | [1.0.11 (release)](https://modrinth.com/mod/prism-lib) |  |
| `PuzzlesLib-v8.1.33-1.20.1-Forge.jar` | Релиз найден | [21.1.64 (release)](https://modrinth.com/mod/puzzles-lib) |  |
| `Quark-4.0-462.jar` | Релиз найден | [4.1-487 (release)](https://modrinth.com/mod/quark) | API требует: Zeta. |
| `relics-1.20.1-0.8.0.11.jar` | Релиз найден | [0.10.7.8 (release)](https://modrinth.com/mod/relics-mod) |  |
| `resourcefulconfig-forge-1.20.1-2.1.3.jar` | Релиз найден | [3.0.11 (release)](https://modrinth.com/mod/resourceful-config) |  |
| `resourcefullib-forge-1.20.1-2.1.29.jar` | Релиз найден | [3.0.12 (release)](https://modrinth.com/mod/resourceful-lib) |  |
| `Searchables-forge-1.20.1-1.0.3.jar` | Релиз найден | [1.0.2 (release)](https://modrinth.com/mod/searchables) |  |
| `simplyswords-forge-1.56.0-1.20.1.jar` | Релиз найден | [1.70.2-1.21.1 (release)](https://modrinth.com/mod/simply-swords) | API требует: Fzzy Config, Simply Tooltips, Architectury API. |
| `sodiumdynamiclights-forge-1.0.10-1.20.1.jar` | Релиз найден | [neoforge-1.21.1-1.0.10 (release)](https://modrinth.com/mod/sodium-dynamic-lights) | API требует: Sodium, Sodium Options API. Выбор рендера не завершён: граф содержит Sodium и исходный Embeddium. Проверить требования и выбрать совместимый комплект; не считать их совместную установку подтверждённой. |
| `sodiumoptionsapi-forge-1.0.10-1.20.1.jar` | Релиз найден | [neoforge-1.21.1-1.0.10 (release)](https://modrinth.com/mod/sodium-options-api) | API требует: Sodium. Выбор рендера не завершён: граф содержит Sodium и исходный Embeddium. Проверить требования и выбрать совместимый комплект; не считать их совместную установку подтверждённой. |
| `sophisticatedbackpacks-1.20.1-3.24.15.1445.jar` | Релиз найден | [1.21.1-3.26.12.2208 (release)](https://modrinth.com/mod/sophisticated-backpacks) | API требует: Sophisticated Core. |
| `sophisticatedcore-1.20.1-1.2.113.1314.jar` | Релиз найден | [1.21.1-1.5.11.2394 (release)](https://modrinth.com/mod/sophisticated-core) |  |
| `starlight-1.1.2+forge.1cda73c.jar` | Версия не найдена | — | Версия 1.21.1 не найдена; старый Forge JAR не является кандидатом для NeoForge 1.21.1. |
| `tempad-forge-1.20.1-2.3.4.jar` | Только prerelease | [3.0.4 (beta)](https://modrinth.com/mod/tempad) | API требует: Resourceful Lib, Kotlin for Forge, Resourceful Config. Prerelease ещё не согласован. |
| `terramity-0.9.8-forge-1.20.1.jar` | Исключён по решению | — | Исключение уже согласовано пользователем. |
| `tombstone-1.20.1-8.9.4.jar` | Релиз найден | [neoforge-1.21.1-9.5.6 (release)](https://modrinth.com/mod/corail-tombstone) |  |
| `traveloptics-6.1.0-1.20.1.jar` | Устаревшая alpha — не брать | [Alpha-4.4.0.1 (alpha)](https://www.curseforge.com/minecraft/mc-mods/to-tweaks-irons-spells/files/all?page=1&pageSize=20&version=1.21.1) | Найдена только Alpha-4.4.0.1 с явной пометкой DEPRECATED DONT USE. Поддерживаемый перенос не подтверждён. |
| `TreeChop-1.20.1-forge-0.19.0-fixed.jar` | Релиз найден | [0.19.3 (release)](https://modrinth.com/mod/treechop) |  |
| `valhelsia_core-forge-1.20.1-1.1.2.jar` | Релиз найден | [1.1.4 (release)](https://modrinth.com/mod/valhelsia-core) |  |
| `VampiresNeedUmbrellas-1.20.1-1.0.1.jar` | Релиз найден | [1.21.1-1.0.3 (release)](https://modrinth.com/mod/vampires-need-umbrellas) |  |
| `Vampirism-1.20.1-1.10.13.jar` | Релиз найден | [1.21-1.10.13 (release)](https://modrinth.com/mod/vampirism) |  |
| `vampirism_integrations-1.20.1-1.8.0.jar` | Релиз найден | [1.21.1-1.10.2 (release)](https://modrinth.com/mod/vampirism-integrations) | API требует: Vampirism. |
| `Werewolves-1.20.1-2.0.2.5.jar` | Релиз найден | [1.21-2.0.3.3 (release)](https://modrinth.com/mod/werewolves) | API требует: Vampirism. |
| `wthit-1.20.1-forge-8.19.3.jar` | Только prerelease | [neo-12.10.2 (beta)](https://modrinth.com/mod/wthit) | API требует: bad packets. Prerelease ещё не согласован. |
| `Xaeros_Minimap_25.2.10_Forge_1.20.jar` | Релиз найден | [neoforge-1.21.1-26.6.0 (release)](https://modrinth.com/mod/xaeros-minimap) |  |
| `XaerosWorldMap_1.39.12_Forge_1.20.jar` | Релиз найден | [neoforge-1.21.1-1.47.0 (release)](https://modrinth.com/mod/xaeros-world-map) |  |
| `yet_another_config_lib_v3-3.6.6+1.20.1-forge.jar` | Релиз найден | [3.8.2+1.21.1-neoforge (release)](https://modrinth.com/mod/yacl) |  |
| `YungsApi-1.20-Forge-4.0.6.jar` | Релиз найден | [1.21.1-NeoForge-5.1.9 (release)](https://modrinth.com/mod/yungs-api) |  |
| `YungsBetterDungeons-1.20-Forge-4.0.4.jar` | Релиз найден | [1.21.1-NeoForge-5.1.4 (release)](https://modrinth.com/mod/yungs-better-dungeons) | API требует: YUNG's API. |
| `Zeta-1.0-31.jar` | Релиз найден | [1.1-40 (release)](https://modrinth.com/mod/zeta) |  |

## Артефакты и воспроизводимость

- `source-audit.json`: исходные JAR, SHA-256, дескрипторы, результаты CRC, конфиги и журналы.
- `audit/modrinth-audit.json`: 139 строк; 102 точных совпадения по SHA-1, 21 ручное сопоставление проектов, 16 строк дополнительно разобраны по первоисточникам CurseForge.
- `audit/manual-review.json`: ручные уточнения и ссылки; `audit/compatibility-matrix.json`: итоговые 139 строк.
- `audit/dependency-audit.json`: опубликованные связи, кандидаты, альтернативы и ограничения графа.
- `audit/modrinth-cache/`: исходные ответы API с URL и временем получения; `audit/web/`: сохранённые результаты проверок страниц.
- `audit/check_modrinth.py`, `audit/check_dependencies.py`, `audit/build_matrix.py`: сбор и формирование отчёта. Кэш сохраняет снимок; повторный запуск с существующим кэшем не является новой проверкой актуальности.

## Следующий спринт после согласования состава

Согласовать отдельно десять предложенных замен, семь дополнительных prerelease и судьбу восьми строк без найденной версии плюс Travel Optics. Затем подготовить отдельный целевой каталог, скачать разрешённые кандидаты, проверить реальные дескрипторы и диапазоны зависимостей, выбрать рендерер и проверить запуск на новом тестовом мире. Перенос существующего мира требует отдельной резервной копии и теста. Стабильность до этих проверок не заявляется.
