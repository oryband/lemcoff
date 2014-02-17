from mongoengine import CASCADE

from app import db


class Page(db.Document):
    title = db.StringField(max_length=255, choices=('research',
                                                    'publications',
                                                    'members',
                                                    'community',
                                                    'links'))
    summary = db.StringField()

    def __unicode__(self):
        return self.title


class Entry(db.Document):
    page = db.ReferenceField(Page, reverse_delete_rule=CASCADE)  # Delete all posts in page when page gets deleted
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


class Image(db.Document):
    caption = db.StringField(required=True, max_length=80)
    image = db.ImageField(required=True)

    def __unicode__(self):
        return self.caption
