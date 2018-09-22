import requests
import sys
import time
from rq import get_current_job

from app import create_app, db
from app.models import User, Manga, Task
from app.src.init_follows import determineComplete, gatherFollows
from app.src.utils import isPNG


app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def get_follows(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        follows, count = gatherFollows(user.mdlist)
        i = 0
        for follow in follows:
            if not determineComplete(follow):
                code = follow[1].split('/')[2]
                if isPNG(code):
                    img = 'png'
                else:
                    img = 'jpg'
                if Manga.query.filter_by(title=follow[0]).first():
                    manga = Manga.query.filter_by(title=follow[0]).first()
                    manga.ongoing = True
                    manga.followers.append(user)
                else:
                    manga = Manga(title=follow[0], link=code, ongoing=True, img=img)
                    db.session.add(manga)
                    manga.followers.append(user)
                user.manga_follows.append(manga)
                print(follow[0], ': ongoing')
            else:
                code = follow[1].split('/')[2]
                if isPNG(code):
                    img = 'png'
                else:
                    img = 'jpg'
                if Manga.query.filter_by(title=follow[0]).first():
                    manga = Manga.query.filter_by(title=follow[0]).first()
                    manga.ongoing = False
                    manga.followers.append(user)
                else:
                    manga = Manga(title=follow[0], link=code, ongoing=False, img=img)
                    db.session.add(manga)
                    manga.followers.append(user)
                user.manga_follows.append(manga)
                print(follow[0], ': completed')
            i += 1
            _set_task_progress(100 * i // count)
            time.sleep(1)

        db.session.commit()
            
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())