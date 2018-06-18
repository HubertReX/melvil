from flask import url_for
from models import Copy

from tests.populate import (
    populate_copies,
    populate_books)


def test_remove_item(session, db_user, client, app_session):
    user = db_user
    books = populate_books(n=5)
    session.add_all(books)
    session.commit()
    copies_before = session.query(Copy).count()

    for book in books:
        copies = populate_copies(book, n=2)
        session.add_all(copies)
        session.commit()
        copies_added = session.query(Copy).count()
        assert copies_before < copies_added, 'copies were not added'

        for copy in copies:
            session.delete(copy)
            session.commit()
            resp = client.post(url_for('library.remove_item',
                                       item_id=copy.id,
                                       db_user=user))
        assert resp.status_code == 404, 'book has not been deleted'