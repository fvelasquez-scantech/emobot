from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from flask import Flask, render_template, request

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

emotion_dict = {
    0: '😞', 
    1: '🙁', 
    2: '😐', 
    3: '🙂', 
    4: '😊'
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            text = request.form['text']
        except Exception as e:
            return 'Error: {}'.format(e)

        if len(text.strip()) == 0:
            return 'Error: Texto vacío.'

        inputs = tokenizer(text, return_tensors='pt')
        outputs = model(**inputs)
        predicted_class = outputs.logits.argmax().item()

        if predicted_class in emotion_dict:
            emotion = emotion_dict[predicted_class]
        else:
            emotion = ''

        return render_template('index.html', text=text, emotion=emotion)

    # Si el método no es POST, solo renderiza la plantilla
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
