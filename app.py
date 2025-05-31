from flask import Flask, request, send_file, send_from_directory
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__, static_folder='static')

# Serve the HTML file
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# Handle word cloud generation
@app.route('/generate', methods=['POST'])
def generate_wordcloud():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return "No text provided", 400

        # Generate word cloud
        wc = WordCloud(width=800, height=400, background_color="black", colormap="Accent")
        wc.generate(text)

        # Save image to bytes
        img_io = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='quadric')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(img_io, format='png', bbox_inches='tight')
        plt.close()
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return f"Server error: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=True)
