import Bot
import Actions
import random
directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
def cut(num, max_num = 7, min_num = 0):
    if num > max_num:
        return num - max_num - 1
    elif num < min_num:
        return num + max_num + 1
    else:
        return num
class Map:
    def __init__(self, size = (180,120), sun_level = 3):
        self.size = size
        self.sun_level = sun_level
        
        self.sun_map = []
        self.minerals_map = []
        self.map = []
        for x in range(self.size[0]):
            self.map.append([])
            self.sun_map.append([])
            self.minerals_map.append([])
            for y in range(self.size[1]):
                if y != 0 and y != self.size[1] - 1:
                    self.map[x].append(0)
                else:
                    self.map[x].append(1)
                
                if y > int(self.size[1]/2):
                    self.sun_map[x].append(0)
                    self.minerals_map[x].append(sun_level)
                else:
                    self.sun_map[x].append(3)
                    self.minerals_map[x].append(0)
    
    def spawn_bot(self, position, genes = '', sun_level = 3, curr_action = 0, energy = 25, direction = 1):
        self.map[position[0]][position[1]] = Bot.Bot(genes, sun_level, curr_action, energy, direction)
    
    def main_cycle(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if type(self.map[x][y]) == Bot.Bot:
                    self.bot_turn(self.map[x][y], x, y)
                elif type(self.map[x][y]) == Bot.Organic:
                    org_func = self.map[x][y].turn()
                    if org_func == 'die':
                        self.map[x][y] = 0
    
    def bot_turn(self, bot, pos_x, pos_y):
        action_points = 1
        actions = 0
        self.map[pos_x][pos_y].add_energy(-1)
        self.map[pos_x][pos_y].change_energy_sources(self.sun_map[pos_x][pos_y], self.minerals_map[pos_x][pos_y])
        while action_points > 0 and actions <= 15:
            action = bot.action()
            
            if action[0] == 'die': #erasing bot
                self.map[pos_x][pos_y] = Bot.Organic()
            
            elif action[0] == 'budd_otn': #spawning new bot
                coords = [cut(pos_x + directions[cut(cut(action[2] + action[1] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] + action[1] % 8))][1], self.size[1] - 1)]
                can_spawn_on_dir = True
                if type(self.map[coords[0]][coords[1]]) != Bot.Bot and type(self.map[coords[0]][coords[1]]) != Bot.Organic:
                    if self.map[coords[0]][coords[1]] == 0:
                        self.spawn_bot([coords[0], coords[1]], action[3], action[4], action[5], action[6], action[7])
                        if random.randint(1,3) <= 1:
                            self.map[coords[0]][coords[1]].mutate()
                    else:
                        can_spawn_on_dir = False
                else:
                    can_spawn_on_dir = False
                if not can_spawn_on_dir:
                    ran_dir_choose = []
                    for i in range(-1,2):
                        for o in range(-1,2):
                            if type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) != Bot.Bot and type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) != Bot.Organic:
                                if self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)] == 0:
                                    ran_dir_choose.append([cut(pos_x + i, self.size[0] - 1), cut(pos_y + o, self.size[1] - 1)])
                    if len(ran_dir_choose) > 0:
                        rand = random.randint(0, len(ran_dir_choose) - 1)
                        self.spawn_bot(ran_dir_choose[rand], action[3], action[4], action[5], action[6], action[7])
                        if random.randint(1,3) <= 1:
                            self.map[ran_dir_choose[rand][0]][ran_dir_choose[rand][1]].mutate()
                    else:
                        self.map[pos_x][pos_y] = Bot.Organic()
                
            elif action[0] == 'move_otn':
                coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                if type(self.map[coords[0]][coords[1]]) == Bot.Bot:
                    if self.map[coords[0]][coords[1]] == self.map[pos_x][pos_y]:
                        num = 1
                    else:
                        num = 2
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                
                if type(self.map[coords[0]][coords[1]]) != Bot.Bot:
                    if self.map[coords[0]][coords[1]] == 0:
                        self.map[coords[0]][coords[1]] = self.map[pos_x][pos_y]
                        self.map[pos_x][pos_y] = 0
            
            elif action[0] == 'move_abs': 
                coords = [cut(pos_x + directions[cut(cut(action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] % 8))][1], self.size[1] - 1)]
                if type(self.map[coords[0]][coords[1]]) == Bot.Bot:
                    if self.map[coords[0]][coords[1]] == self.map[pos_x][pos_y]:
                        num = 1
                    else:
                        num = 2
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                
                if type(self.map[coords[0]][coords[1]]) != Bot.Bot:
                    if self.map[coords[0]][coords[1]] == 0:
                        self.map[coords[0]][coords[1]] = self.map[pos_x][pos_y]
                        self.map[pos_x][pos_y] = 0
            
            elif action[0] == 'turn_abs':
                action_points += 1
                self.map[pos_x][pos_y].jump_action(1)
                
            elif action[0] == 'turn_otn':
                action_points += 1
                self.map[pos_x][pos_y].jump_action(1)
            
            elif action[0] == 'look':
                action_points += 1
                coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                if type(self.map[coords[0]][coords[1]]) == Bot.Bot:
                    if self.map[coords[0]][coords[1]] == self.map[pos_x][pos_y]:
                        num = 1
                    else:
                        num = 2
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                
            elif action[0] == 'eat_otn' or action[0] == 'eat_abs':
                if action[0] == 'eat_otn':
                    coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                else:
                    coords = [cut(pos_x + directions[cut(cut(action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] % 8))][1], self.size[1] - 1)]
                if type(self.map[coords[0]][coords[1]]) == Bot.Bot:
                    num = 1
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 3
                elif self.map[coords[0]][coords[1]] == 0:
                    num = 4
                else:
                    num = 5
                self.map[pos_x][pos_y].receive_jump_action(num)
                
                if type(self.map[coords[0]][coords[1]]) == Bot.Bot:
                    self.map[coords[0]][coords[1]] = 0
                    self.map[pos_x][pos_y].add_energy(80)
                elif type(self.map[coords[0]][coords[1]]) == Bot.Organic:
                    self.map[coords[0]][coords[1]] = 0
                    self.map[pos_x][pos_y].add_energy(70)
                    
            elif action[0] == 'share_otn' or action[0] == 'share_abs':
                if action[0] == 'share_otn':
                    coords = [cut(pos_x + directions[cut(cut(action[3] + action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[3] + action[2] % 8))][1], self.size[1] - 1)]
                else:
                    coords = [cut(pos_x + directions[cut(cut(action[2] % 8))][0], self.size[0] - 1), cut(pos_y + directions[cut(cut(action[2] % 8))][1], self.size[1] - 1)]
                if type(self.map[coords[0]][coords[1]]) == Bot.Bot:
                    energy = int((self.map[pos_x][pos_y].get_energy() + self.map[coords[0]][coords[1]].get_energy())/2)
                    self.map[coords[0]][coords[1]].add_energy(energy, True)
                    self.map[pos_x][pos_y].add_energy(energy, True)
                action_points += 1
                self.map[pos_x][pos_y].jump_action(1)
            
            elif action[0] == 'how_much_energy':
                action_points += 1
                
            elif action[0] == 'if_surrounded':
                surrounded = 0
                for i in range(-1,2):
                    for o in range(-1,2):
                        if type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) == Bot.Bot or type(self.map[cut(pos_x + i, self.size[0] - 1)][cut(pos_y + o, self.size[1] - 1)]) == Bot.Organic:
                            surrounded += 1
                if surrounded == 9:
                    self.map[pos_x][pos_y].receive_jump_action(2)
                else:
                    self.map[pos_x][pos_y].receive_jump_action(3)
                action_points += 1
                
            elif action[0] == 'photosynthesis' or action[0] == 'get_minerals':
                self.map[pos_x][pos_y].jump_action(1)
                
            elif action[0] == 'nrg_source':
                if self.sun_map[pos_x][pos_y] > self.minerals_map[pos_x][pos_y]:
                    self.map[pos_x][pos_y].receive_jump_action(1)
                else:
                    self.map[pos_x][pos_y].receive_jump_action(2)
                action_points += 1
            
            
            action_points -= 1
            actions += 1
    
    def save(self, file_name):
        with open(file_name, 'w') as file:
            for i in range(self.size[0]):
                for o in range(self.size[1]):
                    if type(self.map[i][o]) == Bot.Bot:
                        file.write(f'{["bot", str(self.map[i][o])]}\n')
                    elif type(self.map[i][o]) == Bot.Organic:
                        file.write(f'{["organic", str(self.map[i][o])]}\n')
                    else:
                        file.write(f'{["number", self.map[i][o]]}\n')
    
    def load(self, file_name):
        with open(file_name, 'r') as file:
            c_y = 0
            c_x = 0
            for line in file:
                arr = eval(line)
                if arr[0] == 'number':
                    self.map[c_x][c_y] = arr[1]
                elif arr[0] == 'organic':
                    arr[1] = eval(arr[1])
                    self.map[c_x][c_y] = Bot.Organic(arr[1][0])
                elif arr[0] == 'bot':
                    arr[1] = eval(arr[1])
                    self.spawn_bot([c_x, c_y], arr[1][0], arr[1][1][0], arr[1][1][1], arr[1][1][2], arr[1][1][3])
                c_y += 1
                if c_y == self.size[1]:
                    c_y = 0
                    c_x += 1