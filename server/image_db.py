import pymongo
import gridfs


class DataBaseImg(object):
    db_client = pymongo.MongoClient('mongodb://localhost:27017')
    current_db = db_client['wb_user_inf']
    fs = gridfs.GridFS(current_db)

    def __init__(self, img_inf, file):
        self.img_inf = img_inf
        self.file = file

    def adding_image(self):
        self.fs.put(self.file, filename=self.img_inf['filename'], feels_like=self.img_inf['feels_like'],
                    style=self.img_inf['style'], email=self.img_inf['email'])

    def count(self, email):
        files = list(self.current_db.fs.files.find({'email': email}))
        count = len(list(files))
        return files, count

    def send_images(self, file):
        image = self.fs.get(file['_id']).read()

        return {'filename': file['filename'], 'feels_like': file['feels_like'],
                'style': file['style']}, image
# a, b = DataBaseImg(None, None).count('kuchuk758@mail.ru')
# print(DataBaseImg(None,None).send_images(a[3]))