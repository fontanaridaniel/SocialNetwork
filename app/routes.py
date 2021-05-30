from flask import render_template, flash, redirect, url_for, request
from app import (
    app,
    db,
    bcrypt,
    login_manager,
    logout_user,
    login_required,
    socketio,
    emit,
    join_room,
    leave_room,
)
from app.models import (
    ADMINS,
    ADMIN_deletePost,
    ADMIN_getAllPosts,
    ADMIN_getAllUsers,
    ADMIN_getAllChats,
    Category,
    Post,
    User,
    Message,
    Follower,
    Chat,
    Comment,
    Like,
    addPost,
    addUser,
    addComment,
    addChat,
    compressImage,
    search_Users,
    search_Category,
    top3_users,
    getChatList,
    addMessage,
    getInitMessages,
)
from flask_login import login_user, UserMixin, current_user
import os, urllib, requests
from werkzeug.utils import secure_filename
from datetime import datetime
import shutil


@login_manager.user_loader
def load_user(id):
    if not id == "None":
        return User.query.get(int(id))
    return redirect(url_for("login_page"))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login_page"))


@app.route("/")
def index():
    return redirect(url_for("home_page"))


@app.route("/signup")
def signup_page(msg=""):
    return render_template("signup.html", msg=msg)


@app.route("/signup_form", methods=["POST"])
def signup_form():
    if request.form["passwordInput"] != request.form["confirmPasswordInput"]:
        return redirect(url_for("signup_page", msg="Le password non coincidono"))
    user = User(
        name=request.form["nameInput"].strip(),
        lastname=request.form["lastnameInput"].strip(),
        username=request.form["usernameInput"].strip(),
        email=request.form["emailInput"].strip(),
        password=request.form["passwordInput"].strip(),
    )
    msg = addUser(user)
    if msg == "":
        user = User(
            email=request.form["emailInput"].strip(),
            password=request.form["passwordInput"].strip(),
        )
        if user.login():
            user = User.query.filter_by(email=user.email).first()
            login_user(user, remember=True)
            if os.path.exists(f"app/static/users/{user.username}/imageUser.jpg"):
                return redirect(url_for("home_page"))
            return render_template("setProfileImage.html", user=user)
    return redirect(url_for("signup_page", msg=msg))


@app.route("/setProfileImage", methods=["POST"])
def setProfileImage():
    url = f"https://eu.ui-avatars.com/api/?name={current_user.name}+{current_user.lastname}&bold=true&size=512"
    r = requests.get(url, allow_redirects=True)
    try:
        uploaded_file = request.files["profileImageFile"]
        if len(uploaded_file.filename) == 0:
            open(f"app/static/users/{current_user.username}/imageUser.jpg", "wb").write(
                r.content
            )
        elif uploaded_file.filename != None:
            uploaded_file.save(
                f"app/static/users/{current_user.username}/imageUser.jpg"
            )
    except:
        r = requests.get(url, allow_redirects=True)
        open(f"app/static/users/{current_user.username}/imageUser.jpg", "wb").write(
            r.content
        )
    compressImage(
        name="imageUser.jpg",
        pathImg=f"app/static/users/{current_user.username}/",
        size=320,
    )

    return redirect(url_for("home_page"))


@app.route("/login")
def login_page(msg=""):
    return render_template("login.html", msg=msg)


@app.route("/login_form", methods=["POST"])
def login_form():
    user = User(
        email=request.form["emailInput"].strip(),
        password=request.form["passwordInput"].strip(),
    )
    if user.login():
        user = User.query.filter_by(email=user.email).first()
        login_user(user, remember=True)
        if os.path.exists(f"app/static/users/{user.username}/imageUser.jpg"):
            return redirect(url_for("home_page"))
        return render_template("setProfileImage.html", user=user)
    return redirect(url_for("login_page", msg="Username o Password errati"))


@app.route("/createPost")
@login_required
def createPost_page():
    return render_template("createPost.html")


