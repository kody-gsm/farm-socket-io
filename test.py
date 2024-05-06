from sensor.cam import CamSenSor

with CamSenSor() as cam:
    try:
        data = cam.get_data()
        while not data:
            print("cam none")
            data = cam.get_data()
        print(len(data))
    except Exception as e:
        print(e)