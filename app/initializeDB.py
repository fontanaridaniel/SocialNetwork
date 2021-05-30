from datetime import datetime
import multiprocessing
import shutil, os, json, requests
from random import randint
from random_word import RandomWords
from RandomWordGenerator import RandomWord
import multiprocessing
from app.models import Comment, Follower, Message, User, Post, Like, Chat, addUser, Category, addPost
from multiprocessing import Pool
from app import db

def movePosts():
    POST_LIST = Post.query.all()
    for post in POST_LIST:
        shutil.copyfile(f"app/static/users/{post.owner.username}/posts/{post.id}.jpg",f"app/data/initDB/posts/{post.id}.jpg")
        print("COPIED!")

def moveUsers():
    USER_LIST = User.query.all()
    for user in USER_LIST:
        shutil.copyfile(f"app/static/users/{user.username}/imageUser.jpg",f"app/data/initDB/users/{user.username}.jpg")
        print("COPIED!")

def setImages():
    USER_LIST = User.query.all()
    for user in USER_LIST:
        shutil.copyfile(f"app/data/initDB/users/{user.username}.jpg",f"app/static/users/{user.username}/imageUser.jpg",)
        print("USER COPIED!")
    POST_LIST = Post.query.all()
    for post in POST_LIST:
        try:
            shutil.copyfile(f"app/data/initDB/posts/{post.id}.jpg",f"app/static/users/{post.owner.username}/posts/{post.id}.jpg")
        except:
            pass
        print("POST COPIED!")

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def resetDB():
    try:
        shutil.rmtree("app/static/users")
        os.remove('app/data/data.db')
    except:
        pass
    for user in User.query.all():
        db.session.delete(user)
        print("Deleted USER")
    for post in Post.query.all():
        db.session.delete(post)
        print("Deleted POST")
    for category in Category.query.all():
        db.session.delete(category)
        print("Deleted CATEGORY")
    for comment in Comment.query.all():
        db.session.delete(comment)
        print("Deleted COMMENT")
    for like in Like.query.all():
        db.session.delete(like)
        print("Deleted LIKE")
    for follow in Follower.query.all():
        db.session.delete(follow)
        print("Deleted FOLLOWER")
    for chat in Chat.query.all():
        db.session.delete(chat)
        print("Deleted CHAT")
    for message in Message.query.all():
        db.session.delete(message)
        print("Deleted MESSAGE")
    db.session.commit()

def initDB():
    os.mkdir("app/static/users")
    with open('app/data/data.json') as json_file:
        data = json.load(json_file)
        x = 0
        for user in data["data"]:
            print("[1] ADDED USER:" + str(x) + "/" + str(len(data["data"])))
            x+=1
            user = User(
                name=user[1].strip(),
                lastname=user[2].strip(),
                username=user[2].strip()+user[1].strip(),
                email=user[3].strip(),
                password="qwerty".strip(),
            )
            os.mkdir("app/static/users/" + user.username)
            os.mkdir("app/static/users/" + user.username + "/posts")
            addUser(user=user)

def setImage():
    USER_LIST = User.query.all()
    IMAGE_LIST = [0]
    i = 1
    for user in USER_LIST:
        print("[" + str(1) + "] SET IMAGE:"+str(i)+"/100")
        i+=1
        image_id = 0
        while image_id in IMAGE_LIST:
            response = requests.get("https://source.unsplash.com/320x320/?portrait,person,female,male")
            image_id = response.url.split("photo-")[1].split("?crop")[0]
        IMAGE_LIST.append(image_id)
        file = open("app/static/users/" + user.username + "/imageUser.jpg", "wb")
        file.write(response.content)
        file.close()

def addPosts(thread):
    USER_LIST = User.query.all()
    r = RandomWords()
    for i in range(0,250):
        print("[" + str(thread) + "] ADDED POST:"+str(i)+"/250")
        user = USER_LIST[randint(0,len(USER_LIST)-1)]
        post = Post(
            date=datetime.now(),
            owner=user,
        )
        try:
            post.title = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10, minLength=5, maxLength=20).capitalize()
        except:
            post.title = "Ciao"
        category = Category(
            name=post.title.strip().lower()
        )
        post.category = category
        addPost(user=user, post=post)

def addFollow(thread):
    USER_LIST1 = USER_LIST2 = User.query.all()
    for i in range(0,1000):
        print("[" + str(thread) + "] ADDED FOLLOW: " + str(i) + "/1000")
        USER_LIST1[randint(0,len(USER_LIST1)-1)].toggle_follow(USER_LIST2[randint(0,len(USER_LIST2)-1)])


def addLikes(thread=1):
    POST_LIST = Post.query.all()
    POST_LIST = chunkIt(POST_LIST, 4)
    USER_LIST = User.query.all()
    num = 0
    for post in POST_LIST[thread-1]:
        num += 1
        max = randint(0,len(USER_LIST)-1)
        for _ in range(0, max):
            USER_LIST[randint(0,len(USER_LIST)-1)].toggle_like(post)
        print("[" + str(thread) + "] LIKED POST: " + str(num) + "/" + str(len(POST_LIST[thread-1])))
