from flask import Flask, jsonify
import json
import datetime
import os

app = Flask(__name__)

# Optional: a folder where you'll save converted images
IMAGE_FOLDER = "static/images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def convert_base64_to_file(image_data, news_id):
    import base64
    # get the actual base64 part after 'data:image/jpeg;base64,'
    base64_str = image_data.split(",")[1]
    file_path = os.path.join(IMAGE_FOLDER, f"news_{news_id}.jpg")
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(base64_str))
    # return the path as a URL accessible by Flutter
    return f"http://127.0.0.1:8080/{file_path}"

@app.route('/news.all.get')
def get_news_all_articles():
    with open('news_data.json', 'r') as file:
        data = json.load(file)

    # convert base64 images to file URLs
    for news_item in data:
        img_url = news_item.get("image_url", "")
        if img_url.startswith("data:image"):
            news_item["image_url"] = convert_base64_to_file(img_url, news_item["id"])

    return jsonify(data)

@app.route('/news.categories.get')
def get_news_categories():
    time_now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'title': 'List of Categories',
        'time': time_now_str,
        'categories': [
            {'id': 1, 'name': 'Sports'},
            {'id': 2, 'name': 'Politics'},
            {'id': 3, 'name': 'Education'}
        ]
    }
    return jsonify(data)

@app.route('/')
def index():
    return 'Welcome ENSIA Students from Flask!'

# serve static images
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    from flask import send_from_directory
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run(port=8080)
