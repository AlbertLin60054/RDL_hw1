from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    n_str = request.args.get('n')
    n = None
    if n_str and n_str.isdigit():
        n = int(n_str)
    return render_template('index.html', n=n)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    n = data.get('n')
    start_idx = data.get('start')
    end_idx = data.get('end')
    obstacles = set(data.get('obstacles', []))
    
    actions = ['U', 'D', 'L', 'R']
    policy_str = {}
    for i in range(n * n):
        if i in obstacles or i == end_idx:
            policy_str[i] = None
        else:
            policy_str[i] = random.choice(actions)
            
    V = {i: 0.0 for i in range(n * n)}
    gamma = 0.9
    reward = -1.0
    
    def get_next_state(s, a):
        row = s // n
        col = s % n
        if a == 'U': row -= 1
        elif a == 'D': row += 1
        elif a == 'L': col -= 1
        elif a == 'R': col += 1
        
        if row < 0 or row >= n or col < 0 or col >= n:
            return s
        
        next_s = row * n + col
        if next_s in obstacles:
            return s
            
        return next_s

    while True:
        delta = 0
        new_V = dict(V)
        for s in range(n * n):
            if s in obstacles or s == end_idx:
                continue
            
            a = policy_str[s]
            next_s = get_next_state(s, a)
            
            v = reward + gamma * V[next_s]
            delta = max(delta, abs(V[s] - v))
            new_V[s] = v
            
        V = new_V
        if delta < 1e-4:
            break
            
    arrows = {'U': '↑', 'D': '↓', 'L': '←', 'R': '→'}
    result_policy = {}
    result_v = {}
    for i in range(n * n):
        if i in obstacles:
            result_policy[i] = ''
            result_v[i] = ''
        elif i == end_idx:
            result_policy[i] = '🏁'
            result_v[i] = 0.0
        else:
            result_policy[i] = arrows[policy_str[i]]
            result_v[i] = round(V[i], 2)
            
    return jsonify({
        'status': 'success',
        'policy': result_policy,
        'values': result_v
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
