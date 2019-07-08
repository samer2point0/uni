from multiprocessing import Process
from AuctionClient import AuctionClient
from AuctionServer import AuctionServer
import time

HOST = "localhost"
ports = 10832
numbidders =2
neededtowin =0
itemtypes = ['Picasso', 'Van_Gogh', 'Rembrandt', 'Da_Vinci']
#numitems = {'Picasso': 50, 'Van_Gogh' : 40, 'Rembrandt' : 30, 'Da_Vinci' : 10}
numitems = {}
auction_size = 100
budget = 1000
values = {'Picasso': 4, 'Van_Gogh' : 6, 'Rembrandt' : 8, 'Da_Vinci' : 12}
announce_order = True
winner_pays = 1

args = (HOST, ports, numbidders, neededtowin, itemtypes, numitems, auction_size, budget, values, announce_order, winner_pays
, )

verbose = False


def run_auction(host, ports, numbidders, neededtowin, itemtypes, numitems, auction_size, budget, values, announce_order, winner_pays):
    auctionroom = AuctionServer(host=host, ports=ports, numbidders=numbidders, neededtowin=neededtowin,
    itemtypes=itemtypes, numitems=numitems, auction_size=auction_size, budget=budget, values=values, announce_order=announce_order, winner_pays=winner_pays)
    auctionroom.announce_auction()
    auctionroom.run_auction()


def run_client(port, bidderid, verbose):
    bidbot = AuctionClient(port=port, mybidderid=bidderid, verbose=verbose)
    bidbot.play_auction()


if __name__=='__main__':
    print("Starting AuctionServer")
    auctionserver = Process(target = run_auction, args = args)
    auctionserver.start()
    time.sleep(2)
    bidbots = []
    names={'one':2}#,'four':2,'seven':2,'eight':2,'nine':2,'ten':2,'six':2}#'one':2,#,'five':1}#{'nash1':3,'nash2':3}#'six':3,#, #'copycat':1,'split':1,'discev':1,'discspl':1,'nash':1}
    p=ports
    for key in names:
        for i in range(names[key]):
            name = key + str(i+1)
            print("Starting AuctionClient on port %d with name %s" % (p, name))
            b = Process(target = run_client, args = (p, name, verbose, ))
            bidbots.append(b)
            b.start()
            time.sleep(1)
            p = p + 1
