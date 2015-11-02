# Firebase plugin for Flexget
Saves accepted flexget entries to Firebase.

# Usage
```
  firebase:
      storage: https://<storage>.firebaseio.com
      auth: <token>
      path: "group/{{entry_field}}"
      grouping: yes|no
      key: "{{entry_field}}"
      fields:
          - title
          - url
          - host: '{% set domain = url.split("://")[1].split("/")[0].replace("www.", "") %}{{ domain }}'
```
All fields are optional except <i>storage</i>.

The grouping parameter enables automatic parsing of titles and creating of an additional top level directory. For instance, two entries titled "The Beatles - Abbey Road" and "The Beatles - Help!" will be grouped automatically under "The Beatles".

The key parameter sets a key for an entity. If not set, the key will be assigned automatically by Firebase.

You may use jinja tags in the <i>path</i> and <i>key</i> parameters.
