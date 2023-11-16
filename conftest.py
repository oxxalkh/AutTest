import pytest
from checkers import ssh_checkout, ssh_checkhash
import random
import string
import yaml
from datetime import datetime
from metods import upload_files
with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="function")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "mkdir {} {} {} {}".format(data["tst"], data["out"], data["folder1"], data["folder2"]),
                        "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["tst"], data["out"], data["folder1"],
                                                            data["folder2"]),
                        "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "2222",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["tst"],
                                                                                               filename, data["bs"]),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout("0.0.0.0", "user2", "2222",
                        "cd {}; mkdir {}".format(data["tst"], subfoldername),
                        ""):
        return None, None
    if not ssh_checkout("0.0.0.0", "user2", "2222",
                        "cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["tst"],
                                                                            subfoldername, testfilename, data["bs"]),
                        ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "2222",
                 "cd {}; 7z a {}/bad_arx -t{}".format(data["tst"], data["out"], data["type"]),
                 "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "2222",
                 "truncate -s 1 {}/bad_arx.{}".format(data["out"], data["type"]),
                 "")

@pytest.fixture(autouse=True)
def print_time():
   print("\nStart: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
   yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def start_time():
   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(autouse=True)
def write_statistic():
    yield
    statistic = ssh_checkhash("0.0.0.0", "user2", "2222", "cat /proc/loadavg")
    ssh_checkout("0.0.0.0", "user2", "2222",
                 "echo 'time: {} count:{} size: {} load: {}'>> "
                 "stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], statistic),
                 "")


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "2222", "/home/user/p7zip-full.deb",
                 "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | "
                                                          "sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается в пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | "
                                                          "sudo -S dpkg -s p7zip-full",
                            "Status: install or installed"))
    print(f'{res}')
    return all(res)


@pytest.fixture(autouse=True, scope="module")
def deploy_for_hash():
    res = []

    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | "
                                                          "sudo -S dpkg install libarchive-zip-pearl",
                            "Настраивается в пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | "
                                                          "sudo -S apt list libarchive-zip-pearl ",
                            "Status: installed"))
    print(f'{res}')
    return all(res)


@pytest.fixture(autouse=True)
def save_log():
    with open('logs2.txt', 'a') as f:
        st = ssh_checkhash("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S journalctl "
                                                       "--since '{}'".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write(f'Journal of logs \n {st}')





