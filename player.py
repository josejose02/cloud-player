from flask import Flask
from flask import jsonify
from flask import render_template
import subprocess
import requests
import json
import os,binascii
from wowzaCloudAPI import josestreamCloud

app = Flask(__name__)

@app.route('/player/<id>', methods=['GET'])
def player(id):
    cloud_id = 'bx1vkpcc'
    name = 'Reconciliate con Dios'

    res = josestreamCloud()
    response = res.getTarget(cloud_id)
    token_id = res.getToken(cloud_id)
    src = response['hls_playback']
    variable = '--key=' +token_id
    token_auth = ''
    try:
        result = subprocess.check_output(['python','akamai_token_v2.py','--window=300', variable,'--acl=/*'])
        a = result.rstrip()
        print(a)
        resp = jsonify({'params':a})
        res = resp.json()
        token_auth = res['params']
    except:
        print('Error!')
    player_url = 'https://liveplayer.josestream.com'
    params = {'src':src, 'token':token_auth, 'name':name, 'player_cdn':player_url}
    return render_template('player.html', params=params)

@app.route('/token/<token_id>', methods = ['POST'])
def token(token_id):
    variable = '--key=' +token_id
    try:
        result = subprocess.check_output(['python','akamai_token_v2.py','--window=300', variable,'--acl=/*'])
    except:
        result = 'Error!'
    a = result
    response = jsonify({'params':a})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/player3/<player_id>', methods = ['GET'])
def player2(player_id):
    #try:
    #    r = requests.get('http://api.josestream.com/v1/stream/'+player_id)
    #    r = r.json()
    #    token = r['player_token']
    #    base_hls = r['player_hls']
    #except:
    base_hls = 'https://wowzaprod109-i.akamaihd.net/hls/live/623120/afc62c0c/playlist.m3u8'
    token = '0d84080361930851d9c0eb66a12cd270'
    #url='http://localhost:5000/token/' + token
    #try:
    #    res = requests.post(url)
    #    res = res.json()
    #    token_auth = res['params']
    #except:
    variable = '--key=' + token
    result = subprocess.check_output(['python','akamai_token_v2.py','--window=300', variable,'--acl=/*'])
    a = result.rstrip()
    #resp = jsonify({'params':a})
    #res = resp.json()
    #token_auth = res['params']
    poster = 'https://wallpaper.wiki/wp-content/uploads/2017/06/Blue-gradient-Wallpaper-1080p.png'
    video_url = base_hls + '?hdnts=' + a
    base_html = '<html><head><script src="http://old.josestream.com/p/player.js"></script><link href="http://old.josestream.com/p/min.css" rel="stylesheet"><link href="https://old.josestream.com/player.css" rel="stylesheet"></head><body><video id="content_video" poster="'+poster+'" class="video-js vjs-default-skin vjs-fluid vjs-16-9"  preload="auto"   title="TestVideo1"></video><script>videojs("content_video", {  controls: true,sources: [{ "type": "application/x-mpegURL", "src": "'+video_url+'"  }],  plugins: {  videoJsResolutionSwitcher: {  default: "240",dynamicLabel: false } } ,html5: { hls: {debug: true, } } }, function(){var player = this;player.on("resolutionchange", function(){console.info("Source changed")})});</script></body></body>'
    response = base_html
    return response

@app.route('/stream', methods = ['POST'])
def stream():
    '''
    Define the api request:
        Auth --> UserName: email & api key
        Body --> Name for stream & Input resolution
            - extras: ??

    Key -- SET
    Transcoder -- SET
    Target CDN -- NO
    '''
    user = request.headers.get('user')
    key = request.headers.get('key')
    try:
        userDB = user.objects.get(user=user)
        xkey = user.objects.get() # get the password key
        status = True
    except:
        return 'User not in system'
    if status == True:
        if xkey == key:
            server = 'http://live-eu.josestream.com'

            if input_res >= 1080: # Used to set the transcoder resolution!
                templateName = '1080'
            elif input_res < 1080 and input_res >= 720:
                templateName = '720'
            elif input_res < 720 and input_res >= 576:
                templateName = '576'
            elif input_res < 576 and input_res >= 480:
                templateName = '480'
            elif input_res < 480 and input_res >= 360:
                templateName = '360'
            elif input_res < 360 and input_res >= 0:
                templateName = '240'
            else:
                return jsonify({'error':'invalid input resolution'})

            #create stream key
            key_ok = False
            while key_ok == False:
                key = binascii.b2a_hex(os.urandom(10))
                #
                # Check DB for key's
                #
                if key in db:
                    key_ok = False
                elif key not in db:
                    key_ok = True
                    #
                    # Add key to database, link to account
                    #
            # Get from pool db a target.
            # Move it to link
            # Add to
            copy = '/v2/servers/{}/vhosts/{}/transcoder/templates/{}/actions/{}?dstEntryName={}'.format(serverName, vhostName, templateName, action='copy', newCode = '') # Create a transcoder



            response = { "live_info" : 'test' }
            response = jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80,debug=True)
