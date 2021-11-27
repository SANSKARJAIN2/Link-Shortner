from flask import Blueprint

from controllers.controllers import index,shorten,redirect

ls_bp = Blueprint('ls_bp',__name__,url_prefix="/")
ls_bp.route('/',methods=['GET']) (index)
ls_bp.route('/shorten',methods=['GET']) (shorten)
ls_bp.route('/<string:short_id>',methods=['GET']) (redirect)