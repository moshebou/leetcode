from typing import List
import matplotlib.pyplot as plt
import random
import plotly.express as px
import pandas as pd
import time
# Write any import statements here



def getPlusSignCount(N: int, L: List[int], D: str) -> int:
  def merge_lines(lines, new_line):
    ret_lines = []
    line_inserted = False
    for line in lines:
      if new_line[0] >line[1]:
        ret_lines.append(line)
      elif line[0] > new_line[1]:
        if not line_inserted:
          ret_lines.append(new_line)
          line_inserted = True
        ret_lines.append(line)
      else:
        new_line = [min(new_line[0], line[0]), max(new_line[1], line[1])]
    if not line_inserted:
          ret_lines.append(new_line)
    return ret_lines
        
  
  
  
  
  
  intersection_dict = {}
  
  start = [0,0]
  step_d = {"U": [0,1], "D": [0,-1], "R":[1,0], "L": [-1,0]}

  v_lines = {}
  h_lines = {}
  for i in range(N):
    step = step_d[D[i]].copy()

    step[0] = step[0]*L[i]
    step[1] = step[1]*L[i]
    end_p = [0, 0]
    end_p[0] = start[0] + step[0]
    end_p[1] = start[1] + step[1]
    if D[i] == "U":
      lines = v_lines
      key = end_p[0]
      min_val = start[1]
      max_val = end_p[1]
    elif D[i] == "D":
      min_val = end_p[1]
      max_val = start[1]
      lines = v_lines
      key = end_p[0]
    elif D[i] == "L":
      min_val = end_p[0]
      max_val = start[0]
      lines = h_lines
      key = end_p[1]
    elif D[i] == "R":
      min_val = start[0]
      max_val = end_p[0]
      lines = h_lines
      key = end_p[1]
    
    res = lines.get(key, None)
    if res is None:
      lines[key] =  [[min_val, max_val]]
    else:
      lines[key] = merge_lines(res, [min_val, max_val])
      
    start = end_p

  if len(v_lines) ==0 or len(h_lines) == 0:
    return 0

  
  
  intersection_dict = {}
  for x in v_lines:

    for [y0, y1] in v_lines[x]:
      pnt = intersection_dict.get(tuple([x, y0]), None)
      if pnt is None:
        intersection_dict[tuple([x, y0])] = ["U"]
      else:
        intersection_dict[tuple([x, y0])] = list(set( ["U"]+pnt))
      pnt = intersection_dict.get(tuple([x, y1]), None)
      if pnt is None:
        intersection_dict[tuple([x, y1])] = ["D"]
      else:
        intersection_dict[tuple([x, y1])] = list(set( ["D"]+pnt))
  for y in h_lines:
    for [x0, x1] in v_lines[x]:
      pnt = intersection_dict.get(tuple([x0, y]), None)
      if pnt is None:
        intersection_dict[tuple([x0, y])] = ["R"]
      else:
        intersection_dict[tuple([x0, y])] = list(set( ["R"]+pnt))

      pnt = intersection_dict.get(tuple([x1, y]), None)
      if pnt is None:
        intersection_dict[tuple([x1, y])] = ["L"]
      else:
        intersection_dict[tuple([x1, y])] = list(set( ["L"]+pnt))   
      
  for key in intersection_dict.keys():
    x = key[0]
    y = key[1]
    for x_ in v_lines:
      if x == x_:
        for [y0, y1] in v_lines[x]:
          if y>y0 and y<y1:
            intersection_dict[key] = list(set(intersection_dict[key] + ["U", "D"]))
          elif y == y0:
            intersection_dict[key] = list(set(intersection_dict[key] + ["U"]))
          elif y == y1:
            intersection_dict[key] = list(set(intersection_dict[key] + ["D"]))
    for y_ in h_lines:
      if y == y_:
        for [x0, x1] in h_lines[y]:

          if x>x0 and x<x1:
            intersection_dict[key] = list(set(intersection_dict[key] + ["L", "R"]))
          elif x == x0:
            intersection_dict[key] = list(set(intersection_dict[key] + ["L"]))
          elif x == x1:
            intersection_dict[key] = list(set(intersection_dict[key] + ["R"]))
  for x in v_lines:
    for [y0, y1] in v_lines[x]:
      for y in h_lines:
        for [x0, x1] in h_lines[y]:

          if (x0< x) and (x1>x) and (y < y1) and (y > y0):
            pnt = intersection_dict.get(tuple([x, y]), None)
            if pnt is None:
              intersection_dict[tuple([x, y])] = "UDLR"
              
  intersection = 0
  final_res = []
  for key in intersection_dict.keys():
    if len(set(intersection_dict[key]))== 4:
      final_res.append(key)
      intersection += 1
  
  return intersection, final_res


