from flask import request, render_template, abort, flash, redirect, url_for, g

from blueprints import flash_form_errors
from blueprints.posts import bp
from blueprints.posts.forms import PostForm
from persistence.repository.post import PostRepository
from persistence.model.post import Post
from security.decorators import is_admin, is_fully_authenticated


@bp.route('/')
@is_fully_authenticated
def list_all():
    if request.args.get('search'):
        query_string = request.args.get('query_string')

        if request.args.get("ascending"):
            ascending = True
        else:
            ascending = False

        posts = PostRepository.filter(query_string, ascending)
    else:
        posts = PostRepository.find_all()

    return render_template('posts/list.html', posts=posts)


@bp.route('/view/<int:post_id>')
@is_fully_authenticated
def view(post_id):
    post = PostRepository.find_by_id(post_id) or abort(404)

    return render_template('posts/view.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        post.form_update(form)
        post.author_id = g.user.id
        post.save()
        flash('Post added', 'success')

        return redirect(url_for('posts.edit', post_id=post.id))
    if form.errors:
        flash_form_errors(form)

    return render_template('posts/form.html', form=form, create=True)


@bp.route('/edit/<int:post_id>', methods=('GET', 'POST'))
@is_fully_authenticated
@is_admin
def edit(post_id):
    post = PostRepository.find_by_id(post_id) or abort(404)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.form_update(form)
        post.save()
        flash("Poszt editet", 'success')
        return redirect(url_for('posts.edit', post_id=post.id))
    if form.errors:
        flash_form_errors(form)

    return render_template('posts/form.html', form=form, post=post)


@bp.route('/delete/<int:post_id>', methods=('POST',))
@is_fully_authenticated
@is_admin
def delete(post_id):
    post = PostRepository.find_by_id(post_id) or abort(404)

    post.delete()
    flash('Post deleted.', 'success')

    return redirect(url_for('posts.list_all'))
