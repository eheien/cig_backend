#!/usr/bin/env python

import numpy
import itertools

class ResultData:
    def __init__(self, num_header_lines, file_format):
        self.num_header_lines = num_header_lines
        self.file_format = file_format

    def read_file_ascii(self, filename):
        with open(filename, 'r') as fp:
            # Read header lines
            for i in xrange(self.num_header_lines): fp.readline()
            # Read data lines
            self.data = numpy.array([[float(v) for v in line.split()] for line in fp])

# Calculate the maximum magnitude among all vectors in the data sets
def MaxMagnitude(ds):
    if len(ds) != 2:
        raise Exception("Expected 2 data sets, got "+str(len(ds)))
    return numpy.max(numpy.sqrt([numpy.max([x.dot(x) for x in ds[i]]) for i in xrange(2)]))

# Calculate the l2 norm of the difference between the data sets
def L2Norm(ds):
    if len(ds) != 2:
        raise Exception("Expected 2 data sets, got "+str(len(ds)))
    return numpy.sqrt(numpy.sum([x.dot(x) for x in ds[0]-ds[1]]))

# Calculate the renormalized l2 norm of the difference between the data sets
def L2NormRenormed(ds):
    if len(ds) != 2:
        raise Exception("Expected 2 data sets, got "+str(len(ds)))
    max_mag_val = MaxMagnitude(ds)
    return numpy.sqrt(numpy.sum([x.dot(x) for x in ds[0]-ds[1]]))/max_mag_val

# Calculate the maximum difference in vector magnitudes between the data sets,
# normalized by the maximum vector magnitude in the set
def MaxMagDiffRenormed(ds):
    if len(ds) != 2:
        raise Exception("Expected 2 data sets, got "+str(len(ds)))
    max_mag_diff = numpy.max(numpy.sqrt([x.dot(x) for x in ds[0]-ds[1]]))
    max_mag_val = MaxMagnitude(ds)
    return max_mag_diff/max_mag_val

def TimeSeriesCorrelationCoeff(ds):
    if len(ds) != 2:
        raise Exception("Expected 2 data sets, got "+str(len(ds)))
    ds0 = numpy.array([x[0] for x in ds[0]])
    ds1 = numpy.array([x[0] for x in ds[1]])
    return numpy.corrcoef(ds0, ds1)

# Calculate the mean angle difference between corresponding values of the data sets
def AngleDegDiff(ds):
    if len(ds) != 2:
        raise Exception("Expected 2 data sets, got "+str(len(ds)))
    # Take the dot product between the two datasets
    dot_prod = numpy.array([x.dot(y) for x,y in zip(ds[0], ds[1])])
    # Get the magnitude of the vectors in each data set
    mag = [numpy.sqrt([x.dot(x) for x in ds[i]]) for i in range(2)]
    # Calculate the angle between corresponding vectors
    angles = numpy.arccos(dot_prod/(mag[0]*mag[1]))
    # Calculate the mean angle between vectors, ignoring NaN values
    angle_stats = numpy.array([numpy.mean(numpy.ma.MaskedArray(angles, numpy.isnan(angles)))])
    return (180.0/numpy.pi)*angle_stats

def check_set(compare_set):
    for i in xrange(1, len(compare_set)):
        if compare_set[i-1].file_format != compare_set[i].file_format:
            raise Exception("File formats do not match")

def compare(compare_set, compare_functions):
    check_set(compare_set)
    pos = 0
    result = {}
    for w in compare_set[0].file_format:
        data_subset = [compare_set[i].data[:,pos:pos+w] for i in xrange(len(compare_set))]
        for t in itertools.combinations(range(len(compare_set)), 2):
            # Get the two datasets to compare
            ds = [data_subset[t[i]] for i in range(2)]
            # Record the results
            if not result.has_key(t): result[t] = []
            for comp_func in compare_functions:
                result[t].append(comp_func(ds))
        pos += w

    return result
