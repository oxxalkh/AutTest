
import yaml
from checkers import checkout, checkhash
with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


"""

tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"
folder2 = "/home/user/folder2"

@pytest.fixture()
def make_folders():
    return checkout("mkdir {} {} {} {}".format(tst, out, folder1, folder2), "")


@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(tst, out, folder1, folder2), "")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(tst, filename), ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(tst, subfoldername), ""):
        return None, None
    if not checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(tst, subfoldername, testfilename),
            ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename

"""


class TestPositive:
    def test_step1(self, clear_folders):
        # test1
        result1 = checkout("cd {}; 7z a {}/arx2 -t{}".format(data["tst"], data["out"], data["type"]), "Everything is Ok")
        result2 = checkout(" ls {}".format(data["out"]), "arx2.{}".format(data["type"]))
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(data["tst"], data["out"], data["type"]),
                            "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx2.{} -o{} -y".format(data["out"], data["type"], data["folder1"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; ls".format(data["folder1"]), item))
        assert all(res), "test2 FAIL"

    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z t arx2.{} ".format(data["out"], data["type"]), "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert checkout("cd {}; 7z u arx2.{} ".format(data["tst"], data["type"]), "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2 -t{}".format(data["tst"], data["out"], data["type"]),
                            "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arx2.{}".format(data["out"], data["type"], data["folder1"]), item))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout("cd {}; 7z a {}/arx".format(data["tst"], data["out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["out"], data["type"], data["folder2"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder2"]), item))
        res.append(checkout("ls {}".format(data["folder2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert checkout("cd {}; 7z d arx.{} ".format(data["out"], data["type"]), "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["tst"], item), "Everything is Ok"))
            hash = checkhash("cd {}; crc32 {}".format(data["tst"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["tst"], item), hash))

        assert all(res), "test8 FAIL"