@app.route("/createPost_form", methods=["POST"])
@login_required
def createPost_form():
    user = User.query.filter_by(username=current_user.username).first()
    category = Category.query.filter_by(name=request.form["category"].lower().strip()).first()
    if not category:
        category = Category(
            name=request.form["category"].lower().strip()
        )
    post = Post(
        title=request.form["title"],
        date=datetime.now(),
        owner=user,
        category=category
    )
    addPost(user=current_user, post=post)
    try:
        uploaded_file = request.files["postImageFile"]
        if uploaded_file.filename != None:
            uploaded_file.save(
                f"app/static/users/{current_user.username}/posts/{post.id}.jpg"
            )
    except:
        pass
    compressImage(
        name=str(post.id) + ".jpg",
        pathImg=f"app/static/users/{current_user.username}/posts/",
        size=640,
    )
    return redirect(url_for("home_page"))


@app.route("/post_component")
@login_required
def post_component():
    post_list = current_user.getAllPosts()
    return render_template("components/post_component.html", post_list=post_list)


@app.route("/profile_component")
@login_required
def profile_component():
    username = request.args.get("jsdata")
    if username == "" or username == None:
        return render_template("components/profile_component.html")
    user = User.query.filter_by(username=username).first()
    feedPosts = user.getAllFeedPost()
    followers = user.followers()
    following = user.following()
    isFollowing = current_user.isFollowing(user)
    return render_template(
        "components/profile_component.html",
        feedPosts=feedPosts,
        profile_user=user,
        profile_following=following,
        profile_followers=followers,
        profile_isFollowing=isFollowing,
    )


@app.route("/toggle_follow")
@login_required
def toggle_follow():
    username = request.args.get("jsdata")
    user = User.query.filter_by(username=username).first()
    current_user.toggle_follow(user=user)
    followers = user.followers()
    following = user.following()
    isFollowing = current_user.isFollowing(user)
    return render_template(
        "components/profile_component.html",
        profile_user=user,
        profile_following=following,
        profile_followers=followers,
        profile_isFollowing=isFollowing,
    )


@app.route("/toggle_like")
@login_required
def toggle_like():
    id_post = request.args.get("jsdata")
    post = Post.query.filter_by(id=id_post).first()
    current_user.toggle_like(post)
    return redirect(url_for("home_page"))


@app.route("/search_component")
@login_required
def search_component():
    text = request.args.get("jsdata")
    if text == "":
        return render_template("components/search_component.html")
    search_users = search_Users(text=text)
    uname = False
    if text[0] == "@":
        uname = True
    return render_template(
        "components/search_component.html", search_users=search_users, uname=uname
    )


@app.route("/search_category_component")
@login_required
def search_category_component():
    text = request.args.get("jsdata")
    if text == "":
        search_category = search_Category(text=text)
        return render_template("components/search_category_component.html", posts=search_category)
    if text[0] == "#":
        text = text[1:]
    search_category = search_Category(text=text)
    return render_template(
        "components/search_category_component.html", posts=search_category[:25]
    )


@app.route("/chat")
@login_required
def chat_page_noParams():
    chatList = getChatList(user=current_user)
    return render_template("chat.html", chatList=chatList)


@app.route("/chat/<username>")
@login_required
def chat_page_withParams(username):
    user = User.query.filter_by(username=username).first()
    if not user:  # User does not exists
        return redirect(url_for("home_page"))
    chat, messages = getInitMessages(user1=user, user2=current_user)
    if not chat:  # Chat does not exist
        addChat(Chat(id_user1=current_user.id, id_user2=user.id))
        chat, messages = getInitMessages(user1=user, user2=current_user)
    chatList = getChatList(user=current_user)
    feedPosts = user.getAllFeedPost()
    followers = user.followers()
    following = user.following()
    isFollowing = current_user.isFollowing(user)
    return render_template(
        "chat.html",
        id_chat=chat.id,
        chat=chat,
        chatList=chatList,
        messages=messages,
        receiver=user,
        feedPosts=feedPosts,
        profile_user=user,
        profile_following=following,
        profile_followers=followers,
        profile_isFollowing=isFollowing,
    )


