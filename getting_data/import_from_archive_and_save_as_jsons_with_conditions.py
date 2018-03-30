# Here we are going to import all declarations in a relative small archive
# Then go through it and save as separate jsons only those files which we need (here - annual declarations for 2016)
# Then you can read these files directly using some identifier (here - document id)

from bz2file import open as bzopen
import json

# the archive can be downloaded from https://declarations.com.ua/static/data/full_export.json.bz2
with bzopen("full_export.json.bz2", "rt", encoding = "utf8") as fp:
    for i, l in enumerate(fp):
        print i
        r = json.loads(l) # load one declaration
        if (not r['related_entities']['documents']['corrected']): # check that this declaration was not corrected afterwards
            if (r['infocard']['document_type'] == unicode("Щорічна", "utf-8")): # We need only annual declarations
                # saving jsons as separate files (depending on the structure of json)
                if ('step_0' in r['unified_source'].keys()):
                    if (r['unified_source']['step_0']['declarationYear1'] == unicode(str(2016), "utf-8")): # only 2016
                        with open(".../jsons/" + r['infocard']['id'] + ".json", "w") as fw: 
                            json.dump(r, fw)
                elif ('step_0' in r['unified_source']['data'].keys()):
                    if (r['unified_source']['data']['step_0']['declarationYear1'] == unicode(str(2016), "utf-8")):
                        with open(".../jsons/" + r['infocard']['id'] + ".json", "w") as fw:
                            json.dump(r, fw)
