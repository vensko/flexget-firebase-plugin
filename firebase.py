import logging, urllib, re

from datetime import datetime
from flexget import plugin
from flexget.event import event
from flexget.utils import json, requests
from flexget.utils.template import render_from_entry

log = logging.getLogger('firebase')

class OutputFirebase(object):
    """
    Usage:
        firebase:
            storage: https://my-storage.firebaseio.com
            auth: my-key
            path: "group/{{entry_field}}"
            grouping: yes|no
            key: "{{entry_field}}"
            fields:
                - title
                - url
    """

    schema = {
        'type': 'object',
        'properties': {
            'storage': {'type': 'string'},
            'auth': {'type': 'string'},
            'grouping': {'type': 'boolean', 'default': True},
            'key': {'type': 'string', 'default': ""},
            'path': {'type': 'string', 'default': ""},
            'fields': {'type': 'array', 'items': {'type': 'string'}, 'default': ['title','url']}
        },
        'additionalProperties': False
    }

    def on_task_output(self, task, config):
        for entry in task.accepted:
            item = {}

            for key in config['fields']:
                if entry.get(key):
                    item[key] = entry[key]

            try:
                path = [] if config['path'] == "" else [render_from_entry(config['path'], entry)]

                if config['grouping']:
                    group = entry['title'].replace(".", " ")
                    group = group.replace("_", " ")
                    group = group.split(" - ")[0]
                    group = group.split(",")[0]
                    group = group.split("#")[0]
                    group = group.split(":")[0]
                    group = group.split(" (")[0]
                    group = re.compile("[\d]+").split(group)[0]
                    group = group.strip()
                    item['group'] = group
                    path.append(group)

                if config['key']:
                    path.append(render_from_entry(config['key'], entry))
                    method = "put"
                else:
                    method = "post"

                path = urllib.quote("/".join(path))
                url = config['storage'] + "/" + path + ".json?auth=" + config['auth']

                log.verbose("Requesting Firebase: " + method.upper() + " " + url)
                log.verbose(item)

                response = requests.request(method, config['storage'] + "/" + path + ".json?print=pretty&auth=" + config['auth'], data=json.dumps(item))

                log.verbose('Firebase response: ' + response.text)

                if not response.status_code == 200:
                    entry.fail('http error')

            except Exception as e:
                entry.fail("exception: %s" % e)

@event('plugin.register')
def register_plugin():
    plugin.register(OutputFirebase, 'firebase', api_ver=2)
