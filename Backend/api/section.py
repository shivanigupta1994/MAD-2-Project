from flask import request, jsonify
from model import db, Section, Book, BookRequest, AccessLog, Rating
from flask_jwt_extended import jwt_required
from cache import cache

@jwt_required()
@cache.cached(timeout=300, query_string=True, unless=lambda: request.method != 'GET')
def sectionAPI():
    if request.method == "GET":
        # Use try-except block to handle potential errors in querying the database
        try:
            sections = Section.query.all()
            sections_data = [
                {
                    "id": section.id,
                    "name": section.name,
                    "description": section.description,
                    "date_created": section.date_created.isoformat(),
                }
                for section in sections
            ]
            return jsonify(sections_data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if request.method == "POST":
        cache.clear()
        data = request.get_json()
        required_keys = ["name", "description"]
        missing_keys = [field for field in required_keys if field not in data]

        if missing_keys:
            return (
                jsonify({"error": f"Missing required keys: {', '.join(missing_keys)}"}),
                400,
            )

        try:
            new_section = Section(name=data["name"], description=data["description"])
            db.session.add(new_section)
            db.session.commit()
            return jsonify({"message": "Section created successfully"}), 201
        except Exception as e:
            # Handle database insertion errors
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    if request.method == "PUT":
        cache.clear()
        data = request.get_json()
        section = Section.query.get(data.get("id"))
        if section:
            try:
                section.name = data.get("name", section.name)
                section.description = data.get("description", section.description)
                db.session.commit()
                return jsonify({"message": "Section updated successfully"}), 200
            except Exception as e:
                # Handle database update errors
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
        return jsonify({"error": "Section not found"}), 404

    if request.method == "DELETE":
        cache.clear()
        data = request.get_json()
        section = Section.query.get(data.get("id"))
        if section:
            try:
                # Delete all books and related entities using relationships
                books = Book.query.filter_by(section_id=data.get("id")).all()
                if not books:
                    db.session.delete(section)
                    db.session.commit()
                    return jsonify({"message": "Section deleted successfully"}), 204

                for book in books:
                    # Delete all requests and access logs related to the book
                    BookRequests = BookRequest.query.filter_by(book_id=book.id).all()
                    if BookRequests:
                        for book_req in BookRequests:
                            db.session.delete(book_req)

                    access_logs = AccessLog.query.filter_by(book_id=book.id).all()
                    if access_logs:
                        for access_log in access_logs:
                            db.session.delete(access_log)
                    # Delete all ratings related to the book
                    ratings = Rating.query.filter_by(book_id=book.id).all()
                    if ratings:
                        for rating in ratings:
                            db.session.delete(rating)
                    db.session.commit()
                    db.session.delete(book)
                db.session.commit()
                db.session.delete(section)
                db.session.commit()
                return jsonify({"message": "Section deleted successfully"}), 204
            except Exception as e:
                # Handle database deletion errors
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Section not found"}), 404
