from math import ceil


def paginate(

    query,

    db,

    page: int,

    size: int

):

    total = len(

        db.exec(query).all()

    )

    offset = (

        page - 1

    ) * size

    items = db.exec(

        query.offset(offset)

        .limit(size)

    ).all()

    return {

        "page": page,

        "size": size,

        "total": total,

        "total_pages": ceil(

            total / size

        ),

        "items": items

    }