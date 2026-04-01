from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Leaderboard IoT</title>
    <style>
        body { background: #0d0d15; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; }
        .container { max-width: 900px; margin: 40px auto; padding: 20px; background: #161625; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { font-size: 3em; color: #00d2ff; text-shadow: 0 0 15px #00d2ff; }
        table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
        tr { background: #1f1f35; height: 60px; transition: 0.3s; }
        td { padding: 15px; font-size: 1.4em; border-radius: 5px; }

        /* --- 1. LE GAGNANT (1ère ligne valide) en VERT --- */
        .row-valide:first-child { 
            background: #064e3b !important; /* Vert foncé */
            color: #10b981 !important; /* Vert brillant */
            border: 2px solid #10b981;
        }
        .row-valide:first-child td { font-weight: bold; font-size: 1.8em; }

        /* --- 2. LES AUTRES (Temps moins bons) en GRIS/BLEU --- */
        .row-valide { border-left: 5px solid #3b82f6; }

        /* --- 3. LES FAUX DÉPARTS (ELIMINE) en ROUGE --- */
        .row-elimine { 
            background: #4a0000 !important; 
            color: #ff4d4d !important; 
            font-weight: bold;
            animation: shake 0.3s ease-in-out;
        }

        @keyframes shake {
            0% { transform: translateX(0); }
            25% { transform: translateX(5px); }
            50% { transform: translateX(-5px); }
            100% { transform: translateX(0); }
        }
    </style>
    <script>setInterval(() => location.reload(), 1200);</script>
</head>
<body>
    <div class="container">
        <h1>🏆 CLASSEMENT LIVE 🏆</h1>
        {% if scores %}
        <table>
            <tr><th>RANG</th><th>RASPBERRY</th><th>RÉSULTAT</th></tr>
            {% for score in scores %}
            <tr class="row-{{ score[3]|lower }}">
                <td>{{ loop.index if score[3] == 'VALIDE' else '❌' }}</td>
                <td>{{ score[1] }}</td>
                <td style="font-family: monospace;">{{ score[2] }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <h2 style="color:#444; margin-top:50px;">PRÊT POUR LE DÉPART...</h2>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/scores')
def index():
    try:
        conn = sqlite3.connect('projet_iot.db')
        # On trie : Valides d'abord par temps, puis les éliminés à la fin
        query = """
            SELECT * FROM scores 
            ORDER BY CASE WHEN statut = 'VALIDE' THEN 0 ELSE 1 END, CAST(score_temps AS FLOAT) ASC
        """
        cursor = conn.execute(query)
        scores = cursor.fetchall()
        conn.close()
        return render_template_string(HTML_TEMPLATE, scores=scores)
    except Exception as e:
        return f"Erreur base de données : {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)