def getPlusSignCount1(N: int, L: List[int], D: str) -> int:
  curr_position = [0, 0]
  step_d = {"U": [0,1], "D": [0,-1], "R":[1,0], "L": [-1,0]}
  step_p = {"U": "D", "D": "U", "R":"L", "L": "R"}
  dict_points = {}
  dict_points[tuple(curr_position)] = []
  for i in range(N):
    step = step_d[D[i]]
    for j in range(L[i]):
      dict_points[tuple(curr_position)].append(D[i])

      curr_position[0] += step[0]
      curr_position[1] += step[1]
      val = dict_points.get(tuple(curr_position), None)
      if val is None:
        dict_points[tuple(curr_position)] = []
      dict_points[tuple(curr_position)].append(step_p[D[i]])
  intersection_count = 0
  final_res = []
  for key in dict_points:
    if len(set(dict_points[key])) ==4:
      final_res.append(key)
      intersection_count +=1
  return intersection_count, final_res

def compare_solutions(N, L, D):
    t1 = time.time()
    res1, final_res = getPlusSignCount(N, L, D)
    t2 = time.time()
    res2, final_res2 = getPlusSignCount1(N, L, D)
    t3 = time.time()
    #   D = "ULDRULURD"
    print("res1",res1, "time=", t2-t1, "res2", res2, "time=", t3-t2)

    if res1 != res2:

        print("N", N)
        print("L", L)
        print("D", D)
        draw_path(N, L, D)
        print("not simialr")


def draw_path(N, L, D):
    pos_x = 0
    pos_y = 0
    x_l = []
    y_l = []
    x_l.append(pos_x)
    y_l.append(pos_y)
    for i in range(N):
      x_l.append(pos_x)
      y_l.append(pos_y)
      if D[i] == "U":
        pos_y += L[i]
      elif D[i] == "D":
        pos_y -= L[i]
      elif D[i] == "L":
        pos_x -= L[i]
      elif D[i] == "R":
        pos_x += L[i]
      x_l.append(pos_x)
      y_l.append(pos_y)
    fig = px.line(x=x_l, y=y_l, title="Unsorted Input") 
    fig.show()




