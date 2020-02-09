import serial
import time

data = {
    "player_input": [0, 0],
    "actions_1": dict(),
    "actions_2": dict()
}
disallowed_rfids = ["Scan PICC to see UID and type...", "0: ", "1: ", "0:", "1:"]


def read_from_serial(ser):
    line = ser.readline()
    line = line.decode().strip()
    if line != "" and line != "Scan PICC to see UID and type...":
        return (int(line[:1]), line[3:])
    else:
        return (-1, "")

def get_serial():
    ser = serial.Serial('/dev/ttyACM1', 9600)
    time.sleep(2)
    for _ in range(5):
        ser.readline()
    print("Started!")
    return ser

def run_receiver_exposed(ser):
    (id, rfid) = read_from_serial(ser)
    if id != -1 and rfid not in disallowed_rfids:
        if rfid != "":
            actions = (data["actions_1"] if id == 0 else data["actions_2"])
            if rfid not in actions:
                if len(actions) == 0:
                    print("Player {}: Up: \"{}\"".format(str(id), rfid))
                    actions[rfid] = 1
                elif len(actions) == 1:
                    print("Player {}: Down: \"{}\"".format(str(id), rfid))
                    actions[rfid] = -1
                else:
                    print("Player{}: Nothing: \"{}\"".format(str(id), rfid))
                    actions[rfid] = 0
            if data["player_input"][id] != actions[rfid]:
                print("Player {}: Change action {}".format(str(id), actions[rfid]))
                data["player_input"][id] = actions[rfid]
        else:
            if data["player_input"][id] != 0:
                print("Player {}: Change action 0".format(str(id)))
                data["player_input"][id] = 0

def run_receiver():
    actions_1 = dict()
    actions_2 = dict()
    disallowed_rfids = ["Scan PICC to see UID and type...", "0: ", "1: ", "0:", "1:"]
    with serial.Serial('/dev/ttyACM1', 9600) as ser:
        try:
            time.sleep(2)
            for _ in range(5):
                ser.readline()
            print("Started!")
            while True:
                (id, rfid) = read_from_serial(ser)
                if id != -1 and rfid not in disallowed_rfids:
                    if rfid != "":
                        actions = (actions_1 if id == 0 else actions_2)
                        if rfid not in actions:
                            if len(actions) == 0:
                                print("Player {} Up: \"{}\"".format(str(id), rfid))
                                actions[rfid] = 1
                            elif len(actions) == 1:
                                print("Player {} Down: \"{}\"".format(str(id), rfid))
                                actions[rfid] = -1
                            else:
                                print("Nothing: \"{}\"".format(rfid))
                                actions[rfid] = 0
                        if data["player_input"][id] != actions[rfid]:
                            print("Change action {}".format(actions[rfid]))
                            data["player_input"][id] = actions[rfid]
                    else:
                        data["player_input"][id] = 0
                time.sleep(0.01)
        except Exception as e:
            ser.close()
            raise e