@app.route("/chat_list_component")
@login_required
def chat_list_component():
    chatList = getChatList(user=current_user)
    return render_template("components/chat_list_component.html", chatList=chatList)


@app.route("/chat_msg_component")
@login_required
def chat_msg_component():
    username = request.args.get("jsdata")
    user = User.query.filter_by(username=username).first()
    chat, messages = getInitMessages(user1=user, user2=current_user)
    return render_template(
        "components/chat_msg_component.html", messages=messages, receiver=user, chat=chat
    )


@socketio.on("joined", namespace="/chat")
def joined(data):
    try:
        room = data["room"]
        join_room(room)
        emit("status", {}, room=room)
    except:
        pass


@socketio.on("left", namespace="/chat")
def left(data):
    room = data["room"]
    leave_room(room)
    emit("status", {}, room=room)


@socketio.on("send_msg", namespace="/chat")
def chat(data, methods=["GET", "POST"]):
    id_chat = data["id_chat"]
    msg = urllib.parse.unquote_plus(data["data"])
    room = data["room"]
    username = current_user.username
    message = Message(
        id_chat=id_chat, id_sender=current_user.id, msg=msg, date=datetime.now()
    )
    addMessage(message)
    user = User.query.filter_by(username=username).first()
    x = {}
    num = 0
    x[num] = {}
    x[num]["id"] = message.id
    x[num]["id_chat"] = message.id_chat
    x[num]["id_sender"] = message.id_sender
    x[num]["msg"] = msg
    x[num]["date"] = message.date
    emit("receive", x, room=room)
    emit("notify", msg, room="notify3")


@socketio.on("joined", namespace="/notify")
def joined(data):
    room = "notify"+str(data["room"])
    join_room(room)
    emit("notify", "ciao", room=room)


@socketio.on("joined", namespace="/notify")
def joined(data):
    room = "notify"+str(data["room"])
    join_room(room)


@socketio.on("send_notify", namespace="/notify")
def send_notify(data):
    emit("notify", {
        "msg":data["data"],
        "user": {
            "name":current_user.name, 
            "lastname": current_user.lastname,
            "username":current_user.username
            },
        }, room="notify"+data["room"])


@app.route("/profile")
@login_required
def myProfile_page():
    feedPosts = current_user.getAllFeedPost()
    followers = current_user.followers()
    following = current_user.following()
    return render_template(
        "myProfile.html",
        feedPosts=feedPosts,
        following=following,
        followers=followers,
    )


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for("login_page"))


@app.route("/home")
@login_required
def home_page():
    follow_users = current_user.follow_users()
    post_list = current_user.getAllPosts()
    return render_template("home.html", follow_users=follow_users, post_list=post_list[:25], top_users=top3_users())


@app.route("/home_top_component")
@login_required
def home_top_component():
    return render_template(
        "components/home_top_components.html", top_users=top3_users()
    )


@app.route("/admin")
@login_required
def admin_page():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    return render_template("admin.html", posts=ADMIN_getAllPosts())


@app.route("/deletePost")
@login_required
def deletePost():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    ADMIN_deletePost(post_id=request.args.get("id_post"))
    return render_template("admin.html", db_posts=True, posts=ADMIN_getAllPosts())


@app.route("/selectDB_component")
@login_required
def selectDB_component():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    db = request.args.get("jsdata")
    if db == "users":
        return render_template(
            "components/admin_db_component.html",
            db_users=True,
            users=ADMIN_getAllUsers(),
        )
    elif db == "posts":
        return render_template(
            "components/admin_db_component.html",
            db_posts=True,
            posts=ADMIN_getAllPosts(),
        )
    elif db == "chats":
        return render_template(
            "components/admin_db_component.html",
            db_chats=True,
            chats=ADMIN_getAllChats(),
        )
    return ""


