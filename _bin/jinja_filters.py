import json
import jsonpickle

def slugify_filter(s):
    return s.lower().replace(" ", "-").replace(",", "")

def debug(thing):
  return f"<script>console.log({json.dumps(json.loads(jsonpickle.encode(thing)), indent=2)});</script>"
