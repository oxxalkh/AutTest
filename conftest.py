import pytest
from checkers import checkout, checkhash
import random
import string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="function")
def make_folders():
    return checkout("mkdir {} {} {} {}".format(data["tst"], data["out"], data["folder1"], data["folder2"]), "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["tst"], data["out"], data["folder1"], data["folder2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["tst"], filename,
                                                                                           data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["tst"], subfoldername), ""):
        return None, None
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["tst"],
                                                                     subfoldername, testfilename, data["bs"]), ""):
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
    checkout("cd {}; 7z a {}/bad_arx -t{}".format(data["tst"], data["out"], data["type"]), "Everything is Ok")
    checkout("truncate -s 1 {}/bad_arx.{}".format(data["out"], data["type"]), "")


@pytest.fixture(autouse=True)
def write_statistic():
    yield
    statistic = checkhash("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"),
                                                                            data["count"], data["bs"], statistic), "")