@app.route("/modifyPost_form", methods=["POST"])
@login_required
def modifyPost_form():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    post = Post.query.filter_by(id=request.form["id_post"]).first()
    user = User.query.filter_by(id=request.form["id_user"]).first()
    post.title = request.form["title"]
    if request.files["postImageFile"]:
        try:
            uploaded_file = request.files["postImageFile"]
            if uploaded_file.filename != None:
                uploaded_file.save(
                    f"app/static/users/{user.username}/posts/{post.id}.jpg"
                )
        except:
            pass
        try:  # No image were provided
            compressImage(
                name=str(post.id) + ".jpg",
                pathImg=f"app/static/users/{user.username}/posts/",
                size=640,
            )
        except:
            pass
    db.session.commit()
    return render_template("admin.html", db_posts=True, posts=ADMIN_getAllPosts())


@app.route("/modifyUser_form", methods=["POST"])
@login_required
def modifyUser_form():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    user = User.query.filter_by(id=request.form["id_user"]).first()
    oldUsername = user.username
    user.name = request.form["name"]
    user.lastname = request.form["lastname"]
    user.username = request.form["username"]
    user.email = request.form["email"]
    if not oldUsername == user.username:
        os.rename(
            f"app/static/users/{oldUsername}", f"app/static/users/{user.username}"
        )
    if request.files["postImageFile"]:
        url = f"https://eu.ui-avatars.com/api/?name={user.name}+{user.lastname}&bold=true&size=512"
        r = requests.get(url, allow_redirects=True)
        try:
            uploaded_file = request.files["postImageFile"]
            if len(uploaded_file.filename) == 0:
                open(f"app/static/users/{user.username}/imageUser.jpg", "wb").write(
                    r.content
                )
            elif uploaded_file.filename != None:
                uploaded_file.save(f"app/static/users/{user.username}/imageUser.jpg")
        except:
            r = requests.get(url, allow_redirects=True)
            open(f"app/static/users/{user.username}/imageUser.jpg", "wb").write(
                r.content
            )
        compressImage(
            name="imageUser.jpg",
            pathImg=f"app/static/users/{user.username}/",
            size=320,
        )
    db.session.commit()

    return render_template("admin.html", db_users=True, users=ADMIN_getAllUsers())


@app.route("/ADMIN_delete_chat")
@login_required
def ADMIN_delete_chat():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    Message.query.filter_by(id_chat=request.args.get("chat_id")).delete()
    Chat.query.filter_by(id=request.args.get("chat_id")).delete()
    db.session.commit()
    return render_template(
        "components/admin_db_component.html", db_chats=True, chats=ADMIN_getAllChats()
    )


@app.route("/ADMIN_delete_post")
@login_required
def ADMIN_delete_post():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    Like.query.filter_by(post_id=request.args.get("post_id")).delete()
    Post.query.filter_by(id=request.args.get("post_id")).delete()
    Comment.query.filter_by(post_id=request.args.get("post_id")).delete()
    db.session.commit()
    return render_template(
        "components/admin_db_component.html", db_posts=True, posts=ADMIN_getAllPosts()
    )


@app.route("/ADMIN_delete_user")
@login_required
def ADMIN_delete_user():
    if current_user.email not in ADMINS:
        return url_for("home_page")
    Like.query.filter_by(user_id=request.args.get("user_id")).delete()
    Post.query.filter_by(owner_id=request.args.get("user_id")).delete()
    Follower.query.filter_by(follower_id=request.args.get("user_id")).delete()
    Follower.query.filter_by(following_id=request.args.get("user_id")).delete()
    chats = Chat.query.filter(
        (Chat.id_user1 == request.args.get("user_id"))
        | (Chat.id_user2 == request.args.get("user_id"))
    ).all()
    for chat in chats:
        Message.query.filter_by(id_chat=chat.id).delete()
    Chat.query.filter(
        (Chat.id_user1 == request.args.get("user_id"))
        | (Chat.id_user2 == request.args.get("user_id"))
    ).delete()
    username = User.query.filter_by(id=request.args.get("user_id")).first().username
    User.query.filter_by(id=request.args.get("user_id")).delete()
    shutil.rmtree(f"app/static/users/{username}")
    db.session.commit()
    return render_template(
        "components/admin_db_component.html",
        db_users=True,
        users=ADMIN_getAllUsers(),
    )


