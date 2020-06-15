from flask import Blueprint,flash
from flask_login import login_required
from myblog.models import Post
from myblog.utils import redirect_back
from myblog.extensions import db

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post delete.','success')
    return redirect_back()


