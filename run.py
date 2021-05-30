from shutil import move
from app.models import User, addUser
from app import app, socketio, db
from app.initializeDB import setImage, addFollow, addPosts, resetDB, initDB, addLikes, movePosts, moveUsers, setImages
from multiprocessing import Pool, pool
import timeit

if __name__ == "__main__":
    # socketio.run(
    #     app, ssl_context=("cert.pem", "key.pem"), port=443, host="0.0.0.0", debug=False
    # )

    if False:
        tic = timeit.default_timer()
        if True:
            resetDB()
            db.create_all()
        initDB()        
        p = Pool()
        p.map(addPosts, [1, 2, 3, 4])
        p.map(addFollow, [1, 2])
        p.map(addLikes, [1, 2, 3, 4])
        setImages()
        addUser(User(name="David",lastname="Agostini",username="agostinidavid",email="agostini.david@gmail.com",password="qwerty".strip()))
        addUser(User(name="Daniel",lastname="Fontanari",username="fontanaridaniel",email="fontanaridaniel@gmail.com",password="qwerty".strip()))
        tac = timeit.default_timer()
        db.session.commit()
        print("Elapsed seconds: " + str(tac - tic))
        
    socketio.run(app, port=80, host="0.0.0.0", debug=False)
