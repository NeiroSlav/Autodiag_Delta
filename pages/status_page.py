from init import *


@app.route('/status')
def status_page():
    tokens = []
    users = []

    for number, token in Token._dict.items():
        time_ = int(time.time()) - token._last_active
        time_ = "%02d:%02d" % ((time_ // 60), (time_ % 60))
        username = token.gcdb_data.username
        tokens.append(f'token: {token} time: {time_}')
        users.append(f'user: {username}')

    return render_template(
        'status.html',
        tokens=tokens,
        users=users,
        changes_list=reversed(Token.changes_list),
        title='Статус',
        topinfo='Активные токены:',
        rightinfo='Кто там что дёргал:'
    )
