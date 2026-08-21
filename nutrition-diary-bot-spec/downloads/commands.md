# Commands

## Build HTML overview

```bash
python3 projects/nutrition_diary_bot_spec/build/build_spec_landing.py
```

## View canonical specification

```bash
sed -n '1,260p' projects/nutrition_diary_bot_spec/source/2026-05-07_nutrition_diary_bot_technical_spec_ru_v1.md
```

## Check project files

```bash
find projects/nutrition_diary_bot_spec -maxdepth 2 -type f | sort
```

## Check generated output

```bash
find projects/nutrition_diary_bot_spec/output -maxdepth 2 -type f | sort
```

## Validate YAML metadata

```bash
ruby -e "require 'yaml'; YAML.load_file('projects/nutrition_diary_bot_spec/manifest.yaml'); YAML.load_file('projects/nutrition_diary_bot_spec/status.yaml'); puts 'ok'"
```
