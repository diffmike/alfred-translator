#!python
# -*- coding: utf-8 -*-

import json
import sys
import os
import urllib
from workflow import Workflow3, ICON_WEB, web

def main(wf):
    args = wf.args[0]
    key = args.strip().lower()
    isEn = True if key[0] in 'abcdefghijklmnopqrstuvwxyz' else False
    lang = 'en-ru' if isEn else 'ru-en'

    def get_translations():
        params = 'lang=' + lang + '&text=' + urllib.quote(key.encode('utf8')) + '&key=' + os.environ['yandex_key']
        url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?' + params
        return web.get(url).json()
        
    data = wf.cached_data('translations_' + key, get_translations, max_age=3000)
    # log.debug(json.dumps(data, indent=4, sort_keys=True))

    tranlate_url = 'https://translate.google.com/#' + ('en/ru/' if isEn else 'ru/en/') + key
    for j in data['def']:
        for i in j['tr']:
            title = i['text']

            syn = []
            if 'syn' in i:
                for s in i['syn']: syn.append(s['text'])

            subtitle = ''
            means = []
            if 'mean' in i:
                for m in i['mean']: means.append(m['text'])
                subtitle = ', '.join(means)
            
            ex = []
            if 'ex' in i:
                for e in i['ex']: ex.append(e['text'] + ' = ' + e['tr'][0]['text'])
                subtitle = subtitle + '. ' + ', '.join(ex)

            it = wf.add_item(
                title = title,
                copytext = title,
                subtitle = subtitle,
                largetext = subtitle,
                arg = tranlate_url,
                quicklookurl = tranlate_url,
                valid = True,
                icon = 'dict.png'
            )
            mod = it.add_modifier('alt', 'Add to favorites')
            mod.setvar('fav_text', key)
            mod.setvar('fav_translation', title)

    if not data['def']: 
            wf.add_item(
                title = 'Translations did not found',
                subtitle = tranlate_url,
                arg = tranlate_url,
                quicklookurl = tranlate_url,
                valid = True,
                icon = 'gt.png'
            )
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
