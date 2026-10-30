# N+1 queries

El ORM trae la lista de posts (1 query) y después, en el loop, accede a `post.autor`, que dispara una query por cada post (N queries).

```python
posts = Post.objects.all()[:100]     # 1 query
for p in posts:
    print(p.autor.nombre)            # 100 queries más
```

Con la DB en la misma máquina pasa desapercibido. Con la DB a 2 ms de red, son 200 ms solo en viajes; con réplicas en otra región o con sharding, es mucho peor.

**Fix:** traer todo junto: `JOIN`, `WHERE id IN (...)`, o lo que te dé el ORM (`select_related` / `prefetch_related` en Django, `joinedload` en SQLAlchemy, `include` en Prisma).
