# -*- coding: utf-8 -*-
"""
This should replicate the behaviour of the compute "new" histograms code from
https://github.com/JimHokanson/SegwormMatlabClasses/blob/master/%2Bseg_worm/%2Btesting/%2Bstats/t001_oldVsNewStats.m

We are just trying to achieve the creation of an in-memory object that contains
the statistics generated from comparing a set of 20 Feature .mat Files:
- 10 "Experiment" files and
- 10 "Control" files.

"""

import sys, os, pickle
import matplotlib.pyplot as plt

# We must add .. to the path so that we can perform the 
# import of movement_validation while running this as 
# a top-level script (i.e. with __name__ = '__main__')
sys.path.append('..')
import movement_validation as mv


def main():
    base_path = os.path.abspath(mv.user_config.EXAMPLE_DATA_PATH)
    root_path = os.path.join(base_path, '30m_wait')

    experiment_histograms, control_histograms = \
        obtain_histograms(root_path, "pickled_histograms.dat")


    #for i in range(0, 700, 100):
    for i in range(1):
        plot_histogram(experiment_histograms.hists[i],
                       control_histograms.hists[i])

    plt.show()

    # TODO: test this:
    #stats = mv.StatisticsManager(experiment_histograms, control_histograms)

    # TODO:
    # now somehow display the stats to prove that we generated them!

    # TODO:
    # maybe compare to the segwormmatlabclasses-generated stats somehow?

    # TODO:
    # visualize the data in a grid
    # http://stackoverflow.com/questions/19407950


def plot_histogram(exp_hist, ctl_hist):
    """
    Use matplotlib to plot a Histogram instance.
    
    Note: You must still call plt.show() after calling this function.
    
    Parameters
    -----------------------
    histogram: a Histogram instance
    
    """
    # Verify that we are comparing the same feature
    assert(exp_hist.long_field == ctl_hist.long_field)

    ctl_bins = ctl_hist.bin_midpoints
    ctl_y_values = ctl_hist.pdf

    exp_bins = exp_hist.bin_midpoints
    exp_y_values = exp_hist.pdf
    min_x = min([h.bin_midpoints[0] for h in [ctl_hist, exp_hist]])
    max_x = min([h.bin_midpoints[-1] for h in [ctl_hist, exp_hist]])


    plt.figure(figsize=(12, 9))
    plt.fill(ctl_bins, ctl_y_values, alpha=1, color='0.85', label='Control')
    plt.fill(exp_bins, exp_y_values, alpha=0.5, color='g', label='Experiment')

    plt.xlabel(exp_hist.long_field, fontsize=16)
    plt.ylabel('bin pdf', fontsize = 16)
    plt.title(exp_hist.description, fontsize = 25)
    plt.xlim(min_x, max_x)


    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # ticks only needed at bottom and right
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.legend(loc='upper left')





def get_matlab_filepaths(root_path):
    """
    Recursively traverses from root_path to find all .mat files
    Returns a list of .mat files, with full path

    Parameters
    -----------------------
    root_path: string
        The absolute path to start searching from

    """
    matlab_filepaths = []
    for root, dirs, files in os.walk(root_path):
        mat_files = [f for f in files if f[-4:] == '.mat']
        for f in mat_files:
            matlab_filepaths.append(os.path.join(root, f))

    return matlab_filepaths


def obtain_histograms(root_path, pickle_file_path):
    """
    Compute histograms for 10 experiment and 10 control feature files.
    
    Uses Python's pickle module to save results to disk to save time
    on future times the function is run.
    
    Parameters
    -------------------------
    root_path: string
        A path that has two subfolders, L and R, containing some .mat files,
        for the experiment and control samples, respectively.
    pickle_file_path: string
        A relative path, to the pickle file that has serialized the histograms. This is
        generally found in the examples folder if one wishes to delete it to rerun the code fresh
    
    Returns
    -------------------------
    Two items: experiment_histograms and control_histograms    
    
    """
    if os.path.isfile(pickle_file_path):
        print("Found a pickled version of the histogram managers at:\n%s\n" % pickle_file_path +
              "Let's attempt to unpickle rather than re-calculate, to save time...")
        with open(pickle_file_path, "rb") as pickle_file:
            experiment_histograms = pickle.load(pickle_file)
            control_histograms = pickle.load(pickle_file)
    else:
        print("Could not find a pickled version of the histogram managers " + \
              "so let's calculate from scratch and then pickle")

        experiment_path = os.path.join(root_path, 'L')
        control_path = os.path.join(root_path, 'R')

        experiment_files = get_matlab_filepaths(experiment_path)
        control_files = get_matlab_filepaths(control_path)

        # We need at least 10 files in each
        assert(len(experiment_files) >= 10)
        assert(len(control_files) >= 10)

        # Compute histograms on our files
        experiment_histograms = mv.HistogramManager(experiment_files)
        control_histograms = mv.HistogramManager(control_files)
        with open(pickle_file_path, "wb") as pickle_file:
            pickle.dump(experiment_histograms, pickle_file)
            pickle.dump(control_histograms, pickle_file)

    print("Experiment has a total of " + \
          str(len(experiment_histograms.hists)) + " histograms")

    return experiment_histograms, control_histograms


if __name__ == '__main__':
    main()