if __name__ == "__main__":
#   directions = ['U', 'D', 'L', 'R']
#   for i in range(100):
#     N = random.randint(2, 2000) #2*10**6)
#     L = []
#     D = ''
#     for i in range(N):
#         L.append(random.randint(1, 900) )#10*9))
#         D += directions[random.randint(0, len(directions)-1)]
    N=441
    L= [230, 147, 170, 173, 185, 103, 667, 228, 532, 419, 691, 399, 443, 807, 87, 29, 673, 875, 822, 746, 725, 826, 810, 787, 383, 237, 268, 59, 232, 290, 616, 591, 274, 571, 164, 483, 856, 60, 8, 586, 396, 194, 748, 170, 528, 501, 664, 588, 76, 302, 253, 224, 567, 100, 3, 220, 485, 359, 293, 470, 44, 746, 164, 764, 245, 126, 571, 732, 276, 763, 663, 714, 675, 51, 864, 734, 468, 875, 586, 235, 767, 289, 587, 432, 575, 154, 495, 429, 752, 528, 754, 890, 843, 518, 692, 427, 549, 436, 232, 530, 889, 271, 696, 564, 821, 722, 531, 400, 503, 666, 103, 256, 715, 498, 561, 638, 691, 565, 135, 174, 210, 792, 384, 843, 487, 646, 398, 94, 239, 136, 585, 771, 647, 492, 753, 324, 106, 501, 779, 883, 231, 27, 660, 725, 617, 860, 522, 726, 795, 877, 629, 21, 376, 692, 715, 480, 406, 155, 157, 273, 521, 87, 40, 14, 199, 93, 393, 864, 90, 223, 735, 596, 589, 253, 395, 176, 276, 126, 319, 134, 313, 317, 287, 618, 698, 364, 188, 525, 592, 736, 480, 508, 574, 859, 322, 490, 125, 722, 441, 255, 834, 258, 57, 698, 146, 77, 108, 175, 411, 236, 34, 774, 283, 509, 474, 570, 269, 801, 201, 198, 515, 299, 187, 61, 263, 425, 719, 311, 231, 274, 829, 756, 639, 581, 224, 245, 5, 105, 200, 240, 118, 697, 474, 492, 197, 227, 570, 618, 863, 247, 820, 217, 869, 720, 469, 891, 383, 383, 425, 65, 741, 121, 785, 267, 151, 84, 790, 700, 420, 487, 307, 622, 878, 407, 315, 809, 266, 418, 656, 769, 666, 417, 526, 805, 67, 246, 370, 243, 46, 212, 227, 106, 119, 812, 179, 697, 116, 205, 78, 842, 215, 642, 732, 113, 19, 452, 519, 540, 158, 48, 310, 603, 70, 333, 392, 23, 8, 227, 166, 416, 12, 334, 80, 846, 666, 70, 153, 294, 498, 836, 501, 856, 405, 354, 321, 80, 722, 762, 581, 762, 403, 251, 528, 524, 497, 571, 740, 508, 584, 292, 14, 773, 66, 306, 220, 791, 62, 88, 151, 764, 813, 734, 147, 393, 410, 30, 493, 542, 170, 171, 251, 478, 93, 432, 165, 850, 420, 253, 321, 58, 34, 753, 654, 5, 35, 42, 200, 580, 400, 767, 17, 465, 441, 437, 336, 584, 497, 379, 365, 181, 536, 511, 380, 511, 801, 897, 161, 180, 691, 698, 262, 540, 213, 251, 493, 345, 555, 625, 520, 138, 820, 76, 377, 82, 675, 844, 144, 436, 44, 694, 345, 607, 257, 159, 685, 743, 479, 131, 134, 481, 649]
    D = "DRLDLLRRRDLRURDDRULLRRULURDLDDRUUDLDLUUURUDUUDRLURRDULDDURRRRDLRRLLDDLULDUURDUUULRDDURRUUDDRLDDLLUULRUDLLLDDLLRRDUULDDRRULLRULUDURULUDDLLDRDRUDDURLUULLRLRULDURURLRLLULUURDDLDRDDLURRLRLULLRRUDUDLRURRRULURDUURDRRDLDRRRRDDDURDDDDLLDULLUUDLULLUDUDDLRUUDDRLDRRLRLDRRUUUDRLUDUDRDULRDRDRDLLDDLRUUURDLRUDDUDLULRUULLURDUDDULDUURLRURDLURUDDLDDLRRLULRRRLDDDDDLDDURURRRRUURRDDLRDRRRDUDDDDLUUDULLURLRRLRRUUDLURDRDUULURRRRRUDDRLULULULLDLLUULDUDDLLLLULRDLR"
    compare_solutions(N, L, D)


