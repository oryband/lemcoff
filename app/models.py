import mongoengine

from app import db


class Page(db.Document):
    title = db.StringField(max_length=255)

    def __unicode__(self):
        return self.title


class Post(db.Document):
    # Delete all posts in page when page gets deleted
    page = db.ReferenceField(Page, reverse_delete_rule=mongoengine.CASCADE)
    order = db.IntField()
    title = db.StringField(max_length=255)
    body = db.StringField()

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-order', 'title'],
        'ordering': ['-order']
    }


# class Member(db.Document):
#     order = db.IntField()  # Order in list.
#     name = db.StringField(max_length=255)
#     email = db.EmailField(max_length=255)
#     body = db.StringField()
#     # TODO img =

#     def __repr__(self):
#         return self.name

#     meta = {
#         # 'allow_inheritance': True,
#         'indexes': ['-order', 'name'],
#         'ordering': ['-order']
#     }
