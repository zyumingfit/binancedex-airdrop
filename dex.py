#!phython

import csv
import sys
import fire
from colorama import Fore,Style
import psutil

def status_msg(category, detail):
    if sys.stdout.isatty() and psutil.POSIX:
        fmt = '%-35s %s' % (Fore.BLUE + Style.BRIGHT + str(category),
                            Fore.RESET + Style.RESET_ALL + str(detail))
    else:
        fmt = '%-35s %s' % (category, detail)
    print(fmt)

def msg_div():
    print(Fore.BLACK + Style.BRIGHT + '----------------------------------------------------------------------------------------------------------------------------------------------------------------' + Fore.RESET + Style.RESET_ALL)

def snap2list(filename, ratio, symbol):

    airdropName = symbol + '.csv'

    totoal_airdrop_amount = 0
    total_balance = 0
    total_accounts = 0
    total_none_zero_accounts = 0
    valid_airdrop_accounts = 0
    index = 0
    templ = '%4s %40s %16s %16s %16s %16s %10s %16s %10s'
    print(fire.core.formatting.Bold(
        templ % ('id', 'address', 'available', 'freeze', 'in order', 'total', 'asset', 'airdrop', 'asset')
    ))
    msg_div()
    colour = Fore.LIGHTBLACK_EX
    with open(airdropName, "w", encoding='utf8') as wcsvfile:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[0] == "address":
                    continue

                total_accounts += 1
                balance = int(line[4])* 1.0 / 1e8
                if balance > 0:
                    total_none_zero_accounts += 1

                airdrop_line = []
                airdrop_line.append(line[0])
                total_balance += int(line[4])
                airdrop_amount = 0
                index += 1

                if balance >= 100:
                    airdrop_amount =  int((balance / ratio) * 1e8)
                    valid_airdrop_accounts += 1
                    totoal_airdrop_amount += airdrop_amount
                    airdrop_line.append(airdrop_amount)
                    airdrop_line.append(symbol)
                    #print(index, airdrop_line)
                    writer = csv.writer(wcsvfile)
                    writer.writerow(airdrop_line)
                    colour = Fore.BLACK
                else:
                    colour = Fore.LIGHTBLACK_EX

                content = templ % ("%d" % index, line[0], line[1], line[2], line[3],line[4],line[5], airdrop_amount, symbol)
                print(colour + Style.BRIGHT + content + Fore.RESET + Style.RESET_ALL)

    msg_div()
    print('\n\n')
    status_msg("Total Accounts", total_accounts)
    status_msg("Total None Zero Accounts:", total_none_zero_accounts)
    status_msg("Valid Airdrop Accounts:", valid_airdrop_accounts)
    status_msg("Total Balance:", total_balance/100000000.0)
    status_msg("Total Airdrop Amount:", totoal_airdrop_amount/100000000.0)
    status_msg("Total BNB Cost:", valid_airdrop_accounts*0.0003)
    status_msg("Ratio:", ratio)



def main():
    fire.Fire({
        'snap2list': snap2list,
    })
def exit_handler(signum, frame):
    exit()


if __name__ == "__main__":
    main()
