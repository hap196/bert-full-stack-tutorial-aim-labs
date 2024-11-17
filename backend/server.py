from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# ============= DUMMY VERSION =============
# this version returns random embeddings to simulate a BERT output
def get_dummy_embeddings(text):
    # BERT base outputs 768-dimensional embeddings
    # this creates consistent dummy embeddings based on text length
    np.random.seed(len(text))
    return np.random.randn(768).tolist()


@app.route("/process", methods=["POST"])
def process_text():
    try:
        data = request.json
        text = data.get("text", "")

        # generate dummy embeddings. for loading a real model, see below
        embeddings = get_dummy_embeddings(text)

        return jsonify(
            {
                "success": True,
                "embeddings": embeddings,
                "message": "Text processed successfully (dummy output)",
                "text_length": len(text),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============= REAL MODEL VERSION (uncomment for use) =============
"""
from transformers import BertTokenizer, BertModel
import torch

# load your pre-trained model and tokenizer here
MODEL_PATH = [insert path here]
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained(MODEL_PATH)  # or .from_pretrained('bert-base-uncased') for standard BERT
model.eval()

@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.json
        text = data.get('text', '')
        
        # tokenize input
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # get BERT output
        with torch.no_grad():
            outputs = model(**inputs)
            
        # get the embeddings from the last hidden state
        # add mean pooling (take average of all tokens)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        
        return jsonify({
            'success': True,
            'embeddings': embeddings,
            'message': 'Text processed successfully',
            'text_length': len(text)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
