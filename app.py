from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Post, Comment, followers
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    posts = Post.query.filter_by(is_private=False, is_hidden=False).all()
    return render_template('index.html', posts=posts)

@app.route('/feed')
@login_required
def feed():
    posts = Post.query.join(followers, (followers.c.followed_id == Post.user_id))\
        .filter(followers.c.follower_id == current_user.id)\
        .all()
    return render_template('index.html', posts=posts)

@app.route('/tag/<tag>')
def tag_filter(tag):
    posts = Post.query.filter_by(tag=tag).all()
    return render_template('index.html', posts=posts)

@app.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    current_user.followed.append(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        existing_user = User.query.filter_by(username=request.form['username']).first()

        if existing_user:
            return "Пользователь уже существует!"

        user = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password'])
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            tag=request.form['tag'],
            is_private=True if request.form.get('private') else False,
            is_hidden=True if request.form.get('hidden') else False,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    new_comment = Comment(
        content=request.form['content'],
        user_id=current_user.id,
        post_id=post_id
    )
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    followers_count = user.followers.count()

    # 📊 Статистика
    posts_count = len(posts)
    likes_count = sum([post.liked_by.count() for post in posts])

    return render_template(
        'profile.html',
        user=user,
        posts=posts,
        followers=followers_count,
        posts_count=posts_count,
        likes_count=likes_count
    )

@app.route('/like/<int:post_id>')
@login_required
def like(post_id):
    post = Post.query.get(post_id)

    if post not in current_user.liked:
        current_user.liked.append(post)
        db.session.commit()

    return redirect(request.referrer)

@app.route('/search')
def search():
    query = request.args.get('q')
    posts = Post.query.filter(
        Post.title.contains(query) | Post.content.contains(query)
    ).all()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)