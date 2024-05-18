from api.auth import register_user, login_user
from api.section import sectionAPI
from api.book import bookAPI
from api.bookoperation import book_request, BookAccess, BookRating
from api.profile import UserProfile
from api.summary import SummaryAPI

from app import app

# Auhtentication Routes
app.add_url_rule("/register", view_func=register_user, methods=["POST"])
app.add_url_rule("/login", view_func=login_user, methods=["POST"])
app.add_url_rule("/profile/<int:user_id>", view_func=UserProfile, methods=["GET", "PUT", "DELETE"])

# Section Routes
app.add_url_rule("/section", view_func=sectionAPI, methods=["GET", "POST", "PUT", "DELETE"])

# Book Operation Routes
app.add_url_rule("/book", view_func=bookAPI, methods=["GET", "POST", "PUT", "DELETE"])
app.add_url_rule("/book/request", view_func=book_request, methods=["GET", "POST", "PUT", "DELETE"])
app.add_url_rule("/book/access", view_func=BookAccess, methods=["GET", "PUT"])
app.add_url_rule("/book/rating/<int:book_id>", view_func=BookRating.as_view("book_rating"), methods=["GET", "POST"])

#Summary Route
app.add_url_rule("/summary", view_func=SummaryAPI.as_view("summary"), methods=["GET"])