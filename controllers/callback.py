import re

def addCallback(body, request):
    if 'callback' in request.args:
        callback = request.args.get('callback', 'error')
        if callback == 'error' or not re.match(r'callback\d+', callback):
            return '{"error" : "callback"}'
        return ('%s(%s);' % (callback, body))
    return body
