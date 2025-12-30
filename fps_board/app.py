from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'fps.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ランク画像
RANK_IMAGES = {
    'Unranked': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/0/largeicon.png',
    'Iron': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/3/largeicon.png',
    'Bronze': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/6/largeicon.png',
    'Silver': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/9/largeicon.png',
    'Gold': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/12/largeicon.png',
    'Platinum': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/15/largeicon.png',
    'Diamond': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/18/largeicon.png',
    'Ascendant': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/21/largeicon.png',
    'Immortal': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/24/largeicon.png',
    'Radiant': 'https://media.valorant-api.com/competitivetiers/03621f52-342b-cf4e-4f86-9350a49c6d04/27/largeicon.png'
}

ROLE_ICONS = {
    'Duelist': 'https://media.valorant-api.com/agents/roles/dbe8757e-9e92-4ed4-a393-f7958e481880/displayicon.png',
    'Initiator': 'https://media.valorant-api.com/agents/roles/1b47567f-8f7b-444b-a602-0e2538d9134a/displayicon.png',
    'Controller': 'https://media.valorant-api.com/agents/roles/4ee40330-ecdd-4f2f-98a8-eb12434484f5/displayicon.png',
    'Sentinel': 'https://media.valorant-api.com/agents/roles/5fc02f99-4091-4486-a531-98459a3e95e9/displayicon.png'
}

AGENTS_DATA = {
    'Astra': {'role': 'Controller', 'url': 'https://media.valorant-api.com/agents/41fb69c1-4189-7b37-f117-bcaf1e96f1bf/displayicon.png'},
    'Breach': {'role': 'Initiator', 'url': 'https://media.valorant-api.com/agents/5f8d3a7f-467b-97f3-062c-13acf203c006/displayicon.png'},
    'Brimstone': {'role': 'Controller', 'url': 'https://media.valorant-api.com/agents/9f0d8ba9-4140-b941-57d3-a7ad57c6b417/displayicon.png'},
    'Chamber': {'role': 'Sentinel', 'url': 'https://media.valorant-api.com/agents/22697a3d-45bf-8dd7-4fec-84a9e28c69d7/displayicon.png'},
    'Clove': {'role': 'Controller', 'url': 'https://media.valorant-api.com/agents/e370fa57-4757-3604-3648-499e1f642d3f/displayicon.png'},
    'Cypher': {'role': 'Sentinel', 'url': 'https://media.valorant-api.com/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png'},
    'Deadlock': {'role': 'Sentinel', 'url': 'https://media.valorant-api.com/agents/cc8b64c8-4b25-4ff9-6e2f-04b4ced69603/displayicon.png'},
    'Fade': {'role': 'Initiator', 'url': 'https://media.valorant-api.com/agents/dade69b4-4f5a-8528-247b-219e5a1fc413/displayicon.png'},
    'Gekko': {'role': 'Initiator', 'url': 'https://media.valorant-api.com/agents/e370fa57-4757-3604-3648-499e1f642d3f/displayicon.png'},
    'Harbor': {'role': 'Controller', 'url': 'https://media.valorant-api.com/agents/95c7823b-4286-18f6-e3ff-599c35d9f4c5/displayicon.png'},
    'Iso': {'role': 'Duelist', 'url': 'https://media.valorant-api.com/agents/0e38b510-41a8-5780-5e8f-568b2a4f2d6c/displayicon.png'},
    'Jett': {'role': 'Duelist', 'url': 'https://media.valorant-api.com/agents/ad7e0ced-4d74-850a-44b6-39ad69f68f74/displayicon.png'},
    'KAY/O': {'role': 'Initiator', 'url': 'https://media.valorant-api.com/agents/601db09a-4309-4c51-507c-9b8897f26a11/displayicon.png'},
    'Killjoy': {'role': 'Sentinel', 'url': 'https://media.valorant-api.com/agents/1e58de9c-4950-5125-93e9-a0aee9f97bb8/displayicon.png'},
    'Neon': {'role': 'Duelist', 'url': 'https://media.valorant-api.com/agents/bb2a4828-46eb-8cd1-e765-15848195d751/displayicon.png'},
    'Omen': {'role': 'Controller', 'url': 'https://media.valorant-api.com/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png'},
    'Phoenix': {'role': 'Duelist', 'url': 'https://media.valorant-api.com/agents/eb93336a-449b-9c1b-0a54-a891f7921d69/displayicon.png'},
    'Raze': {'role': 'Duelist', 'url': 'https://media.valorant-api.com/agents/f94c3b30-42be-e959-889c-5aa313dba261/displayicon.png'},
    'Reyna': {'role': 'Duelist', 'url': 'https://media.valorant-api.com/agents/a3bc4048-406d-8bb5-e917-50850a3860d4/displayicon.png'},
    'Sage': {'role': 'Sentinel', 'url': 'https://media.valorant-api.com/agents/56439cd1-4b44-f37b-9173-5a969206ee05/displayicon.png'},
    'Skye': {'role': 'Initiator', 'url': 'https://media.valorant-api.com/agents/6f2a04ca-43e0-be17-7598-18af18de2753/displayicon.png'},
    'Sova': {'role': 'Initiator', 'url': 'https://media.valorant-api.com/agents/320b2a34-4d2e-b054-6888-f6399547c845/displayicon.png'},
    'Viper': {'role': 'Controller', 'url': 'https://media.valorant-api.com/agents/707eab51-4833-9983-3492-5af73f60049b/displayicon.png'},
    'Vyse': {'role': 'Sentinel', 'url': 'https://media.valorant-api.com/agents/26fa0576-4c4f-c081-36ba-bd9d20c5c4fa/displayicon.png'},
    'Yoru': {'role': 'Duelist', 'url': 'https://media.valorant-api.com/agents/7f94d92c-4234-0a36-9e39-0a881448df8d/displayicon.png'}
}

