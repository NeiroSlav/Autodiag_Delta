from init import *


@app.route('/status')
def status_page():
    token_dict = token_dict_image_get()
    tokens = []
    timeouts = []
    usernames = []

    for token, data in token_dict.items():
        tokens.append(token)
        timeout = int(time.time()) - data['_last_active']
        timeout = "%02d:%02d" % ((timeout // 60), (timeout % 60))
        timeouts.append(timeout)
        usernames.append(data['gcdb_data'].username)

    context = {
        'tokens': tokens,
        'timeouts': timeouts,
        'usernames': usernames}

    return render_template(
        'status.html',
        context=context,
        title='Статус',
        topinfo='Активные токены:')
