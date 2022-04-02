# Yo!nk

[![wakatime](https://wakatime.com/badge/gitlab/Rigil-Kent/yoink.svg)](https://wakatime.com/badge/gitlab/Rigil-Kent/yoink) [![Tests](https://github.com/Rigil-Kent/yoink/actions/workflows/tests.yml/badge.svg)](https://github.com/Rigil-Kent/yoink/actions/workflows/tests.yml/badge.sv)

Yo!nk is a multi-site media download tool that scrapes comic images from online aggragate sites like [readallcomics.com](http://readallcomics.com) and [dragonballsupermanga.net](https://dragonballsupermanga.net/) compressing them into a ```.cbr``` archive.  Magnet links support from ```tpb.party``` coming soon.

## Supported Sites

| Name  | URL |
|------|-----|
| readallcomics  | [http://readallcomics.com](http://readallcomics.com) |
| dragonballsupermanga | [https://dragonballsupermanga.net/](https://dragonballsupermanga.net/) |
| mangadex  | [https://www.mangadex.tv](https://www.mangadex.tv)  |

## Installing/Getting Started

Navigate to the downloaded folder &amp; install using pip

```shell
pip install -e .
```

## Usage

Downloaded archives will appear in ```$HOME/yoink/library/comics``` unless otherwise specified in a ```yoink.json``` config file. Yoink will look both in the root of the program folder or in ```$HOME/.config/yoink``` before defaulting to a preconfigured dict.

### You can download a single comic issue

```shell
yoink http://readallcomics.com/static-season-one-6-2022/
```

### Or an entire series from a starting point

```shell
yoink -s http://readallcomics.com/static-season-one-6-2022/
```
