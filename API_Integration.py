from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    recommended_jobs = recommend_jobs(user_id)
    return jsonify(recommended_jobs)

if __name__ == '__main__':
    app.run(debug=True)
