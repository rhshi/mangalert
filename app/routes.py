from flask import Markup, render_template

from app import app


@app.route('/')
@app.route('/index')
def index():
    content = Markup(
        '''
        <div class="blurb">
	        <h1>Welcome to mangalert!</h1>
        </div><!-- /.blurb -->
        '''
    )
    return render_template('default.html', content=content)