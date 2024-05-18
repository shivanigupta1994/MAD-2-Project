from flask import request, jsonify
from model import db, BookRequest, User, Book, AccessLog, Rating, Section
from flask_jwt_extended import jwt_required
from datetime import datetime
from flask.views import MethodView
from sqlalchemy import func
from cache import cache

@jwt_required()
def book_request():
    if request.method == "GET":
        books_query = BookRequest.query.all()
        books = []
        for book in books_query:
            books.append(book.__serialize__())

        return jsonify(books), 200

    if request.method == "POST":
        data = request.get_json()
        required_keys = ["user_id", "book_id"]

        # check user_id and book_id exist in the database
        user = User.query.get(data.get("user_id"))
        book = Book.query.get(data.get("book_id"))

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not book:
            return jsonify({"error": "Book not found"}), 404

        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            return (
                jsonify({"error": f"Missing required keys: {', '.join(missing_keys)}"}),
                400,
            )

        # check if user has already requested the book
        existing_request = BookRequest.query.filter_by(
            user_id=data["user_id"], book_id=data["book_id"], status="Pending"
        ).first()

        if existing_request:
            return (
                jsonify(
                    {"message": "Book request already exists!! \nPending for Approval"}
                ),
                200,
            )

        # check if user has already issued the book
        existing_access_log = AccessLog.query.filter_by(
            user_id=data["user_id"], book_id=data["book_id"], status="Issued"
        ).first()

        if existing_access_log:
            return (
                jsonify(
                    {"message": "Book already issued!! \nNo need to raise a request."}
                ),
                200,
            )

        # logic to check count of books borrowed/requested by user is less than 5
        issued_count = AccessLog.query.filter_by(
            user_id=data["user_id"], status="Issued"
        ).count()
        pending_count = BookRequest.query.filter_by(
            user_id=data["user_id"], status="Pending"
        ).count()

        total_count = issued_count + pending_count

        if total_count >= 5:
            return (
                jsonify(
                    {
                        "message": """Maximum limit reached of 5 at a time!! To raise a new request:
                            \n1. You can return some books. \n2. Take back book issuance request."""
                    }
                ),
                200,
            )

        # create new book request
        new_book_request = BookRequest(
            user_id=data["user_id"],
            book_id=data["book_id"],
        )
        db.session.add(new_book_request)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Book request created successfully \nPending for approval by Librarian.."
                }
            ),
            201,
        )

    # define put method to approve/deny requests

    if request.method == "PUT":
        data = request.get_json()
        book = BookRequest.query.get(data.get("id"))

        if book:
            if data.get("approved") == "True":
                setattr(book, "status", "Approved")
                setattr(book, "approved_date", datetime.now())
                new_access_log = AccessLog(user_id=book.user_id, book_id=book.book_id)
                db.session.add(new_access_log)
                db.session.commit()

                return jsonify({"message": "Successfully, Book request approved"}), 200

            elif data.get("approved") == "False":
                setattr(book, "status", "Rejected")
                db.session.commit()
                return jsonify({"message": "Successfully, book request rejected"}), 200
        else:
            return jsonify({"message": "Error, Book request not found!!"}), 400
        
    if request.method == "DELETE":
        data = request.get_json()
        book = BookRequest.query.get(data.get("id"))

        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"message": "Successfully, Book request deleted"}), 200
        else:
            return jsonify({"message": "Error, Book request not found!!"}), 400    


def BookAccess():
    if request.method == "GET":
        books_query = AccessLog.query.all()
        books = []
        for book in books_query:
            books.append(book.__serialize__())
        return jsonify(books), 200

    # define put method to return book and update status as returned and return date
    if request.method == "PUT":
        data = request.get_json()
        book = AccessLog.query.get(data.get("id"))

        if book:
            if data.get("returned") == "True":
                setattr(book, "status", "Returned")
                setattr(book, "return_date", datetime.now())
                print(datetime.now())
                db.session.commit()
                return jsonify({"message": "Book returned successfully!!"}), 200
            elif data.get("revoke") == "True":
                setattr(book, "status", "Revoked")
                setattr(book, "revoke_date", datetime.now())
                db.session.commit()
                return jsonify({"message": "Book revoked successfully!!"}), 200
        else:
            return jsonify({"message": "Error, Book Access log not found!!"}), 400


class BookRating(MethodView):
    def get(self, book_id):
        # Get and return ratings for the specified book_id
        ratings_query = Rating.query.filter_by(book_id=book_id).all()
        ratings = [rating.__serialize__() for rating in ratings_query]
        return jsonify({"book_id": book_id, "ratings": ratings}), 200

    def post(self, book_id):
        cache.clear()
        data = request.get_json()
        required_keys = ["user_id", "rating_value"]

        # check user_id and book_id exist in the database
        user = User.query.get(data.get("user_id"))
        book = Book.query.get(book_id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        if not book:
            return jsonify({"error": "Book not found"}), 404

        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            return (
                jsonify(
                    {"error": f"Missing required keys: {', '.join(missing_keys)}"}
                ),
                400,
            )

        # Check if the user has either issued or returned the book
        access_log = AccessLog.query.filter_by(user_id=user.id, book_id=book.id).first()

        if not access_log:
            return jsonify({"error": "You can only rate a book you have issued or returned"}), 400

        # Validate rating_value (assuming it should be between 1 and 5)
        rating_value = data.get("rating_value")
        if not (1 <= rating_value <= 5):
            return jsonify({"error": "Invalid rating_value. It should be between 1 and 5"}), 400

        # Check if the user has already rated the book
        rating = Rating.query.filter_by(user_id=user.id, book_id=book.id).first()

        if rating:
            # Update existing rating
            rating.rating_value = rating_value
            db.session.commit()
            return jsonify({"message": "Book rating updated successfully"}), 200
        else:
            new_rating = Rating(user_id=user.id, book_id=book.id, rating_value=rating_value)
            db.session.add(new_rating)
            db.session.commit()

        # Calculate average rating for the book using SQLAlchemy's func.avg
        avg_rating = (
            db.session.query(func.avg(Rating.rating_value))
            .filter_by(book_id=book.id)
            .scalar()
        )

        # Update avg_rating in the Book table
        book.avg_rating = avg_rating
        db.session.commit()

        return jsonify({"message": "Book rating created successfully"}), 201

