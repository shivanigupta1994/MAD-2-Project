from flask_restful import Resource
from flask import jsonify
from model import db, User, Section, Book, BookRequest, AccessLog, Rating
from sqlalchemy import func
from datetime import datetime, timedelta
import random

class SummaryAPI(Resource):
    def get(self):
        try:
            result = {}
            # Calculate total users
            # total_users = User.query.count()
            total_users = User.query.filter(User.id != 1, User.user_type != 'admin').count()

            # Calculate total books
            total_books = Book.query.count()
         
            # Calculate total sections
            total_sections = Section.query.count()

            # Calculate total issued books
            total_issued_books = AccessLog.query.filter(AccessLog.status == "Issued").count()

            # Calculate section-wise book count
            section_wise_book_count = {}
            sections = Section.query.all()
            for section in sections:
                book_count = Book.query.filter_by(section_id=section.id).count()
                section_wise_book_count[section.name] = book_count

            # Calculate top-rated books (Assuming top 5 based on rating_value)
            top_books_query = (
                db.session.query(Book, func.avg(Rating.rating_value).label("avg_rating"))
                .join(Rating, Book.id == Rating.book_id)
                .group_by(Book.id)
                .order_by(func.avg(Rating.rating_value).desc())
                .limit(5)
            )
            top_books_list = top_books_query.all()
            random.shuffle(top_books_list)
            top_books = [
                {
                    "book_name": book.name,
                    "average_rating": avg_rating,
                }
                for book, avg_rating in top_books_list
            ]

            # Prepare the summary data
            result = {
                "total_users": total_users,
                "total_books": total_books,
                "total_sections": total_sections,
                "total_issued_books": total_issued_books,
                "section_wise_book_count": section_wise_book_count,
                "top_books": top_books,
            }

            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
