from flask import Blueprint,flash,current_app,render_template,request,redirect,url_for
from flask_login import login_required
from myblog.models import Post
from myblog.utils import redirect_back
from myblog.extensions import db
from myblog.forms import PostForm,Category

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post delete.','success')
    return redirect_back()

@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['MYBLOG_MANAGE_POST_PER_PAGE'])
    posts=pagination.items
    return render_template('admin/manage_post.html',page=page,pagination=pagination,posts=posts)

@admin_bp.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        title=form.title.data
        body=form.body.data
        category=Category.query.get(form.category.data)
        post=Post(title=title,body=body,category=category)
        # same with:
        # category_id = form.category.data
        # post = Post(title=title, body=body, category_id=category_id)
        db.session.add(post)
        db.session.commit()
        flash('Post created.','success')
        return redirect(url_for('blog.show_post',post_id=post.id))
    return render_template('admin/new_post.html',form=form)


