# import schedule
# import time
#
# def sudo_placement():
#     print("get ready for sudo placement")
#
#
# def good_luck():
#     print("good luck for test")
#
#
# def work():
#     print("study and work hard")
#
#
# def bedtime():
#     print("it is bed time go rest")
#
#
# def geeks():
#     print("shaurya says geeksforgeeks")
#
#
# schedule.every(10).minutes.do(geeks)
#
# schedule.every().hour.do(geeks)
#
# schedule.every().day.at("00:00").do(bedtime)
#
# schedule.every(5).to(10).minutes.do(work)
#
# schedule.every().monday.do(good_luck)
#
# schedule.every().tuesday.at("18:00").do(sudo_placement)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)


with open("ss.txt","w+") as f:
    f.write("soke")
