import builder


def www(data):
    builder.publish(data, push_www=True, push_app=False)


def app(data):
    builder.publish(data, push_www=False, push_app=True)


def all(data):
    builder.publish(data, push_www=True, push_app=True)


def refresh(data):
    builder.publish(data, push_www=False, push_app=False)

def validate(data):
    builder.validate(data)
