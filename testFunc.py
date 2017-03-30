
class Shoe:
    Soldout = False
    AvailableNow = True
    NewlyAdded = False
    Restock = False

    def __init__(self, link, sizePrice, status):
        self.link = link
        self.sizePrice = sizePrice
        self.status = status


# statusTest = Shoe("asf",["adf","adf"],"restock")
#
# print statusTest.link
# print statusTest.sizePrice
# print statusTest.status
#
#
# statusTest.status = "soldour"
#
# print statusTest.status


l = ['8-SoldOut', '8.5-SoldOut', '9-SoldOut', '9.5-$190.00USD', '10-$190.00USD', '10.5-$190.00USD', '11-$190.00USD', '11.5-$190.00USD', '12-$190.00USD', '13-SoldOut', '14-SoldOut']

s = set(l)


list = ['8-SoldOut', '8.5-SoldOut', '9-SoldOut', '9.5-$190.00USD', '10-$190.00USD', '10.5-$190.00USD', '11-$190.00USD', '11.5-$190.00USD', '12-$190.00USD', '13-SoldOut', '14-SoldOut']
se = set(list)
print  s
print se


if s == se:
    print True
else:
    print False

