#!flask/bin/python
from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from flask import make_response
import vpn_switcher

app = Flask(__name__)

@app.route('/active', methods=['GET'])
def get_active():
    return jsonify({'active-id': vpn_switcher.current_config_id})

@app.route('/active', methods=['PUT'])
def set_active():
    print request.json
    if not request.json:
        abort(400)
    if 'config_id' in request.json and type(request.json['config_id']) != unicode:
        abort(400)
    
    vpn_id = request.json.get('config_id', vpn_switcher.current_config_id)
    
    vpn = [vpn for vpn in vpn_switcher.vpn_configs if vpn['config_id'] == vpn_id]
    if len(vpn) == 0:
        abort(404)
        
    vpn_switcher.switch_config(
            vpn_id,
            vpn[0]["country"],
            vpn[0]["out_channel"]
        )
    if vpn_switcher.error:
        abort(400)
    return jsonify({'active-id': vpn_switcher.current_config_id})
    
@app.route('/vpns', methods=['GET'])
def get_vpns():
    return jsonify({'vpns': vpn_switcher.vpn_configs})
    
    
@app.route('/vpns/<string:vpn_id>', methods=['GET'])
def get_vpn(vpn_id):
    vpn = [vpn for vpn in vpn_switcher.vpn_configs if vpn['config_id'] == vpn_id]
    if len(vpn) == 0:
        abort(404)
    return jsonify({'vpn': vpn[0]})
    
@app.route('/vpns/<string:vpn_id>', methods=['PUT'])
def update_vpn(vpn_id):
    vpn = [vpn for vpn in vpn_switcher.vpn_configs if vpn['config_id'] == vpn_id]
    if len(vpn) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'vpn': vpn[0]})
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    vpn_switcher.setup()
    app.run(debug=True)
    vpn_switcher.main_loop()