"""
Synfirechain-like example
"""
import unittest

import spynnaker.plot_utils as plot_utils
import spynnaker.spike_checker as spike_checker

import p7_integration_tests.scripts.synfire_run as synfire_run

class Synfire2RunResetNewPopIfCurrExp(unittest.TestCase):
    @unittest.skip("skipping test_multi_call_examples/"
                   "test_synfire_2_run_reset_file_write_issue.py")
    def test_run(self):
        nNeurons = 200  # number of neurons in each population
        results = synfire_run.do_run(nNeurons,  runtimes=[1000, 1000],
                                     extract_between_runs=False, reset=True)
        (v, gsyn, spikes) = results
        self.assertEquals(53, len(spikes))
        spike_checker.synfire_spike_checker(spikes, nNeurons)

spikeArray = {'spike_times': [[0, 1050]]}

if __name__ == '__main__':
    nNeurons = 200  # number of neurons in each population
    results = synfire_run.do_run(nNeurons, runtimes=[1000, 1000],
                                 extract_between_runs=False, reset=True)
    (v, gsyn, spikes) = results
    print len(spikes)
    plot_utils.plot_spikes(spikes)
    plot_utils.heat_plot(v, title="v")
    plot_utils.heat_plot(gsyn, title="gysn")
