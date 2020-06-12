from flask import Blueprint,render_template,request,current_app
from myblog.models import Post,Category,Comment

blog_bp=Blueprint('blog',__name__)

@blog_bp.route('/')
def index():
    page=request.args.get('page',1,type=int)  # 从查询字符串获取当前页数
    per_page=current_app.config['MYBLOG_POST_PER_PAGE']  # 每页数量
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=per_page) # 分页对象
    posts=pagination.items  # 当前页数的记录页表
    return render_template('blog/index.html',pagination=pagination,posts=posts)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category=Category.query.get_or_404(category_id)
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['MYBLOG_POST_PER-PAGE']
    pagination=Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page,per_page)
    posts=pagination.items
    return render_template('blog/category.html',category=category,pagination=pagination,posts=posts)

@blog_bp.route('/post/<int:post_id>')
def show_post(post_id):
    post=Post.query.get_or_404(post_id)
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['MYBOLG_COMMENT_PER_PAGE']
    pagination=Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
      page,per_page)
    comments=pagination.items
    return render_template('blog/post.html',post=post,pagination=pagination,comments=comments)