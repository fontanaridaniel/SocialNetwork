from operator import pos
from app import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy import and_, or_
import os
from PIL import Image, ExifTags
from datetime import datetime

ADMINS = ["agostini.david@gmail.com", "fontanaridaniel@gmail.com", "admin@admin"]


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    posts = db.relationship("Post", backref="category")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    text = db.Column(db.String(260))
    date = db.Column(db.String(30))


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)


class Follower(db.Model):
    # Followere(follower=user, following=user)
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    following_id = db.Column(db.Integer)


class User(db.Model, UserMixin):
    # User(username=username, email=email, name=name, lastname=lastname, password=password)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    password = db.Column(db.String(255))
    comments = db.relationship("Comment", backref="owner")
    posts = db.relationship("Post", backref="owner")

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(password, self.password)

    def login(self):
        user = User.query.filter_by(email=self.email).first()
        try:
            user = User.query.filter_by(email=self.email).first()
            return self.check_password(password=user.password)
        except:
            pass
        return False

    def followers(self):
        return len(Follower.query.filter_by(following_id=self.id).all())

    def following(self):
        return len(Follower.query.filter_by(follower_id=self.id).all())

    def isFollowing(self, user):
        if Follower.query.filter_by(follower_id=self.id, following_id=user.id).first():
            return True
        return False

    def toggle_follow(self, user):
        if (
            Follower.query.filter_by(follower_id=self.id, following_id=user.id).delete()
            == 0
            and self.id != user.id
        ):
            db.session.add(Follower(follower_id=self.id, following_id=user.id))
        db.session.commit()

    def toggle_like(self, post):
        if Like.query.filter_by(user_id=self.id, post_id=post.id).delete() == 0:
            db.session.add(Like(user_id=self.id, post_id=post.id))
        db.session.commit()

    def isLiked(self, post):
        if Like.query.filter_by(user_id=self.id, post_id=post.id).first():
            return True
        return False

    def getAllPosts(self):
        following_id = Follower.query.filter_by(follower_id=self.id).all()
        following_id.append(Follower(follower_id=self.id, following_id=self.id))
        posts = []
        for i in following_id:
            post_list = Post.query.filter_by(owner_id=i.following_id).all()
            for x in post_list:
                posts.append(x)
        posts.sort(key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S.%f"))
        posts = [x for x in posts[::-1]]
        res = []
        for post in posts:
            x = []
            x.append(post)
            x.append(post.likes())
            x.append(self.isLiked(post))
            comments = post.getAllComments()
            comments.reverse()
            x.append(comments[:2])
            res.append(x)
        return res

    def getAllFeedPost(self):
        posts = Post.query.filter_by(owner_id=self.id).all()
        length = len(posts)
        s = length
        new_list = [None] * length
        for item in posts:
            s = s - 1
            new_list[s] = item
        return new_list

    def follow_users(self):
        follow_id = Follower.query.filter_by(follower_id=self.id).all()
        users = []
        for id in follow_id:
            users.append(User.query.filter_by(id=id.following_id).first())
        return users

    def getLikedPost(self):
        postLiked = Like.query.filter_by(user_id=self.id).all()
        allLikedPosts = []
        for post in postLiked:
            allLikedPosts.append(Post.query.filter_by(id=post.post_id).first())
        return allLikedPosts

    def isAdmin(self):
        return self.email in ADMINS


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user1 = db.Column(db.Integer)
    id_user2 = db.Column(db.Integer)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_chat = db.Column(db.Integer)
    id_sender = db.Column(db.Integer)
    msg = db.Column(db.String(1024))
    date = db.Column(db.String(30))


class Post(db.Model):
    # Post(user=User, title=title)
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    title = db.Column(db.String(80))
    date = db.Column(db.String(30))
    comments = db.relationship("Comment", backref="post")

    def getNumComments(self):
        return len(self.getAllComments())

    def getPostDate(self):
        diff = datetime.now() - datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S.%f")
        date = self.date
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if days > 0:
            date = date.split(" ")[0]
        else:
            if hours > 0:
                date = f"{hours}h fa"
            else:
                if minutes > 0:
                    date = f"{minutes}m fa"
                else:
                    if seconds == 0:
                        date = "ora"
                    else:
                        date = f"{seconds}s fa"
        return date

    def likes(self):
        return len(Like.query.filter_by(post_id=self.id).all())

    def getAllComments(self):
        return Comment.query.filter_by(post_id=self.id).all()


old_messages = []


def getMessages(id_chat, flag):
    global old_messages
    new_messages = Message.query.filter_by(id_chat=int(id_chat)).all()
    if len(new_messages) > len(old_messages):
        x = []
        for i in range(len(old_messages), len(new_messages)):
            x.append(new_messages[i])
        old_messages = new_messages
        return x
    return None


# Chat.query \
#     .filter((Chat.id_user1 == user1.id) | (Chat.id_user1 == user1.id)) \
#     .filter((Chat.id_user2 == user2.id) | (Chat.id_user2 == user2.id)) \
#     .all()


def getInitMessages(user1, user2):
    global old_messages
    chat = (
        Chat.query.filter((Chat.id_user1 == user1.id) | (Chat.id_user2 == user1.id))
        .filter((Chat.id_user1 == user2.id) | (Chat.id_user2 == user2.id))
        .all()
    )
    try:
        old_messages = Message.query.filter_by(id_chat=chat[0].id).all()
        return chat[0], old_messages
    except:
        return None, None


def getChatList(user):
    x = Chat.query.filter((Chat.id_user1 == user.id) | (Chat.id_user2 == user.id)).all()
    result = []
    for chat in x:
        date = ""
        try:
            date = (
                Message.query.filter_by(id_chat=chat.id)
                .order_by(Message.id.desc())
                .first()
                .date.split(" ")[1]
                .split(".")[0][:-3]
            )
        except:
            date = ""
        if user.id == chat.id_user1:
            result.append(
                [chat.id, User.query.filter_by(id=chat.id_user2).first(), date]
            )
        else:
            result.append(
                [chat.id, User.query.filter_by(id=chat.id_user1).first(), date]
            )
    return result


def addUser(user):
    global USER_LIST
    try:
        if User.query.filter_by(username=user.username).first():
            return "Username già presente"
    except:
        pass
    try:
        if User.query.filter_by(email=user.email).first():
            return "Email già presente"
    except:
        pass
    user.set_password(user.password)
    user.name = user.name.capitalize()
    user.lastname = user.lastname.capitalize()
    db.session.add(user)
    db.session.commit()
    if not os.path.exists(f"app/static/users/{user.username}"):
        os.makedirs(f"app/static/users/{user.username}")
    if not os.path.exists(f"app/static/users/{user.username}/posts"):
        os.makedirs(f"app/static/users/{user.username}/posts")
    USER_LIST = User.query.all()
    return ""


def addComment(comment):
    db.session.add(comment)
    db.session.commit()


def addPost(user, post):
    db.session.add(post)
    db.session.commit()
    if not os.path.exists(f"app/static/users/{user.username}/posts"):
        os.makedirs(f"app/static/users/{user.username}/posts")


def addMessage(message):
    db.session.add(message)
    db.session.commit()


def addChat(chat):
    db.session.add(chat)
    db.session.commit()


def freeId(user):
    return len(Post.query.all())


def search_Category(text):
    res = []
    list_post = Post.query.all()
    for post in list_post:
        if text.lower() in post.category.name.lower():
            res.append(post)
            if len(res) > 100:
                return res
    return res


def search_Users(text):
    uname = False
    if text[0] == "@":
        uname = True
        text = text.replace("@", "")
    list_user = USER_LIST
    res = []
    for user in list_user:
        if uname:
            if text.lower() in user.username.lower():
                res.append(user)
        else:
            if (
                text.lower() in f"{user.name.lower()} {user.lastname.lower()}"
                or text.lower() in f"{user.lastname.lower()} {user.name.lower()}"
            ):
                res.append(user)
        if len(res) > 5:
            return res
    return res


def top3_users():
    global USER_LIST
    list_user = USER_LIST
    list = []
    for i in list_user:
        list.append(i.followers())
    final_list = []
    index = 0
    try:
        for i in range(0, 3):
            max = -1
            user = []
            for j in range(0, len(list)):
                if list[j] > max:
                    index = j
                    max = list[j]

            list.remove(max)
            user.append(max)
            user.append(list_user[index])
            posts = Post.query.filter_by(owner_id=list_user[index].id).all()
            list_user.remove(list_user[index])
            posts = posts[-2:]
            posts.reverse()
            user.append(posts)
            final_list.append(user)
    except:
        pass

    USER_LIST = User.query.all()
    return final_list


def compressImage(name=None, pathImg=None, size=None):
    img = Image.open(pathImg + name)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except:
        pass

    width, height = img.size
    if width < height:
        left = (width - width) / 2
        top = (height - width) / 2
        right = (width + width) / 2
        bottom = (height + width) / 2
    else:
        left = (width - height) / 2
        top = (height - height) / 2
        right = (width + height) / 2
        bottom = (height + height) / 2

    img = img.crop((left, top, right, bottom))
    img = img.resize((size, size), Image.ANTIALIAS)
    img = img.convert("RGB")
    os.remove(pathImg + name)
    img.save(pathImg + name, quality=80, subsampling=0)


def ADMIN_getAllPosts():
    return Post.query.all()


def ADMIN_deletePost(post_id):
    Post.query.filter_by(id=post_id).delete()
    Like.query.filter_by(post_id=post_id).delete()
    db.session.commit()


def ADMIN_getAllUsers():
    return User.query.all()


def ADMIN_getAllChats():
    chats = Chat.query.all()
    res = []
    for chat in chats:
        res.append(
            [
                chat,
                User.query.filter_by(id=chat.id_user1).first(),
                User.query.filter_by(id=chat.id_user2).first(),
            ]
        )
    return res


db.create_all()

USER_LIST = User.query.all()