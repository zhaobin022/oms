from celery import task

@task()
def add(x, y):
    with open('/tmp/a.txt' , 'w') as f:
        f.write('aaaaaaaaaaaaaaaaaaaaaaa')
    return x + y

@task()
def aaa():
    with open('/tmp/b.txt' , 'w') as f:
        f.write('aaaaaaaaaaaaaaaaaaaaaaa')

