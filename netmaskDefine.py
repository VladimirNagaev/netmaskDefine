import unittest


def ipNormaliser(ipaddr):
    ipaddr += "."
    length = len(ipaddr)
    temp = ""
    temp1 = ""
    for i in range(0, length):
        if ipaddr[i] != ".":
            temp1 += ipaddr[i]
        else:
            if len(temp1) == 3:
                temp += '{:08b}'.format(int(temp1))
            elif len(temp1) == 2:
                temp += '{:08b}'.format(int("0" + temp1))
            elif len(temp1) == 1:
                temp += '{:08b}'.format(int("00" + temp1))
            else:
                temp += '{:08b}'.format(int("000"))
            temp1 = ""
    return temp


def ipListInputter():
    outputArray = []
    tempStr = input("input ip address  ")
    while len(tempStr) != 0:
        outputArray.append(ipNormaliser(tempStr))
        tempStr = input("input ip address  ")
    return outputArray


def netMaskDefine(ipparray):
    pair = []
    if len(ipparray) > 0:
        pair.append(ipparray[0])
    else:
        pair.append("00000000000000000000000000000000")
    for i in range(0, 32):
        for j in range(0, len(ipparray)):
            if ipparray[0][i] != ipparray[j][i]:
                pair.append(i)
                return pair
    pair.append(32)
    return pair


def binToDec(dight):
    if dight == 0:
        return 0
    length = len(dight)
    dec_number = 0
    for i in range(0, length):
        dec_number = dec_number + int(dight[i]) * (2 ** (length - i - 1))
    return dec_number


def result_to_String(binIp, mask):
    newIp = ""
    octet = ""
    ip = ""
    counter = 0
    dec = []
    for i in range(0, 32):
        if i <= mask:
            newIp += binIp[i]
        else:
            newIp.ljust(32, "0")
            break
    for j in range(0, len(newIp)):
        if counter < 8:
            octet += str(newIp[j])
            counter += 1
        else:
            if octet == "00000000":
                dec.append(0)
                continue
            dec.append(binToDec(octet))
            octet = ""
            counter = 0
    while len(dec) < 4:
        dec.append(0)
    ip += str(dec[0])
    ip += "."
    ip += str(dec[1])
    ip += "."
    ip += str(dec[2])
    ip += "."
    ip += str(dec[3])
    ip += "/"
    ip += str(mask)
    return ip


class TestNetMaskDefine(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(netMaskDefine([])[1], 32)
        # print(result_to_String(netMaskDefine([])[0], netMaskDefine([])[1]))

    def testSingleIp(self):
        self.assertEqual(netMaskDefine([ipNormaliser("192.168.0.1")])[1], 32)
        # print(result_to_String(netMaskDefine([ipNormaliser("192.168.0.1")])[0], netMaskDefine([ipNormaliser("192.168.0.1")])[1]))

    def testIpArray2(self):
        self.assertEqual(netMaskDefine([ipNormaliser("192.168.1.1"), ipNormaliser("192.168.0.1")])[1], 23)
        print(result_to_String(netMaskDefine([ipNormaliser("192.168.1.1"), ipNormaliser("192.168.0.1")])[0],
                               netMaskDefine([ipNormaliser("192.168.1.1"), ipNormaliser("192.168.0.1")])[1]))

    def testIpArray3(self):
        self.assertEqual(
            netMaskDefine([ipNormaliser("192.165.1.1"), ipNormaliser("192.168.1.1"), ipNormaliser("192.168.1.2")])[1],
            12)

    def testFirstOctDifferent(self):
        self.assertEqual(netMaskDefine([ipNormaliser("192.168.1.1"), ipNormaliser("193.168.1.1")])[1], 7)

    def testZeroCommonBits(self):
        self.assertEqual(netMaskDefine([ipNormaliser("192.168.1.1"), ipNormaliser("10.168.0.1")])[1], 0)


if __name__ == '__main__':
    unittest.main()
# else:
# print(netMaskDefine(ipListInputter()))
