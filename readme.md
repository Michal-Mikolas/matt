# Quickstart

1. Import Matt as [git submodule](https://www.atlassian.com/git/tutorials/git-submodule)

```sh
git submodule add https://github.com/Michal-Mikolas/matt.git
```

2. Use it :-)

```py
from matt.matt import Matt

matt = Matt(
    cache_file='cache/matt.json'
)
matt.set_ui({
    'start': ['start.png', 'start_selected.png'],
    'settings': 'settings.png',
})

matt.click('start')
matt.click('settings')
```
