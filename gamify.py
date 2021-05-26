def initialize():
    global hedons
    hedons = 0
    global health_points
    health_points = 0
    global tired
    tired = False
    global time
    time = 0
    global star_counter
    star_counter = []
    global star_type
    star_type = True
    global last_activity
    last_activity = True
    global last_activity_length
    last_activity_length = 0
    global rested
    rested = 0

def get_cur_hedons():
    global hedons
    return hedons

def get_cur_health():
    global health_points
    return health_points

def offer_star(activity):
    global star_counter
    global time
    global star_type
    if star_type != False:
        if activity == "running":
            star_counter.append(time)
            star_type = "running"
        elif activity == "textbooks":
            star_counter.append(time)
            star_type = "textbooks"
        elif activity == "resting":
            star_counter.append(time)
            star_type = "resting"
        if len(star_counter) >2:
            time_difference = 0
            time_difference += star_counter[-1]
            time_difference -= star_counter[-3]
            if time_difference < 120:
                star_type = False

def perform_activity(activity, duration):
    global hedons
    global health_points
    global tired
    global time
    global star_counter
    global star_type
    global last_activity
    global last_activity_length
    global rested
    if activity == "running" and duration > 0:
        rested = 0
        if last_activity == "running" and (duration + last_activity_length) > 180 and last_activity_length < 180:
            health_points += 3 * (180 - last_activity_length)
            health_points += (duration - (180 - last_activity_length))
        elif last_activity == "running" and (duration + last_activity_length) > 180 and last_activity_length >= 180:
            health_points += duration
        elif duration > 180:
            health_points += 3 * 180
            health_points += (duration - 180)
        else:
            health_points += 3 * duration
        if tired == True:
            if star_type == "running":
                if duration > 10:
                    hedons += 10
                    hedons -= 2 * (duration - 10)
                else:
                    hedons += duration
            else:
                hedons -= 2 * duration
        else:
            if star_type == "running":
                if duration > 10:
                    hedons += 50
                    hedons -= 2 * (duration - 10)
                else:
                    hedons += 5 * duration
            else:
                if duration > 10:
                    hedons += 20
                    hedons -= 2 * (duration - 10)
                else:
                    hedons += 2 * duration
        last_activity = "running"
        time += duration
        tired = True
        last_activity_length += duration
        if star_type != False:
            star_type = True
    elif activity == "textbooks" and duration > 0:
        rested = 0
        health_points += 2 * duration
        last_activity_length = 0
        if tired == True:
            if star_type == "textbooks":
                if duration > 10:
                    hedons += 10
                    hedons -= 2 * (duration - 10)
                else:
                    hedons += duration
            else:
                hedons -= 2 * duration
        else:
            if star_type == "textbooks":
                if duration > 20:
                    hedons += 50
                    hedons -= (duration - 20)
                elif duration > 10:
                    hedons += 40
                    hedons += (duration - 10)
                else:
                    hedons += 4 * duration
            else:
                if duration > 20:
                    hedons += 20
                    hedons -= 1 * (duration - 20)
                else:
                    hedons += duration
        last_activity = "textbooks"
        time += duration
        tired = True
        if star_type != False:
            star_type = True
    elif activity == "resting" and duration > 0:
        last_activity = "resting"
        time += duration
        last_activity_length = 0
        rested += duration
        if rested >= 120:
            tired = False
        if star_type != False:
            star_type = True

def star_can_be_taken(activity):
    global star_counter
    global time
    if len(star_counter) == 0:
        return False
    if star_counter[-1] == time and star_type != False and star_type == activity:
        if len(star_counter)>1:
            if (time - star_counter[-2]) < 120:
                return False
        return True
    else:
        return False

def most_fun_activity_minute():
    a = 0
    b = 0
    c = 0
    global tired
    global star_type
    global last_activity
    global last_activity_length
    if tired == True:
        if star_type == "running":
            a += 1
        else:
            a -= 2
    else:
        if star_type == "running":
            a += 5
        else:
            a += 2
    if tired == True:
        if star_type == "textbooks":
            b += 1
        else:
            b -= 2
    else:
        if star_type == "textbooks":
            b += 4
        else:
            b += 1
    if a > b >= c or a > c >= b:
        return "running"
    if b > a >= c or b > c >= a:
        return "textbooks"
    if c > a >= b or c > b >= a:
        return "resting"

if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            #-20 = 10 * 2 + 20 * (-2)
    print(get_cur_health())            #90 = 30 * 3
    print(most_fun_activity_minute())  #resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute())  #running
    perform_activity("textbooks", 30)
    print(get_cur_health())            #150 = 90 + 30*2
    print(get_cur_hedons())            #-80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            #210 = 150 + 20 * 3
    print(get_cur_hedons())            #-90 = -80 + 10 * (3-2) + 10 * (-2)
    perform_activity("running", 170)
    print(get_cur_health())            #700 = 210 + 160 * 3 + 10 * 1
    print(get_cur_hedons())            #-430 = -90 + 170 * (-2)
