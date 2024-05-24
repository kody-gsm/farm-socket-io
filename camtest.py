from sensor.cam import CamSenSor

with CamSenSor() as cam:
    try:
        data = cam.get_data() 
        print(cam, data)
        if data:
            print(len(data))
        else:
            print("cam none")
    except:
        print("error")
