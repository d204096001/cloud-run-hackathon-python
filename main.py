
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
#     logger.info(request.json)
    json = request.json
    
    self_url = json['_links']['self']['href']
    self_state = json['arena']['state'][self_url]
    
    def fine_nearest_corner():
        nearest_corner_x = nearest_corner_y = 0
        move_x = move_y = 0
        if self_state['x'] >= json['arena']['dims'][0]/2:
            nearest_corner_x = json['arena']['dims'][0] - 1
        if self_state['y'] >= json['arena']['dims'][1]/2:
            nearest_corner_y = json['arena']['dims'][1] - 1
        move_x = nearest_corner_x - self_state['x']
        move_y = nearest_corner_y - self_state['y']
        return move_x, move_y
    
    def move(move_x, move_y):
        r = random.random()
        if r > 0.2:
            if move_x > 0:
                if self_state['direction'] == 'E':
                    return 'F'
                elif self_state['direction'] == 'W':
                    return 'L'
                elif self_state['direction'] == 'S':
                    return 'L'
                elif self_state['direction'] == 'N':
                    return 'R'
                else:
                    return 'at'
            elif move_x < 0:
                if self_state['direction'] == 'E':
                    return 'L'
                elif self_state['direction'] == 'W':
                    return 'F'
                elif self_state['direction'] == 'S':
                    return 'R'
                elif self_state['direction'] == 'N':
                    return 'L'
                else:
                    return 'at'
            elif move_y > 0:
                if self_state['direction'] == 'E':
                    return 'R'
                elif self_state['direction'] == 'W':
                    return 'R'
                elif self_state['direction'] == 'S':
                    return 'F'
                elif self_state['direction'] == 'N':
                    return 'L'
                else:
                    return 'at'
            elif move_y < 0:
                if self_state['direction'] == 'E':
                    return 'L'
                elif self_state['direction'] == 'W':
                    return 'R'
                elif self_state['direction'] == 'S':
                    return 'L'
                elif self_state['direction'] == 'N':
                    return 'F'
                else:
                    return 'at'
            else:
                return 'at'
        else:
            if move_y > 0:
                if self_state['direction'] == 'E':
                    return 'R'
                elif self_state['direction'] == 'W':
                    return 'R'
                elif self_state['direction'] == 'S':
                    return 'F'
                elif self_state['direction'] == 'N':
                    return 'L'
                else:
                    return 'at'
            elif move_y < 0:
                if self_state['direction'] == 'E':
                    return 'L'
                elif self_state['direction'] == 'W':
                    return 'R'
                elif self_state['direction'] == 'S':
                    return 'L'
                elif self_state['direction'] == 'N':
                    return 'F'
                else:
                    return 'at'
            elif move_x > 0:
                if self_state['direction'] == 'E':
                    return 'F'
                elif self_state['direction'] == 'W':
                    return 'L'
                elif self_state['direction'] == 'S':
                    return 'L'
                elif self_state['direction'] == 'N':
                    return 'R'
                else:
                    return 'at'
            elif move_x < 0:
                if self_state['direction'] == 'E':
                    return 'L'
                elif self_state['direction'] == 'W':
                    return 'F'
                elif self_state['direction'] == 'S':
                    return 'R'
                elif self_state['direction'] == 'N':
                    return 'L'
                else:
                    return 'at'
            else:
                return 'at'
    
    def fine_target_fire():
        # update map
        map_arr = np.zeros(json['arena']['dims'], dtype='uint8')
        url_list = list(json['arena']['state'].keys())
        for u in url_list:
            x = json['arena']['state'][u]['x']
            y = json['arena']['state'][u]['y']
            map_arr[x, y] = 1
        # detection
        if self_state['x'] == 0:
            x_near_num = map_arr[1:4, 0].sum()
        else:
            x_near_num = map_arr[-4:-1, 0].sum()
        if self_state['y'] == 0:
            y_near_num = map_arr[0, 1:4].sum()
        else:
            y_near_num = map_arr[0, -4:-1].sum()
        if x_near_num >= y_near_num:
            if self_state['x'] == 0:
                fire_direction = 'E'
            else:
                fire_direction = 'W'
        elif x_near_num < y_near_num:
            if self_state['y'] == 0:
                fire_direction = 'S'
            else:
                fire_direction = 'N'
        # action
        if self_state['direction'] == fire_direction:
            return 'T'
        elif fire_direction == 'N':
            if self_state['direction'] == 'W':
                return 'R'
            else: 
                return 'L'
        elif fire_direction == 'E':
            if self_state['direction'] == 'N':
                return 'R'
            else: 
                return 'L'
        elif fire_direction == 'W':
            if self_state['direction'] == 'S':
                return 'R'
            else: 
                return 'L'
        elif fire_direction == 'S':
            if self_state['direction'] == 'E':
                return 'R'
            else: 
                return 'L'
        else:
            return 'T'
    
    move_x, move_y = fine_nearest_corner()
    act = move(move_x, move_y)
    if act != 'at':
        return act
    else: # at corner
        act = fine_target_fire()
        return act
    
#     return moves[random.randrange(len(moves))]
#     return json

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
