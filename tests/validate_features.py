# -*- coding: utf-8 -*-
"""
Validate that the features calculations in open-worm-analysis-toolbox
match those of the original Matlab codebase, by comparing
calculated features with a saved copy of the file generated by 
the original Matlab code.
To run this code files should be obtained from:
https://drive.google.com/folderview?id=0B7to9gBdZEyGNWtWUElWVzVxc0E&usp=sharing
In addition the user_config.py file should be created in the 
open-worm-analysis-toolbox package based on the user_config_example.txt
"""
import sys, os

# We must add .. to the path so that we can perform the 
# import of open_worm_analysis_toolbox while running this as 
# a top-level script (i.e. with __name__ = '__main__')
sys.path.append('..')
import open_worm_analysis_toolbox as mv


def test_features():
    """
    Compare Schafer-generated features with our new code's generated features
    """
    # Set up the necessary file paths for file loading
    #----------------------
    base_path = os.path.abspath(mv.user_config.EXAMPLE_DATA_PATH)
    matlab_generated_file_path = os.path.join(
        base_path,'example_video_feature_file.mat')
    data_file_path = os.path.join(base_path,"example_video_norm_worm.mat")

    # OPENWORM
    #----------------------
    # Load the normalized worm from file
    nw = mv.NormalizedWorm.from_schafer_file_factory(data_file_path)

    # Generate the OpenWorm version of the features
    openworm_features = mv.WormFeatures(nw)

    # SCHAFER LAB
    #----------------------
    # Load the Matlab codes generated features from disk
    matlab_worm_features = \
        mv.WormFeatures.from_disk(matlab_generated_file_path)

    # COMPARISON
    #----------------------
    # Show the results of the comparison
    print("\nComparison of computed features to those computed with "
          "old Matlab code:")

    categories = ['locomotion', 'posture', 'morphology', 'path']
    
    # Compare each feature category to make sure they are equal
    for category in categories:
        is_test_passed = (getattr(matlab_worm_features, category) ==
                          getattr(openworm_features, category))
        print(str.capitalize(category)+ ": " + str(is_test_passed))
        assert(is_test_passed)

    print("\nDone validating features")


if __name__ == '__main__':
    start_time = mv.utils.timing_function()
    test_features()
    print("Time elapsed: %.2f seconds" % 
          (mv.utils.timing_function() - start_time))