# Firebase plugin for Flexget
Saves accepted flexget entries to Firebase.

# Usage
```
  firebase:
      storage: https://my-storage.firebaseio.com
      auth: my-key
      path: "group/{{entry_field}}"
      grouping: yes|no
      key: "{{entry_field}}"
      fields:
          - title
          - url
```

The grouping parameter enables automatic parsing of titles and creating of an additional top level directory. For instance, two entries titled "The Beatles - Abbey Road" and "The Beatles - Help!" will be grouped automatically under "The Beatles".

The key parameter sets a key for an entity. If not set, the key will be assigned automatically by Firebase.

You may use jinja tags in the <i>path</i> and <i>key</i> parameters.

Full Firebase path will look like this: <i>storage/path/grouping/key</i>, where only storage is mandatory.

To add custom fields, use the [set](http://flexget.com/wiki/Plugins/set) plugin:
```
  set:
    datetime: "{{ now }}"
    domain: '{% set domain = url.split("://")[1].split("/")[0].replace("www.", "") %}{{ domain }}'
  firebase:
    fields:
      - title
      - domain
      - datetime
```
