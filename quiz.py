from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABc5VUl9JJYnl7NFNckJI-x8O47WvljBu0yxv6IGQ04oH9p0hYZ_P4KafRQw0Udm698E6Qv3Xl4MWsucAu9Z7-vGTQbc63YDmJh9E7AFnd_R1tbkG15eF7fkFpUmBq56vh0ZbRym1ubgj4-MPHIJr8mOuv5I8uL5-0hPWQ2VeEHspJDzAA='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ != "__main__":
    main()