# 選択肢の定義
VC_OPTIONS = ['🔊 VCあり', '🔇 VCなし', '🎧 聞き専']
PLAY_STYLES = ['🏆 ランク上げ', '🔥 ガチアンレート', '☕️ エンジョイ', '🤝 デュオ募集']

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    message = db.Column(db.String(500))
    time = db.Column(db.String(10))
    rank_url = db.Column(db.String(200))
    agent_url = db.Column(db.String(200))
    role_url = db.Column(db.String(200))
    image_filename = db.Column(db.String(200))
    riot_id = db.Column(db.String(50))
    is_recruit = db.Column(db.Boolean, default=False)
    # 新機能用
    vc_type = db.Column(db.String(20))
    play_style = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        rank_name = request.form.get('rank')
        agent_name = request.form.get('agent')
        riot_id = request.form.get('riot_id')
        is_recruit = 'recruit' in request.form
        
        # 新機能: VCとスタイル取得
        vc_type = request.form.get('vc_type')
        play_style = request.form.get('play_style')
        
        file = request.files.get('image')
        filename = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if name and message:
            rank_url = RANK_IMAGES.get(rank_name, RANK_IMAGES['Unranked'])
            agent_info = AGENTS_DATA.get(agent_name)
            if agent_info:
                agent_url = agent_info['url']
                role_name = agent_info['role']
                role_url = ROLE_ICONS.get(role_name, '')
            else:
                agent_url = ''
                role_url = ''

            new_post = Post(name=name, message=message, time=datetime.now().strftime('%H:%M'), 
                            rank_url=rank_url, agent_url=agent_url, role_url=role_url,
                            image_filename=filename, riot_id=riot_id, is_recruit=is_recruit,
                            vc_type=vc_type, play_style=play_style)
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('home'))

    posts = Post.query.order_by(Post.id.desc()).all()
    # テンプレートに選択肢を渡す
    return render_template('index.html', posts=posts, ranks=RANK_IMAGES, agents=sorted(AGENTS_DATA.keys()),
                           vc_options=VC_OPTIONS, play_styles=PLAY_STYLES)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)