@app.route("/profile_post_component")
@login_required
def profile_post_component():
    post = Post.query.filter_by(id=request.args.get("post_id")).first()
    return render_template(
        "components/profile_post_component.html",
        post=post,
        liked=current_user.isLiked(post=post),
        likes=post.likes(),
    )


@app.route("/profile_comments_component")
@login_required
def profile_comments_component():
    post = Post.query.filter_by(id=request.args.get("post_id")).first()
    comments = post.getAllComments()
    comments.reverse()
    return render_template(
        "components/profile_comments_component.html", post=post, comments=comments
    )


@app.route("/add_comment")
@login_required
def add_comment():
    post = Post.query.filter_by(id=request.args.get("post_id")).first()
    addComment(
        Comment(
            owner=current_user,
            post=post,
            text=request.args.get("text"),
            date=datetime.now(),
        )
    )
    comments = post.getAllComments()
    comments.reverse()
    return render_template(
        "components/profile_comments_component.html", post=post, comments=comments
    )


@app.route("/likes")
@login_required
def likes_page():
    likes = current_user.getLikedPost()
    likes.reverse()
    return render_template(
        "likes.html",
        likes=likes,
    )


@app.route("/change_personal")
@login_required
def change_personal():
    attr = request.args.get("attr")
    value = request.args.get("value")
    user = User.query.filter_by(id=current_user.id).first()
    if(attr == "name"):
        user.name = value.strip().capitalize()
    elif(attr == "lastname"):
        user.lastname = value.strip().capitalize()
    elif(attr == "username"):
        #CONTROLLI
        if current_user.username == value:
            return ""
        if not User.query.filter_by(username=value).first():
            os.rename(
                f"app/static/users/{user.username}", f"app/static/users/{value}"
            )
            user.username = value
        else:
            return "Username già presente"
    elif(attr == "email"):
        #CONTROLLI
        if current_user.email == value:
            return ""
        if not User.query.filter_by(email=value).first():
            user.email = value
        else:
            return "Email già presente"
    else:
        return "errore generico"
    db.session.commit()
    return ""


@app.route("/change_image", methods=["POST"])
@login_required
def change_image():
    if request.files["profileImageFile"]:
        url = f"https://eu.ui-avatars.com/api/?name={current_user.name}+{current_user.lastname}&bold=true&size=512"
        r = requests.get(url, allow_redirects=True)
        try:
            uploaded_file = request.files["profileImageFile"]
            if len(uploaded_file.filename) == 0:
                open(f"app/static/users/{current_user.username}/imageUser.jpg", "wb").write(
                    r.content
                )
            elif uploaded_file.filename != None:
                uploaded_file.save(f"app/static/users/{current_user.username}/imageUser.jpg")
        except:
            r = requests.get(url, allow_redirects=True)
            open(f"app/static/users/{current_user.username}/imageUser.jpg", "wb").write(
                r.content
            )
        compressImage(
            name="imageUser.jpg",
            pathImg=f"app/static/users/{current_user.username}/",
            size=320,
        )
    db.session.commit()
    return redirect(url_for("editProfile_page"))


@app.route("/change_password")
@login_required
def change_password():
    oldPdw = request.args.get("oldPdw")
    newPdw = request.args.get("newPdw")
    if User(password=oldPdw.strip()).check_password(password=current_user.password):#password vecchia inserita correttamente
        current_user.set_password(newPdw)
        db.session.commit()
        return ""
    return "error" 


@app.route("/editProfile")
@login_required
def editProfile_page():
    return render_template("editProfile.html")


@app.route("/category")
@login_required
def category_page():
    posts = Post.query.all()
    posts.reverse()
    return render_template("category.html", posts=posts[:50])