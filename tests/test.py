import sys
from os import path
from pprint import pprint
import unittest

TEST_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = path.join(TEST_DIR, "..")
sys.path.insert(1, path.join(BASE_DIR, "dist"))

import hdlConvertor


def dumpFile(fname, language):
    f = path.join(BASE_DIR, "tests/", fname)
    res = hdlConvertor.parse(f, language, [TEST_DIR], debug=True)
    return f, res


class BasicTC(unittest.TestCase):

    def test_vhld_dump_mux(self):
        f, res = dumpFile("mux.vhd", "vhdl")
        str(res)

    def test_vhdl_package_array_const(self):
        f, res = dumpFile("package_array_const.vhd", "vhdl")
        str(res)

    def test_vhdl_package_component(self):
        f, res = dumpFile("package_component.vhd", "vhdl")
        str(res)

    def test_vhdl_package_constants(self):
        f, res = dumpFile("package_constants.vhd", "vhdl")
        str(res)

    def test_verilog_uart(self):
        f, res = dumpFile("uart.v", "verilog")
        str(res)

    def test_verilog_arbiter(self):
        f, res = dumpFile("arbiter.v", "verilog")
        str(res)
        e = res["entities"]
        self.assertEqual(len(e), 1)
        a = e[0]
        self.assertEqual(a["name"], "arbiter")
        self.assertEqual(len(a["generics"]), 0)
        self.assertEqual(len(a["ports"]), 10)
        ports = {
            "clk" :"IN" ,
            "rst" :"IN" ,
            "req3":"IN" ,
            "req2":"IN" ,
            "req1":"IN" ,
            "req0":"IN" ,
            "gnt3":"OUT",
            "gnt2":"OUT",
            "gnt1":"OUT",
            "gnt0":"OUT",
        }

        _ports = { p["variable"]["name"]: p['direction'] for p in a["ports"]}
        self.assertDictEqual(_ports, ports)

    def test_verilog_include(self):
        f, res = dumpFile("include.v", "verilog")
        str(res)
        e = res["entities"]
        self.assertEqual(len(e), 2)
        a = e[0]
        self.assertEqual(a["name"], "arbiter")
        u = e[1]
        self.assertEqual(u["name"], "uart")

    def test_verilog_define(self):
        f, res = dumpFile("define.v", "verilog")
        str(res)

    def test_verilog_fifo_rx(self):
        f, res = dumpFile("fifo_rx.v", "verilog")
        e = res['entities']
        self.assertEqual(len(e), 1)
        e = e[0]
        self.assertEqual(len(e['generics']), 2)
        self.assertEqual(len(e['ports']), 11)
        str(res)

    def test_multiple_files_at_once(self):
        f = [path.join(BASE_DIR, "tests/", f) for f in ["fifo_rx.v", "define.v", "arbiter.v", "uart.v"]]
        res = hdlConvertor.parse(f, "verilog", [TEST_DIR], debug=True)
        e = res["entities"]
        self.assertSetEqual(set(_e["name"] for _e in e),
                            {'fifo_rx', 'test', 'arbiter', 'uart'})
        str(res)

    def test_verilog_macro(self):
        f, res = dumpFile("macro.v",'verilog')
        str(res)

    def test_directive_verilogpp(self):
        f, res = dumpFile("directive_verilogpp.v",'verilog')
        str(res)

#    def test_system_verilog_mem_base_object(self):
#        f, res = dumpFile("mem_base_object.sv",  "systemVerilog")
#        str(res)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(BasicTC('test_read'))
    suite.addTest(unittest.makeSuite(BasicTC))

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
