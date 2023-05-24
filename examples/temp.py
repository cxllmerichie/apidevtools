def t():
    ...

from = t

class test:
    async def select(self):
        ...

    def from():
        ...


id_ = 1
res = (await db.select('*')
       .from_table('mytest')
       .where(dict(id=id_))
       .order_by('id')
       .limit(100)
       .offset(50))

format = ''


res = await db.select('*').table('mytest').where(dict(id=1)).order_by('id').limit(100).offset(50)
