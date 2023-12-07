from init import *


@app.route('/status')
def status_page():
    token_dict = token_dict_image_get()
    tokens = []
    users = []

    for token, data in token_dict.items():
        time_ = int(time.time()) - data['_last_active']
        time_ = "%02d:%02d" % ((time_ // 60), (time_ % 60))
        user = data['gcdb_data'].username
        tokens.append(f'token: {token} time: {time_}')
        users.append(f'user: {user}')

    return render_template(
        'status.html',
        tokens=tokens,
        users=users,
        changes_list=reversed(changes_list),
        title='Статус',
        topinfo='Активные токены:',
        rightinfo='Кто там что дёргал:'
    )
