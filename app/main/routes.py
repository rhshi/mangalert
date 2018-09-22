from datetime import datetime
from flask import flash, redirect, render_template, request, url_for, current_app, jsonify
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.main.forms import EditProfileForm, MDListForm, PostForm, MessageForm
from app.models import User, Post, Message, Notification, Manga
from app.src.utils import createLink, diffDay


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, title=form.title.data, link=form.link.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post is now live!')
        return redirect(url_for('main.index'))
    if current_user.is_authenticated:
        following_online = [user for user in User.query.all() if diffDay(user, current_app.config['ONLINE_LAST']) and user in list(current_user.user_followed)]
        page = request.args.get('page', 1, type=int)
        posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main.index', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('main.index', page=posts.prev_num) \
            if posts.has_prev else None
        return render_template('index.html', type='following online', users=following_online, form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)
    else:
        return render_template('index.html')


@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    popular_users = {user: user.followers.count() for user in User.query.all()}
    sorted_pop =  sorted(popular_users.items(), key=lambda kv: kv[1])
    users = list(zip(*sorted_pop))[0][:20]
    return render_template("explore.html", type='popular users', users=users, title='explore', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)
    

@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = MDListForm()
    if form.validate_on_submit():
        current_user.mdlist = form.mdlist.data
        current_user.launch_task('get_follows', 'getting follows...', timeout='1h')
        db.session.commit()
        flash('thank you for connecting your mdlist.')
        return redirect(url_for('main.user', username=current_user.username))
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', title=user.username, user=user, form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        if form.mdlist.data and form.mdlist.data != current_user.mdlist:
            current_user.mdlist = form.mdlist.data
            for manga in Manga.query.filter(Manga.followers.any(User.username==current_user.username)).all():
                manga.followers.remove(current_user)
            current_user.launch_task('get_follows', 'getting follows...', timeout='1h')
            db.session.commit()
        elif form.mdlist.data and form.mdlist.data == current_user.mdlist:
            pass
        else:
            current_user.mdlist = None
            for manga in Manga.query.filter(Manga.followers.any(User.username==current_user.username)).all():
                manga.followers.remove(current_user)
            db.session.commit()
        flash('your changes have been saved')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='edit profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('user {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('you cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('you are now following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('user {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('you cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('you have unfollowed {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages()) 
        db.session.commit()
        flash('your message has been sent.')
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title='send message',
                           form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@bp.route('/follows')
@login_required
def follows():
    ongoing = Manga.query.join(Manga.followers).filter(User.username==current_user.username, Manga.ongoing==True).all()
    complete = Manga.query.join(Manga.followers).filter(User.username==current_user.username, Manga.ongoing==False).all()
    return render_template('manga_follows.html', ongoing=ongoing, complete=complete)








