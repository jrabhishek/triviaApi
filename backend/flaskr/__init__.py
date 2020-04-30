import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  def question_pagination(page):
    start = (page - 1) *10
    end = start + 10
    questions = Question.query.all()
    length = len(questions)
    questions = questions[start:end]
    formeted_ques = [Question.format(question) for question in questions]
    return formeted_ques, length


  @app.after_request
  def after_request(responce):
      responce.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      responce.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return responce


  @app.route('/questions', methods=['GET'])
  def all_question():
      try:
          page = request.args.get('page', 1, type=int)
          questions = question_pagination(page)
          categories = Category.query.all()
          if(len(questions[0])==0):
              abort(404)
          formated_category = [Category.format(category) for category in categories]
          return jsonify({"questions": questions[0],
                          "total_questions": questions[1],
                          "categories": formated_category,
                          "current_category": "science"
                          })
      except:
          abort(500)


  @app.route('/questions', methods=['POST'])
  def search_question():
      try:
          search_term = request.get_json()['searchTerm']
          questions = Question.query.filter(Question.question.like(f'%{search_term}%')).all()
          formated_question = [Question.format(question) for question in questions]
          return jsonify({"questions": formated_question,
                          "total_questions": len(questions),
                          "current_category": "science"
                          })
      except:
          abort(422)


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      try:
          question = Question.query.filter(Question.id == question_id).one_or_none()
          question.delete()
          return jsonify({"success": True})
      except:
          abort(404)


  @app.route('/add',methods=['POST'])
  def add_question():
      try:
          body = request.get_json()
          question = Question(question=body['question'],difficulty=body['difficulty'],answer=body['answer'],
                              category=body['category'])
          question.insert()
          return jsonify({"success":True})
      except:
          abort(422)

  @app.route('/categories',methods=['GET'])
  def get_category():
      try:
          categories = Category.query.all()
          formated_category =[Category.format(category) for category in categories]
          return jsonify({"categories":formated_category,
                          "success":True})
      except:
          abort(500)
  @app.route('/categories/<int:category_id>',methods=['GET'])
  def get_categoryBy(category_id):
      try:
          id = "{}".format(category_id)
          questions = Question.query.filter(Question.category == id).all()
          formated_ques = [Question.format(question) for question in questions]
          return jsonify({"questions":formated_ques,
                "total_questions":len(formated_ques),
                "current_category":None})
      except:
          abort(422)

  @app.route('/quizzes',methods=['POST'])
  def play_quiz():
      try:
          body = request.get_json()
          category = body['quiz_category']
          print(category)
          previous_questions = body['previous_questions']
          category_id = "{}".format(category['id'])
          if(category_id == "0"):
              all_ques = Question.query.order_by(func.random()).all()
          else:
              all_ques = Question.query.filter(Question.category == category_id).order_by(func.random()).all()
          formated_all_question = [Question.format(q) for q  in all_ques]
          new_question = ""
          for question in formated_all_question:
              if(question['id'] not in previous_questions):
                  new_question = question
                  break
          return jsonify({"question":new_question})
      except:
          abort(422)
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({"success":False,
                      "error":404,
                      "message":"resource not found"}),404

  @app.errorhandler(422)
  def not_found(error):
      return jsonify({"success":False,
                      "error":422,
                      "message":"unable to proccess request"}),422

  @app.errorhandler(500)
  def not_found(error):
      return jsonify({"success":False,
                      "error":500,
                      "message":"something went wrong"}),500

  @app.errorhandler(400)
  def not_found(error):
      return jsonify({"success":False,
                      "error":400,
                      "message":"something went wrong"}),400
  
  return app

    