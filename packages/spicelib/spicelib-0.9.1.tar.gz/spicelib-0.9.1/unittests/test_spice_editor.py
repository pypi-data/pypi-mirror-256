#!/usr/bin/env python
# coding=utf-8

# -------------------------------------------------------------------------------
#
#  ███████╗██████╗ ██╗ ██████╗███████╗██╗     ██╗██████╗
#  ██╔════╝██╔══██╗██║██╔════╝██╔════╝██║     ██║██╔══██╗
#  ███████╗██████╔╝██║██║     █████╗  ██║     ██║██████╔╝
#  ╚════██║██╔═══╝ ██║██║     ██╔══╝  ██║     ██║██╔══██╗
#  ███████║██║     ██║╚██████╗███████╗███████╗██║██████╔╝
#  ╚══════╝╚═╝     ╚═╝ ╚═════╝╚══════╝╚══════╝╚═╝╚═════╝
#
# Name:        test_spice_editor.py
# Purpose:     Tool used validate the Spice Files Editor
#
# Author:      Nuno Brum (nuno.brum@gmail.com)
#
# Licence:     refer to the LICENSE file
# -------------------------------------------------------------------------------

import os
import sys
import unittest

sys.path.append(
    os.path.abspath((os.path.dirname(os.path.abspath(__file__)) + "/../")))  # add project root to lib search path

import spicelib

test_dir = '../examples/testfiles/' if os.path.abspath(os.curdir).endswith('unittests') else './examples/testfiles/'
golden_dir = './golden/' if os.path.abspath(os.curdir).endswith('unittests') else './unittests/golden/'


class SpiceEditor_Test(unittest.TestCase):

    def setUp(self):
        self.edt = spicelib.editor.spice_editor.SpiceEditor(test_dir + "DC sweep.net")

    def test_component_editing(self):
        self.assertEqual(self.edt.get_component_value('R1'), '10k', "Tested R1 Value")  # add assertion here
        self.assertListEqual(self.edt.get_components(), ['Vin', 'R1', 'R2', 'D1'], "Tested get_components")  # add assertion here
        self.edt.set_component_value('R1', '33k')
        self.edt.save_netlist(test_dir + 'test_components_output.net')
        self.equalFiles(test_dir + 'test_components_output.net', golden_dir + 'test_components_output.net')
        self.assertEqual(self.edt.get_component_value('R1'), '33k', "Tested R1 Value")  # add assertion here
        self.edt.remove_component('R1')
        self.edt.save_netlist(test_dir + 'test_components_output_1.net')
        self.equalFiles(test_dir + 'test_components_output_1.net', golden_dir + 'test_components_output_1.net')

    def test_parameter_edit(self):
        self.assertEqual(self.edt.get_parameter('TEMP'), '0', "Tested TEMP Parameter")  # add assertion here
        self.edt.set_parameter('TEMP', 25)
        self.assertEqual(self.edt.get_parameter('TEMP'), '25', "Tested TEMP Parameter")  # add assertion here
        self.edt.save_netlist(test_dir + 'test_parameter_output.net')
        self.equalFiles(test_dir + 'test_parameter_output.net', golden_dir + 'test_parameter_output.net')
        self.edt.set_parameter('TEMP', 0)  # reset to 0
        self.assertEqual(self.edt.get_parameter('TEMP'), '0', "Tested TEMP Parameter")  # add assertion here

    def test_instructions(self):
        self.edt.add_instruction('.ac dec 10 1 100k')
        self.edt.add_instruction('.save V(vout)')
        self.edt.add_instruction('.save I(R1)')
        self.edt.add_instruction('.save I(R2)')
        self.edt.add_instruction('.save I(D1)')
        self.edt.save_netlist(test_dir + 'test_instructions_output.net')
        self.equalFiles(test_dir + 'test_instructions_output.net', golden_dir + 'test_instructions_output.net')
        self.edt.remove_instruction('.save I(R1)')
        self.edt.save_netlist(test_dir + 'test_instructions_output_1.net')
        self.equalFiles(test_dir + 'test_instructions_output_1.net', golden_dir + 'test_instructions_output_1.net')
        self.edt.remove_Xinstruction(r"\.save\sI\(.*\)")  # removes all .save instructions for currents
        self.edt.save_netlist(test_dir + 'test_instructions_output_2.net')
        self.equalFiles(test_dir + 'test_instructions_output_2.net', golden_dir + 'test_instructions_output_2.net')

    def equalFiles(self, file1, file2):
        with open(file1, 'r') as f1:
            lines1 = f1.readlines()
        with open(file2, 'r') as f2:
            lines2 = f2.readlines()
        self.assertEqual(len(lines1), len(lines2), "Files have different number of lines")
        for i, lines in enumerate(zip(lines1, lines2)):
            self.assertEqual(lines[0], lines[1], "Line %d" % i)


if __name__ == '__main__':
    unittest.main()
